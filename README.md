
# Installation and Configuration Instructions
```bash
docker-compose up -d --build
docker exec -it spark_python_container bash
```
## Prerequisites

Install the necessary dependencies:

```bash
 apt-get update
 apt-get install libpq-dev
```

Create a Python virtual environment and install packages:

```bash
apt install python3.10-venv
python3 -m venv env_app
env_app/bin/pip3 install -U pip setuptools
env_app/bin/pip3 install poetry 
```

Activate the virtual environment:

```bash
source env_app/bin/activate
```


Install the project dependencies with Poetry:

```bash
poetry install
```

Run the Python script:

```bash
poetry run python3 src/jobs/load_conso.py
```

## PostgreSQL Configuration with Docker

Launch a Docker container for PostgreSQL:

```bash
docker run --name streaming-postgres --hostname streaming-postgres --network pysparkappblanche_default -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -d postgres
```

Create a database and configure users:

```sql
CREATE DATABASE streaming;
\c streaming

CREATE USER streaming WITH PASSWORD 'streaming';
GRANT ALL PRIVILEGES ON DATABASE streaming TO streaming;
```

Create the necessary tables:

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

## Kafka Configuration with Docker

Run the Docker container for Kafka:

```bash
docker-compose -f kafka-single-node.yml up -d
```

Check if the Kafka container is operational:

```bash
docker ps
```

To stop and remove the configuration:

```bash
docker-compose -f kafka-single-node.yml down
```

Access the Kafka broker:

```bash
docker exec -it kafka-broker /bin/bash
```

Navigate to the Kafka scripts directory:

```bash
cd /opt/bitnami/kafka
```

### Create Kafka Topic ###

```bash
./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.conso.input --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.input --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.critical --partitions 1 --replication-factor 1

./bin/kafka-topics.sh --bootstrap-server localhost:29092 --create --topic streaming.alerts.highvolume --partitions 1 --replication-factor 1
```
