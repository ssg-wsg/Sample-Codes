"""
Contains all classes and functions relevant for the deletion of a course run.
"""
import requests
import streamlit as st

from core.abc.abstract import AbstractRequest
from core.models.course_runs import DeleteRunInfo
from core.constants import Endpoints, HttpMethod
from utils.http_utils import HTTPRequestBuilder

from typing import Literal


class DeleteCourseRun(AbstractRequest):
    """
    Class used for deleting a course run
    """

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 delete_runinfo: DeleteRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired, delete_runinfo)

    def __repr__(self):
        """Representation of this DeleteCourseRun instance"""

        return self.req.repr(DeleteCourseRun._TYPE)

    def __str__(self):
        """String representation of this DeleteCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 delete_runinfo: DeleteRunInfo) -> None:
        """
        Scaffolds the request body and prepares it for execution

        :param runId: Run ID
        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param delete_runinfo: Response body encapsulation
        """

        match st.session_state["url"]:
            case Endpoints.PRODUCTION:
                url = Endpoints.prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/courses/courseRuns/edit/{runId}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

        match include_expired:
            case "Yes":
                self.req = self.req.with_param("includeExpiredCourses", True)
            case "No":
                self.req = self.req.with_param("includeExpiredCourses", False)

        self.req = self.req.with_body(delete_runinfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
