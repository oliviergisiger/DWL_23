from weather_data.ports.weather_data import WeatherDataSource
from airflow.hooks.S3_hook import S3Hook

BUCKET = 's3-raw-data-dwl23'

class WeatherDataSourceAdapter(WeatherDataSource):
    """
    should fetch newes file from S3 / minio and transform it
    should inherit from an abstract class
    """
    def __init__(self, connection):
        self._connection = connection



    def read_source(self, execution_date, filetype): # filestorage is equivalent to s3
        source_file_system = S3Hook(self._connection)
        filename = f'{filetype}_{execution_date}.json'
        bucket = BUCKET

        # source_file_system.check_for_key(key=filename, bucket_name=bucket)

        return source_file_system.check_for_key(key=filename, bucket_name=bucket)




if __name__ == '__main__':
    pass


