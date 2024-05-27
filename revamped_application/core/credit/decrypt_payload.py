import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from core.models.credit import DecryptPayloadInfo
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class DecryptPayload(AbstractRequest):
    """Class used for decrypting a request"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, encrypt: DecryptPayloadInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(encrypt)

    def __repr__(self):
        return self.req.repr(DecryptPayload._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, encrypt: DecryptPayloadInfo) -> None:
        """
        Creates an HTTP request decrypting a payload

        :param encrypt: Request to be encrypted
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_direct_argument("skillsFutureCredits/claims/decryptRequests") \
            .with_body(encrypt.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
