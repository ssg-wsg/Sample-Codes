"""
Contains class used for editing a course run.
"""

import requests
import streamlit as st

from revamped_application.core.models.course_runs import EditRunInfo
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import HttpMethod, OptionalSelector
from revamped_application.utils.http_utils import HTTPRequestBuilder


class EditCourseRun(AbstractRequest):
    """Class used for editing a course run."""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, runId: str, include_expired: OptionalSelector, runinfo: EditRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired, runinfo)

    def __repr__(self):
        """Representation of this EditCourseRun instance"""

        return self.req.repr(EditCourseRun._TYPE)

    def __str__(self):
        """String representation of this EditCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: OptionalSelector, runinfo: EditRunInfo) -> None:
        """
        Creates an HTTP POST request for editing the details of a course run.

        :param runId: Run ID
        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument=f"/courses/courseRuns/edit/{runId}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

        match include_expired:
            case OptionalSelector.YES:
                self.req = self.req.with_param("includeExpiredCourses", "true")
            case OptionalSelector.NO:
                self.req = self.req.with_param("includeExpiredCourses", "false")

        self.req = self.req.with_body(runinfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post()
