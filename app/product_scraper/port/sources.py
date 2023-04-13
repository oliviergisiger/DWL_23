from abc import ABC, abstractmethod
from datetime import date

import pandas as pd


class ScraperSource(ABC):

    @abstractmethod
    def _get_product_links(self, url):
        pass

    @abstractmethod
    def get_product_info_df(self):
        pass


class ScraperSink(ABC):

    @abstractmethod
    def write_to_s3(self, data: pd.DataFrame, execution_date: date):
        pass
