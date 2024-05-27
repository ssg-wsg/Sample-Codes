import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from core.models.credit import EncryptPayloadInfo
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class EncryptPayload(AbstractRequest):
    """Class used for cancelling a claim"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, encrypt: EncryptPayloadInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(encrypt)

    def __repr__(self):
        return self.req.repr(EncryptPayload._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, encrypt: EncryptPayloadInfo) -> None:
        """
        Creates an HTTP request encrypting a payload

        :param encrypt: Request to be encrypted
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_direct_argument("skillsFutureCredits/claims/encryptRequests") \
            .with_body(encrypt.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
