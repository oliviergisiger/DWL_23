from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from api_sync.usecases.sync_api_usecase import SyncAPI
from api_sync.adapters.sync_api_source import APISyncRequestSourceRaw
from api_sync.adapters.sync_api_sink import APISyncRequestSinkRaw
from airflow.models import Variable

RUNTIME_CONFIG_VAR = "sync_weather_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR, deserialize_json=True)


ACCESS_TOKEN = RUNTIME_CONFIG.get("access_token")


# configs
FILETYPE_CONFIGS = {
    'filetype': 'weather_data_bern'
}

API_CONFIGS = {
    'url': 'https://api.srgssr.ch/srf-meteo/forecast/46.9490,7.3871?type=hour',
    'headers': {
        'authorization': f'Bearer {ACCESS_TOKEN}',  # g2UzkG9CHifRew5jetKxk3NNvoWt
        'accept': 'application/json'
    }
}

S3_CONFIGS = {
    'connection': 'S3_DEVELOPMENT'  #change to "S3_PRODUCTION" for prduction :)
}




def _sync_weather_data(execution_date):
    source = APISyncRequestSourceRaw(url=API_CONFIGS.get('url'),
                                     headers=API_CONFIGS.get('headers'))
    sink = APISyncRequestSinkRaw(filetype=FILETYPE_CONFIGS.get('filetype'),
                                 connection=S3_CONFIGS.get('connection'))
    usecase = SyncAPI(source=source, sink=sink)
    usecase.execute_usecase(execution_date=execution_date)

    # to be used later as an xcom
    return str(execution_date)



def build_sync_dag(dag_configs=None):
    with DAG(
        dag_id='sync_weather_data',
        description='requests data from srg meteo api, writes df to file',
        schedule_interval='0 12 * * *',
        start_date=datetime(2023, 3, 7),
        end_date=None
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
