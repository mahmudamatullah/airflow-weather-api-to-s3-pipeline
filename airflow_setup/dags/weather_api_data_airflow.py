from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from weather_api_data import extract_weather_data

default_args = {
    "owner": "Amatullah",
    "retries": 2,
}

with DAG(
    dag_id="weather_api_to_s3",
    default_args=default_args,
    description="Pull weather data from API and upload to S3 daily",
    schedule_interval="@daily",
    start_date=datetime(2025, 6, 15),
    catchup=False,
    tags=["weather", "s3", "api"]
) as dag:

    extract_task = PythonOperator(
        task_id="extract_and_upload",
        python_callable=extract_weather_data
    )

    extract_task
