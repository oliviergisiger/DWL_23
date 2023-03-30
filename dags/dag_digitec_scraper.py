from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from product_scraper.adapters.digitec_deal_of_day_scraper_selenium import DigitecDayDealScraper
from airflow.models import Variable

def _scrape_digitec_data(execution_date):
    day_deals = DigitecDayDealScraper('https://www.digitec.ch/en/daily-deal')
    day_deals.get_product_info_df()

    # to be used later as an xcom
    return str(execution_date)



def build_sync_dag(dag_configs=None):
    with DAG(
        dag_id='scrape_digitec_data',
        description='scrapes daily deals from digitec',
        schedule='0 12 * * *',
        start_date=datetime(2023, 3, 24),
        end_date=None
    ) as dag:
        start = EmptyOperator(
            task_id='start'
        )

        end = EmptyOperator(
            task_id='end'
        )

        scrape_digitec_data = PythonOperator(
            task_id='scrape_digitec_data',
            python_callable=_scrape_digitec_data
        )

        start.set_downstream(scrape_digitec_data)
        scrape_digitec_data.set_downstream(end)

    return dag


_dag = build_sync_dag()
