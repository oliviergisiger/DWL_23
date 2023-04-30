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

CONNECTION = 'S3_DEVELOPMENT'
BUCKET = 's3-raw-data-dwl23'


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
    source_file_system = S3Hook(CONNECTION)
    filename = f'{filetype}_{execution_date.date()}.json'
    print(filename)
    return source_file_system.check_for_key(key=filename, bucket_name=bucket)


def _check_if_file_exists(scraper_name, execution_date):
    filetype = f'{scraper_name}_day_deals'
    bucket = BUCKET
    _check_file(execution_date=execution_date,
                filetype=filetype,
                bucket=bucket)


def _load_digitec_file_from_storage(execution_date):

    database = _get_database()

    source = ScraperDataSourceAdapter(scraper_name='digitec', connection=CONNECTION, bucket=BUCKET)
    sink = ScraperDataSinkAdapter(scraper_name='digitec', db_config=database)

    usecase = DeliverScraperData(source=source,
                                 sink=sink)
    usecase.execute_usecase(execution_date)


def _load_galaxus_file_from_storage(execution_date):

    source = ScraperDataSourceAdapter('galaxus', CONNECTION, BUCKET)

    data = source.read_source(execution_date)

    print(data)


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
                'scraper_name': 'digitec'}
        )

        load_digitec_file = PythonOperator(
            task_id='load_digitec_file',
            python_callable=_load_digitec_file_from_storage
        )

        check_galaxus_file = PythonOperator(
            task_id='check_galaxus_file',
            python_callable=_load_galaxus_file_from_storage,
            op_kwargs={
                'scraper_name': 'galaxus'
            }
        )

        load_galaxus_file = PythonOperator(
            task_id='load_galaxus_file',
            python_callable=_load_galaxus_file_from_storage
        )

        start.set_downstream([check_digitec_file, check_galaxus_file])
        check_digitec_file.set_downstream(load_digitec_file)
        check_galaxus_file.set_downstream(load_galaxus_file)
        load_digitec_file.set_downstream(end)
        load_galaxus_file.set_downstream(end)

    return dag


_dag = build_deliver_dag()



