from tulip_api import TulipAPI, TulipTable, TulipTableCSVUploader

api = TulipAPI(
    "abc.tulip.co",
)

filename = "example.csv"
table_id = "PT929bpqB3s84bbTf"
uploaded_records = TulipTableCSVUploader(TulipTable(api, table_id), filename).execute(
    create_random_id=True, warn_on_failure=True
)
print(f"Uploaded {uploaded_records} to table {table_id}")
