# Importations
from helpers.spark import start_spark
from usecases.streaming_analytics import StreamingAnalytics



# Fonction principale du job ETL
def main():
    # Démarrer l'application Spark et obtenir la session Spark, le journal et la configuration
    spark, log, config = start_spark(
        master='local[*]',
        app_name='streaming_analytics',  # Nom de l'application Spark
        files=['./settings/jobs/streaming_analytics_config.json']  # Fichiers de configuration
    )

    try:
        # Logique du job ETL
        log.warn('streaming_analytics is up-and-running')  # Début du job ETL
        streaming_analytics = StreamingAnalytics(spark)
        streaming_analytics.execute()  # Exécution de la logique du job ETL
        log.warn('streaming_analytics is finished:')  # Fin du job ETL
    except Exception as e:
        log.error(f'An error occurred: {str(e)}')  # Gérer les erreurs

    finally:
        # Arrêter l'application Spark (quel que soit le résultat du job)
        spark.stop()

if __name__ == '__main__':
    main()  # Point d'entrée pour l'application PySpark ETL
