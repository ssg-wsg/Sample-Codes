"""
This file contains the CourseSessionAttendance class, which is used for sending requests to the
View Course Session Attendance API.
"""

import requests
import streamlit as st

from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import Endpoints, HttpMethod
from revamped_application.utils.http_utils import HTTPRequestBuilder


class CourseSessionAttendance(AbstractRequest):
    """Class used for retrieving the attendance of a course session"""

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, runId: int, crn: str, session_id: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, crn, session_id)

    def __repr__(self):
        return self.req.repr(CourseSessionAttendance._TYPE)

    def __str__(self):
        return str(self.req)

    def _prepare(self, runId: int, crn: str, session_id: str) -> None:
        """
        Creates an HTTP get request for getting all course sessions

        :param runId: Run ID
        :param crn: CRN
        :param session_id: Course Session ID
        """

        match st.session_state["url"]:
            case Endpoints.PRODUCTION:
                url = Endpoints.public_prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/courses/runs/{runId}/sessions/attendance") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_param("uen", st.session_state["uen"]) \
            .with_param("courseReferenceNumber", crn) \
            .with_param("sessionId", session_id)

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
