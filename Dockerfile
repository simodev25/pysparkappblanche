# Utilise l'image officielle d'Ubuntu 22.04 comme base
FROM ubuntu:22.04

# Installe Python 3.10, wget et autres dépendances
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip wget default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définit la variable d'environnement pour Java (nécessaire pour Spark)
ENV JAVA_HOME /usr/lib/jvm/default-java

# Télécharge et installe Apache Spark
RUN wget -q https://downloads.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.0-bin-hadoop3.tgz -C /opt && \
    rm spark-3.5.0-bin-hadoop3.tgz

# Définit la variable d'environnement pour Spark
ENV SPARK_HOME /opt/spark-3.5.0-bin-hadoop3
ENV PATH $PATH:$SPARK_HOME/bin

# Installe les bibliothèques Python nécessaires
RUN python3.10 -m pip install pyspark findspark

ENV POSTGRES_JDBC_VERSION 42.2.18

# Télécharger le pilote JDBC de PostgreSQL et le copier dans un dossier accessible
RUN wget -O /$SPARK_HOME/jars/postgresql-${POSTGRES_JDBC_VERSION}.jar \
  https://jdbc.postgresql.org/download/postgresql-${POSTGRES_JDBC_VERSION}.jar

# Définit le répertoire de travail
WORKDIR /workspace

# Commande par défaut : lance un shell bash
CMD ["/bin/bash"]
