"""
Contains classes that help encapsulate data for sending requests to the Assessments APIs.
"""

import json
import streamlit as st

import datetime
from typing import Optional, Literal

from revamped_application.core.abc.abstract import AbstractRequestInfo
from revamped_application.core.constants import (Grade, IdTypeSummary, Results, AssessmentUpdateVoidActions,
                                                 SortField, SortOrder)
from revamped_application.utils.verify import verify_uen
from revamped_application.utils.json_utils import remove_null_fields


class CreateAssessmentInfo(AbstractRequestInfo):
    """Encapsulates information about the creation of an assessment record"""

    def __init__(self):
        self._grade: Optional[Grade] = None
        self._score: Optional[int] = None
        self._course_runId: str = None
        self._course_referenceNumber: str = None
        self._result: Results = None
        self._trainee_id: str = None
        self._trainee_idType: IdTypeSummary = None
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

    def __eq__(self, other):
        if not isinstance(other, CreateAssessmentInfo):
            return False

        return (
            self._grade == other._grade
            and self._score == other._score
            and self._course_runId == other._course_runId
            and self._course_referenceNumber == other._course_referenceNumber
            and self._result == other._result
            and self._trainee_id == other._trainee_id
            and self._trainee_idType == other._trainee_idType
            and self._trainee_fullName == other._trainee_fullName
            and self._skillCode == other._skillCode
            and self._assessmentDate == other._assessmentDate
            and self._trainingPartner_code == other._trainingPartner_code
            and self._trainingPartner_uen == other._trainingPartner_uen
            and self._conferringInstitute_code == other._conferringInstitute_code
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._course_runId is None or len(self._course_runId) == 0:
            errors.append("No Course Run ID is provided!")

        if self._course_referenceNumber is None or len(self._course_referenceNumber) == 0:
            errors.append("No Course Reference Number is provided!")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No Trainee ID is provided!")

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
                raise AttributeError("There are some required fields that are missing! Use validate() to find the "
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

    def set_grade(self, grade: Grade) -> None:
        if not isinstance(grade, Grade):
            try:
                grade = Grade(grade)
            except Exception:
                raise ValueError(f"Invalid Grade provided")

        self._grade = grade.value

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

    def set_result(self, result: Results) -> None:
        if not isinstance(result, Results):
            try:
                result = Results(result)
            except Exception:
                raise ValueError(f"Invalid Result provided!")

        self._result = result.value

    def set_traineeId(self, id: str) -> None:
        if not isinstance(id, str):
            raise ValueError(f"Invalid Trainee ID provided")

        self._trainee_id = id

    def set_trainee_id_type(self, idType: IdTypeSummary) -> None:
        if not isinstance(idType, IdTypeSummary):
            try:
                idType = IdTypeSummary(idType)
            except Exception:
                raise ValueError(f"Invalid Trainee ID Type provided!")

        self._trainee_idType = idType.value

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
        self._action: AssessmentUpdateVoidActions = None
        self._assessmentReferenceNumber: str = None

    def __eq__(self, other):
        if not isinstance(other, UpdateVoidAssessmentInfo):
            return False

        return (
            super().__eq__(other)
            and self._action == other._action
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._action is None:
            errors.append("No Action provided!")

        # action, score and assessment date is automatically specified if the user mark it as specified
        if self._trainee_fullName is not None and len(self._trainee_fullName) == 0:
            warnings.append("Trainee Full Name is empty even though Trainee Full Name is marked as specified!")

        if self._skillCode is not None and len(self._skillCode) == 0:
            warnings.append("Skill Code is empty even though Skill Code is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use validate() to find the "
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

    def is_update(self) -> bool:
        return self._action == "update"

    def set_action(self, action: Literal["update", "void"]) -> None:
        if not isinstance(action, AssessmentUpdateVoidActions):
            try:
                action = AssessmentUpdateVoidActions(action)
            except Exception:
                raise ValueError(f"Invalid Action provided")

        self._action = action.value

    def get_referenceNumber(self) -> str:
        raise NotImplementedError("This method is not supported!")

    def set_conferringInstitute_code(self, conferringInstitute_code: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_trainingPartner_code(self, trainingPartner_code: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_trainingPartner_uen(self, uen: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_trainee_id_type(self, idType: IdTypeSummary) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_traineeId(self, id: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_course_referenceNumber(self, course_reference_number: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_course_runId(self, course_run_id: str) -> None:
        raise NotImplementedError("This method is not supported!")


class SearchAssessmentInfo(AbstractRequestInfo):
    """Encapsulates information about the searching for an assessment record"""

    def __init__(self):
        self._lastUpdateDateTo: Optional[datetime.date] = None
        self._lastUpdateDateFrom: Optional[datetime.date] = None
        self._sortBy_field: Optional[SortField] = None
        self._sortBy_order: Optional[SortOrder] = None
        self._parameters_page: int = None
        self._parameters_pageSize: int = None
        self._assessment_courseRunId: Optional[str] = None
        self._assessment_referenceNumber: Optional[str] = None
        self._assessment_traineeId: Optional[str] = None
        self._assessment_enrolement_referenceNumber: Optional[str] = None
        self._assessment_skillCode: Optional[str] = None
        self._trainingPartner_uen: Optional[str] = None
        self._trainingPartner_code: Optional[str] = None

    def __eq__(self, other):
        if not isinstance(other, SearchAssessmentInfo):
            return False

        return (
            self._lastUpdateDateTo == other._lastUpdateDateTo
            and self._lastUpdateDateFrom == other._lastUpdateDateFrom
            and self._sortBy_field == other._sortBy_field
            and self._sortBy_order == other._sortBy_order
            and self._parameters_page == other._parameters_page
            and self._parameters_pageSize == other._parameters_pageSize
            and self._assessment_courseRunId == other._assessment_courseRunId
            and self._assessment_referenceNumber == other._assessment_referenceNumber
            and self._assessment_traineeId == other._assessment_traineeId
            and self._assessment_enrolement_referenceNumber == other._assessment_enrolement_referenceNumber
            and self._assessment_skillCode == other._assessment_skillCode
            and self._trainingPartner_uen == other._trainingPartner_uen
            and self._trainingPartner_code == other._trainingPartner_code
        )

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

    def set_sortBy_field(self, sortBy_field: SortField) -> None:
        if not isinstance(sortBy_field, SortField):
            try:
                sortBy_field = SortField(sortBy_field)
            except Exception:
                raise ValueError(f"Invalid Sort By Field provided")

        self._sortBy_field = sortBy_field.value

    def set_sortBy_order(self, sortBy_order: SortOrder) -> None:
        if not isinstance(sortBy_order, SortOrder):
            try:
                sortBy_order = SortOrder(sortBy_order)
            except Exception:
                raise ValueError(f"Invalid Sort By Order provided")

        self._sortBy_order = sortBy_order.value[0]

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

    def set_traineeId(self, traineeId: str) -> None:
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
