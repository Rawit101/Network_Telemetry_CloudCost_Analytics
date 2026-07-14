# 📊 Network Telemetry & Cloud Cost Analytics — End-to-End ETL Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📌 Overview

An end-to-end, containerized Data Engineering pipeline that ingests raw network traffic telemetry (based on the CICIDS-style flow dataset), cleans and transforms it, loads it into PostgreSQL, and visualizes traffic/DDoS classification metrics in Grafana. The whole stack — orchestration, database, and dashboard — is defined in a single `docker-compose.yml`, and the pipeline is scheduled and monitored with Apache Airflow.

## 🏗️ Architecture

```
 ┌────────────┐      ┌──────────────────┐      ┌──────────────┐      ┌─────────┐
 │  Raw CSV   │ ──▶  │  Airflow DAG      │ ──▶  │  PostgreSQL  │ ──▶  │ Grafana │
 │ (network   │      │  (extract/clean/  │      │  network_    │      │ Dashboard│
 │  flow logs)│      │   load script)    │      │  traffic     │      │         │
 └────────────┘      └──────────────────┘      └──────────────┘      └─────────┘
```

- **Airflow** (`webserver` + `scheduler`) triggers the ETL script daily via a `BashOperator`.
- **`scripts/ingest_network_logs.py`** reads the CSV, drops junk columns, cleans `Infinity`/`NaN` values, renames columns to snake_case, and bulk-loads the result into Postgres with SQLAlchemy.
- **PostgreSQL** stores the cleaned data in the `network_traffic` table (schema in `sql/staging/01_create_schema.sql`).
- **Grafana** reads directly from Postgres to render the traffic classification dashboard.

## 🎯 Core Data Engineering Skills Demonstrated

- **Orchestration:** Scheduling and monitoring a daily ETL job with Apache Airflow (DAGs, retries, LocalExecutor).
- **Data Ingestion & Extraction:** Reading and processing large CSV datasets efficiently with pandas.
- **Data Transformation & Cleaning:** Handling missing values, normalizing infinite data points (`Infinity`, `NaN`), and standardizing schemas.
- **Database Design:** Structuring a PostgreSQL table for time-series network flow data.
- **Infrastructure as Code:** Fully containerized stack (Airflow + Postgres + Grafana) via Docker Compose.
- **Security Best Practices:** Using `.env` files to keep database credentials out of source control.
- **Data Visualization:** A Grafana dashboard for monitoring traffic patterns and anomalies (e.g. DDoS labels).

## 📂 Project Structure

```text
.
├── dags/
│   └── network_pipeline_dag.py       # Airflow DAG: daily_network_telemetry_etl
├── dashboards/
│   ├── dashbjson/                    # Grafana dashboard JSON (importable)
│   └── images/                       # Dashboard screenshots
├── data/
│   └── raw/                          # Raw input CSVs (gitignored)
├── docs/                             # Project documentation
├── notebooks/                        # Exploratory analysis notebooks
├── plugins/                          # Airflow custom plugins
├── scripts/
│   └── ingest_network_logs.py        # Main ETL script (Extract → Clean → Load)
├── sql/
│   ├── staging/
│   │   └── 01_create_schema.sql      # network_traffic table definition
│   └── marts/                        # Downstream/aggregated models
├── tests/                            # Test suite
├── docker-compose.yml                # Airflow + Postgres + Grafana stack
├── .env.example                      # Environment variable template
└── README.md
```

## 🖥️ Tech Stack

| Layer          | Tool                         |
|----------------|-------------------------------|
| Orchestration  | Apache Airflow 2.9.1 (LocalExecutor) |
| Database       | PostgreSQL 14                |
| Visualization  | Grafana                      |
| Transformation | Python (pandas, numpy, SQLAlchemy) |
| Infra          | Docker & Docker Compose      |

## 📊 Dashboard

![Traffic Classification Dashboard](dashboards/images/dashboard_trafficclassification.png)

Import `dashboards/dashbjson/dashboard_trafficclassification.json` into Grafana to reproduce it, pointing it at the `network_traffic` table.

## 🗄️ Database Schema

```sql
CREATE TABLE network_traffic (
    id SERIAL PRIMARY KEY,
    destination_port INT,
    flow_duration BIGINT,
    total_fwd_packets BIGINT,
    total_bwd_packets BIGINT,
    total_length_fwd_packets BIGINT,
    total_length_bwd_packets BIGINT,
    flow_bytes_per_sec FLOAT,
    flow_packets_per_sec FLOAT,
    label VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- A network flow CSV dataset (e.g. [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)) placed at `data/raw/`

### 1. Clone the repo
```bash
git clone https://github.com/Rawit101/Network_Telemetry_CloudCost_Analytics.git
cd Network_Telemetry_CloudCost_Analytics
```

### 2. Configure environment variables
Copy the example file and fill in your own credentials:
```bash
cp .env.example .env
```

```dotenv
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql://your_user:your_password@postgres:5432/postgres
```

> ⚠️ Inside Docker, services talk to each other by **service name**, not `localhost`. `DATABASE_URL` must point to `postgres` (the service name in `docker-compose.yml`), not `localhost`.

### 3. Start the stack
```bash
docker compose up -d
```

This spins up:
| Service              | URL                     | Default login   |
|----------------------|--------------------------|------------------|
| Airflow Webserver    | http://localhost:8080    | admin / admin    |
| Grafana              | http://localhost:3000    | admin / admin    |
| PostgreSQL           | localhost:5432            | —               |

### 4. Run the pipeline
In the Airflow UI, enable and trigger the `daily_network_telemetry_etl` DAG — or run the script directly for a quick test:
```bash
docker compose exec airflow-webserver python /opt/airflow/scripts/ingest_network_logs.py
```

### 5. Explore in Grafana
Add PostgreSQL as a data source (`postgres:5432`, database `postgres`) and import the dashboard from `dashboards/dashbjson/`.

## 🗺️ Roadmap

- [ ] `sql/marts/` — aggregated/analytics-ready models on top of staging data
- [ ] Cloud cost analytics module (tying network telemetry to cloud spend)
- [ ] Automated tests in `tests/`
- [ ] CI pipeline for linting/testing the DAG and ETL script

## 📄 License

Not yet specified.
