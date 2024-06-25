import requests
import streamlit as st

from core.constants import HttpMethod
from core.models.enrolment import CreateEnrolmentInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder


class CreateEnrolment(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, enrolment_info: CreateEnrolmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_info)

    def __repr__(self):
        return self.req.repr(CreateEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_info: CreateEnrolmentInfo) -> None:
        """
        Creates an HTTP request for enrolment creation

        :param enrolment_info: CreateEnrolmentInfo object containing all information required to
                                create a new enrolment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument="/tpg/enrolments") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(enrolment_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
