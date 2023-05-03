import json
import logging
from scraper_data_db_pipeline.ports.sources import ScraperDataSource
from airflow.hooks.S3_hook import S3Hook


class ScraperDataSourceAdapter(ScraperDataSource):
    """
    Reads in file from S3 / minio.
    """
    def __init__(self, scraper_name, connection, bucket):
        self._scraper_name = scraper_name
        self._connection = connection
        self._bucket = bucket

    def read_source(self, execution_date):
        source_file_system = S3Hook(self._connection)
        filename = f'{self._scraper_name}_day_deals_{execution_date.date()}.json'

        data = source_file_system.read_key(key=filename, bucket_name=self._bucket)
        data_dict = json.loads(data)
        logging.info('data retrieved from source.')
        logging.info(data_dict)

        return data_dict


if __name__ == '__main__':
    pass

