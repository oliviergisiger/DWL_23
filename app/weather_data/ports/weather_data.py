
from abc import ABC, abstractmethod



class WeatherDataSource(ABC):

    @abstractmethod
    def read_source(self, execution_date, filetype):
        pass



class WeatherDataSink(ABC):

    @abstractmethod
    def export(self):
        pass
