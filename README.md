# community-tulip-api
This package wraps the Tulip API. This is not an official Tulip package.

If you are just getting started with the Tulip API I recommend reading [this support article](https://support.tulip.co/docs/how-to-use-the-table-api).

# Authenticating
This package provides 3 methods of authenticating with Tulip.



1. Environment Variable
2. API Key & Secret
3. base64 encoded auth string

## Environment Variable
Set an environment variable `TULIP_AUTH` with base64 encoded `{username}.{password}` value of your bot user.
After creating a bot this value can be found under `Auth Header` and will look like `Basic {credential}`.
```bash
export TULIP_AUTH=YXBpa2V5LjJfQzU5a0w4YWdMNndBSDZOM3Y6UmlsS1V3a3pIZ0ZPc19MUkczWFQ3djdaN0tZVEZpZVVscG1WTmR5QllLaQ==
```
```python
from tulip_api import TulipAPI

api = TulipAPI("abc.tulip.co")
```


## API Key & Secret
Pass in the API Key name and Secret to the `TulipAPI` class.

Example:
```python
from tulip_api import TulipAPI

api = TulipAPI(
    "abc.tulip.co",
    api_key="apikey.2_C59kL8agL6wAH6N3v",
    api_key_secret="RilKUwkzHgFOs_LRG3XT7v7Z7KYTFieUlpmVNdyBYKi",
)
```

## Base64 encoded auth string
Pass in the base64 encoded auth string. This would be the same value that the environment variables expects.

Example:
```python
from tulip_api import TulipAPI

api = TulipAPI(
    "abc.tulip.co",
    auth="YXBpa2V5LjJfQzU5a0w4YWdMNndBSDZOM3Y6UmlsS1V3a3pIZ0ZPc19MUkczWFQ3djdaN0tZVEZpZVVscG1WTmR5QllLaQ=="
)
```

