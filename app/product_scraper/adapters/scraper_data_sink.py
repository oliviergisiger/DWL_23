import logging
import json
import pandas as pd
from datetime import date
from airflow.hooks.S3_hook import S3Hook
from product_scraper.port.sources import ScraperSink


class ScraperDataSink(ScraperSink):

    def __init__(self, data: pd.DataFrame, connection: str, filename: str):
        self.data = data
        self._connection = connection
        self._filename = filename

    def write_to_s3(self, execution_date: date):
        filename = f'{self._filename}_{execution_date.date()}.json'

        bytes_json = json.dumps(self.data.to_json()).encode('utf-8')

        s3 = S3Hook(self._connection)
        s3.load_bytes(bytes_data=bytes_json,
                      key=filename,
                      bucket_name="s3-raw-data-dwl23",
                      replace=True)

        logging.info(f'written {len(self.data)} to file: {filename}')
