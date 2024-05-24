import json
import streamlit as st

from typing import Optional

from core.constants import ID_TYPE_MAPPING, SURVEY_LANGUAGE_MAPPINGS, ATTENDANCE_CODE_MAPPINGS
from utils.json_utils import remove_null_fields
from core.abc.abstract import AbstractRequestInfo


class UploadAttendanceInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course session attendance"""

    def __init__(self):
        self._sessionId: str = None
        self._status_code: str = None
        self._trainee_id: str = None
        self._trainee_name: str = None
        self._trainee_email: Optional[str] = None
        self._trainee_id_type: str = None
        self._contactNumber_mobile: str = None
        self._contactNumber_areacode: Optional[int] = None
        self._contactNumber_countryCode: int = None
        self._numberOfHours: Optional[float] = None
        self._surveyLanguage_code: str = None
        self._referenceNumber: str = None
        self._corppassId: str = None

    def __repr__(self):
        return self.payload(as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._sessionId is None or len(self._sessionId) == 0:
            errors.append("No session ID specified!")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No trainee ID specified!")

        if self._trainee_name is None or len(self._trainee_name) == 0:
            errors.append("No trainee name specified!")

        if self._trainee_id_type not in ID_TYPE_MAPPING:
            errors.append("Unknown trainee ID type!")

        if self._contactNumber_countryCode is None:
            errors.append("No country code specified!")

        if self._surveyLanguage_code is None or len(self._surveyLanguage_code) == 0:
            errors.append("No survey language code specified!")

        if self._referenceNumber is None or len(self._referenceNumber) == 0:
            errors.append("No reference number specified!")

        if self._corppassId is None or len(self._corppassId) == 0:
            errors.append("No CorpPass ID specified!")

        if self._trainee_email is None and (self._contactNumber_mobile is None or len(self._contactNumber_mobile) == 0):
            errors.append("You need to specify either the trainee's mobile number or email address!")

        # optional param verification
        if self._trainee_email is not None and len(self._trainee_email) == 0:
            errors.append("No trainee email specified!")



        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "uen": st.session_state["uen"],
            "course": {
                "sessionID": self._sessionId,
                "attendance": {
                    "status": {
                        "code": self._status_code
                    },
                    "trainee": {
                        "id": self._trainee_id,
                        "name": self._trainee_name,
                        "email": self._trainee_email,
                        "idType": {
                            "code": self._trainee_id_type
                        },
                        "contactNumber": {
                            "mobile": self._contactNumber_mobile,
                            "areaCode": self._contactNumber_areacode,
                            "countryCode": self._contactNumber_countryCode,
                        },
                        "numberOfHours": round(self._numberOfHours, 2) if self._numberOfHours is not None else None,
                        "surveyLanguage": {
                            "code": self._surveyLanguage_code,
                        }
                    }
                },
                "referenceNumber": self._referenceNumber
            },
            "corppassId": self._corppassId
        }

        # we can exclude the areaCode field and allow it to be null, as documented in the API reference
        pl = remove_null_fields(pl, exclude=("areaCode", ))

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_sessionId(self, sessionId: str) -> None:
        if not isinstance(sessionId, str):
            raise ValueError("Invalid session ID")

        self._sessionId = sessionId

    def set_statusCode(self, status_code: str) -> None:
        if not isinstance(status_code, str) or status_code not in ATTENDANCE_CODE_MAPPINGS:
            raise ValueError("Invalid status code")

        self._status_code = status_code

    def set_trainee_id(self, trainee_id: str) -> None:
        if not isinstance(trainee_id, str):
            raise ValueError("Invalid trainee ID")

        self._trainee_id = trainee_id

    def set_trainee_name(self, trainee_name: str) -> None:
        if not isinstance(trainee_name, str):
            raise ValueError("Invalid trainee name")

        self._trainee_name = trainee_name

    def set_trainee_email(self, trainee_email: str) -> None:
        if not isinstance(trainee_email, str):
            raise ValueError("Invalid trainee email")

        self._trainee_email = trainee_email

    def set_trainee_id_type(self, trainee_id_type: str) -> None:
        if not isinstance(trainee_id_type, str) or trainee_id_type not in ID_TYPE_MAPPING:
            raise ValueError("Invalid trainee ID type")

        self._trainee_id_type = trainee_id_type

    def set_contactNumber_mobile(self, contactNumber_mobile: str) -> None:
        if not isinstance(contactNumber_mobile, str):
            raise ValueError("Invalid trainee contact number")

        self._contactNumber_mobile = contactNumber_mobile

    def set_contactNumber_areacode(self, contactNumber_areacode: int) -> None:
        if not isinstance(contactNumber_areacode, int):
            raise ValueError("Invalid trainee contact number area code")

        self._contactNumber_areacode = contactNumber_areacode

    def set_contactNumber_countryCode(self, contactNumber_countryCode: int) -> None:
        if not isinstance(contactNumber_countryCode, int):
            raise ValueError("Invalid trainee contact number country code")

        self._contactNumber_countryCode = contactNumber_countryCode

    def set_numberOfHours(self, numberOfHours: float) -> None:
        if not isinstance(numberOfHours, float):
            raise ValueError("Invalid number of hours")

        self._numberOfHours = numberOfHours

    def set_surveyLanguage_code(self, surveyLanguage_code: str) -> None:
        if not isinstance(surveyLanguage_code, str) or surveyLanguage_code not in SURVEY_LANGUAGE_MAPPINGS:
            raise ValueError("Invalid survey language code")

        self._surveyLanguage_code = surveyLanguage_code

    def set_referenceNumber(self, referenceNumber: str) -> None:
        if not isinstance(referenceNumber, str):
            raise ValueError("Invalid reference number")

        self._referenceNumber = referenceNumber

    def set_corppassId(self, corppassId: str) -> None:
        if not isinstance(corppassId, str):
            raise ValueError("Invalid CorpPass ID")

        self._corppassId = corppassId
