from configurations.configs import START_DATE, END_DATE
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.S3_hook import S3Hook
from weather_data.adapters.weather_data_source import WeatherDataSourceAdapter

CONNECTION = 'S3_DEVELOPMENT'
BUCKET = 's3-raw-data-dwl23'



def _check_file(execution_date, filetype, bucket):
    source_file_system = S3Hook(CONNECTION)
    filename = f'{filetype}_{execution_date}.json'
    return source_file_system.check_for_key(key=filename, bucket_name=bucket)


def _check_if_file_exists():
    execution_date = '2023-03-25'
    filetype = 'weather_data_bern'
    bucket = BUCKET
    _check_file(execution_date=execution_date,
                filetype=filetype,
                bucket=bucket)


def _load_file_from_storage():

    execution_date = '2023-03-25'
    filetype = 'weather_data_bern'
    bucket = BUCKET

    source = WeatherDataSourceAdapter(CONNECTION)

    file = source.read_source(execution_date, filetype, bucket)

    print(f'***********{file}')







def build_deliver_dag(dag_configs=None):
    with DAG(
        dag_id='deliver_weather_data',
        description='test',
        schedule_interval='0 12 * * *',
        start_date=START_DATE,
        end_date=END_DATE
    ) as dag:
        start = DummyOperator(
            task_id='start'
        )

        end = DummyOperator(
            task_id='end'
        )

        check_file = PythonOperator(
            task_id='check_file',
            python_callable=_check_if_file_exists
        )

        load_file = PythonOperator(
            task_id='load_file',
            python_callable=_load_file_from_storage
        )

        start.set_downstream(check_file)
        check_file.set_downstream(load_file)
        load_file.set_downstream(end)

    return dag


_dag = build_deliver_dag()
