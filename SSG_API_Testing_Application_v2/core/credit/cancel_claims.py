import requests

import streamlit as st

from SSG_API_Testing_Application_v2.core.abc.abstract import AbstractRequest
from SSG_API_Testing_Application_v2.core.constants import HttpMethod
from SSG_API_Testing_Application_v2.core.models.credit import CancelClaimsInfo
from SSG_API_Testing_Application_v2.utils.http_utils import HTTPRequestBuilder


class CancelClaims(AbstractRequest):
    """Class used for cancelling a claim"""

    _TYPE: HttpMethod.POST = HttpMethod.POST

    def __init__(self, claimId: str, cancel_claim: CancelClaimsInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(claimId, cancel_claim)

    def __repr__(self):
        return self.req.repr(CancelClaims._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, claimId: str, cancel_claim: CancelClaimsInfo) -> None:
        """
        Creates an HTTP request for cancelling a claim

        :param claimId: Claim ID
        :param cancel_claim: Claim to be cancelled
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument=f"/skillsFutureCredits/claims/{claimId}") \
            .with_header("accept", "application/json") \
            .with_body(cancel_claim.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
