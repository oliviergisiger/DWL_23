# ToDo: This script should load data to a datalake. STRUCTURED
# as a placeholder, data is loaded to a file
#-------------------------------------------------------------
import logging
from datetime import datetime
import os
import pathlib
from pathlib import Path
import pandas as pd

PATH = ''


class WeatherDataSink():

    def __init__(self):
        self.file = 'weather_data_bern'

    def write_to_file(self, df: pd.DataFrame, execution_date: datetime):
        filename = self._get_file_name(self.file, execution_date.date())
        df.to_csv(filename)
        logging.info(f'written {df.shape} to file: {filename}')


    def _get_file_name(self, filename, execution_date):
        return f'{filename}_{execution_date}.csv'




if __name__ == '__main__':
    pass