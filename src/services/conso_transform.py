from pyspark.sql.functions import *
from pyspark.sql.types import *

class ConsoTransform:
    def __init__(self, df):
        """Initialise avec un DataFrame Spark."""
        self.df = df

    def remove_negative_numbers(self):

        """Filtre les lignes où 'num_pce' est supérieur à 0."""
        # Assurer que 'num_pce' est converti correctement, en prenant en compte des valeurs non numériques
        self.df = self.df.withColumn('num_pce', col('num_pce').cast(IntegerType()))
        # Assurez-vous que la conversion a réussi en filtrant les valeurs non nulles
        self.df = self.df.filter(col('num_pce').isNotNull())
        # Filtre les lignes où 'num_pce' est supérieur à 0, après s'assurer que les données sont correctement formatées
        self.df = self.df.filter(col('num_pce') >= 0)
        return self

    def remove_duplicates_num_pce(self):
        """Supprime les doublons basés sur 'num_pce'."""
        self.df = self.df.dropDuplicates(['num_pce'])
        return self

    def convert_data_forma(self):

        """Convertit les colonnes de dates en timestamps."""
        self.df = self.df.withColumn("date_debut_consommation", to_timestamp(self.df["date_debut_consommation"], "dd/MM/yyyy HH:mm"))
        self.df = self.df.withColumn("date_fin_consommation", to_timestamp(self.df["date_fin_consommation"], "dd/MM/yyyy HH:mm"))
        self.df = self.df.withColumn("volume_brut", self.df["volume_brut"].cast(DecimalType(10, 2)))
        self.df = self.df.withColumn("volume_converti", self.df["volume_converti"].cast(DecimalType(10, 2)))
        self.df = self.df.withColumn("energie", self.df["energie"].cast(DecimalType(10, 2)))

        return self

    def run(self):
        """Exécute les transformations configurées et renvoie le DataFrame résultant."""
        return self.df

    @staticmethod
    def get_StructType():
        schema = StructType() \
            .add("num_pce", StringType()) \
            .add("arf_type_releve", DoubleType()) \
            .add("date_debut_consommation", TimestampType()) \
            .add("date_fin_consommation", TimestampType()) \
            .add("volume_brut", DoubleType()) \
            .add("energie", DoubleType()) \
            .add("volume_converti", DoubleType())
        return schema
