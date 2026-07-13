# 📊 Data Engineering Project: End-to-End ETL Pipeline (Network Telemetry)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 📌 Overview
An end-to-end Data Engineering pipeline designed to process high-volume, time-series data. This project demonstrates core ETL (Extract, Transform, Load) capabilities by ingesting raw network telemetry logs, handling dirty data, and structuring it for analytical queries and real-time monitoring.

## 🎯 Core Data Engineering Skills Demonstrated
- **Data Ingestion & Extraction:** Reading and processing large CSV datasets efficiently.
- **Data Transformation & Cleaning:** Handling missing values, normalizing infinite data points (`Infinity`, `NaN`), and standardizing schemas.
- **Database Design:** Structuring tables for time-series data and optimizing data types for fast querying.
- **Security Best Practices:** Utilizing `.env` files to secure database credentials and environment variables.
- **Data Visualization:** Creating a dynamic monitoring dashboard to track metrics and anomalies.

## 📂 Project Structure
```text
.
├── pipeline.py         # Main ETL script
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore file (excludes datasets and .env)
├── .env.example        # Example of environment variables setup
└── README.md           # Project documentation
