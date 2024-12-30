import requests

import streamlit as st

from app.core.abc.abstract import AbstractRequest
from app.core.constants import HttpMethod
from app.core.models.credit import DecryptPayloadInfo
from app.utils.http_utils import HTTPRequestBuilder


class DecryptPayload(AbstractRequest):
    """Class used for decrypting a request"""

    _TYPE: HttpMethod.POST = HttpMethod.POST

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
            .with_endpoint(st.session_state["url"].value,
                           direct_argument="skillsFutureCredits/claims/decryptRequests") \
            .with_header("accept", "application/json") \
            .with_body(encrypt.payload())

    def execute(self, encryption_key, cert_pem, key_pem) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post_encrypted(encryption_key, cert_pem, key_pem)
