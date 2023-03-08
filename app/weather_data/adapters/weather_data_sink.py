# ToDo: This script should load data to a datalake. STRUCTURED
# as a placeholder, data is loaded to a file
#-------------------------------------------------------------
import os
import pathlib
from pathlib import Path
import pandas as pd

PATH = '../../../data/weather.csv'


class WeatherDataSink():

    def __init__(self):
        pass


    def write_to_file(self, df):
        df_in = self._read_existing_file()
        if not df_in:
            df.to_csv(PATH, index=False)
        else:
            df_out = pd.concat([df_in, df])
            df_out.to_csv(PATH, index=False)


    @staticmethod
    def _read_existing_file():
        if Path(PATH).is_file():
            return pd.read_csv(PATH)




if __name__ == '__main__':
    pass