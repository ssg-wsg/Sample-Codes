"""
Contains class used for viewing course sessions.
"""

import requests
import streamlit as st

from app.utils.http_utils import HTTPRequestBuilder
from app.core.abc.abstract import AbstractRequest
from app.core.constants import HttpMethod, Month, OptionalSelector

from typing import Optional


class ViewCourseSessions(AbstractRequest):
    """Class used for viewing course sessions."""

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, runId: str, crn: str, session_month: Optional[Month], session_year: Optional[int],
                 include_expired: OptionalSelector):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, crn, session_month, session_year, include_expired)

    def __repr__(self) -> str:
        """Representation of this ViewCourseRun instance"""

        return self.req.repr(ViewCourseSessions._TYPE)

    def __str__(self) -> str:
        """String representation of this ViewCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, crn: str, session_month: Optional[Month], session_year: Optional[int],
                 include_expired: OptionalSelector) -> None:
        """
        Creates an HTTP GET request for retrieving course sessions.

        :param runId: Run ID
        :param crn: CRN
        :param session_month: Session month
        :param session_year: Session year
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value, direct_argument=f"/courses/runs/{runId}/sessions") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_param("uen", st.session_state["uen"]) \
            .with_param("courseReferenceNumber", crn)

        if session_month is not None and session_year is not None:
            if session_month.value[0] < 10:
                self.req = self.req.with_param("sessionMonth", f"0{session_month.value[0]}{session_year}")
            else:
                self.req = self.req.with_param("sessionMonth", f"{session_month.value[0]}{session_year}")

        match include_expired:
            case OptionalSelector.YES:
                self.req = self.req.with_param("includeExpiredCourses", "true")
            case OptionalSelector.NO:
                self.req = self.req.with_param("includeExpiredCourses", "false")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.get()
