import requests
import streamlit as st

from revamped_application.core.models.assessments import SearchAssessmentInfo
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod, Endpoints
from revamped_application.utils.http_utils import HTTPRequestBuilder


class SearchAssessment(AbstractRequest):
    """Class used for finding/searching for an assessment"""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, search_info: SearchAssessmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(search_info)

    def __repr__(self):
        return self.req.repr(SearchAssessment._TYPE)

    def __str__(self):
        return str(self.req)

    def _prepare(self, search_info: SearchAssessmentInfo):
        """
        Creates an HTTP get request for getting all course sessions

        :param search_info: SearchAssessmentInfo object containing all information required to
                            find/search for an assessment record
        """

        # importing enums from another module causes problems when checking for equality
        # so we must recreate the endpoint enum object to test for equality
        to_test = Endpoints(st.session_state["url"].value)

        match to_test:
            case Endpoints.PRODUCTION:
                url = Endpoints.prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument="/tpg/assessments/search") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(search_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
