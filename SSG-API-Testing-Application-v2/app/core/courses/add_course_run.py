"""
Contains class used for adding a course run.
"""

import requests
import streamlit as st

from app.core.models.course_runs import AddRunInfo
from app.core.abc.abstract import AbstractRequest
from app.core.constants import HttpMethod, OptionalSelector
from app.utils.http_utils import HTTPRequestBuilder


class AddCourseRun(AbstractRequest):
    """Class used for adding a course run."""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, include_expired: OptionalSelector, runinfo: AddRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(include_expired, runinfo)

    def __repr__(self):
        """Representation of this AddCourseRun instance"""

        return self.req.repr(AddCourseRun._TYPE)

    def __str__(self):
        """String representation of this AddCourseRun instance"""

        return self.__repr__()

    def _prepare(self, include_expired: OptionalSelector, runinfo: AddRunInfo) -> None:
        """
        Creates an HTTP POST request for creating/publishing a course run.

        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument="/courses/courseRuns/publish")

        match include_expired:
            case OptionalSelector.YES:
                self.req = self.req.with_param("includeExpiredCourses", "true")
            case OptionalSelector.NO:
                self.req = self.req.with_param(
                    "includeExpiredCourses", "false")

        self.req = self.req.with_body(runinfo.payload())

    def execute(self, encryption_key, cert_pem, key_pem) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post_encrypted(encryption_key, cert_pem, key_pem)
