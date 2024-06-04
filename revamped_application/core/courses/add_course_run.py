"""
Contains class used for adding a course run.
"""

import requests
import streamlit as st

from typing import Literal

from revamped_application.core.models.course_runs import AddRunInfo
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import Endpoints, HttpMethod
from revamped_application.utils.http_utils import HTTPRequestBuilder


class AddCourseRun(AbstractRequest):
    """Class used for adding a course run."""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, include_expired: Literal["Select a value", "Yes", "No"], runinfo: AddRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(include_expired, runinfo)

    def __repr__(self):
        """Representation of this AddCourseRun instance"""

        return self.req.repr(AddCourseRun._TYPE)

    def __str__(self):
        """String representation of this AddCourseRun instance"""

        return self.__repr__()

    def _prepare(self, include_expired: Literal["Select a value", "Yes", "No"], runinfo: AddRunInfo) -> None:
        """
        Scaffolds the request body and prepares it for execution

        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param runinfo: Response body encapsulation
        """

        # importing enums from another module causes problems when checking for equality
        # so we must recreate the endpoint enum object to test for equality
        to_test = Endpoints(st.session_state["url"].value)

        match to_test:
            case Endpoints.PRODUCTION:
                url = Endpoints.prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument="/courses/courseRuns/publish") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \

        match include_expired:
            case "Yes":
                self.req = self.req.with_param("includeExpiredCourses", "true")
            case "No":
                self.req = self.req.with_param("includeExpiredCourses", "false")

        self.req = self.req.with_body(runinfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
