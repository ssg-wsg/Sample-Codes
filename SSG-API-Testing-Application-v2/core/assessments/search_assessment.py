"""
Contains a class used for querying for assessment records.
"""

import requests
import streamlit as st

from core.models.assessments import SearchAssessmentInfo
from core.abc.abstract import AbstractRequest
from core.constants import HttpMethod
from utils.http_utils import HTTPRequestBuilder


class SearchAssessment(AbstractRequest):
    """Class used for finding/searching for an assessment record."""

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
        Creates an encrypted HTTP POST request for retrieving assessment records that
        meet the criteria that the user has specified.

        :param search_info: SearchAssessmentInfo object containing all information required to
                            find/search for an assessment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument="/tpg/assessments/search") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(search_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
