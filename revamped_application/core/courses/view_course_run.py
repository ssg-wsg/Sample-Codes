import requests

from utils.http_utils import HTTPRequestBuilder, BASE_PROD_URL
from core.abc.abstract import AbstractRequest

from typing import Literal


class ViewCourseRun(AbstractRequest):
    """
    Class used for viewing course runs.
    """

    _TYPE: Literal["GET"] = "GET"

    def __init__(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"]):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired)

    def __repr__(self) -> str:
        """Representation of this ViewCourseRun instance"""

        return self.req.repr(ViewCourseRun._TYPE)

    def _prepare(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"]) -> None:
        """
        Creates an HTTP get request for getting course runs by runId

        :param runId: Run ID
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(BASE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/courses/courseRuns/id/{runId}")

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
