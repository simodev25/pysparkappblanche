from pyspark.sql import SparkSession
from pyspark.sql.functions import col, struct, to_json, to_timestamp
from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType

class PublishToKafka:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Publish in Kafka") \
            .getOrCreate()

    def read_csv(self, file):
        schema = StructType([
            StructField("num_pce", StringType(), True),
            StructField("arf_type_releve", DoubleType(), True),
            StructField("date_debut_consommation", StringType(), True),  # Temporarily as StringType
            StructField("date_fin_consommation", StringType(), True),  # Temporarily as StringType
            StructField("volume_brut", DoubleType(), True),
            StructField("volume_converti", DoubleType(), True),
            StructField("energie", DoubleType(), True)
        ])
        df = self.spark.read.option("delimiter", ";").csv(file, header=True, schema=schema)
        df = df.withColumn("date_debut_consommation", to_timestamp("date_debut_consommation", "dd/MM/yyyy HH:mm")) \
            .withColumn("date_fin_consommation", to_timestamp("date_fin_consommation", "dd/MM/yyyy HH:mm"))
        return df

    def select_columns(self, df):
        df = df.fillna("")  # Remplir les valeurs nulles si nécessaire

        # Transformer les données selon le besoin et préparer pour la conversion en JSON
        messages_df = df.select(
            col("num_pce").cast(StringType()).alias("key"),
            to_json(struct("*")).alias("value")
        )
        return messages_df

    def publish_to_kafka(self, df):
        df.write.format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("topic", "streaming.conso.input") \
            .save()

    def stop_spark(self):
        self.spark.stop()

if __name__ == "__main__":
    kafka_publisher = PublishToKafka()
    df = kafka_publisher.read_csv("files/SMDC01_20200115100204563.csv")
    messages_df = kafka_publisher.select_columns(df)
    kafka_publisher.publish_to_kafka(messages_df)
    kafka_publisher.stop_spark()
