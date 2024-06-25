import requests

import streamlit as st

from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod
from revamped_application.core.models.credit import EncryptPayloadInfo
from revamped_application.utils.http_utils import HTTPRequestBuilder


class EncryptPayload(AbstractRequest):
    """Class used for cancelling a claim"""

    _TYPE: HttpMethod.POST = HttpMethod.POST

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
            .with_endpoint(st.session_state["url"].value,
                           direct_argument="skillsFutureCredits/claims/encryptRequests") \
            .with_header("accept", "application/json") \
            .with_body(encrypt.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
