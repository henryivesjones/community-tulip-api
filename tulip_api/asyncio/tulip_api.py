import os
from base64 import b64encode
from typing import Any, Union

import aiohttp

from tulip_api.exceptions import (
    TulipAPIAsyncAuthorizationError,
    TulipAPIAsyncInternalError,
    TulipAPIAsyncMalformedRequestError,
    TulipAPIAsyncNotFoundError,
    TulipAPIAsyncUnknownResponse,
    TulipAPINoCredentialsFound,
)
from tulip_api.tulip_api import TulipAPIResponseCodes


class TulipAPI:
    """
    Asynio enabled

    Wraps the `self.session.` function with authentication, response processing, and base url construction.
    """

    def __init__(
        self,
        tulip_url: str,
        concurrency: int = 40,
        api_key: Union[str, None] = None,
        api_key_secret: Union[str, None] = None,
        auth: Union[str, None] = None,
        use_full_url: bool = False,
    ):
        """
        use_full_url: if set to true, the tulip_url must include `http://` or `https://` as well as the fqdn. For example `https://abc.tulip.co`
        """
        self.host = self._construct_base_url(tulip_url, use_full_url)

        self.auth = TulipAPI._provide_api_credentials(
            api_key=api_key, api_key_secret=api_key_secret, auth=auth
        )

        self.headers = self._construct_headers()
        self.concurrency = concurrency

    def __enter__(self):
        self.connector = aiohttp.TCPConnector(limit=self.concurrency)
        return self

    def __exit__(self, _, __, ___):
        self.connector.close()

    async def make_request(
        self,
        path: str,
        method: str,
        params: Union[dict, None] = None,
        json: Any = None,
    ):
        """
        Makes a request against the Tulip API. Parses and returns JSON returned from the Tulip API.
        """
        async with aiohttp.request(
            method,
            self._construct_url(path),
            params=params,
            json=json,
            headers=self.headers,
            connector=self.connector,
        ) as response:
            return await self._handle_api_response(response).json()

    async def make_request_expect_nothing(
        self,
        path: str,
        method: str,
        params: Union[dict, None] = None,
        json: Any = None,
    ):
        """
        Makes a request against the Tulip API. Returns nothing.
        """
        async with aiohttp.request(
            method,
            self._construct_url(path),
            params=params,
            json=json,
            headers=self.headers,
        ) as response:
            self._handle_api_response(response)

    @staticmethod
    def _provide_api_credentials(
        api_key: Union[str, None] = None,
        api_key_secret: Union[str, None] = None,
        auth: Union[str, None] = None,
    ):
        if auth:
            return auth
        if api_key and api_key_secret:
            return b64encode(f"{api_key}:{api_key_secret}".encode("utf-8")).decode(
                "utf-8"
            )
        if "TULIP_AUTH" in os.environ:
            return os.environ["TULIP_AUTH"]
        raise TulipAPINoCredentialsFound()

    @staticmethod
    def _construct_base_url(host, use_full_url):
        if use_full_url:
            return f"{host}/api/v3"
        cleaned_host = host.replace("http://", "").replace("https://", "")
        return f"https://{cleaned_host}/api/v3/"

    def _construct_url(self, path):
        return f"{self.host}{path}"

    def _construct_headers(self):
        return {"Authorization": f"Basic {self.auth}"}

    def _handle_api_response(self, response: aiohttp.ClientResponse):
        if response.status in TulipAPIResponseCodes.SUCCESS_CODES:
            return response
        if response.status in TulipAPIResponseCodes.MALFORMED_CODES:
            raise TulipAPIAsyncMalformedRequestError(response)
        if response.status in TulipAPIResponseCodes.NOT_FOUND_CODES:
            raise TulipAPIAsyncNotFoundError(response)
        if response.status in TulipAPIResponseCodes.UNAUTHENTICATED_CODES:
            raise TulipAPIAsyncAuthorizationError(response)
        if response.status in TulipAPIResponseCodes.UNEXCPECTED_ERROR_CODES:
            raise TulipAPIAsyncInternalError(response)
        raise TulipAPIAsyncUnknownResponse(response)
