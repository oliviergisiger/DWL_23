from weather_data.adapters.weather_data_source import WeatherDataSource
from weather_data.adapters.weather_data_sink import WeatherDataSink



class SyncWeatherData:

    def __init__(self, source: WeatherDataSource, sink: WeatherDataSink):
        self.source = source
        self.sink = sink

    def invoke_workflow(self):
        df = self.source.get_weather_df()
        self.sink.write_to_file(df)


if __name__ == '__main__':
    from weather_data.adapters import SRG_METEO_API_CONFIGS as configs
    url = configs.get('url')
    headers = configs.get('headers')
    _source = WeatherDataSource(url, headers)
    _sink = WeatherDataSink()

    usecase = SyncWeatherData(source=_source,
                              sink=_sink)

    usecase.invoke_workflow()