

from api_sync.adapters.sync_api_source import APISyncRequestSourceRaw
from api_sync.adapters.sync_api_sink import APISyncRequestSinkRaw


class SyncAPI:

    def __init__(self, source: APISyncRequestSourceRaw, sink: APISyncRequestSinkRaw):
        self._source = source
        self._sink = sink


    def execute_usecase(self, execution_date):
        data = self._source.get_json()
        self._sink.write_to_s3(data=data, execution_date=execution_date)



