from abc import ABC, abstractmethod
from datetime import date
import pandas as pd


class ScraperSource(ABC):

    @abstractmethod
    def _get_product_links(self, url):
        pass


class ScraperSink(ABC):

    @abstractmethod
    def write_to_s3(self, data: pd.DataFrame, excecution_date: date):
        pass