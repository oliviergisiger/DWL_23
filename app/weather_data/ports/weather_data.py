
from abc import ABC, abstractmethod



class WeatherDataSource(ABC):

    @abstractmethod
    def source(self):
        pass



class WeatherDataSink(ABC):

    @abstractmethod
    def sink(self):
        pass
