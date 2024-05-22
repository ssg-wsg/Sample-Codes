import requests

from typing import Literal

from core.models.enrolment import CreateEnrolmentInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class CreateEnrolment(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, enrolment_info: CreateEnrolmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_info)

    def __repr__(self):
        return self.req.repr(CreateEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_info: CreateEnrolmentInfo) -> None:
        """
        Creates an HTTP request for enrolment creation

        :param enrolment_info: CreateEnrolmentInfo object containing all information required to
                                create a new enrolment record
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/tpg/enrolments") \
            .with_body(enrolment_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
