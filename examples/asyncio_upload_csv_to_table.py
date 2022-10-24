import asyncio
import time

from tulip_api.asyncio import TulipAPI, TulipTable, TulipTableCSVUploader

concurrency = 40
filename = "example.csv"
table_id = "PT929bpqB3s84bbTf"


async def main():
    start_time = time.time()
    with TulipAPI(
        "abc.tulip.co",
        concurrency=concurrency,
    ) as api:
        uploaded_records = await TulipTableCSVUploader(
            TulipTable(api, table_id), filename
        ).execute(create_random_id=True, warn_on_failure=True)
        print(
            f"Uploaded {uploaded_records} to table {table_id} in {round(time.time() - start_time, 2)} seconds."
        )


if __name__ == "__main__":
    asyncio.run(main())
