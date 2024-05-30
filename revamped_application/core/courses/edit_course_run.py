import requests

from typing import Literal

from core.models.course_runs import EditRunInfo
from core.abc.abstract_course import ABCCourse
from utils.http import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class EditCourseRun(ABCCourse):
    """
    Class used for editing a course run
    """

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 runinfo: EditRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired, runinfo)

    def __repr__(self):
        """Representation of this EditCourseRun instance"""

        return self.req.repr(EditCourseRun._TYPE)

    def __str__(self):
        """String representation of this EditCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 runinfo: EditRunInfo) -> None:
        """
        Scaffolds the request body and prepares it for execution

        :param runId: Run ID
        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_direct_argument(f"/courses/courseRuns/edit/{runId}")

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
