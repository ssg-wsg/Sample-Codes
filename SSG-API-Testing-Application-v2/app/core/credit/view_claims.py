import requests

import streamlit as st

from app.core.abc.abstract import AbstractRequest
from app.core.constants import HttpMethod
from app.utils.http_utils import HTTPRequestBuilder


class ViewClaims(AbstractRequest):
    """Class used for viewing the details of a claim"""

    _TYPE: HttpMethod.GET = HttpMethod.GET

    def __init__(self, nric: str, claimId: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(nric, claimId)

    def __repr__(self):
        return self.req.repr(ViewClaims._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, nric: str, claimId: str) -> None:
        """
        Creates an HTTP request for viewing the details of a claim

        :param nric: NRIC number
        :param claimId: Claim ID
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument=f"/skillsFutureCredits/claims/{claimId}") \
            .with_header("accept", "application/json") \
            .with_param("nric", nric)

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
