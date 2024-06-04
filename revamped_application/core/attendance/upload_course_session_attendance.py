import requests
import streamlit as st

from revamped_application.core.abc.abstract import AbstractRequest
from revamped_application.core.constants import Endpoints, HttpMethod
from revamped_application.core.models.attendance import UploadAttendanceInfo
from revamped_application.utils.http_utils import HTTPRequestBuilder


class UploadCourseSessionAttendance(AbstractRequest):
    """Class used for uploading session attendance for a course session"""

    _TYPE: HttpMethod = HttpMethod.POST

    def __init__(self, runId: int, attendanceInfo: UploadAttendanceInfo):
        super().__init__()
        self.req: HTTPRequestBuilder = None
        self._prepare(runId, attendanceInfo)

    def __repr__(self):
        return self.req.repr(UploadCourseSessionAttendance._TYPE)

    def __str__(self):
        return self.__repr__()

    def _prepare(self, runId: int, attendanceInfo: UploadAttendanceInfo) -> None:
        # importing enums from another module causes problems when checking for equality
        # so we must recreate the endpoint enum object to test for equality
        to_test = Endpoints(st.session_state["url"].value)

        match to_test:
            case Endpoints.PRODUCTION:
                url = Endpoints.public_prod()
            case Endpoints.UAT | Endpoints.MOCK:
                url = st.session_state["url"].urls[0]
            case _:
                raise ValueError("Invalid URL Type!")

        self.req = HTTPRequestBuilder() \
            .with_endpoint(url, direct_argument=f"/courses/runs/{runId}/sessions/attendance") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(attendanceInfo.payload())

    def execute(self) -> requests.Response:
        return self.req.post_encrypted()
