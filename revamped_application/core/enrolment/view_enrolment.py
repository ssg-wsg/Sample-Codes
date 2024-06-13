import requests
import streamlit as st

from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod
from revamped_application.utils.http_utils import HTTPRequestBuilder


class ViewEnrolment(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, enrolment_reference_num: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_reference_num)

    def __repr__(self):
        return self.req.repr(ViewEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_reference_num: str) -> None:
        """
        Creates an HTTP request for enrolment creation

        :param enrolment_reference_num: Enrolment Record Reference Number
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/tpg/enrolments/details/"
                                           f"{enrolment_reference_num}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
