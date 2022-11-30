# **community-tulip-api**

This package wraps the Tulip API. This is not an official Tulip package.

If you are just getting started with the Tulip API I recommend reading [this support article](https://support.tulip.co/docs/how-to-use-the-table-api).

# **Authenticating**

This package provides 3 methods of authenticating with Tulip.


1. Environment Variable
2. API Key & Secret
3. base64 encoded auth string

## **Environment Variable**

Set an environment variable `TULIP_AUTH` with base64 encoded `{username}.{password}` value of your bot user. After creating a bot this value can be found under `Auth Header` and will look like `Basic {credential}`.

```
export TULIP_AUTH=YXBpa2V5LjJfQzU5a0w4YWdMNndBSDZOM3Y6UmlsS1V3a3pIZ0ZPc19MUkczWFQ3djdaN0tZVEZpZVVscG1WTmR5QllLaQ==
```

```python
from tulip_api import TulipAPI

api = TulipAPI("abc.tulip.co")
```

## **API Key & Secret**

Pass in the API Key name and Secret to the `TulipAPI` class.

Example:

```python
from tulip_api import TulipAPI

api = TulipAPI(
    "abc.tulip.co",
    api_key="apikey.2_C59kL8agL6wAH6N3v",
    api_key_secret="RilKUwkzHgFOs_LRG3XT7v7Z7KYTFieUlpmVNdyBYKi",
)

```

## **Base64 encoded auth string**

Pass in the base64 encoded auth string. This would be the same value that the environment variables expects.

Example:

```python
from tulip_api import TulipAPI

api = TulipAPI(
    "abc.tulip.co",
    auth="YXBpa2V5LjJfQzU5a0w4YWdMNndBSDZOM3Y6UmlsS1V3a3pIZ0ZPc19MUkczWFQ3djdaN0tZVEZpZVVscG1WTmR5QllLaQ=="
)
```

# TulipTable Class

Table objects reflect the current state of a table.

## Create Table Object

Pass the Table ID (from the table UI) and the TulipAPI object to create a TulipTable object.

Example:

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB
```

### TulipTable.create_record(data)

Create a record in a Tulip Table Object. The record data must be a json encoded dict with each key matching the unique field Ids in the TableUI. Not all fields in the table must be populated.

The `create_random_id` parameter is an optional attribute that will automatically set a record id if one hasn’t been given

Example:

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

record_data = {
    'id': '123456',
    'asfkha_field1': 12,
    'fhasif_field2': True
}
table.create_record(record_data)
```

### TulipTable.update_record(record_id, data)

Update the record in a given table with a specific id. The record data must be a json encoded dict with each key matching the unique field Ids in the TableUI. Not all fields in the table must be populated.

Example:

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

record_data = {
    'asfkha_field1': 12,
    'fhasif_field2': True
}
table.update_record('123',record_data)
```

### TulipTable.delete_record(record_id)

Update the record with the given record id.

Example:

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

table.delete_record('1234')
```

### TulipTable.get_record(record_id)

Returns the json encoded data from a single record with the given record id.

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

rec_data = table.get_record("1234")
```

### TulipTable.get_records()

Returns a list of records. This is limited to 100 records, but the `offset` parameter can be leveraged to loop through all of the records in a table.

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB


recs_data = table.get_records()
```

### TulipTable.stream_records()

Stream table records from a Tulip Table. This will progressively return records in a table. All Table records will be returned as they are available. This is the most performative way to do anything with all of the records in a table.

```python
from tulip_api import TulipAPI,TulipTable

api = TulipAPI("abc.tulip.co")
table = TulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

for record in table.stream_records():
    print(record)
    #DO SOMETHING
```

# CachedTulipTable Class

Reflects a cached representation of a Tulip Table for more performative bulk data operations. The table is stored to memory.

## Create Cached Tulip Table Object

```python
from tulip_api import TulipAPI, CachedTulipTable


api = TulipAPI("abc.tulip.co")
table = CachedTulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

```

## CachedTulipTable.update_data()

Forces the update of a cached Tulip Table

```python
from tulip_api import TulipAPI,CachedTulipTable

api = TulipAPI("abc.tulip.co")
table = CachedTulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

table.update_data()
```

## CachedTulipTable.get_record(record_id)

Returns the cached data from a Tulip Table with the associated `record_id`.

```python
from tulip_api import TulipAPI,CachedTulipTable

api = TulipAPI("abc.tulip.co")
table = CachedTulipTable(api, 'bQLv6iMsau4ipqRiB')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

table.get_record("1234")
```

# TulipTableLink Class

Represents the linked records between two Tulip Tables with the `Linked Record` type Table field.

The link id is the prefix for the field id in the table. *For example, Table field `crN9z6v6qXidrj8TX_link_right_column` has the link id `crN9z6v6qXidrj8TX`*

## Create Tulip Table Link Object

```python
from tulip_api import TulipAPI,TulipTableLink

api = TulipAPI("abc.tulip.co")
link = TulipTableLink(api, 'crN9z6v6qXidrj8TX')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB
```

## TulipTableLink.link_records(left_record_id,right_record_id)

Links the records in 2 tables based on the record IDs in each table. The `left` and `right` record definition is included in the table record field id’s (*ex:`crN9z6v6qXidrj8TX_link_right_column` )*

```python
from tulip_api import TulipAPI,TulipTableLink

api = TulipAPI("abc.tulip.co")
link = TulipTableLink(api, 'crN9z6v6qXidrj8TX')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

link.link_records('1234','5678')
```

## TulipTableLink.unlink_records(left_record_id,right_record_id)

Unlinks the records in 2 tables based on the record IDs in each table. The `left` and `right` record definition is included in the table record field id’s (***ex:`crN9z6v6qXidrj8TX_link_right_column` )*

```python
from tulip_api import TulipAPI,TulipTableLink

api = TulipAPI("abc.tulip.co")
link = TulipTableLink(api, 'crN9z6v6qXidrj8TX')
# table url: https://abc.tulip.co/table/bQLv6iMsau4ipqRiB

link.unlink_records('1234','5678')
```
