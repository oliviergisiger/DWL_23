import logging
import json
import pandas as pd
from datetime import date
from airflow.hooks.S3_hook import S3Hook
from product_scraper.port.sources import ScraperSink


class ScraperDataSink(ScraperSink):

    def __init__(self, connection: str, filename: str):
        self._connection = connection
        self._filename = filename

    def write_to_s3(self, data: pd.DataFrame, execution_date: date):
        filename = f'{self._filename}_{execution_date.date()}.json'

        bytes_json = json.dumps(data.to_json()).encode('utf-8')

        s3 = S3Hook(self._connection)
        s3.load_bytes(bytes_data=bytes_json,
                      key=filename,
                      bucket_name="s3-raw-data-dwl23.1",
                      replace=True)

        logging.info(f'written {len(data)} to file: {filename}')
