import requests

from typing import Literal

from core.models.course_runs import AddRunInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class AddCourseRun(AbstractRequest):
    """
    Class used for adding a course run
    """

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, include_expired: Literal["Select a value", "Yes", "No"], runinfo: AddRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(include_expired, runinfo)

    def __repr__(self):
        return self.req.repr(AddCourseRun._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, include_expired: Literal["Select a value", "Yes", "No"], runinfo: AddRunInfo) -> None:
        """
        Scaffolds the request body and prepares it for execution

        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/courses/courseRuns/publish")

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
