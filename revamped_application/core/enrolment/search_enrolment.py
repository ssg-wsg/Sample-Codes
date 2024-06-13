import requests
import streamlit as st

from revamped_application.core.constants import HttpMethod
from revamped_application.core.models.enrolment import SearchEnrolmentInfo
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.utils.http_utils import HTTPRequestBuilder


class SearchEnrolment(AbstractRequest):
    """Class used for searching for an enrolment for a course run"""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, enrolment_info: SearchEnrolmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_info)

    def __repr__(self):
        return self.req.repr(SearchEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_info: SearchEnrolmentInfo) -> None:
        """
        Creates an HTTP request for enrolment query

        :param enrolment_info: SearchEnrolmentInfo object containing all information required to
                                query for an enrolment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/tpg/enrolments/search") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(enrolment_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
