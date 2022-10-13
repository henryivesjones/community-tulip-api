import json
from typing import Any, Dict, Generator, Iterable, List, Union
from uuid import uuid4

from .exceptions import (
    TulipAPIInvalidChunkSize,
    TulipAPIMalformedRequestError,
    TulipApiTableRecordCreateMustIncludeID,
)
from .tulip_api import TulipAPI


class TulipTable:
    """
    An interface with a Tulip Table.
    """

    def __init__(self, tulip_api: TulipAPI, table_id: str):
        self.tulip_api = tulip_api
        self.table_id = table_id

    def get_details(self):
        """
        GET `/tables/{tableId}`

        Gets details about a Tulip Table's metadata and schema.
        """
        return self.tulip_api.make_request(self._construct_base_path(), "GET")

    def update_table(
        self,
        label: Union[str, None] = None,
        description: Union[str, None] = None,
        deleted: bool = False,
        new_columns: List = [],
        hide_columns: List[str] = [],
        unhide_columns: List[str] = [],
    ):
        """
        PUT `/tables/{tableId}`

        Update the tables metadata or schema.
        This method pulls the table's current metadata and schema before updating with any values passed in.

        new_columns: A list of columns to add to the table schema

        hide_columns: A list of columnId's to mark as hidden.

        unhide_columns: A list of columnId's to unmark as hidden.
        """
        table = self.get_details()
        if label:
            table["label"] = label
        if description:
            table["description"] = description

        for column in table["columns"]:
            if column["name"] in hide_columns:
                column["hidden"] = True
            if column["name"] in unhide_columns:
                column["hidden"] = False

        table["columns"] += new_columns

        return self.tulip_api.make_request(
            self._construct_base_path(),
            "PUT",
            json={
                "label": table["label"],
                "description": table["description"],
                "deleted": deleted,
                "columns": table["columns"],
            },
        )

    def get_records(
        self,
        limit: int = 100,
        offset: int = 0,
        filters: List = [],
        sort_by: str = "_updatedAt",
        sort_asc: bool = False,
        filter_aggregator: str = "all",
    ):
        """
        GET `/tables/{tableId}/records`

        Get a list of table records.

        `filters`: A list of filters
        ```
        {
          "field": "{field}",
          "arg": "{arg}",
          "functionType": "{functionType}",
        }
        ```
        """
        params = {
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by,
            "filterAggregator": filter_aggregator,
            "sortDir": "asc" if sort_asc else "desc",
        }
        for index, filter in enumerate(filters):
            for key, value in filter.items():
                params[f"filters.{index}.{key}"] = value
        return self.tulip_api.make_request(
            self._construct_records_path(), "GET", params=params
        )

    def stream_records(
        self,
        filters: List = [],
        sort_by: str = "_updatedAt",
        sort_asc: bool = False,
        filter_aggregator: str = "all",
        chunk_size: int = 100,
        limit: Union[int, None] = None,
    ) -> Generator[dict, None, None]:
        """
        Returns a Generator that will pull all (or up to a limit) records from a Tulip Table.

        `chunk_size`: Must be between 1 and 100
        """
        if chunk_size < 1 or chunk_size > 100:
            raise TulipAPIInvalidChunkSize(chunk_size)
        offset = 0
        index = 0
        while True:
            records = self.get_records(
                limit=chunk_size,
                offset=offset,
                filters=filters,
                sort_by=sort_by,
                sort_asc=sort_asc,
                filter_aggregator=filter_aggregator,
            )
            if len(records) == 0:
                break

            for record in self._stream_records_helper(records, limit, index):
                index += 1
                yield record

            offset += chunk_size

            if index < offset:
                break

    @staticmethod
    def _stream_records_helper(
        records: List, limit: Union[int, None], index
    ) -> Iterable:
        if limit is None:
            for record in records:
                yield record
            return

        for record in records:
            if index > limit:
                return
            index += 1
            yield record

    def get_record(self, record_id: str):
        """
        GET `/tables/{tableId}/records/{recordId}`

        Returns a record from a Tulip Table given it's ID
        """
        return self.tulip_api.make_request(
            self._construct_record_path(record_id), "GET"
        )

    def get_record_by_sort_filter(
        self,
        filters: List = [],
        sort_by: str = "_updatedAt",
        sort_asc: bool = False,
    ) -> Union[dict, None]:
        """
        GET `/tables/{tableId}/records`

        Returns the first record from a Tulip Table `get_records` request.
        """
        records = self.get_records(
            limit=1, filters=filters, sort_by=sort_by, sort_asc=sort_asc
        )
        if len(records) != 1:
            return None
        return records[0]

    def create_record(self, record: dict, create_random_id=False) -> Dict:
        """
        POST `/tables/{tableId}/records`

        Create a new record in a Tulip Table.
        Either `record` must contain `id` or the `create_random_id` flag must be set to `True`.

        Returns the created record.
        """
        if create_random_id:
            record["id"] = uuid4().hex
        if "id" not in record:
            raise TulipApiTableRecordCreateMustIncludeID()
        return self.tulip_api.make_request(
            self._construct_records_path(), "POST", json=record
        )

    def create_records(
        self, records: Iterable[dict], create_random_id=False, warn_on_failure=False
    ) -> int:
        """
        Iterates over a list of records and creates them. Calling `create_record`

        Returns the # of successfully created records.

        `warn_on_failure`: set to True if you want to continue with creating the rest of the records
        , despite a malformed request.

        """
        created_records = 0
        failed_records = 0
        for record in records:
            try:
                self.create_record(record, create_random_id=create_random_id)
                created_records += 1
            except TulipAPIMalformedRequestError as exception:
                failed_records += 1
                print(f"There was an issue creating the record:\n{json.dumps(record)}")
                if not warn_on_failure:
                    raise exception
        if warn_on_failure and failed_records > 0:
            print(f"Failed to create {failed_records} records.")

        return created_records

    def update_record(self, record_id: str, record: dict = {}):
        """
        PUT `/tables/{tableId}/records/{recordId}`

        Updates a Tulip Table record. Only modifies the passed in columns.
        """
        return self.tulip_api.make_request(
            self._construct_record_path(record_id), "PUT", json=record
        )

    def delete_record(self, record_id: str):
        """
        DELETE `/tables/{tableId}/records/{recordId}`

        Deletes a Tulip Table record.

        Returns the deleted record.
        """
        return self.tulip_api.make_request(
            self._construct_record_path(record_id), "DELETE"
        )

    def increment_record_column(self, record_id: str, column_id: str, value: int):
        """
        PATCH `/tables/{tableId}/records/{recordId}/increment`

        Increments a given record/column's value by the given value.
        """
        return self.tulip_api.make_request(
            self._construct_increment_record_path(record_id),
            "PATCH",
            json={"fieldName": column_id, "value": value},
        )

    @staticmethod
    def coalesce(value: Any, default: Any = 0):
        """
        A helper method to wrap possibly null table column values with a default value.

        EX:
        ```
        TulipTable.coalesce(record['a_column']) + 1
        ```
        """
        if not value:
            return default
        return value

    def _construct_base_path(self):
        return f"tables/{self.table_id}"

    def _construct_records_path(self):
        return f"{self._construct_base_path()}/records"

    def _construct_record_path(self, record_id: str):
        return f"{self._construct_records_path()}/{record_id}"

    def _construct_increment_record_path(self, record_id: str):
        return f"{self._construct_record_path(record_id)}/increment"
