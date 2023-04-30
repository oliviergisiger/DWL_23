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
        df = self._generate_df(data, execution_date)
        engine = create_engine(self._db_config.connection_string())
        df.to_sql(f'{self._scraper_name}_data', con=engine, index=False)

    @staticmethod
    def _generate_df(data: dict, execution_date):
        df = pd.DataFrame.from_dict(data)

        df['scraping_date'] = execution_date

        return df


if __name__ == '__main__':
    pass
