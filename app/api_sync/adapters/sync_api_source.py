from api_sync.ports.sync_api import APISyncRequestSource
from typing import Dict
import requests


class APISyncRequestSourceRaw(APISyncRequestSource):

    def __init__(self, url: str, headers: Dict):
        self._url = url
        self._headers = headers

    def get_json(self, cols=[]):
        response = requests.get(url=self._url, headers=self._headers)
        if not cols:
            return response.json()

        return {k: v for k, v in zip(cols, response.text.split('\n'))}

