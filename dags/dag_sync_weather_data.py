import pandas as pd
from datetime import datetime, timedelta
from random import randint
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from weather_data.adapters.weather_data_source import WeatherDataSource
from weather_data.adapters.weather_data_sink import WeatherDataSink
from weather_data.usecases.sync_weather_data import SyncWeatherData


API_CONFIGS = {
    'url': 'https://api.srgssr.ch/srf-meteo/forecast/46.9478%2C7.4474?type=hour',
    'headers': {
        'authorization': 'Bearer Ntn2y4I54auYOuz9Lp6Z5z6AZSe7',
        'accept': 'application/json'
    }
}


def _sync_weather_data():
    source = WeatherDataSource(url=API_CONFIGS.get('url'),
                               headers=API_CONFIGS.get('headers'))
    sink = WeatherDataSink()
    usecase = SyncWeatherData(source=source,
                              sink=sink)
    usecase.invoke_workflow()




def build_demo_dag(dag_configs=None):
    with DAG(
        dag_id='sync_api_demo_dag',
        description='tests airflow functionality, prints out head of pd.DataFrame',
        schedule_interval='0 12 * * *',
        start_date=datetime(2023, 2, 25),
        end_date=None
    ) as dag:
        start = DummyOperator(
            task_id='start'
        )

        end = DummyOperator(
            task_id='end'
        )

        print_df_head = PythonOperator(
            task_id='sync_weather_data',
            python_callable=_sync_weather_data
        )

        start.set_downstream(print_df_head)
        print_df_head.set_downstream(end)

    return dag






_dag = build_demo_dag()


# run dag from pycharm
if __name__ == '__main__':
    _sync_weather_data()