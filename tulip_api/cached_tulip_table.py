from typing import Dict, List

from .exceptions import (
    TulipAPICachedTableDuplicateIDFound,
    TulipApiCachedTableRecordNotFound,
)
from .tulip_api import TulipAPI
from .tulip_table import TulipTable


class CachedTulipTable:
    """
    Pulls a given table/filter into memory. Reference the List `.records` or use the `get_record` method to get a specific record by it's ID.

    Use with caution and only with small tables.
    """

    def __init__(self, tulip_api: TulipAPI, table_id: str, filters: List = []):
        self.tulip_api = tulip_api
        self.table_id = table_id
        self.filters = filters
        self.tulip_table = TulipTable(self.tulip_api, self.table_id)
        self.update_data()

    def _fetch_data(self) -> List:
        return list(self.tulip_table.stream_records(filters=self.filters))

    def update_data(self):
        self.records = self._fetch_data()

    def get_record(self, record_id: str) -> Dict:
        records = list(filter(lambda record: record["id"] == record_id, self.records))
        records_length = len(records)
        if records_length == 1:
            return records[0]
        elif records_length == 0:
            raise TulipApiCachedTableRecordNotFound(record_id)
        else:
            raise TulipAPICachedTableDuplicateIDFound(record_id)
