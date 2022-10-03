import requests


class BaseTulipAPIException(Exception):
    """All custom exceptions from within this package inherit from this exception"""

    pass


class TulipAPINoCredentialsFound(BaseTulipAPIException):
    """No credential provider was able to provide credentials."""

    pass


class TulipAPIAuthorizationError(BaseTulipAPIException):
    """The given credentials were unable to authenticate with the tulip instance."""

    def __init__(self, response: requests.Response):
        self.message = (
            f"The {response.request.method} request to {response.url} was not able to authenticate using the given credentials.\n"
            f"Response status code: {response.status_code}."
        )
        super().__init__(self.message)


class TulipAPIConnectionError(BaseTulipAPIException):
    """Unable to connect to the given tulip instance."""

    pass


class TulipAPIMalformedRequestError(BaseTulipAPIException):
    """The request was malformed"""

    def __init__(self, response: requests.Response):
        self.message = (
            f"The {response.request.method} request to {response.url} was malformed.\n"
            f"Response status code: {response.status_code}."
        )
        super().__init__(self.message)


class TulipAPINotFoundError(BaseTulipAPIException):
    """The requested resource was not found"""

    def __init__(self, response: requests.Response):
        self.message = (
            f"The {response.request.method} request to {response.url} did not find the requested resource.\n"
            f"Response status code: {response.status_code}."
        )
        super().__init__(self.message)


class TulipAPIInternalError(BaseTulipAPIException):
    """The requested resource was not found"""

    def __init__(self, response: requests.Response):
        self.message = (
            f"The {response.request.method} request to {response.url} resulted in an internal error.\n"
            f"Response status code: {response.status_code}.\n"
            "Request Body:\n"
            f"{response.request.body}"
        )
        super().__init__(self.message)


class TulipAPIUnknownResponse(BaseTulipAPIException):
    """The requested resource was not found"""

    def __init__(self, response: requests.Response):
        self.message = (
            f"The {response.request.method} request to {response.url} resulted in an unknown response.\n"
            f"Response status code: {response.status_code}."
        )
        super().__init__(self.message)


class TulipAPIInvalidChunkSize(BaseTulipAPIException):
    """Tulip Table record limit must be between 1 and 100"""

    def __init__(self, chunk_size: int):
        self.message = f"Chunk Size must be between 1 and 100. {chunk_size} is invalid."


class TulipAPICachedTableDuplicateIDFound(BaseTulipAPIException):
    """Multiple records with the same id were found in a cached table"""

    def __init__(self, record_id: str):
        self.message = "Multiple records were found with the id {record_id}"
        super().__init__(self.message)


class TulipApiCachedTableRecordNotFound(BaseTulipAPIException):
    """Record was not found in a cached tulip table"""

    def __init__(self, record_id: str):
        self.message = "No record found with the id {record_id}"
        super().__init__(self.message)


class TulipApiTableRecordCreateMustIncludeID(BaseTulipAPIException):
    def __init__(self):
        self.message = "Table Record creates must include an `id` key in the record, or the `create_random_id` flag must be set to True."
