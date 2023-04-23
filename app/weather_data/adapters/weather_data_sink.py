from weather_data.ports.weather_data import WeatherDataSink
import ast
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

from weather_data.adapters import WEATHER_DATA_CONFIGS as cfg
SQL = """CREATE TABLE weather_data (
            local_date_time         date,
            TTT_C                   float8,
            TTL_C                   float8,
            TTH_C                   float8,
            TTTFEEL_C               float8,
            DEWPOINT_C              float8,
            PROBPCP_PERCENT         float8,
            RRR_MM                  float8,
            RELHUM_PERCENT          float8,
            FF_KMH                  float8,
            FX_KMH                  float8,
            DD_DEG                  float8,
            SUN_MIN                 float8,
            IRRADIANCE_WM2          float8,
            FRESHSNOW_CM            float8,
            PRESSURE_HPA            float8
        ); """


class WeatherDataSinkAdapter(WeatherDataSink):
    """
    should upload source object.data to rdbms --> either using peewee or similar
    should inherit from abstract class
    """
    def __init__(self, connection, db_config):
        self._connection = connection
        self._db_config = db_config


    def export(self):
        hook = PostgresHook(postgres_conn_id=self._connection, schema=self._db_config)
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data")
        print([i for i in cursor])


    def _generate_df(self, data):
        data_dict = ast.literal_eval(data)
        content = data_dict.get(cfg['content'][0]).get(cfg['content'][1])
        meta = data_dict.get(cfg['meta'][0]).get(cfg['meta'][1])

        # add rows
        df = pd.DataFrame(content)
        df['geo'] = meta

        return df




if __name__ == '__main__':
    pass

