import random

from tulip_api import TulipAPI, TulipTable

api = TulipAPI(
    "abc.tulip.co",
)

table_id = "y8rPN23g67yxdLiqT"
table = TulipTable(api, table_id)


# This adds a number between 0.0 and 100.0 to the value in column `afdeq_d`
# for each record that the `id` contains the phrase `ab`
for record in table.stream_records(
    filters=[
        {
            "field": "id",
            "functionType": "contains",
            "arg": "ab",
        },
    ]
):
    table.update_record(
        record["id"], {"afgga_d": record["afgga_d"] + random.random() * 100.0}
    )
