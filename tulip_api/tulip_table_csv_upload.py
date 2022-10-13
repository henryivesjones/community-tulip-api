from csv import DictReader
from typing import Any, Dict, Iterable, TextIO, Union

from dateutil import parser

from .tulip_table import TulipTable


class TulipTableCSVUploader:
    tulip_table: TulipTable

    def __init__(self, tulip_table: TulipTable, csv_file: Union[str, TextIO]):
        self.tulip_table = tulip_table
        self.csv_file = csv_file

    def execute(self, create_random_id=False, warn_on_failure=False) -> int:
        if isinstance(self.csv_file, str):
            with open(self.csv_file, "r") as csv_file:
                return self._upload_records(csv_file, create_random_id=create_random_id, warn_on_failure=warn_on_failure)

        return self._upload_records(self.csv_file, create_random_id=create_random_id, warn_on_failure=warn_on_failure)


    def _upload_records(self, file: TextIO, create_random_id=False, warn_on_failure=False):
        table_columns = self.tulip_table.get_details()["columns"]
        column_types = {
            column["name"]: column["dataType"]["type"] for column in table_columns
        }
        reader = DictReader(file)
        TulipTableCSVUploader._validate_csv_columns(reader.fieldnames, column_types)

        return self.tulip_table.create_records(
            TulipTableCSVUploader._yield_coerced_records(reader, column_types),
            warn_on_failure=warn_on_failure,
            create_random_id=create_random_id,
        )

    @staticmethod
    def _coerce_type(value: Any, type: str):
        if type == "string":
            return str(value)
        if type == "integer":
            if isinstance(value, str):
                return int(float(value))
            return int(value)
        if type == "float":
            return float(value)
        if type == "boolean":
            return bool(value)
        if type == "timestamp":
            return parser.parse(value, ignoretz=True).strftime("%Y-%m-%dT%H:%M:%SZ")

        raise Exception("Unsupported datatype: {type}. Value: {value}")

    @staticmethod
    def _coerce_record_types(record: Dict[str, Any], column_types: Dict[str, str]):
        new_record = {}
        for column_id, value in record.items():
            if column_id not in column_types:
                raise Exception(
                    f"Column {column_id} found in record, but not in table."
                )
            new_record[column_id] = TulipTableCSVUploader._coerce_type(
                value, column_types[column_id]
            )
        return new_record

    @staticmethod
    def _yield_coerced_records(records: Iterable, column_types: Dict[str, str]):
        for record in records:
            yield TulipTableCSVUploader._coerce_record_types(record, column_types)

    @staticmethod
    def _validate_csv_columns(csv_fieldnames, table_columns):
        for csv_fieldname in csv_fieldnames:
            if not csv_fieldname in table_columns:
                raise Exception(
                    f"Column {csv_fieldname} is not found in the Tulip Table columns."
                )
