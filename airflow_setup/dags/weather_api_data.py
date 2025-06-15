import requests
import awswrangler as wr
import pandas as pd
from datetime import datetime
import boto3
from airflow.models import Variable

def extract_weather_data():

    boto3_session = boto3.Session(
        aws_access_key_id= Variable.get("ACCESS_KEY"),
        aws_secret_access_key= Variable.get("SECRET_KEY"),
        region_name="eu-north-1"
    )
    
    api_key = Variable.get("weather_api_key")
    url = "https://api.weatherbit.io/v2.0/current"
    params = {
        "lat": 6.5244,
        "lon": 3.3792,
        "key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    daily_data = response.json()
    df = pd.json_normalize(daily_data['data'])


    date_str = datetime.utcnow().date().isoformat()
    s3_path = f"s3://amatullah-data-bucket/weather_data_{date_str}.parquet"

    wr.s3.to_parquet(
        df=df,
        path=s3_path,
        boto3_session=boto3_session,
        dataset=False
    )
