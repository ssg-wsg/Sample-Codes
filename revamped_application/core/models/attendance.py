"""
Contains classes that help encapsulate data for sending requests to the Attendance APIs.
"""

import json
import streamlit as st

from typing import Optional, Annotated
from email_validator import validate_email

from revamped_application.core.constants import SurveyLanguage, Attendance, IdType
from revamped_application.utils.json_utils import remove_null_fields
from revamped_application.core.abc.abstract import AbstractRequestInfo


class UploadAttendanceInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course session attendance"""

    EXCLUSION_LIST: tuple[str] = ("areaCode", )

    sessionId_: str = None
    status_code_: Attendance = None
    trainee_id_: Annotated[str, "string($varchar(50))"] = None
    trainee_name_: Annotated[str, "string($varchar(66))"] = None
    trainee_email_: Annotated[str, "string($varchar(320))"] = None
    trainee_id_type_: Annotated[IdType, "string($varchar(2))"] = None
    contactNumber_mobile_: Annotated[str, "string($varchar(15))"] = None
    contactNumber_areacode_: Annotated[Optional[int], "integer($number(5))"] = None
    contactNumber_countryCode_: Annotated[int, "integer($number(3))"] = None
    numberOfHours_: Annotated[Optional[float], "0.5 - 8.0; mandatory for On-the-Job Mode of Training"] = None
    surveyLanguage_code_: Annotated[SurveyLanguage, "string($varchar(2))"] = None
    referenceNumber_: str = None
    corppassId_: str = None

    @property
    def sessionId(self):
        return self.sessionId_

    @sessionId.setter
    def sessionId(self, sessionId: str):
        if not isinstance(sessionId, str):
            raise ValueError("Invalid session ID")

        self.sessionId_ = sessionId

    @property
    def status_code(self):
        return self.status_code_

    @status_code.setter
    def status_code(self, status_code: Attendance):
        if not isinstance(status_code, Attendance):
            try:
                status_code = Attendance(status_code)
            except Exception:
                raise ValueError("Invalid status code")

        self.status_code_ = status_code

    @property
    def trainee_id(self):
        return self.trainee_id_

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        if not isinstance(trainee_id, str):
            raise ValueError("Invalid trainee ID")

        self.trainee_id_ = trainee_id

    @property
    def trainee_name(self):
        return self.trainee_name_

    @trainee_name.setter
    def trainee_name(self, trainee_name: str):
        if not isinstance(trainee_name, str):
            raise ValueError("Invalid trainee name")

        self.trainee_name_ = trainee_name

    @property
    def trainee_email(self):
        return self.trainee_email_

    @trainee_email.setter
    def trainee_email(self, trainee_email: str):
        if not isinstance(trainee_email, str):
            raise ValueError("Invalid trainee email")

        self.trainee_email_ = trainee_email

    @property
    def trainee_id_type(self):
        return self.trainee_id_type_

    @trainee_id_type.setter
    def trainee_id_type(self, trainee_id_type: IdType):
        if not isinstance(trainee_id_type, IdType):
            raise ValueError("Invalid trainee ID type")

        self.trainee_id_type_ = trainee_id_type

    @property
    def contactNumber_mobile(self):
        return self.contactNumber_mobile_

    @contactNumber_mobile.setter
    def contactNumber_mobile(self, contactNumber_mobile: str):
        if not isinstance(contactNumber_mobile, str):
            raise ValueError("Invalid trainee contact number")

        self.contactNumber_mobile_ = contactNumber_mobile

    @property
    def contactNumber_areacode(self):
        return self.contactNumber_areacode_

    @contactNumber_areacode.setter
    def contactNumber_areacode(self, contactNumber_areacode: int):
        if not isinstance(contactNumber_areacode, int):
            raise ValueError("Invalid trainee contact number area code")

        self.contactNumber_areacode_ = contactNumber_areacode

    @property
    def contactNumber_countryCode(self):
        return self.contactNumber_countryCode_

    @contactNumber_countryCode.setter
    def contactNumber_countryCode(self, contactNumber_countryCode: int):
        if not isinstance(contactNumber_countryCode, int):
            raise ValueError("Invalid trainee contact number country code")

        self.contactNumber_countryCode_ = contactNumber_countryCode

    @property
    def numberOfHours(self):
        return self.numberOfHours_

    @numberOfHours.setter
    def numberOfHours(self, numberOfHours: float):
        if not isinstance(numberOfHours, float) or numberOfHours < 0.5 or numberOfHours > 8.0:
            raise ValueError("Invalid number of hours")

        self.numberOfHours_ = numberOfHours

    @property
    def surveyLanguage_code(self):
        return self.surveyLanguage_code_

    @surveyLanguage_code.setter
    def surveyLanguage_code(self, surveyLanguage_code: SurveyLanguage):
        if not isinstance(surveyLanguage_code, SurveyLanguage):
            raise ValueError("Invalid survey language code")

        self.surveyLanguage_code_ = surveyLanguage_code

    @property
    def referenceNumber(self):
        return self.referenceNumber_

    @referenceNumber.setter
    def referenceNumber(self, referenceNumber: str):
        if not isinstance(referenceNumber, str):
            raise ValueError("Invalid reference number")

        self.referenceNumber_ = referenceNumber

    @property
    def corppassId(self):
        return self.corppassId_

    @corppassId.setter
    def corppassId(self, corppassId: str):
        if not isinstance(corppassId, str):
            raise ValueError("Invalid CorpPass ID")

        self.corppassId_ = corppassId

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, UploadAttendanceInfo):
            return False

        return (
            self.sessionId_ == other.sessionId_
            and self.status_code_ == other.status_code_
            and self.trainee_id_ == other.trainee_id_
            and self.trainee_name_ == other.trainee_name_
            and self.trainee_email_ == other.trainee_email_
            and self.trainee_id_type_ == other.trainee_id_type_
            and self.contactNumber_mobile_ == other.contactNumber_mobile_
            and self.contactNumber_areacode_ == other.contactNumber_areacode_
            and self.contactNumber_countryCode_ == other.contactNumber_countryCode_
            and self.numberOfHours_ == other.numberOfHours_
            and self.surveyLanguage_code_ == other.surveyLanguage_code_
            and self.referenceNumber_ == other.referenceNumber_
            and self.corppassId_ == other.corppassId_
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self.sessionId_ is None or len(self.sessionId_) == 0:
            errors.append("No Session ID specified!")

        if self.trainee_id_ is None or len(self.trainee_id_) == 0:
            errors.append("No Trainee ID specified!")

        if self.trainee_name_ is None or len(self.trainee_name_) == 0:
            errors.append("No Trainee Name specified!")

        if self.contactNumber_countryCode_ is None:
            errors.append("No Country Code specified!")

        if self.referenceNumber_ is None or len(self.referenceNumber_) == 0:
            errors.append("No Attendance Reference Number specified!")

        if self.corppassId_ is None or len(self.corppassId_) == 0:
            errors.append("No CorpPass ID specified!")

        if (self.trainee_email_ is None or len(self.trainee_email_) == 0) and \
                (self.contactNumber_mobile_ is None or len(self.contactNumber_mobile_) == 0):
            errors.append("You need to specify either the trainee's mobile number or email address!")

        if self.trainee_email_ is not None and len(self.trainee_email_) > 0:
            try:
                validate_email(self.trainee_email_)
            except Exception:
                errors.append("Email specified is not of the correct format!")

        # optional param verification
        if self.trainee_email_ is not None and len(self.trainee_email_) == 0:
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
                "sessionID": self.sessionId_,
                "attendance": {
                    "status": {
                        "code": self.status_code_.value[0] if self.status_code_ is not None else None
                    },
                    "trainee": {
                        "id": self.trainee_id_,
                        "name": self.trainee_name_,
                        "email": self.trainee_email_,
                        "idType": {
                            "code": self.trainee_id_type_.value[0] if self.trainee_id_type_ is not None else None
                        },
                        "contactNumber": {
                            "mobile": self.contactNumber_mobile_,
                            "areaCode": self.contactNumber_areacode_,
                            "countryCode": self.contactNumber_countryCode_,
                        },
                        "numberOfHours": round(self.numberOfHours_, 2) if self.numberOfHours_ is not None else None,
                        "surveyLanguage": {
                            "code": (self.surveyLanguage_code_.value[0]
                                     if self.surveyLanguage_code_ is not None
                                     else None),
                        }
                    }
                },
                "referenceNumber": self.referenceNumber_
            },
            "corppassId": self.corppassId_
        }

        # we can exclude the areaCode field and allow it to be null, as documented in the API reference
        pl = remove_null_fields(pl, exclude=UploadAttendanceInfo.EXCLUSION_LIST)

        if as_json_str:
            return json.dumps(pl)

        return pl
