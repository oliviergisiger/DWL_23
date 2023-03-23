from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from product_scraper.adapters.source_digitec_deal_of_day_scraper import DigitecDayDealScraperSource



def _scrape_digitec_data(excecution_date):
    source = DigitecDayDealScraperSource('https://www.digitec.ch/en/daily-deal')
    source.get_product_info_df()

    return str(excecution_date)



def build_sync_dag(dag_configs=None):
    with DAG(
        dag_id='scrape_digitec_data',
        description='scrape products from deal of day page',
        schedule_interval='0 12 * * *',
        start_date=datetime(2023, 3, 22),
        end_date=None
    ) as dag:
        start = DummyOperator(
            task_id='start'
        )

        end = DummyOperator(
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