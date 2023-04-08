import pandas as pd
from datetime import date
from airflow.hooks.S3_hook import S3Hook
from product_scraper.port.sources import ScraperSink


class ScraperDataSink(ScraperSink):

    def __init__(self, data: pd.DataFrame, connection: str, filename: str):
        self.data = data
        self._connection = connection
        self._filename = filename

    def write_to_s3(self, execution_data: date):
        filename = f'{self._filename}_{execution_data}.csv'
        filepath = f"s3://s3-raw-data-dwl23/{filename}"

        self.data.to_csv(filepath, index=False,
                         storage_options={
                             "key": AWS_ACCESS_KEY_ID,
                             "secret": AWS_SECRET_ACCESS_KEY,
                             "token": AWS_SESSION_TOKEN
                         })
