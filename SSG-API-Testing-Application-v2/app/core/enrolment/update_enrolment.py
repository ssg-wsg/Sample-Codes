import requests
import streamlit as st

from app.core.constants import HttpMethod
from app.core.models.enrolment import UpdateEnrolmentInfo
from app.core.abc.abstract import AbstractRequest
from app.utils.http_utils import HTTPRequestBuilder


class UpdateEnrolment(AbstractRequest):
    """Class used for updating an enrolment for a course run"""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, enrolment_reference_num: str, update_enrolment_info: UpdateEnrolmentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(enrolment_reference_num, update_enrolment_info)

    def __repr__(self):
        return self.req.repr(UpdateEnrolment._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, enrolment_reference_num: str, update_enrolment_info: UpdateEnrolmentInfo) -> None:
        """
        Creates an HTTP request for enrolment updating

        :param enrolment_reference_num: Enrolment Record Reference Number
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/tpg/enrolments/details/{enrolment_reference_num}") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(update_enrolment_info.payload())

    def execute(self,encryption_key,cert_pem,key_pem) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post_encrypted(encryption_key,cert_pem,key_pem)
