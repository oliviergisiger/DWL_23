from hydro_data.adapters.hydro_data_source import HydroDataSource
from hydro_data.adapters.hydro_data_sink import HydroDataSink


class DeliverHydroData:
    """
    should build a usecas wrapper for weather data delivery.
    should inherit from abstract class "usecase", which is to be defined.
    """

    def __init__(self, source: HydroDataSource, sink: HydroDataSink):
        self._source = source
        self._sink = sink

    def execute_usecase(self, execution_date):
        data = self._source.read_source(execution_date)
        self._sink.export(data, execution_date)


if __name__ == '__main__':
    pass
