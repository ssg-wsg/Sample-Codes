"""
Contains a class used for uploading course session attendance for a particular course
session or course run.
"""

import requests
import streamlit as st

from SSG_API_Testing_Application_v2.core.abc.abstract import AbstractRequest
from SSG_API_Testing_Application_v2.core.constants import HttpMethod
from SSG_API_Testing_Application_v2.core.models.attendance import UploadAttendanceInfo
from SSG_API_Testing_Application_v2.utils.http_utils import HTTPRequestBuilder


class UploadCourseSessionAttendance(AbstractRequest):
    """Class used for uploading session attendance for a course session."""

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
        """
        Creates an encrypted HTTP POST request to upload the course session attendance to
        the API.

        :param runId: Run ID
        :param attendanceInfo: UploadAttendanceInfo object containing all relevant information
                               to include in the request body
        """

        self.req = HTTPRequestBuilder() \
            .with_endpoint(st.session_state["url"].value,
                           direct_argument=f"/courses/runs/{runId}/sessions/attendance") \
            .with_header("accept", "application/json") \
            .with_header("Content-Type", "application/json") \
            .with_body(attendanceInfo.payload())

    def execute(self) -> requests.Response:
        """
        Executes the HTTP request and returns the response object.

        :return: requests.Response object
        """

        return self.req.post_encrypted()
