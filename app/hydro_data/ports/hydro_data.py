
from abc import ABC, abstractmethod



class HydroDataSource(ABC):

    @abstractmethod
    def read_source(self, execution_date):
        pass



class HydroDataSink(ABC):

    @abstractmethod
    def export(self, data, execution_date):
        pass
