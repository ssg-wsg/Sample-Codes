"""
Contains classes that help encapsulate data for sending requests to the Attendance APIs.
"""

import json
import streamlit as st

from typing import Optional, Annotated
from email_validator import validate_email, EmailSyntaxError

from revamped_application.core.constants import SurveyLanguage, Attendance, IdType
from revamped_application.utils.json_utils import remove_null_fields
from revamped_application.core.abc.abstract import AbstractRequestInfo


class UploadAttendanceInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course session attendance"""

    EXCLUSION_LIST: tuple[str] = ("areaCode", )

    def __init__(self):
        self._sessionId: str = None
        self._status_code: Attendance = None
        self._trainee_id: Annotated[str, "string($varchar(50))"] = None
        self._trainee_name: Annotated[str, "string($varchar(66))"] = None
        self._trainee_email: Annotated[str, "string($varchar(320))"] = None
        self._trainee_id_type: IdType = None
        self._contactNumber_mobile: Annotated[str, "string($varchar(15))"] = None
        self._contactNumber_areacode: Annotated[Optional[int], "integer($number(5))"] = None
        self._contactNumber_countryCode: Annotated[int, "integer($number(3))"] = None
        self._numberOfHours: Annotated[Optional[float], "0.5 - 8.0; mandatory for On-the-Job Mode of Training"] = None
        self._surveyLanguage_code: Annotated[SurveyLanguage, "string($varchar(2))"] = None
        self._referenceNumber: str = None
        self._corppassId: str = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, UploadAttendanceInfo):
            return False

        return (
            self._sessionId == other._sessionId
            and self._status_code == other._status_code
            and self._trainee_id == other._trainee_id
            and self._trainee_name == other._trainee_name
            and self._trainee_email == other._trainee_email
            and self._trainee_id_type == other._trainee_id_type
            and self._contactNumber_mobile == other._contactNumber_mobile
            and self._contactNumber_areacode == other._contactNumber_areacode
            and self._contactNumber_countryCode == other._contactNumber_countryCode
            and self._numberOfHours == other._numberOfHours
            and self._surveyLanguage_code == other._surveyLanguage_code
            and self._referenceNumber == other._referenceNumber
            and self._corppassId == other._corppassId
        )

    @property
    def sessionId(self):
        return self._sessionId

    @sessionId.setter
    def sessionId(self, sessionId: str):
        if not isinstance(sessionId, str):
            raise ValueError("Invalid session ID")

        self._sessionId = sessionId

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, status_code: Attendance):
        if not isinstance(status_code, Attendance):
            try:
                status_code = Attendance(status_code)
            except Exception:
                raise ValueError("Invalid status code")

        self._status_code = status_code

    @property
    def trainee_id(self):
        return self._trainee_id

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        if not isinstance(trainee_id, str):
            raise ValueError("Invalid trainee ID")

        self._trainee_id = trainee_id

    @property
    def trainee_name(self):
        return self._trainee_name

    @trainee_name.setter
    def trainee_name(self, trainee_name: str):
        if not isinstance(trainee_name, str):
            raise ValueError("Invalid trainee name")

        self._trainee_name = trainee_name

    @property
    def trainee_email(self):
        return self._trainee_email

    @trainee_email.setter
    def trainee_email(self, trainee_email: str):
        if not isinstance(trainee_email, str):
            raise ValueError("Invalid trainee email")

        self._trainee_email = trainee_email

    @property
    def trainee_id_type(self):
        return self._trainee_id_type

    @trainee_id_type.setter
    def trainee_id_type(self, trainee_id_type: IdType):
        if not isinstance(trainee_id_type, IdType):
            raise ValueError("Invalid trainee ID type")

        self._trainee_id_type = trainee_id_type

    @property
    def contactNumber_mobile(self):
        return self._contactNumber_mobile

    @contactNumber_mobile.setter
    def contactNumber_mobile(self, contactNumber_mobile: str):
        if not isinstance(contactNumber_mobile, str):
            raise ValueError("Invalid trainee contact number")

        self._contactNumber_mobile = contactNumber_mobile

    @property
    def contactNumber_areacode(self):
        return self._contactNumber_areacode

    @contactNumber_areacode.setter
    def contactNumber_areacode(self, contactNumber_areacode: int):
        if not isinstance(contactNumber_areacode, int):
            raise ValueError("Invalid trainee contact number area code")

        self._contactNumber_areacode = contactNumber_areacode

    @property
    def contactNumber_countryCode(self):
        return self._contactNumber_countryCode

    @contactNumber_countryCode.setter
    def contactNumber_countryCode(self, contactNumber_countryCode: int):
        if not isinstance(contactNumber_countryCode, int):
            raise ValueError("Invalid trainee contact number country code")

        self._contactNumber_countryCode = contactNumber_countryCode

    @property
    def numberOfHours(self):
        return self._numberOfHours

    @numberOfHours.setter
    def numberOfHours(self, numberOfHours: float):
        if not isinstance(numberOfHours, float) or numberOfHours < 0.5 or numberOfHours > 8.0:
            raise ValueError("Invalid number of hours")

        self._numberOfHours = numberOfHours

    @property
    def surveyLanguage_code(self):
        return self._surveyLanguage_code

    @surveyLanguage_code.setter
    def surveyLanguage_code(self, surveyLanguage_code: SurveyLanguage):
        if not isinstance(surveyLanguage_code, SurveyLanguage):
            raise ValueError("Invalid survey language code")

        self._surveyLanguage_code = surveyLanguage_code

    @property
    def referenceNumber(self):
        return self._referenceNumber

    @referenceNumber.setter
    def referenceNumber(self, referenceNumber: str):
        if not isinstance(referenceNumber, str):
            raise ValueError("Invalid reference number")

        self._referenceNumber = referenceNumber

    @property
    def corppassId(self):
        return self._corppassId

    @corppassId.setter
    def corppassId(self, corppassId: str):
        if not isinstance(corppassId, str):
            raise ValueError("Invalid CorpPass ID")

        self._corppassId = corppassId

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._sessionId is None or len(self._sessionId) == 0:
            errors.append("No Session ID specified!")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No Trainee ID specified!")

        if self._trainee_name is None or len(self._trainee_name) == 0:
            errors.append("No Trainee Name specified!")

        if self._contactNumber_countryCode is None:
            errors.append("No Country Code specified!")

        if self._referenceNumber is None or len(self._referenceNumber) == 0:
            errors.append("No Attendance Reference Number specified!")

        if self._corppassId is None or len(self._corppassId) == 0:
            errors.append("No CorpPass ID specified!")

        if (self._trainee_email is None or len(self._trainee_email) == 0) and \
                (self._contactNumber_mobile is None or len(self._contactNumber_mobile) == 0):
            errors.append("You need to specify either the trainee's mobile number or email address!")

        if self._trainee_email is not None and len(self._trainee_email) > 0:
            try:
                validate_email(self._trainee_email)
            except EmailSyntaxError:
                errors.append("Trainee Email specified is not of the correct format!")

        # optional param verification
        if self._trainee_email is not None and len(self._trainee_email) == 0:
            warnings.append("No Trainee Email specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        """
        The payload function will do all the heavy lifting in terms of converting the enums into its
        respective values.
        """

        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use validate() to find the "
                                     "missing fields!")

        pl = {
            "uen": st.session_state["uen"] if "uen" in st.session_state else None,
            "course": {
                "sessionID": self._sessionId,
                "attendance": {
                    "status": {
                        "code": self._status_code.value[0] if self._status_code is not None else None
                    },
                    "trainee": {
                        "id": self._trainee_id,
                        "name": self._trainee_name,
                        "email": self._trainee_email,
                        "idType": {
                            "code": self._trainee_id_type.value[0] if self._trainee_id_type is not None else None
                        },
                        "contactNumber": {
                            "mobile": self._contactNumber_mobile,
                            "areaCode": self._contactNumber_areacode,
                            "countryCode": self._contactNumber_countryCode,
                        },
                        "numberOfHours": round(self._numberOfHours, 2) if self._numberOfHours is not None else None,
                        "surveyLanguage": {
                            "code": (self._surveyLanguage_code.value[0]
                                     if self._surveyLanguage_code is not None
                                     else None),
                        }
                    }
                },
                "referenceNumber": self._referenceNumber
            },
            "corppassId": self._corppassId
        }

        # we can exclude the areaCode field and allow it to be null, as documented in the API reference
        pl = remove_null_fields(pl, exclude=UploadAttendanceInfo.EXCLUSION_LIST)

        if as_json_str:
            return json.dumps(pl)

        return pl
