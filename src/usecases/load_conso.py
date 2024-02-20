from services.conso_transform import ConsoTransform
from repositories.conso_repositories import ConsoRepository
class LoadConso:
    def __init__(self, spark_sess):
        self.spark_sess = spark_sess
        self.db_params = ConsoRepository.get_db_params(self.spark_sess.conf)


    def extract_data(self):
        # Simplified data extraction logic
        file_location = self.spark_sess.conf.get("spark.countepce.smd")
        df = self.spark_sess.read.csv(file_location, header=True, sep=";", inferSchema=True)
        return df

    def transform_data(self, df):
        # Clear and concise transformation logic
        transformer = ConsoTransform(df)
        return transformer.remove_duplicates_num_pce().convert_data_forma().run()
    def processing_data(self, df):
        # Streamlined data loading logic
        # Aggregate data with window of 5 seconds, compute total volume value by num_pce
        return df

    def load_data(self, df):
        # Streamlined data loading logic

        print(f"Number of records to load: {df.count()}")
        try:
          df.write.jdbc(self.db_params['url'], "conso", properties=self.db_params, mode="append")
        except Exception as e:
          print(f'An error occurred: {str(e)}')


    def execute(self):
        # Execute the ETL process
        df = self.extract_data()
        df = self.transform_data(df)
        df = self.processing_data(df)
        self.load_data(df)
        # If counting elements is still required here, it's already printed in load_data.

