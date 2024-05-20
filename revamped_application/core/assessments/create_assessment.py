import requests

from typing import Literal

from core.models.assessments import CreateAssessmentInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class CreateAssessment(AbstractRequest):
    """Class used for creating an assessment for a course run"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, assessment_info: CreateAssessmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(assessment_info)

    def __repr__(self):
        return self.req.repr(CreateAssessment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, assessment_info: CreateAssessmentInfo) -> None:
        """
        Creates an HTTP get request for getting all course sessions

        :param assessment_info: CreateAssessmentInfo object containing all information required to
                                create a new assessment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/tpg/assessments") \
            .with_body(assessment_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
