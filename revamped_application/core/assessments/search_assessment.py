import requests

from typing import Literal

from core.models.assessments import SearchAssessmentInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class SearchAssessment(AbstractRequest):
    """Class used for finding/searching for an assessment"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, search_info: SearchAssessmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(search_info)

    def __repr__(self):
        return self.req.repr(SearchAssessment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, search_info: SearchAssessmentInfo):
        """
        Creates an HTTP get request for getting all course sessions

        :param search_info: SearchAssessmentInfo object containing all information required to
                            find/search for an assessment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument("/tpg/assessments/search") \
            .with_body(search_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
