from configurations.configs import START_DATE, END_DATE
from datetime import datetime, date
from time import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from api_sync.usecases.sync_api_usecase import SyncAPI
from api_sync.adapters.sync_api_source import APISyncRequestSourceRaw
from api_sync.adapters.sync_api_sink import APISyncRequestSinkRaw
from api_sync import SRGToken
from airflow.models import Variable
from dags.dag_utils import update_connection, get_aws_session_credentials

# dynamic environment settings
ENVIRONMENT_VAR = "ENVIRONMENT"
ENVIRONMENT = Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV')

START_DATE = START_DATE if ENVIRONMENT == 'LOCAL_DEV' else date(2023, 4, 8)
END_DATE = END_DATE if ENVIRONMENT == 'LOCAL_DEV' else None



# runtime configs
RUNTIME_CONFIG_VAR = "sync_weather_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                              deserialize_json=True,
                              default_var={})




# configs
FILETYPE_CONFIGS = {'filetype': 'weather_data_bern'}
S3_CONNECTION = 'S3_DEVELOPMENT' if ENVIRONMENT == 'LOCAL_DEV' else 'S3_PRODUCTION'


def _get_api_configs():
    access_token = SRGToken().oauth_token
    api_configs = {
        'url': 'https://api.srgssr.ch/srf-meteo/forecast/46.9490,7.3871?type=hour',
        'headers': {
            'authorization': f'Bearer {access_token}',  # g2UzkG9CHifRew5jetKxk3NNvoWt
            'accept': 'application/json'
        }
    }
    return api_configs




def _sync_weather_data(execution_date):

    if ENVIRONMENT != 'LOCAL_DEV':
        aws_session_credentials = get_aws_session_credentials(time())
        update_connection(S3_CONNECTION, _extra=aws_session_credentials)

    api_configs = _get_api_configs()

    source = APISyncRequestSourceRaw(url=api_configs.get('url'),
                                     headers=api_configs.get('headers'))

    sink = APISyncRequestSinkRaw(filetype=FILETYPE_CONFIGS.get('filetype'),
                                 connection=S3_CONNECTION)
    usecase = SyncAPI(source=source, sink=sink)
    usecase.execute_usecase(execution_date=execution_date)

    # to be used later as an xcom
    return str(execution_date)



def build_sync_dag(dag_configs=None):
    with DAG(
        dag_id='sync_weather_data',
        description='requests data from srg meteo api, writes dict to json ',
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

        sync_weather_data = PythonOperator(
            task_id='sync_weather_data',
            python_callable=_sync_weather_data
        )

        start.set_downstream(sync_weather_data)
        sync_weather_data.set_downstream(end)

    return dag


_dag = build_sync_dag()
