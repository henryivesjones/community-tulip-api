from csv import DictWriter

from tulip_api import TulipAPI, TulipTable

filename = "a-csv.csv"

instance = "abc.tulip.co"
table_id = "aKzv1scg1C6d2PRZ3"


api = TulipAPI(instance)
table = TulipTable(api, table_id)

ex_record = table.get_record_by_sort_filter()
if ex_record is None:
    raise Exception("Table has no data.")

headers = list(ex_record.keys())

with open(filename, "w") as f:
    writer = DictWriter(f, fieldnames=headers)
    writer.writeheader()

    for record in table.stream_records():
        writer.writerow(record)
