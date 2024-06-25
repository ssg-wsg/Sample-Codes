import requests
import streamlit as st

from core.constants import HttpMethod
from core.models.enrolment import UpdateEnrolmentFeeCollectionInfo
from core.abc.abstract import AbstractRequest
from utils.http_utils import HTTPRequestBuilder


class UpdateEnrolmentFeeCollection(AbstractRequest):
    """Class used for creating an enrolment for a course run"""

    _TYPE: HttpMethod = HttpMethod.POST

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
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/tpg/enrolments/feeCollections"
                                           f"/{enrolment_reference_num}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(update_enrolment_fee_collection_info.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post_encrypted()
