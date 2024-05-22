import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class ViewEnrolment(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: Literal["GET"] = "GET"

    def __init__(self, enrolment_reference_num: str):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_reference_num)

    def __repr__(self):
        return self.req.repr(ViewEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_reference_num: str) -> None:
        """
        Creates an HTTP request for enrolment creation

        :param enrolment_reference_num: Enrolment Record Reference Number
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/tpg/enrolments/details/{enrolment_reference_num}")

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.get()
