import logging
import pandas as pd
from datetime import date
from airflow.hooks.S3_hook import S3hook
from product_scraper.port.sources import ScraperSink


class DigitecDayDealScraperSink(ScraperSink):


    def __init__(self, filetype: str, connection:str):
        self._filetype = filetype
        self._connection = connection


    def write_to_s3(self, data: pd.DataFrame, excecution_date: date):
        filename = self._get_file_name(self._filetype, execution_date.date())
        data.to_csv(filename, index=False)

        print(self._connection)
        print(data)


    @staticmethod
    def _get_file_name(filename, execution_date):
        return f"{filename}_{execution_date}.csv"
