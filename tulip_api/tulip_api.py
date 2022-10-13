import os
from base64 import b64encode
from typing import Any, List, Tuple, Union

import requests

from .exceptions import (
    TulipAPIAuthorizationError,
    TulipAPIInternalError,
    TulipAPIMalformedRequestError,
    TulipAPINoCredentialsFound,
    TulipAPINotFoundError,
    TulipAPIUnknownResponse,
)


class TulipAPI:
    """
    Wraps the `requests.request` function with authentication, response processing, and base url construction.
    """

    def __init__(
        self,
        tulip_url: str,
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

    def _make_request(
        self,
        path: str,
        method: str,
        params: Union[dict, List[Tuple], bytes, None] = None,
        json: Any = None,
    ):
        return self._handle_api_response(
            requests.request(
                method,
                self._construct_url(path),
                params=params,
                json=json,
                headers=self.headers,
            )
        )

    def make_request(
        self,
        path: str,
        method: str,
        params: Union[dict, List[Tuple], bytes, None] = None,
        json: Any = None,
    ):
        """
        Makes a request against the Tulip API. Parses and returns JSON returned from the Tulip API.
        """
        return self._make_request(path, method, params=params, json=json).json()

    def make_request_expect_nothing(
        self,
        path: str,
        method: str,
        params: Union[dict, List[Tuple], bytes, None] = None,
        json: Any = None,
    ):
        """
        Makes a request against the Tulip API. Returns nothing.
        """
        self._make_request(path, method, params=params, json=json)

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

    def _handle_api_response(self, response: requests.Response):
        if response.status_code in TulipAPIResponseCodes.SUCCESS_CODES:
            return response
        if response.status_code in TulipAPIResponseCodes.MALFORMED_CODES:
            raise TulipAPIMalformedRequestError(response)
        if response.status_code in TulipAPIResponseCodes.NOT_FOUND_CODES:
            raise TulipAPINotFoundError(response)
        if response.status_code in TulipAPIResponseCodes.UNAUTHENTICATED_CODES:
            raise TulipAPIAuthorizationError(response)
        if response.status_code in TulipAPIResponseCodes.UNEXCPECTED_ERROR_CODES:
            raise TulipAPIInternalError(response)
        raise TulipAPIUnknownResponse(response)


class TulipAPIResponseCodes:
    SUCCESS_CODES = {200, 201, 204}
    MALFORMED_CODES = {400, 422}
    NOT_FOUND_CODES = {404}
    UNAUTHENTICATED_CODES = {401, 403}
    UNEXCPECTED_ERROR_CODES = {500}
