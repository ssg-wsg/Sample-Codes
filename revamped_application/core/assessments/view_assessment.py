import requests
import streamlit as st

from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod, Endpoints
from revamped_application.utils.http_utils import HTTPRequestBuilder


class ViewAssessment(AbstractRequest):
    """Class used for viewing the attendance of a course session"""

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, referenceNumber: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(referenceNumber)

    def __repr__(self):
        return self.req.repr(ViewAssessment._TYPE)

    def __str__(self):
        return str(self.req)

    def _prepare(self, referenceNumber: str) -> None:
        """
        Creates an HTTP get request for updating or voiding a course session attendance

        :param referenceNumber: Reference number of the course session
        """

        match st.session_state["url"]:
            case Endpoints.PRODUCTION:
                url = Endpoints.prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/tpg/assessments/details/{referenceNumber}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
