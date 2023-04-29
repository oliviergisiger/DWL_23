import ast
import pandas as pd
from sqlalchemy import create_engine
from base.configurations.db_config import DatabaseConfig
from weather_data.ports.weather_data import WeatherDataSink
from weather_data.capabilities.database_orm import weather_data_table
from weather_data.adapters import WEATHER_DATA_CONFIGS as cfg


class WeatherDataSinkAdapter(WeatherDataSink):
    """
    should upload source object.data to rdbms --> either using peewee or similar
    should inherit from abstract class
    """
    def __init__(self, db_config: DatabaseConfig):
        self._db_config = db_config

    def export(self, data, execution_date):
        df = self._generate_df(data, execution_date)
        engine = create_engine(self._db_config.connection_string())
        df.to_sql('weather_data', con=engine, index=False, if_exists='append', dtype=weather_data_table)

    @staticmethod
    def _generate_df(data, execution_date):
        data_dict = ast.literal_eval(data)
        content = data_dict.get(cfg['content'][0]).get(cfg['content'][1])
        meta = data_dict.get(cfg['meta'][0]).get(cfg['meta'][1])

        # add columns
        df = pd.DataFrame(content)
        df['geo'] = meta
        df['ExecutionDate'] = execution_date
        df = df.drop('cur_color', axis=1)

        return df


if __name__ == '__main__':
    pass

