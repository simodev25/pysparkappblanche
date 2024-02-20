from services.conso_transform import ConsoTransform
from pyspark.sql.functions import from_json, col , current_timestamp, window, sum as _sum ,concat_ws
from repositories.conso_repositories import ConsoRepository
class StreamingAnalytics:
    def __init__(self, spark_sess):
        self.spark_sess = spark_sess
        self.db_params = ConsoRepository.get_db_params(spark_sess.conf)
        self.consoRepository = ConsoRepository(spark_sess.conf)
        self.consoRepository.set_up()
        self.kafka_servers = spark_sess.conf.get('spark.kafka.servers')
        self.kafka_topic = spark_sess.conf.get('spark.kafka.topic')



    def extract_data(self):

        #.option("startingOffsets", "earliest") \
        df = self.spark_sess.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("subscribe", self.kafka_topic) \
            .option("startingOffsets", "earliest") \
            .option('maxOffsetsPerTrigger', 200) \
            .load()

        return df

    def write_to_postgresql(self, df, epoch_id):
        # Streamlined data loading logic
        df_transformed = df.withColumn("INTERVAL_TIMESTAMP", concat_ws(" - ", col("window.start"), col("window.end"))) \
            .withColumnRenamed("num_pce", "PCE") \
            .withColumnRenamed("volume_total", "TOTAL_Volume") \
            .select("INTERVAL_TIMESTAMP", "PCE", "TOTAL_Volume")

        try:
            # df_transformed.write.jdbc(self.db_params['url'], "volume_total", properties=self.db_params, mode="append")
            pandas_df = df_transformed.toPandas()
            for index, row in pandas_df.iterrows():
                # Assuming your insertConso method accepts the row values directly
                # You might need to adjust the parameters based on your table schema
                self.consoRepository.insert_total_volume(row['INTERVAL_TIMESTAMP'],row['PCE'],row['TOTAL_Volume'])

        except Exception as e:
            print("An exception occurred:", e)  # Afficher l'erreur ici
    def transform_data(self, df):
        # Convert JSON from Kafka into DataFrame
        consoDf = df \
            .selectExpr("CAST(value AS STRING) as conso") \
            .select(from_json(col("conso"), ConsoTransform.get_StructType()).alias("conso")) \
            .select("conso.*")

        return ConsoTransform(consoDf).run()
    def processing_data(self, df):
        # Streamlined data loading logic
        # Aggregate data with window of 5 seconds, compute total volume value by num_pce

        windoweVolume_total = df \
            .selectExpr("num_pce","date_debut_consommation", "volume_brut + volume_converti as value") \
            .withColumn("timestamp", current_timestamp()) \
            .withWatermark("timestamp", "5 seconds") \
            .groupBy(window(col("timestamp"), "5 seconds"), col("num_pce")) \
            .agg(_sum("value").alias("volume_total"))
        return windoweVolume_total
    def load_data(self, df):


        query = df.writeStream \
            .outputMode("complete") \
            .foreachBatch(self.write_to_postgresql) \
            .start() \
            .awaitTermination()

    def execute(self):
        # Execute the ETL process
        df = self.extract_data()
        df = self.transform_data(df)
        df = self.processing_data(df)
        self.load_data(df)

