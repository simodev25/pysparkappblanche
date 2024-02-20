
from usecases.load_conso import LoadConso # Importez la classe correcte
from helpers.spark import start_spark


from pyspark.sql.types import StringType


# Fonction principale du job ETL
def main():
    # Démarrer l'application Spark et obtenir la session Spark, le journal et la configuration
    spark, log, config = start_spark(
        master='local[*]',
        app_name='LoadConso',  # Nom de l'application Spark
        files=['./settings/jobs/conso_config.json']  # Fichiers de configuration
    )

    try:
        # Logique du job ETL
        log.warn('load_conso is up-and-running')  # Début du job ETL
        load_conso = LoadConso(spark)
        load_conso.execute()  # Exécution de la logique du job ETL
        log.warn('load_conso is finished:')  # Fin du job ETL
    except Exception as e:
        log.error(f'An error occurred: {str(e)}')  # Gérer les erreurs

    finally:
        # Arrêter l'application Spark (quel que soit le résultat du job)
        spark.stop()

if __name__ == '__main__':
    main()  # Point d'entrée pour l'application PySpark ETL
