"""
Contains class used for viewing course sessions.
"""

import requests
import streamlit as st

from revamped_application.utils.http_utils import HTTPRequestBuilder
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import Endpoints, HttpMethod, NUM2MONTH

from typing import Literal, Optional


class ViewCourseSessions(AbstractRequest):
    """Class used for viewing course sessions."""

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, runId: str, crn: str, session_month: Optional[str], session_year: Optional[int],
                 include_expired: Literal["Select a value", "Yes", "No"]):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, crn, session_month, session_year, include_expired)

    def __repr__(self) -> str:
        """Representation of this ViewCourseRun instance"""

        return self.req.repr(ViewCourseSessions._TYPE)

    def __str__(self) -> str:
        """String representation of this ViewCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, crn: str, session_month: Optional[int], session_year: Optional[int],
                 include_expired: Literal["Select a value", "Yes", "No"]) -> None:
        """
        Creates an HTTP get request for getting all course sessions

        :param runId: Run ID
        :param crn: CRN
        :param session_month: Session month
        :param session_year: Session year
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        # importing enums from another module causes problems when checking for equality
        # so we must recreate the endpoint enum object to test for equality
        to_test = Endpoints(st.session_state["url"].value)

        match to_test:
            case Endpoints.PRODUCTION:
                url = Endpoints.public_prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/courses/runs/{runId}/sessions") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_param("uen", st.session_state["uen"]) \
            .with_param("courseReferenceNumber", crn)

        if session_month is not None and session_year is not None:
            if session_month < 10:
                self.req = self.req.with_param("sessionMonth", f"0{session_month}{session_year}")
            else:
                self.req = self.req.with_param("sessionMonth", f"{session_month}{session_year}")

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
