from configurations.configs import LOCAL_DEV, PRODUCTION
from base.configurations.db_config import DatabaseConfig
from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.S3_hook import S3Hook
from hydro_data.adapters.hydro_data_source import HydroDataSourceAdapter
from hydro_data.adapters.hydro_data_sink import HydroDataSinkAdapter
from hydro_data.usecases.deliver_hydro_data import DeliverHydroData



# dynamic environment settings
ENVIRONMENT_VAR = "ENVIRONMENT"
ENVIRONMENT = LOCAL_DEV if Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV') == 'LOCAL_DEV' else PRODUCTION
START_DATE = ENVIRONMENT.dag_start_date
END_DATE = ENVIRONMENT.dag_end_data
S3_CONNECTION = ENVIRONMENT.connections.get('S3')

# runtime configs
RUNTIME_CONFIG_VAR = "deliver_weather_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                              deserialize_json=True,
                              default_var={})

# static configs
FILETYPE_CONFIGS = {'filetype': 'hydro_data_bern'}
BUCKET = 's3-raw-data-dwl23.1'


def _get_database():
    db_config = Variable.get('DATABASE_CONFIG', deserialize_json=True)

    database = DatabaseConfig(
        hostname=db_config.get('hostname'),
        port=db_config.get('port'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        db_name=db_config.get('database_name')
    )

    return database


def _check_file(execution_date, filetype, bucket):
    source_file_system = S3Hook(S3_CONNECTION)
    filename = f'{filetype}_{execution_date.strftime("%y-%m-%dT%H%M")}.json'
    print(filename)
    return source_file_system.check_for_key(key=filename, bucket_name=bucket)



def _check_if_file_exists(execution_date):
    filetype = 'hydro_data_bern'
    bucket = BUCKET
    _check_file(execution_date=execution_date,
                filetype=filetype,
                bucket=bucket)


def _load_file_from_storage(execution_date):

    database = _get_database()

    source = HydroDataSourceAdapter(S3_CONNECTION, BUCKET)
    sink = HydroDataSinkAdapter(db_config=database)

    usecase = DeliverHydroData(source=source,
                               sink=sink)
    usecase.execute_usecase(execution_date)



def build_deliver_dag(dag_configs=None):
    with DAG(
        dag_id='deliver_hydro_data',
        description='test',
        schedule_interval=None,
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
