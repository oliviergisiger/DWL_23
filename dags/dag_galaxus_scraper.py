from time import time
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from product_scraper.adapters.galaxus_deal_of_day_scraper_selenium import GalaxusDayDealScraper
from product_scraper.adapters.scraper_data_sink import ScraperDataSink
from airflow.models import Variable
from dags.dag_utils import update_connection, get_aws_session_credentials

# dynamic environment settings
ENVIRONMENT_VAR = "ENVIRONMENT"
ENVIRONMENT = Variable.get(ENVIRONMENT_VAR, default_var='LOCAL_DEV')

# runtime configs
RUNTIME_CONFIG_VAR = "scrape_digitec_data_runtime_config"
RUNTIME_CONFIG = Variable.get(RUNTIME_CONFIG_VAR,
                              deserialize_json=True,
                              default_var={})

S3_CONNECTION = 'S3_DEVELOPMENT' if ENVIRONMENT == 'LOCAL_DEV' else 'S3_PRODUCTION'


def _scrape_galaxus_data(execution_date):

    if ENVIRONMENT != 'LOCAL_DEV':
        aws_session_credentials = get_aws_session_credentials(time())
        update_connection(S3_CONNECTION, _extra=aws_session_credentials)

    day_deals = GalaxusDayDealScraper('https://www.galaxus.ch/en/daily-deal')
    day_deals_df = day_deals.get_product_info_df()

    filename = "galaxus_day_deals"
    sink = ScraperDataSink(day_deals_df, S3_CONNECTION, filename)
    sink.write_to_s3(execution_date)

    # to be used later as an xcom
    return str(execution_date)


def build_sync_dag(dag_configs=None):
    with DAG(
        dag_id='scrape_galaxus_data',
        description='scrapes daily deals from galaxus',
        schedule='0 12 * * *',
        start_date=datetime(2023, 3, 24),
        end_date=None,
        catchup=False
    ) as dag:
        start = EmptyOperator(
            task_id='start'
        )

        end = EmptyOperator(
            task_id='end'
        )

        scrape_galaxus_data = PythonOperator(
            task_id='scrape_galaxus_data',
            python_callable=_scrape_galaxus_data
        )

        start.set_downstream(scrape_galaxus_data)
        scrape_galaxus_data.set_downstream(end)

    return dag


_dag = build_sync_dag()
