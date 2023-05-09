import ast
import pandas as pd
from sqlalchemy import create_engine
from base.configurations.db_config import DatabaseConfig
from hydro_data.ports.hydro_data import HydroDataSink
from hydro_data.capabilities.database_orm import hydro_data_table
from hydro_data.adapters import WEATHER_DATA_CONFIGS as cfg


class HydroDataSinkAdapter(HydroDataSink):
    """
    should upload source object.data to rdbms --> either using peewee or similar
    should inherit from abstract class
    """
    def __init__(self, db_config: DatabaseConfig):
        self._db_config = db_config

    def export(self, data, execution_date):
        df = self._generate_df(data, execution_date)
        engine = create_engine(self._db_config.connection_string())
        df.to_sql('hydro_data', con=engine, index=False, if_exists='append', dtype=hydro_data_table)

    @staticmethod
    def _generate_df(data, execution_date):
        data_dict = ast.literal_eval(data)
        print('******************************')
        print(type(data_dict))


        # add columns
        df = pd.DataFrame(data_dict, index=[0])
        df['ExecutionDate'] = execution_date
        print(df.head())

        return df


if __name__ == '__main__':
    pass

