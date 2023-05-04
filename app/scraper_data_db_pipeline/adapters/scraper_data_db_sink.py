import ast
import logging
import pandas as pd
from sqlalchemy import create_engine
from base.configurations.db_config import DatabaseConfig
from scraper_data_db_pipeline.ports.sources import ScraperDataSink


class ScraperDataSinkAdapter(ScraperDataSink):
    """
    Uploads source object to RDS (Postgres DB).
    """
    def __init__(self, scraper_name, db_config: DatabaseConfig):
        self._scraper_name = scraper_name
        self._db_config = db_config

    def export(self, data, execution_date):
        df = self._generate_df(data)
        df = self._clean_manipulate_df(df, execution_date)

        logging.info(self._db_config.connection_string())
        engine = create_engine(self._db_config.connection_string())
        logging.info('Connection to DB made')

        df.to_sql(f'{self._scraper_name}_data', con=engine, index=False, if_exists='append')
        logging.info('Data written to DB')
        logging.info(data)

    @staticmethod
    def _generate_df(data):
        data_dict = ast.literal_eval(data)

        df = pd.DataFrame(data_dict)

        logging.info(df.head())

        return df

    @staticmethod
    def _clean_manipulate_df(df: pd.DataFrame, execution_date):

        df['weight_gram'] = df['weight'].apply(lambda x: float(x.split()[0]) * 1000 if 'kg' in x else float(x.split()[0]))
        df.drop(columns=['weight'], inplace=True)
        df['scraping_date'] = execution_date.date()

        return df


if __name__ == '__main__':
    pass
