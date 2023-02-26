import pandas as pd
from datetime import datetime, timedelta
from random import randint
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

OPEN_WEATHER_URL = 'https://api.open-meteo.com/v1/forecast?latitude=46.95&longitude=7.45&daily=temperature_2m_max,temperature_2m_min,uv_index_max,uv_index_clear_sky_max,windspeed_10m_max&timezone=Europe%2FBerlin'


# dummy dataframe for testing purpose
"""
df = pd.DataFrame(
    {
        'date': [pd.to_datetime(datetime.today() + timedelta(i)).date() for i in range(50)],
        'temperature_c': [randint(-10, 30) for i in range(50)],
        'wind_kmh': [randint(0, 120) for i in range(50)]
    }
)
"""


def _get_weather_data():
    ow_json = requests.get(OPEN_WEATHER_URL).json()
    df = pd.DataFrame.from_dict(ow_json)
    print(df.head())




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
            task_id='print_df_head',
            python_callable=_get_weather_data
        )

        start.set_downstream(print_df_head)
        print_df_head.set_downstream(end)

    return dag






_dag = build_demo_dag()


# run dag from pycharm
if __name__ == '__main__':
    _dag.clear()
    _dag.run()