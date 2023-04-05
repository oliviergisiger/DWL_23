from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from product_scraper.adapters.galaxus_deal_of_day_scraper_selenium import GalaxusDayDealScraper
from airflow.models import Variable

def _scrape_galaxus_data(execution_date):
    day_deals = GalaxusDayDealScraper('https://www.galaxus.ch/en/daily-deal')
    day_deals.get_product_info_df()

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
