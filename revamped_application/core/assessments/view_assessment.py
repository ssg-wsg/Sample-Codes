import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class ViewAssessment(AbstractRequest):
    """Class used for viewing the attendance of a course session"""

    _TYPE: Literal["POST"] = "GET"

    def __init__(self, referenceNumber: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(referenceNumber)

    def __repr__(self):
        return self.req.repr(ViewAssessment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, referenceNumber: str) -> None:
        """
        Creates an HTTP get request for updating or voiding a course session attendance

        :param referenceNumber: Reference number of the course session
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/tpg/assessments/details/{referenceNumber}")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
