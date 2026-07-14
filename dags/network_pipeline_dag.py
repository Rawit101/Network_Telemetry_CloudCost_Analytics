from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 7, 1), 
    'retries': 1, #
    'retry_delay': timedelta(minutes=5), 
}


with DAG(
    'daily_network_telemetry_etl',
    default_args=default_args,
    description='Automated ETL Pipeline for Network Logs',
    schedule_interval=timedelta(days=1), 
    catchup=False,
) as dag:
    run_etl_script = BashOperator(
        task_id='run_ingest_network_logs',
        bash_command='python /opt/airflow/scripts/ingest_network_logs.py',
    )
    run_etl_script