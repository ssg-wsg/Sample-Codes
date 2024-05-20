import requests
import streamlit as st

from typing import Literal

from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, BASE_PROD_URL


class CourseSessionAttendance(AbstractRequest):
    """Class used for retrieving the attendance of a course session"""

    _TYPE: Literal["GET"] = "GET"

    def __init__(self, runId: str, crn: str, session_id: str, include_expired: Literal["Select a value", "Yes", "No"]):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, crn, session_id, include_expired)

    def __repr__(self):
        return self.req.repr(CourseSessionAttendance._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, runId: str, crn: str, session_id: str,
                 include_expired: Literal["Select a value", "Yes", "No"]) -> None:
        """
        Creates an HTTP get request for getting all course sessions

        :param runId: Run ID
        :param crn: CRN
        :param session_id: Course Session ID
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(BASE_PROD_URL) \
            .with_direct_argument(f"/courses/runs/{runId}/sessions/attendance") \
            .with_param("uen", st.session_state["uen"]) \
            .with_param("courseReferenceNumber", crn) \
            .with_param("sessionId", session_id)

        match include_expired:
            case "Yes":
                self.req = self.req.with_param("includeExpiredCourses", "true")
            case "No":
                self.req = self.req.with_param("includeExpiredCourses", "false")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
