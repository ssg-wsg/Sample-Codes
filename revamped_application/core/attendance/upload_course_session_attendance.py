import requests

from typing import Literal

from core.abc.abstract import AbstractRequest
from core.constants import Endpoints, HttpMethod
from core.models.attendance import UploadAttendanceInfo
from utils.http_utils import HTTPRequestBuilder


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
        self.req = HTTPRequestBuilder() \
            .with_endpoint(Endpoints.prod(), direct_argument=f"/courses/runs/{runId}/sessions/attendance") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(attendanceInfo.payload())

    def execute(self) -> requests.Response:
        return self.req.post_encrypted()
