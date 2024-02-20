from pyspark.sql.functions import col, window , trim, upper


class StreamingAlertsAndThresholds:
    def __init__(self, spark_sess):
        self.spark_sess = spark_sess
        self.kafka_bootstrap_servers = spark_sess.conf.get('spark.kafka.servers')
        self.input_topic = spark_sess.conf.get('spark.kafka.topics.alerts')
        self.critical_alerts_topic = spark_sess.conf.get('streaming.alerts.critical')
        self.high_volume_alerts_topic = spark_sess.conf.get('spark.kafka.topics.alerts.highvolume')

    def extract_data(self):
        df = self.spark_sess.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.input_topic) \
            .option("failOnDataLoss", "false") \
            .load()
        return df

    def transform_data(self, df):
        alerts_df = df.selectExpr("translate(value, '\"', '') as value") \
            .selectExpr(
            "cast(split(value, ',')[0] as TIMESTAMP) as timestamp",
            "split(value, ',')[1] as level",
            "split(value, ',')[2] as code",
            "split(value, ',')[3] as message")
        return alerts_df

    def process_data(self, alerts_df):
        # Here you can define any processing logic, for now, it's just a placeholder
        # For example, you might want to enrich the data, filter specific records, etc.
        return alerts_df

    def load_data(self, alerts_df):
        # Filter critical alerts and write to Kafka topic
        critical_df = alerts_df.filter(upper(trim(col("level"))) == 'CRITICAL')
        critical_df.selectExpr("format_string('%s,%s,%s', timestamp, code, message) as value") \
            .writeStream \
            .format("kafka") \
            .option("checkpointLocation", "/tmp/cp-critical") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("topic", self.critical_alerts_topic) \
            .start()

        # Find codes with high volume and write to Kafka topic
        code_summary = alerts_df.withWatermark("timestamp", "10 seconds") \
            .groupBy(window(col("timestamp"), "10 seconds"), col("code")) \
            .count() \
            .filter("count > 2")
        code_summary.selectExpr("format_string('%s,%s,%d', window.start, code, count) as value") \
            .writeStream \
            .format("kafka") \
            .option("checkpointLocation", "/tmp/cp-summary") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("topic", self.high_volume_alerts_topic) \
            .start()

    def execute(self):
        df = self.extract_data()
        transformed_df = self.transform_data(df)
        processed_df = self.process_data(transformed_df)  # Process data (placeholder for actual processing logic)
        self.load_data(processed_df)  # Write processed data to Kafka
        self.spark_sess.streams.awaitAnyTermination()


