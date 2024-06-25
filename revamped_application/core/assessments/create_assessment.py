"""
Contains a class used for creating assessment records.
"""

import requests
import streamlit as st

from revamped_application.core.models.assessments import CreateAssessmentInfo
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod
from revamped_application.utils.http_utils import HTTPRequestBuilder


class CreateAssessment(AbstractRequest):
    """Class used for creating an assessment record for a course run."""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, assessment_info: CreateAssessmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(assessment_info)

    def __repr__(self):
        return self.req.repr(CreateAssessment._TYPE)

    def __str__(self):
        return str(self.req)

    def _prepare(self, assessment_info: CreateAssessmentInfo) -> None:
        """
        Creates an encrypted HTTP POST request for creating a new assessment record.

        :param assessment_info: CreateAssessmentInfo object containing all information required to
                                create a new assessment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument="/tpg/assessments") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(assessment_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
