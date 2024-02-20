# Importations
from helpers.spark import start_spark
from usecases.streaming_alerts_and_thresholds import StreamingAlertsAndThresholds



# Fonction principale du job ETL
def main():
    # Démarrer l'application Spark et obtenir la session Spark, le journal et la configuration
    spark, log, config = start_spark(
        master='local[*]',
        app_name='streaming_analytics',  # Nom de l'application Spark
        files=['./settings/jobs/streaming_alerts_and_thresholds_config.json']  # Fichiers de configuration
    )

    try:
        # Logique du job ETL
        log.warn('streaming_alerts_and_thresholds is up-and-running')  # Début du job ETL
        streaming_alerts_and_thresholds = StreamingAlertsAndThresholds(spark)
        streaming_alerts_and_thresholds.execute()  # Exécution de la logique du job ETL
        log.warn('streaming_alerts_and_thresholds is finished:')  # Fin du job ETL
    except Exception as e:
        log.error(f'An error occurred: {str(e)}')  # Gérer les erreurs

    finally:
        # Arrêter l'application Spark (quel que soit le résultat du job)
        spark.stop()

if __name__ == '__main__':
    main()  # Point d'entrée pour l'application PySpark ETL
