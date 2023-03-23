from weather_data.ports.weather_data import WeatherDataSource
from airflow.hooks.S3_hook import S3Hook
import panadas as pd

class WeatherDataSourceAdapter(WeatherDataSource):
    """
    should fetch newes file from S3 / minio and transform it
    should inherit from an abstract class
    """
    def __init__(self, connection):
        self._connection = connection




    def read_file(self, filename: str) -> pd.DataFrame:
        pass

    def _build_source_file_system(self):
        s3 = S3Hook(self._connection)
        s3.




if __name__ == '__main__':
    pass


