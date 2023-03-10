# ToDo: This script should load data to a datalake. STRUCTURED
# as a placeholder, data is loaded to a file
#-------------------------------------------------------------
import logging
from datetime import datetime
from typing import Dict
import json
from airflow.hooks.S3_hook import S3Hook


class WeatherDataSink:

    def __init__(self, filetype: str, connection: str):
        self._filetype = filetype
        self._connection = connection


    def write_to_s3(self, data: Dict, execution_date: datetime):
        filename = self._get_file_name(self._filetype, execution_date.date())
        bytes_json = json.dumps(data).encode('utf-8')

        s3 = S3Hook(self._connection)
        s3.load_bytes(bytes_data=bytes_json,
                      key=filename,
                      bucket_name="raw",
                      replace=True)

        logging.info(f'written {len(data)} to file: {filename}')


    @staticmethod
    def _get_file_name(filename, execution_date):
        return f'{filename}_{execution_date}.json'




if __name__ == '__main__':
    pass