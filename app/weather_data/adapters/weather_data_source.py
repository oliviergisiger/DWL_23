from weather_data.ports.weather_data import WeatherDataSource
from airflow.hooks.S3_hook import S3Hook
import pandas as pd


class WeatherDataSourceAdapter(WeatherDataSource):
    """
    should fetch newes file from S3 / minio and transform it
    should inherit from an abstract class
    """
    def __init__(self, connection, bucket):
        self._connection = connection
        self._bucket = bucket

    def read_source(self, execution_date):  # filestorage is equivalent to s3
        source_file_system = S3Hook(self._connection)
        filename = f'weather_data_bern_{execution_date.date()}.json'

        data = source_file_system.read_key(key=filename, bucket_name=self._bucket)

        return data




if __name__ == '__main__':
    pass


