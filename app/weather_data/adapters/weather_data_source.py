from weather_data.ports.weather_data import WeatherDataSource
from airflow.hooks.S3_hook import S3Hook


class WeatherDataSourceAdapter(WeatherDataSource):
    """
    should fetch newes file from S3 / minio and transform it
    should inherit from an abstract class
    """
    def __init__(self):
        pass



    def read_file(self, filename: str) -> pd.DataFrame:





if __name__ == '__main__':
    pass


