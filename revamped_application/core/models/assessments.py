import json
import streamlit as st

import datetime
from typing import Optional, Literal

from core.abc.abstract import AbstractRequestInfo
from core.constants import GRADES, ID_TYPE, RESULTS, ASSESSMENT_UPDATE_VOID_ACTIONS
from utils.json_utils import remove_null_fields


class CreateAssessmentInfo(AbstractRequestInfo):
    """Encapsulates information about the creation of an assessment record"""

    def __init__(self):
        self._grade: Optional[Literal["A", "B", "C", "D", "E", "F"]] = None
        self._score: Optional[int | float] = None
        self._course_runId: str = None
        self._course_referenceNumber: str = None
        self._result: Literal["Pass", "Fail", "Exempt"] = None
        self._trainee_id: str = None
        self._trainee_idType: Literal["NRIC", "FIN", "OTHERS"] = None
        self._trainee_fullName: str = None
        self._skillCode: Optional[str] = None
        self._assessmentDate: datetime.date = None
        self._trainingPartner_code: str = None
        self._conferringInstitute_code: Optional[str] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._course_runId is None or len(self._course_runId) == 0:
            errors.append("No Course Run ID is provided!")

        if self._course_referenceNumber is None or len(self._course_referenceNumber) == 0:
            errors.append("No Course Reference Number is provided!")

        if self._result is None or self._result not in RESULTS:
            errors.append("Result must be of values: [Pass, Fail, Exempt]")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No Trainee ID is provided!")

        if self._trainee_idType is None or self._trainee_idType not in ID_TYPE:
            errors.append("Invalid Trainee ID Type!")

        if self._trainee_fullName is None or len(self._trainee_fullName) == 0:
            errors.append("No Trainee Full Name is provided!")

        if self._assessmentDate is None:
            errors.append("No Assessment Date is provided!")

        if self._trainingPartner_code is None or len(self._trainingPartner_code) == 0:
            errors.append("No Training Partner Code is provided!")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "assessment": {
                "grade": self._grade,
                "score": self._score,
                "course": {
                    "run": {
                        "id": self._course_runId
                    },
                    "referenceNumber": self._course_referenceNumber
                },
                "result": self._result,
                "trainee": {
                    "id": self._trainee_id,
                    "idType": self._trainee_idType,
                    "fullName": self._trainee_fullName
                },
                "skillCode": self._skillCode,
                "assessmentDate": self._assessmentDate.strftime("%Y-%m-%d"),
                "trainingPartner": {
                    "uen": st.session_state["uen"],
                    "code": self._trainingPartner_code
                },
                "conferringInstitute": {
                    "code": self._conferringInstitute_code
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def get_referenceNumber(self) -> str:
        return self._course_referenceNumber

    def set_grade(self, grade: Literal["A", "B", "C", "D", "E", "F"]) -> None:
        if grade not in GRADES:
            raise ValueError(f"Invalid Grade provided")

        self._grade = grade

    def set_score(self, score: float | int) -> None:
        if not isinstance(score, float) and not isinstance(score, int):
            raise ValueError(f"Invalid Score provided")

        self._score = score

    def set_course_runId(self, course_run_id: str) -> None:
        if not isinstance(course_run_id, str):
            raise ValueError(f"Invalid Course Run ID provided")

        self._course_runId = course_run_id

    def set_course_referenceNumber(self, course_reference_number: str) -> None:
        if not isinstance(course_reference_number, str):
            raise ValueError(f"Invalid Course Reference Number provided")

        self._course_referenceNumber = course_reference_number

    def set_result(self, result: Literal["Pass", "Fail", "Exempt"]) -> None:
        if result not in RESULTS:
            raise ValueError(f"Invalid Result provided")

        self._result = result

    def set_trainee_id(self, idType: str) -> None:
        if not isinstance(idType, str):
            raise ValueError(f"Invalid Trainee ID provided")

        self._trainee_id = idType

    def set_trainee_id_type(self, idType: Literal["NRIC", "FIN", "OTHERS"]) -> None:
        if idType not in ID_TYPE:
            raise ValueError(f"Invalid Trainee ID Type provided")

        self._trainee_idType = idType

    def set_trainee_fullName(self, fullName: str) -> None:
        if not isinstance(fullName, str):
            raise ValueError(f"Invalid Trainee Full Name provided")

        self._trainee_fullName = fullName

    def set_skillCode(self, skillCode: str) -> None:
        if not isinstance(skillCode, str):
            raise ValueError(f"Invalid Skill Code provided")

        self._skillCode = skillCode

    def set_assessmentDate(self, assessmentDate: datetime.date) -> None:
        if not isinstance(assessmentDate, datetime.date):
            raise ValueError(f"Invalid Assessment Date provided")

        self._assessmentDate = assessmentDate

    def set_trainingPartner_code(self, trainingPartner_code: str) -> None:
        if not isinstance(trainingPartner_code, str):
            raise ValueError(f"Invalid Training Partner Code provided")

        self._trainingPartner_code = trainingPartner_code

    def set_conferringInstitute_code(self, conferringInstitute_code: str) -> None:
        if not isinstance(conferringInstitute_code, str):
            raise ValueError(f"Invalid Conferring Institute Code provided")

        self._conferringInstitute_code = conferringInstitute_code


class UpdateVoidAssessmentInfo(CreateAssessmentInfo):
    """Encapsulates information about the updating or voiding of an assessment record"""

    def __init__(self):
        super().__init__()
        self._action: Literal["update", "void"] = None

    def validate(self) -> None | list[str]:
        if self._action is None or self._action not in ["update", "void"]:
            return ["No action provided!"]

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "assessment": {
                "grade": self._grade,
                "score": self._score,
                "action": self._action,
                "result": self._result,
                "trainee": {
                    "fullName": self._trainee_fullName,
                },
                "skillCode": self._skillCode,
                "assessmentDate": (self._assessmentDate.strftime("%Y-%m-%d")
                                   if self._assessmentDate is not None else None),
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def is_void(self) -> bool:
        return self._action == "void"

    def is_update(self) -> bool:
        return self._action == "update"

    def set_action(self, action: Literal["update", "void"]) -> None:
        if not isinstance(action, str) or action not in ASSESSMENT_UPDATE_VOID_ACTIONS:
            raise ValueError(f"Invalid Action provided")

        self._action = action
