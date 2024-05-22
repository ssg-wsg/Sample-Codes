import requests

from typing import Literal

from core.models.enrolment import UpdateEnrolmentFeeCollectionInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class UpdateEnrolmentFeeCollection(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, enrolment_reference_num: str,
                 update_enrolment_fee_collection_info: UpdateEnrolmentFeeCollectionInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_reference_num, update_enrolment_fee_collection_info)

    def __repr__(self):
        return self.req.repr(UpdateEnrolmentFeeCollection._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_reference_num: str,
                 update_enrolment_fee_collection_info: UpdateEnrolmentFeeCollectionInfo) -> None:
        """
        Creates an HTTP request for enrolment creation

        :param enrolment_reference_num: Enrolment Record Reference Number
        :param update_enrolment_fee_collection_info: UpdateEnrolmentFeeCollectionInfo object
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_direct_argument(f"/tpg/enrolments/feeCollections/{enrolment_reference_num}") \
            .with_body(update_enrolment_fee_collection_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
