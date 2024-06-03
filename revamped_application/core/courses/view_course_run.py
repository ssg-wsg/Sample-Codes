import requests
import streamlit as st

from revamped_application.utils.http_utils import HTTPRequestBuilder
from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import Endpoints, HttpMethod

from typing import Literal


class ViewCourseRun(AbstractRequest):
    """
    Class used for viewing course runs.
    """

    _TYPE: HttpMethod = HttpMethod.GET

    def __init__(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"]):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired)

    def __repr__(self) -> str:
        """Representation of this ViewCourseRun instance"""

        return self.req.repr(ViewCourseRun._TYPE)

    def __str__(self):
        """String representation of this ViewCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"]) -> None:
        """
        Creates an HTTP get request for getting course runs by runId

        :param runId: Run ID
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        match st.session_state["url"]:
            case Endpoints.PRODUCTION:
                url = Endpoints.public_prod()
            case Endpoints.UAT | Endpoints.MOCK:
                print("i matched lol")
                url = st.session_state["url"].urls[0]
            case _:
                print(f">>> {st.session_state["url"]}")
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/courses/courseRuns/id/{runId}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json")

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
