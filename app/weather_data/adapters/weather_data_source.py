from typing import Dict, List

import pandas as pd
import requests
from weather_data.ports.sync_api_source import SyncAPI
from weather_data.adapters import SRG_METEO_API_CONFIGS as configs


#SRG_WEATHER_API_TOKEN = 'Ntn2y4I54auYOuz9Lp6Z5z6AZSe7'



class WeatherDataSource(SyncAPI):

    def __init__(self, url: str, headers: Dict = None):
        self._url = url
        self._headers = headers


    def get_weather_df(self):
        index_column = configs.get('index_column')
        resp = self._get_json()
        df = pd.DataFrame.from_dict(resp['forecast']['hour'])
        df[index_column] = pd.to_datetime(df[index_column])
        return df[configs.get('columns')]


    def _get_json(self):
        return requests.get(url=self._url, headers=self._headers).json()

    def _get_dummy_df(self): # for testing reasons
        return pd.DataFrame({'a': [1, 1, 2, 1, 23, 4, 5, 1, 1],
                             'b': [1, 1, 2, 1, 23, 4, 5, 1, 1]})




if __name__ == '__main__':
    pass


