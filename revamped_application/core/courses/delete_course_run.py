"""
Contains all classes and functions relevant for the deletion of a course run.
"""
import requests

from core.abc.abstract_course import ABCCourse
from core.models.course_runs import DeleteRunInfo
from utils.http import HTTPRequestBuilder, ALTERNATIVE_PROD_URL

from typing import Literal


class DeleteCourseRun(ABCCourse):
    """
    Class used for deleting a course run
    """

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 delete_runinfo: DeleteRunInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, include_expired, delete_runinfo)

    def __repr__(self):
        """Representation of this DeleteCourseRun instance"""

        return self.req.repr(DeleteCourseRun._TYPE)

    def __str__(self):
        """String representation of this DeleteCourseRun instance"""

        return self.__repr__()

    def _prepare(self, runId: str, include_expired: Literal["Select a value", "Yes", "No"],
                 delete_runinfo: DeleteRunInfo) -> None:
        """
        Scaffolds the request body and prepares it for execution

        :param runId: Run ID
        :param include_expired:  Indicate whether to retrieve expired courses or not
        :param delete_runinfo: Response body encapsulation
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_direct_argument(f"/courses/courseRuns/edit/{runId}")

        match include_expired:
            case "Yes":
                self.req = self.req.with_param("includeExpiredCourses", True)
            case "No":
                self.req = self.req.with_param("includeExpiredCourses", False)

        self.req = self.req.with_body(delete_runinfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
