import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from core.models.credit import UploadDocumentInfo
from utils.http_utils import HTTPRequestBuilder, ALTERNATIVE_PROD_URL


class UploadDocument(AbstractRequest):
    """Class used for uploading the supporting documents for a claim"""

    _TYPE: Literal["POST"] = "POST"

    def __init__(self, claimId: str, upload_doc: UploadDocumentInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(claimId, upload_doc)

    def __repr__(self):
        return self.req.repr(UploadDocument._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, claimId: str, upload_doc: UploadDocumentInfo) -> None:
        """
        Creates an HTTP request for uploading the supporting documents for a claim

        :param claimId: Claim ID
        :param upload_doc: Supporting Documents
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(ALTERNATIVE_PROD_URL) \
            .with_header("accept", "application/json") \
            .with_direct_argument(f"/skillsFutureCredits/claims/{claimId}/supportingdocuments") \
            .with_body(upload_doc.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object

        :return: requests.Response object
        """

        return self.req.post()
