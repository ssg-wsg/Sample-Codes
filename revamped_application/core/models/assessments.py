import json
import streamlit as st

import datetime
from typing import Optional, Literal

from core.abc.abstract import AbstractRequestInfo
from core.constants import GRADES, ID_TYPE, RESULTS, ASSESSMENT_UPDATE_VOID_ACTIONS, \
    SORT_FIELD, SORT_ORDER
from utils.verify import verify_uen
from utils.json_utils import remove_null_fields


class CreateAssessmentInfo(AbstractRequestInfo):
    """Encapsulates information about the creation of an assessment record"""

    def __init__(self):
        self._grade: Optional[Literal["A", "B", "C", "D", "E", "F"]] = None
        self._score: Optional[int] = None
        self._course_runId: str = None
        self._course_referenceNumber: str = None
        self._result: Literal["Pass", "Fail", "Exempt"] = None
        self._trainee_id: str = None
        self._trainee_idType: Literal["NRIC", "FIN", "OTHERS"] = None
        self._trainee_fullName: str = None
        self._skillCode: Optional[str] = None
        self._assessmentDate: datetime.date = None
        self._trainingPartner_code: str = None
        self._trainingPartner_uen: Optional[str] = None
        self._conferringInstitute_code: Optional[str] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

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

        if self._trainingPartner_uen is not None and not verify_uen(self._trainingPartner_uen):
            errors.append("Specified Training Partner UEN is invalid!")

        # optional parameter verification
        if self._skillCode is not None and len(self._skillCode) == 0:
            warnings.append("Skill Code is empty even though Skill Code is marked as specified!")

        if self._conferringInstitute_code is not None and len(self._conferringInstitute_code) == 0:
            warnings.append("Conferring Institute Code is empty even though Conferring Institute Code is marked "
                            "as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
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
                    "uen": st.session_state["uen"] if self._trainingPartner_uen is None else self._trainingPartner_uen,
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

    def set_score(self, score: int) -> None:
        if not isinstance(score, int):
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

    def set_trainingPartner_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise ValueError(f"Invalid Training Partner UEN provided")

        self._trainingPartner_uen = uen

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
        self._assessmentReferenceNumber: str = None

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._assessmentReferenceNumber is None or len(self._assessmentReferenceNumber) == 0:
            errors.append("Invalid Assessment Reference Number provided!")

        if self._action is None or self._action not in ASSESSMENT_UPDATE_VOID_ACTIONS:
            errors.append("No Action provided!")

        if self._result is not None and self._result not in RESULTS:
            errors.append("Result must be of values: [Pass, Fail, Exempt]")

        # optionals check
        if self._trainee_fullName is not None and len(self._trainee_fullName) == 0:
            warnings.append("Trainee Full Name is empty even though Trainee Full Name is marked as specified!")

        if self._skillCode is not None and len(self._skillCode) == 0:
            warnings.append("Skill Code is empty even though Skill Code is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
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

    def get_assessment_reference_number(self) -> str:
        return self._assessmentReferenceNumber

    def set_assessment_referenceNumber(self, assessment_reference_number: str) -> None:
        if not isinstance(assessment_reference_number, str):
            raise ValueError(f"Invalid Assessment Reference Number provided")

        self._assessmentReferenceNumber = assessment_reference_number

    def is_update(self) -> bool:
        return self._action == "update"

    def set_action(self, action: Literal["update", "void"]) -> None:
        if not isinstance(action, str) or action not in ASSESSMENT_UPDATE_VOID_ACTIONS:
            raise ValueError(f"Invalid Action provided")

        self._action = action


class SearchAssessmentInfo(AbstractRequestInfo):
    """Encapsulates information about the searching for an assessment record"""

    def __init__(self):
        self._lastUpdateDateTo: Optional[datetime.date] = None
        self._lastUpdateDateFrom: Optional[datetime.date] = None
        self._sortBy_field: Optional[Literal["updatedOn", "createdOn", "assessmentDate"]] = None
        self._sortBy_order: Optional[str] = None
        self._parameters_page: int = None
        self._parameters_pageSize: int = None
        self._assessment_courseRunId: Optional[str] = None
        self._assessment_referenceNumber: Optional[str] = None
        self._assessment_traineeId: Optional[str] = None
        self._assessment_enrolement_referenceNumber: Optional[str] = None
        self._assessment_skillCode: Optional[str] = None
        self._trainingPartner_uen: Optional[str] = None
        self._trainingPartner_code: Optional[str] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._lastUpdateDateTo is not None and self._lastUpdateDateFrom is not None \
                and (self._lastUpdateDateFrom > self._lastUpdateDateTo):
            errors.append("Last Update Date From cannot be greater than Last Update Date To!")

        if self._parameters_page is None:
            errors.append("Page number is not specified!")

        if self._parameters_pageSize is None:
            errors.append("Page size is not specified!")

        if self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0 and \
                not verify_uen(self._trainingPartner_uen):
            errors.append("Invalid Training Partner UEN specified!")

        # optionals check
        if self._assessment_courseRunId is not None and len(self._assessment_courseRunId) == 0:
            warnings.append("Course Run ID is empty even though Course Run ID is marked as specified!")

        if self._assessment_referenceNumber is not None and len(self._assessment_referenceNumber) == 0:
            warnings.append("Reference Number is empty even though Reference Number is marked as specified!")

        if self._assessment_traineeId is not None and len(self._assessment_traineeId) == 0:
            warnings.append("Trainee ID is empty even though Trainee ID is marked as specified!")

        if self._assessment_enrolement_referenceNumber is not None and \
                len(self._assessment_enrolement_referenceNumber) == 0:
            warnings.append("Enrolment Reference Number is empty even though Enrolment Reference Number "
                            "is marked as specified!")

        if self._assessment_skillCode is not None and len(self._assessment_skillCode) == 0:
            warnings.append("Skill Code is empty even though Skill Code is marked as specified!")

        if self._trainingPartner_uen is not None and len(self._trainingPartner_uen) == 0:
            warnings.append("Training Partner UEN is empty even though Training Partner UEN is marked as specified!")

        if self._trainingPartner_code is not None and len(self._trainingPartner_code) == 0:
            warnings.append("Training Partner Code is empty even though Training Partner Code is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if err is not None and len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "meta": {
                "lastUpdateDateTo": (self._lastUpdateDateTo.strftime("%Y-%m-%d")
                                     if self._lastUpdateDateTo is not None else None),
                "lastUpdateDateFrom": (self._lastUpdateDateFrom.strftime("%Y-%m-%d")
                                       if self._lastUpdateDateFrom is not None else None),
            },
            "sortBy": {
                "field": self._sortBy_field,
                "order": self._sortBy_order,
            },
            "parameters": {
                "page": self._parameters_page,
                "pageSize": self._parameters_pageSize,
            },
            "assessment": {
                "course": {
                    "run": {
                        "id": self._assessment_courseRunId
                    },
                    "referenceNumber": self._assessment_referenceNumber,
                }
            },
            "trainee": {
                "id": self._assessment_traineeId,
            },
            "enrolment": {
                "referenceNumber": self._assessment_enrolement_referenceNumber
            },
            "skillCode": self._assessment_skillCode,
            "trainingPartner": {
                "uen": self._trainingPartner_uen if self._trainingPartner_uen is not None else st.session_state["uen"],
                "code": self._trainingPartner_code,
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_lastUpdateDateTo(self, lastUpdateDateTo: datetime.date) -> None:
        if not isinstance(lastUpdateDateTo, datetime.date):
            raise ValueError(f"Invalid Last Update Date provided")

        self._lastUpdateDateTo = lastUpdateDateTo

    def set_lastUpdateDateFrom(self, lastUpdateDateFrom: datetime.date) -> None:
        if not isinstance(lastUpdateDateFrom, datetime.date):
            raise ValueError(f"Invalid Last Update Date provided")

        self._lastUpdateDateFrom = lastUpdateDateFrom

    def set_sortBy_field(self, sortBy_field: str) -> None:
        if not isinstance(sortBy_field, str) or sortBy_field not in SORT_FIELD:
            raise ValueError(f"Invalid Sort By Field provided")

        self._sortBy_field = sortBy_field

    def set_sortBy_order(self, sortBy_order: str) -> None:
        if not isinstance(sortBy_order, str) or sortBy_order not in SORT_ORDER:
            raise ValueError(f"Invalid Sort By Order provided")

        self._sortBy_order = sortBy_order

    def set_page(self, page: int) -> None:
        if not isinstance(page, int):
            raise ValueError(f"Invalid Page provided")

        self._parameters_page = page

    def set_pageSize(self, pageSize: int) -> None:
        if not isinstance(pageSize, int):
            raise ValueError(f"Invalid Page size provided")

        self._parameters_pageSize = pageSize

    def set_courseRunId(self, courseRunId: str) -> None:
        if not isinstance(courseRunId, str):
            raise ValueError(f"Invalid Course Run ID provided")

        self._assessment_courseRunId = courseRunId

    def set_courseReferenceNumber(self, courseReferenceNumber: str) -> None:
        if not isinstance(courseReferenceNumber, str):
            raise ValueError(f"Invalid Course Reference Number provided")

        self._assessment_referenceNumber = courseReferenceNumber

    def set_trainee_id(self, traineeId: str) -> None:
        if not isinstance(traineeId, str):
            raise ValueError(f"Invalid Trainee ID provided")

        self._assessment_traineeId = traineeId

    def set_enrolment_referenceNumber(self, enrolmentReferenceNumber: str) -> None:
        if not isinstance(enrolmentReferenceNumber, str):
            raise ValueError(f"Invalid Enrolment Reference Number provided")

        self._assessment_enrolement_referenceNumber = enrolmentReferenceNumber

    def set_skillCode(self, skillCode: str) -> None:
        if not isinstance(skillCode, str):
            raise ValueError(f"Invalid Skill Code provided")

        self._assessment_skillCode = skillCode

    def set_trainingPartner_code(self, trainingPartner_code: str) -> None:
        if not isinstance(trainingPartner_code, str):
            raise ValueError(f"Invalid Training Partner Code provided")

        self._trainingPartner_code = trainingPartner_code

    def set_trainingPartner_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise ValueError(f"Invalid Training Partner UEN provided")

        self._trainingPartner_uen = uen
