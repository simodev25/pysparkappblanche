from os import environ, listdir, path
import json
from pyspark import SparkFiles
from pyspark.sql import SparkSession
from helpers import logging_app

def start_spark(app_name='my_spark_app', master='local[*]', jar_packages=[], files=[], spark_config={}):
    """Start Spark session, get Spark logger, and load config files.

    :param app_name: Name of Spark app.
    :param master: Cluster connection details (defaults to local[*]).
    :param jar_packages: List of Spark JAR package names.
    :param files: List of files to send to Spark cluster (master and workers).
    :param spark_config: Dictionary of config key-value pairs.
    :return: A tuple of references to the Spark session, logger, and config dict (only if available).
    """

    # Initialize Spark session builder with master and app name
    spark_builder = SparkSession.builder.master(master).appName(app_name)

    # Convert jar packages and files into comma-separated strings and set them in the builder
    if jar_packages:
        spark_jars_packages = ','.join(jar_packages)
        spark_builder.config('spark.jars.packages', spark_jars_packages)

    if files:
        spark_files = ','.join(files)
        spark_builder.config('spark.files', spark_files)

    # Add other configuration parameters
    for key, val in spark_config.items():
        spark_builder.config(key, val)

    # Now create the Spark session
    spark_sess = spark_builder.getOrCreate()
    spark_logger = logging_app.Log4j(spark_sess)

    # Log the loaded configuration for files
    spark_logger.warn('Loaded config from ' + ', '.join(files))

    # Attempt to load config file if present
    config_dict = load_config_file(spark_logger)
    for key, value in config_dict.items():
        spark_sess.conf.set(key, value)
    return spark_sess, spark_logger, config_dict

def load_config_file(spark_logger):
    """Load configuration from a JSON file sent with the Spark job.

    :param spark_logger: Logger for logging messages.
    :return: Configuration dictionary if a config file is found, else None.
    """
    spark_files_dir = SparkFiles.getRootDirectory()
    config_files = [filename for filename in listdir(spark_files_dir) if filename.endswith('config.json')]

    if config_files:
        path_to_config_file = path.join(spark_files_dir, config_files[0])
        with open(path_to_config_file, 'r') as config_file:
            config_dict = json.load(config_file)
        spark_logger.warn('Loaded config from ' + config_files[0])
        return config_dict
    else:
        spark_logger.warn('No config file found')
        return None
