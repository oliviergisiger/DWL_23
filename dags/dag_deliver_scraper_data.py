from configurations.configs import LOCAL_DEV, PRODUCTION
from datetime import datetime
from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.hooks.S3_hook import S3Hook
from base.configurations.db_config import DatabaseConfig
from scraper_data_db_pipeline.adapters.scraper_data_db_source import ScraperDataSourceAdapter
from scraper_data_db_pipeline.adapters.scraper_data_db_sink import ScraperDataSinkAdapter
from scraper_data_db_pipeline.usecases.deliver_scraper_data import DeliverScraperData


# dynamic environment settings
ENVIRONMENT_VAR = "ENVIRONMENT"
ENVIRONMENT = LOCAL_DEV if Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV') == 'LOCAL_DEV' else PRODUCTION
START_DATE = ENVIRONMENT.dag_start_date
END_DATE = ENVIRONMENT.dag_end_data
S3_CONNECTION = ENVIRONMENT.connections.get('S3')

# runtime configs
RUNTIME_CONFIG_VAR = "deliver_scraper_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                              deserialize_json=True,
                              default_var={})

# static configs
FILETYPE_CONFIGS = {'filetype': 'weather_data_bern'}
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
    filename = f'{filetype}_{execution_date.date()}.json'
    print(filename)
    return source_file_system.check_for_key(key=filename, bucket_name=bucket)


def _check_if_file_exists(scraper_name, execution_date):
    filetype = f'{scraper_name}_day_deals'
    bucket = BUCKET
    _check_file(execution_date=execution_date,
                filetype=filetype,
                bucket=bucket)


def _load_digitec_file_from_storage_to_db(execution_date):

    database = _get_database()

    source = ScraperDataSourceAdapter(scraper_name='digitec', connection=S3_CONNECTION, bucket=BUCKET)
    sink = ScraperDataSinkAdapter(scraper_name='digitec', db_config=database)

    usecase = DeliverScraperData(source=source,
                                 sink=sink)
    usecase.execute_usecase(execution_date)


def _load_galaxus_file_from_storage_to_db(execution_date):

    database = _get_database()

    source = ScraperDataSourceAdapter('galaxus', S3_CONNECTION, BUCKET)
    sink = ScraperDataSinkAdapter(scraper_name='galaxus', db_config=database)

    usecase = DeliverScraperData(source=source,
                                 sink=sink)
    usecase.execute_usecase(execution_date)


def build_deliver_dag(dag_configs=None):
    with DAG(
            dag_id='deliver_scraper_data',
            description='reads in scraped data from digitec and galaxus from S3 and writes it into DB',
            schedule_interval='0 13 * * *',
            start_date=datetime(2023, 3, 24),
            end_date=None,
            catchup=False
    ) as dag:
        start = DummyOperator(
            task_id='start'
        )

        end = DummyOperator(
            task_id='end'
        )

        check_digitec_file = PythonOperator(
            task_id='check_digitec_file',
            python_callable=_check_if_file_exists,
            op_kwargs={
                'scraper_name': 'digitec'
            }
        )

        load_digitec_file = PythonOperator(
            task_id='load_digitec_file',
            python_callable=_load_digitec_file_from_storage_to_db
        )

        check_galaxus_file = PythonOperator(
            task_id='check_galaxus_file',
            python_callable=_load_galaxus_file_from_storage_to_db,
            op_kwargs={
                'scraper_name': 'galaxus'
            }
        )

        load_galaxus_file = PythonOperator(
            task_id='load_galaxus_file',
            python_callable=_load_galaxus_file_from_storage_to_db
        )

        start.set_downstream([check_digitec_file, check_galaxus_file])
        check_digitec_file.set_downstream(load_digitec_file)
        check_galaxus_file.set_downstream(load_galaxus_file)
        load_digitec_file.set_downstream(end)
        load_galaxus_file.set_downstream(end)

    return dag


_dag = build_deliver_dag()



