from abc import ABC, abstractmethod
from datetime import date
from typing import Dict


class APISyncRequestSource(ABC):

    @abstractmethod
    def get_json(self, url: str, headers: Dict):
        pass


class APISyncRequestSink(ABC):

    @abstractmethod
    def write_to_s3(self, data: Dict, execution_date: date):
        pass