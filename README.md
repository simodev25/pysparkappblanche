# Instructions d'installation et de configuration
```bash
docker-compose up -d --build
docker exec -it spark_python_container bash
```
## Prérequis

Installer les dépendances nécessaires :

```bash
 apt-get update
 apt-get install libpq-dev
```

Créer un environnement virtuel Python et installer les paquets :

```bash
apt install python3.10-venv
python3 -m venv env_app
env_app/bin/pip3 install -U pip setuptools
env_app/bin/pip3 install poetry 
```

Activer l'environnement virtuel :

```bash
source env_app/bin/activate
```


Installer les dépendances du projet avec Poetry :

```bash
poetry install
```

Exécuter le script Python :

```bash
poetry run python3 src/jobs/load_conso.py
```

## Configuration de PostgreSQL avec Docker

Lancer un conteneur Docker pour PostgreSQL :

```bash
docker run --name streaming-postgres --hostname streaming-postgres --network pysparkappblanche_default -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -d postgres
```

Créer une base de données et configurer les utilisateurs :

```sql
CREATE DATABASE streaming;
\c streaming

CREATE USER streaming WITH PASSWORD 'streaming';
GRANT ALL PRIVILEGES ON DATABASE streaming TO streaming;
```

Créer les tables nécessaires :

```sql
CREATE TABLE conso (
    num_pce VARCHAR(45) PRIMARY KEY,
    arf_type_releve VARCHAR(45),
    date_debut_consommation TIMESTAMP,
    date_fin_consommation TIMESTAMP,
    volume_brut DOUBLE PRECISION,
    volume_converti DOUBLE PRECISION,
    energie DOUBLE PRECISION
);

GRANT ALL PRIVILEGES ON TABLE conso TO streaming;

CREATE TABLE volume_total (
    ID SERIAL PRIMARY KEY,
    INTERVAL_TIMESTAMP VARCHAR(45) DEFAULT NULL,
    PCE VARCHAR(45) DEFAULT NULL,
    TOTAL_Volume DOUBLE PRECISION DEFAULT NULL
);

GRANT ALL PRIVILEGES ON TABLE volume_total TO streaming;
GRANT USAGE, SELECT ON SEQUENCE volume_total_id_seq TO streaming;
```

## Configuration de Kafka avec Docker

Exécuter le conteneur Docker pour Kafka :

```bash
docker-compose -f kafka-single-node.yml up -d
```

Vérifier si le conteneur Kafka est opérationnel :

```bash
docker ps
```

Pour arrêter et supprimer la configuration :

```bash
docker-compose -f kafka-single-node.yml down
```

Accéder au broker Kafka :

```bash
docker exec -it kafka-broker /bin/bash
```

Naviguer vers le répertoire des scripts Kafka :

```bash
cd /opt/bitnami/kafka
```

### Créer topic Kafka ###

```bash
./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.conso.input --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.input --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.critical --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.highvolume --partitions 1 --replication-factor 1


```
