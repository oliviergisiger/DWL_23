
from typing import Dict
from abc import ABC, abstractmethod



class SyncAPI(ABC):

    @abstractmethod
    def _get_json(self):
        pass
