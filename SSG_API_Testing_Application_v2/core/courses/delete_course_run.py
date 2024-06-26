"""
Contains class used for the deletion of a course run.
"""

import requests
import streamlit as st

from SSG_API_Testing_Application_v2.core.abc.abstract import AbstractRequest
from SSG_API_Testing_Application_v2.core.models.course_runs import DeleteRunInfo
from SSG_API_Testing_Application_v2.core.constants import HttpMethod, OptionalSelector
from SSG_API_Testing_Application_v2.utils.http_utils import HTTPRequestBuilder


class DeleteCourseRun(AbstractRequest):
    """Class used for deleting a course run."""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, runId: str, include_expired: OptionalSelector, delete_runinfo: DeleteRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired, delete_runinfo)

    def __repr__(self):
        """Representation of this DeleteCourseRun instance"""

        return self.req.repr(DeleteCourseRun._TYPE)

    def __str__(self):
        """String representation of this DeleteCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: OptionalSelector, delete_runinfo: DeleteRunInfo) -> None:
        """
        Creates an HTTP POST request for deleting a course run.

        :param runId: Run ID
        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param delete_runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument=f"/courses/courseRuns/edit/{runId}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

        match include_expired:
            case OptionalSelector.YES:
                self.req = self.req.with_param("includeExpiredCourses", True)
            case OptionalSelector.NO:
                self.req = self.req.with_param("includeExpiredCourses", False)

        self.req = self.req.with_body(delete_runinfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post()
