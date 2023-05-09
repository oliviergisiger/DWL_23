from configurations.configs import LOCAL_DEV, PRODUCTION
from datetime import datetime, date
from time import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from api_sync.usecases.sync_api_usecase import SyncAPI
from api_sync.adapters.sync_api_source import APISyncRequestSourceRaw
from api_sync.adapters.sync_api_sink import APISyncRequestSinkRaw
from airflow.models import Variable
from dags.dag_utils import update_connection, get_aws_session_credentials

# dynamic environment settings
ENVIRONMENT_VAR = "ENVIRONMENT"
ENVIRONMENT = LOCAL_DEV if Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV') == 'LOCAL_DEV' else PRODUCTION
START_DATE = ENVIRONMENT.dag_start_date
END_DATE = ENVIRONMENT.dag_end_data
S3_CONNECTION = ENVIRONMENT.connections.get('S3')

# runtime configs
RUNTIME_CONFIG_VAR = "sync_hydro_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                              deserialize_json=True,
                              default_var={})

# static configs
FILETYPE_CONFIGS = {'filetype': 'hydro_data_bern'}
COLS=['aare_temp', 'aare_flow']


def _get_api_configs():
    api_configs = {
        'url': 'https://aareguru.existenz.ch/v2018/current?city=bern&app=my.app.ch&version=1.0.42&values=aare.temperature%2Caare.flow',
        'headers': {'accept': '*/json'}
    }
    return api_configs




def _sync_hydro_data(execution_date):

    if ENVIRONMENT.environment != 'LOCAL_DEV':
        aws_session_credentials = get_aws_session_credentials(time())
        update_connection(S3_CONNECTION, _extra=aws_session_credentials)

    api_configs = _get_api_configs()

    source = APISyncRequestSourceRaw(url=api_configs.get('url'),
                                     headers=api_configs.get('headers'))

    sink = APISyncRequestSinkRaw(filetype=FILETYPE_CONFIGS.get('filetype'),
                                 connection=S3_CONNECTION)
    usecase = SyncAPI(source=source, sink=sink)
    usecase.execute_usecase(execution_date=execution_date, cols=COLS, time_filename=True)

    # to be used later as an xcom
    return str(execution_date)



def build_sync_dag():
    with DAG(
        dag_id='sync_hydro_data',
        description='requests data from aare guru api, writes dict to json ',
        schedule_interval='0 2,5,8,11,14,17,20,23 * * *',
        catchup=False,
        start_date=START_DATE,
        end_date=END_DATE
    ) as dag:
        start = DummyOperator(
            task_id='start'
        )

        end = DummyOperator(
            task_id='end'
        )

        sync_hydro_data = PythonOperator(
            task_id='sync_hydro_data',
            python_callable=_sync_hydro_data
        )

        trigger_deliver = TriggerDagRunOperator(
            task_id='trigger_deliver',
            trigger_dag_id='deliver_hydro_data',
            execution_date="{{ execution_date }}",
            reset_dag_run=True
        )

        start.set_downstream(sync_hydro_data)
        sync_hydro_data.set_downstream(trigger_deliver)
        trigger_deliver.set_downstream(end)

    return dag


_dag = build_sync_dag()
