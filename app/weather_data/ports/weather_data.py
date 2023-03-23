from abc import ABC, abstractmethod

import pandas as pd


class WeatherDataSource(ABC):

    @abstractmethod
    def read_file(self, filename: str) -> pd.DataFrame:
        """
        reads in a file (json) return a pd.DataFrame
        """
        pass



class WeatherDataSink(ABC):

    @abstractmethod
    def export_data(self, data: pd.DataFrame) -> None:
        """
        reads pd.DataFrame and writes it to a relational DB table.
        """
        pass