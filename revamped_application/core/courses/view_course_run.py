import requests

from utils.http import HTTPRequestBuilder, ALTERNATIVE_PROD_URL
from core.abc.abstract_course import ABCCourse

from typing import Literal


class ViewCourseRun(ABCCourse):
    """
    Class used for viewing course runs.
    """

    _TYPE: Literal["GET"] = "GET"

    def __init__(self, runId: str, include_expired: bool):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired)

    def __repr__(self) -> str:
        """Representation of this ViewCourseRun instance"""

        return self.req.repr(ViewCourseRun._TYPE)

    def _prepare(self, runId: str, include_expired: bool) -> None:
        """
        Creates an HTTP get request for getting course runs by runId

        :param runId: Run ID
        :param include_expired: Indicate whether to retrieve expired courses or not
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_api_version("v1.0") \
            .with_direct_argument(f"/{runId}") \
            .with_param("includeExpiredCourses", "true" if include_expired else "false")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
