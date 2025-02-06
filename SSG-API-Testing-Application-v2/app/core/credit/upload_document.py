import requests

import streamlit as st

from app.core.abc.abstract import AbstractRequest
from app.core.constants import HttpMethod
from app.core.models.credit import UploadDocumentInfo
from app.utils.http_utils import HTTPRequestBuilder


class UploadDocument(AbstractRequest):
    """Class used for uploading the supporting documents for a claim"""

    _TYPE: HttpMethod.POST = HttpMethod.POST

    def __init__(self, claimId: str, upload_doc: UploadDocumentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(claimId, upload_doc)

    def __repr__(self):
        return self.req.repr(UploadDocument._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, claimId: str, upload_doc: UploadDocumentInfo) -> None:
        """
        Creates an HTTP request for uploading the supporting documents for a claim

        :param claimId: Claim ID
        :param upload_doc: Supporting Documents
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/skillsFutureCredits/claims/{claimId}/supportingdocuments") \
            .with_header("accept", "application/json") \
            .with_body(upload_doc.payload())

    def execute(self, encryption_key, cert_pem, key_pem) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post_encrypted(encryption_key, cert_pem, key_pem)
