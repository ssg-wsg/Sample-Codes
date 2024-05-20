import base64
import datetime
import json
import streamlit as st

from typing import Optional, Literal
from streamlit.runtime.uploaded_file_manager import UploadedFile

from core.abc.abstract import AbstractRequestInfo
from utils.json_utils import remove_null_fields


# ===== Session Info ===== #
class RunSessionInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course run's sessions"""

    def __init__(self, action: Literal["add", "update", "delete"]):
        if action not in ["add", "update", "delete"]:
            raise ValueError(f"Invalid action: {action}")

        self._action: Literal["add", "update", "delete"] = action
        self._sessionId: Optional[str] = None
        self._startDate: Optional[datetime.date] = None
        self._endDate: Optional[datetime.date] = None
        self._startTime: Optional[datetime.time] = None
        self._endTime: Optional[datetime.time] = None
        self._modeOfTraining: Optional[Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]] = None
        self._venue_block: Optional[str] = None
        self._venue_street: Optional[str] = None
        self._venue_floor: str = None
        self._venue_unit: str = None
        self._venue_building: Optional[str] = None
        self._venue_postalCode: str = None
        self._venue_room: str = None
        self._venue_wheelChairAccess: Optional[bool] = None
        self._venue_primaryVenue: Optional[bool] = None

    def __repr__(self):
        return self.payload(as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._action is None or len(self._action) == 0:
            errors.append("No action specified!")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "action": self._action,
            "sessionId": self._sessionId,
            "startDate": self._startDate.strftime("%Y%m%d"),
            "endDate": self._endDate.strftime("%Y%m%d"),
            "startTime": self._startTime.strftime("%H:%M:%S"),
            "endTime": self._endTime.strftime("%H:%M:%S"),
            "modeOfTraining": self._modeOfTraining,
            "venue": {
                "block": self._venue_block,
                "street": self._venue_street,
                "floor": self._venue_floor,
                "unit": self._venue_unit,
                "building": self._venue_building,
                "postalCode": self._venue_postalCode,
                "room": self._venue_room,
                "wheelChairAccess": self._venue_wheelChairAccess,
                "primaryVenue": self._venue_primaryVenue,
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def is_asynchronous_or_on_the_job(self) -> bool:
        return self._modeOfTraining == "2" or self._modeOfTraining == "4"

    def set_session_id(self, session_id: str) -> None:
        if not isinstance(session_id, str):
            raise ValueError("Invalid session id")

        self._sessionId = session_id

    def set_startDate(self, startDate: datetime.date) -> None:
        if not isinstance(startDate, datetime.date):
            raise ValueError("Invalid start date")

        self._startDate = startDate

    def set_endDate(self, endDate: datetime.date) -> None:
        if not isinstance(endDate, datetime.date):
            raise ValueError("Invalid end date")

        self._endDate = endDate

    def set_startTime(self, startTime: datetime.time) -> None:
        if not isinstance(startTime, datetime.time):
            raise ValueError("Invalid start time")

        self._startTime = startTime

    def set_endTime(self, endTime: datetime.time) -> None:
        if not isinstance(endTime, datetime.time):
            raise ValueError("Invalid end time")

        self._endTime = endTime

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        if not isinstance(modeOfTraining, str) or modeOfTraining not in [
            "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]:
            raise ValueError("Invalid mode of training")
        self._modeOfTraining = modeOfTraining

    def set_venue_block(self, venue_block: str) -> None:
        if not isinstance(venue_block, str):
            raise ValueError("Invalid venue block")

        self._venue_block = venue_block

    def set_venue_street(self, venue_street: str) -> None:
        if not isinstance(venue_street, str):
            raise ValueError("Invalid venue street")

        self._venue_street = venue_street

    def set_venue_floor(self, venue_floor: str) -> None:
        if not isinstance(venue_floor, str):
            raise ValueError("Invalid venue floor")

        self._venue_floor = venue_floor

    def set_venue_unit(self, venue_unit: str) -> None:
        if not isinstance(venue_unit, str):
            raise ValueError("Invalid venue unit")

        self._venue_unit = venue_unit

    def set_venue_building(self, venue_building: str) -> None:
        if not isinstance(venue_building, str):
            raise ValueError("Invalid venue building")

        self._venue_building = venue_building

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        if not isinstance(venue_postalCode, str):
            raise ValueError("Invalid venue postal code")

        self._venue_postalCode = venue_postalCode

    def set_venue_room(self, venue_room: str) -> None:
        if not isinstance(venue_room, str):
            raise ValueError("Invalid venue room")

        self._venue_room = venue_room

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(wheelChairAccess, str) or wheelChairAccess not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid wheel chair access indicator")

        match wheelChairAccess:
            case "Select a value":
                self._venue_wheelChairAccess = None
            case "Yes":
                self._venue_wheelChairAccess = True
            case "No":
                self._venue_wheelChairAccess = False

    def set_venue_primaryVenue(self, primaryVenue: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(primaryVenue, str) or primaryVenue not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid primary venue indicator")

        match primaryVenue:
            case "Select a value":
                self._venue_primaryVenue = None
            case "Yes":
                self._venue_primaryVenue = True
            case "No":
                self._venue_primaryVenue = False


class RunSessionAddInfo(RunSessionInfo):
    def __init__(self, action: Literal["add", "update", "delete"]) -> None:
        super().__init__(action)

    def validate(self) -> None | list[str]:
        errors = []

        if self._startDate is None:
            errors.append("No start date is specified")

        if self._endDate is None:
            errors.append("No end date is specified")

        if self._startDate > self._endDate:
            errors.append("Start date must be before end date")

        if self._startTime is None:
            errors.append("No start time is specified")

        if self._endTime is None:
            errors.append("No end time is specified")

        if self._startTime > self._endTime:
            errors.append("Starting time must be before ending time")

        if self._modeOfTraining is None or len(self._modeOfTraining) == 0:
            errors.append("No mode of training is specified")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        if len(errors) > 0:
            return errors


# ===== Trainer Info ===== #
class RunTrainerInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a trainer in a course run"""

    def __init__(self, action: Literal["add", "update", "delete"]):
        if action not in ["add", "update", "delete"]:
            raise ValueError(f"Invalid action: {action}")

        self._trainerType_code: Literal["1", "2"] = None
        self._trainerType_description: str = None
        self._indexNumber: Optional[int] = None
        self._id: Optional[str] = None
        self._name: str = None
        self._email: str = None
        self._idNumber: str = None
        self._idType_code: Literal["SB", "SP", "SO", "FP", "OT"] = None
        self._idType_description: Literal["Singapore Pink Identification Card",
                                         "Singapore Blue Identification Card",
                                         "FIN/Work Permit",
                                         "Foreign Passport",
                                         "Others"] = None
        self._roles: list[dict] = []
        self._inTrainingProviderProfile: Optional[bool] = None
        self._domainAreaOfPractice: Optional[str] = None
        self._experience: Optional[str] = None
        self._linkedInURL: Optional[str] = None
        self._salutationId: Optional[Literal[1, 2, 3, 4, 5, 6]] = None
        self._photo_name: Optional[str] = None
        self._photo_content: Optional[UploadedFile] = None
        self._linkedSsecEQAs: Optional[list[dict]] = []

    def __repr__(self):
        return self.payload()

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._trainerType_code is None or len(self._trainerType_code) == 0:
            errors.append("No trainerType code specified")

        if self._trainerType_description is None or len(self._trainerType_description) == 0:
            errors.append("No trainerType description specified")

        if self._name is None or len(self._name) == 0:
            errors.append("No name specified")

        if self._email is None or len(self._email) == 0:
            errors.append("No email specified")

        if self._idNumber is None or len(self._idNumber) == 0:
            errors.append("No Trainer ID number specified")

        if self._idType_code is None or self._idType_description is None or len(self._idType_description) == 0 or \
                len(self.idType_code) == 0:
            errors.append("No Trainer ID type specified")

        if self._roles is None or len(self._roles) == 0:
            errors.append("No roles specified")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "trainer": {
                "trainerType": {
                    "code": self._trainerType_code,
                    "description": self._trainerType_description,
                },
                "indexNumber": self._indexNumber,
                "id": self._id,
                "name": self._name,
                "email": self._email,
                "idNumber": self._idNumber,
                "idType": {
                    "code": self._idType_code,
                    "description": self._idType_description,
                },
                "roles": self._roles,
                "inTrainingProviderProfile": self._inTrainingProviderProfile,
                "domainAreaOfPractice": self._domainAreaOfPractice,
                "experience": self._experience,
                "linkedInURL": self._linkedInURL,
                "salutationId": self._salutationId,
                "photo": {
                    "name": self._photo_name,
                    "content": self._photo_content
                },
                "linkedSsecEQAs": self._linkedSsecEQAs
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def is_existing_trainer(self):
        if self._trainerType_code is None:
            raise ValueError("Unable to infer trainer type as no trainer type code was provided!")

        return self._trainerType_code == "1"

    def is_new_trainer(self):
        if self._trainerType_code is None:
            raise ValueError("Unable to infer trainer type as no trainer type code was provided!")

        return self._trainerType_code == "2"

    def set_trainer_type_code(self, trainer_type: str) -> None:
        if not isinstance(trainer_type, str):
            raise ValueError("Invalid trainer type")

        self._trainerType_code = trainer_type

    def set_trainer_type_description(self, trainer_type_description: str) -> None:
        if not isinstance(trainer_type_description, str):
            raise ValueError("Invalid trainer type description")

        self._trainerType_description = trainer_type_description

    def set_indexNumber(self, indexNumber: int) -> None:
        if not isinstance(indexNumber, int):
            raise ValueError("Invalid indexNumber")

        self._indexNumber = indexNumber

    def set_trainer_id(self, id: str) -> None:
        if not isinstance(id, str):
            raise ValueError("Invalid trainer id")

        self._id = id

    def set_trainer_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("Invalid trainer name")

        self._name = name

    def set_trainer_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise ValueError("Invalid trainer email")

        self._email = email

    def set_trainer_idNumber(self, idNumber: str) -> None:
        if not isinstance(idNumber, str):
            raise ValueError("Invalid trainer idNumber")

        self._idNumber = idNumber

    def set_trainer_idType(self, idType: Literal["SB", "SP", "SO", "FP", "OT"]) -> None:
        if not isinstance(idType, str) or idType not in ["SB", "SP", "SO", "FP", "OT"]:
            raise ValueError("Invalid trainer idType")

        self._idType_code = idType

        match idType:
            case "SB":
                self._idType_description = "Singapore Blue Identification Card"
            case "SP":
                self._idType_description = "Singapore Pink Identification Card"
            case "SO":
                self._idType_description = "Fin/Work Permit"
            case "FP":
                self._idType_description = "Foreign Passport"
            case "OT":
                self._idType_description = "Others"

    def set_trainer_roles(self, roles: list[dict]) -> None:
        if not isinstance(roles, list):
            raise ValueError("Invalid trainer roles")

        self._roles = roles

    def add_trainer_role(self, role: dict) -> None:
        if not isinstance(role, dict):
            raise ValueError("Invalid trainer role")

        self._roles.append(role)

    def set_inTrainingProviderProfile(self, inTrainingProviderProfile: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(inTrainingProviderProfile, str) or \
                inTrainingProviderProfile not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid In Training Provider Profile indicator")

        match inTrainingProviderProfile:
            case "Select a value":
                self._inTrainingProviderProfile = None
            case "Yes":
                self._inTrainingProviderProfile = True
            case "No":
                self._inTrainingProviderProfile = False

    def set_domainAreaOfPractice(self, domainAreaOfPractice: str) -> None:
        if not isinstance(domainAreaOfPractice, str):
            raise ValueError("Invalid domainAreaOfPractice")

        self._domainAreaOfPractice = domainAreaOfPractice

    def set_experience(self, experience: str) -> None:
        if not isinstance(experience, str):
            raise ValueError("Invalid experience")

        self._experience = experience

    def set_linkedInURL(self, linkedInURL: str) -> None:
        if not isinstance(linkedInURL, str):
            raise ValueError("Invalid linkedInURL")

        self._linkedInURL = linkedInURL

    def set_salutationId(self, salutationId: int) -> None:
        if not isinstance(salutationId, int):
            raise ValueError("Invalid salutationId")

        self._salutationId = salutationId

    def set_photo_name(self, photo_name: str) -> None:
        if not isinstance(photo_name, str):
            raise ValueError("Invalid photo_name")

        self._photo_name = photo_name

    def set_photo_content(self, photo_content: UploadedFile) -> None:
        if photo_content is not None and not isinstance(photo_content, UploadedFile):
            raise ValueError("Invalid photo_content")

        self._photo_content = photo_content

    def set_linkedSsecEQAs(self, linkedSsecEQAs: list[dict]) -> None:
        if not isinstance(linkedSsecEQAs, list):
            raise ValueError("Invalid linkedSsecEQAs")

        self._linkedSsecEQAs = linkedSsecEQAs

    def add_linkedSsecEQA(self, linkedSsecEQA: dict) -> None:
        if not isinstance(linkedSsecEQA, dict):
            raise ValueError("Invalid linkedSsecEQA")

        self._linkedSsecEQAs.append(linkedSsecEQA)


class RunTrainerAddInfo(RunTrainerInfo):
    def __init__(self, action: Literal["add", "update", "delete"]) -> None:
        super().__init__(action)

    def validate(self) -> None | list[str]:
        errors = []

        if self._trainerType_code is None or len(self._trainerType_code) == 0:
            errors.append("No trainerType code specified")

        if self._trainerType_description is None or len(self._trainerType_description) == 0:
            errors.append("No trainerType description specified")

        if self._name is None or len(self._name) == 0:
            errors.append("No name specified")

        if self._email is None or len(self._email) == 0:
            errors.append("No email specified")

        if self._idNumber is None or len(self._idNumber) == 0:
            errors.append("No id number specified")

        if self._idType_code is None or self._idType_description is None or len(self._idType_description) == 0 or \
                len(self.idType_code) == 0:
            errors.append("No id type code specified")

        if self._roles is None or len(self._roles) == 0:
            errors.append("No roles specified")

        if len(errors) > 0:
            return errors


# ===== Run Info ===== #
class RunInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course run"""

    ACTION_DESCRIPTION = "Action to be performed to the course run, i.e. update or delete"
    SEQUENCE_NUMBER_DESCRIPTION = "Sequence number, defaults to 0"
    REGISTRATION_DATE_DESCRIPTION_OPENING = ("Course run registration opening date as YYYYMMDD format, "
                                             "timezone -> UTC+08:00")
    REGISTRATION_DATE_DESCRIPTION_CLOSING = ("Course run registration opening date as YYYYMMDD format, "
                                             "timezone -> UTC+08:00")

    def __init__(self, action: Literal["delete", "update"]="update"):
        if action not in ["add", "update", "delete"]:
            raise ValueError(f"Invalid action: {action}")

        self._action = action
        self._crid: str = None
        self._sequenceNumber: Optional[int] = None
        self._registrationDates_opening: datetime.date = None
        self._registrationDates_closing: datetime.date = None
        self._courseDates_start: datetime.date = None
        self._courseDates_end: datetime.date = None
        self._scheduleInfoType_code: str = None
        self._scheduleInfoType_description: Optional[str] = None
        self._scheduleInfo: Optional[str] = None
        self._venue_block: Optional[str] = None
        self._venue_street: Optional[str] = None
        self._venue_floor: str = None
        self._venue_unit: str = None
        self._venue_building: Optional[str] = None
        self._venue_postalCode: str = None
        self._venue_room: str = None
        self._venue_wheelChairAccess: Optional[bool] = None
        self._intakeSize: Optional[int] = None
        self._threshold: Optional[int] = None
        self._registeredUserCount: Optional[int] = None
        self._modeOfTraining: Optional[str] = None
        self._courseAdminEmail: Optional[str] = None
        self._courseVacancy_code: str = None
        self._courseVacancy_description: Optional[str] = None
        self._file_Name: Optional[str] = None
        self._file_content: Optional[UploadedFile] = None
        self._sessions: Optional[list[RunSessionInfo]] = []
        self._linkCourseRunTrainer: Optional[list] = []

    def __repr__(self):
        return self.payload(as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No Course Reference ID specified")

        if self._action is None or len(self._action) == 0:
            errors.append("No action specfied")

        if self._registrationDates_opening is None:
            errors.append("No opening registrationDates specfied")

        if self._registrationDates_closing is None:
            errors.append("No closing registrationDates specfied")

        if self._registrationDates_opening > self._registrationDates_closing:
            errors.append("Registration dates opening date must be before closing date")

        if self._courseDates_start is None:
            errors.append("No start registrationDates specfied")

        if self._courseDates_end is None:
            errors.append("No end registrationDates specfied")

        if self._courseDates_start > self._courseDates_end:
            errors.append("Registration start date must be before registration end date")

        if self._scheduleInfoType_code is None or len(self._scheduleInfoType_code) == 0:
            errors.append("No scheduleInfoTypeCode specfied")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified")

        if self._courseVacancy_code is None or len(self._courseVacancy_code) == 0:
            errors.append("No course vacancy code is spe_cified")

        if len(self._sessions) > 0:
            for session in self._sessions:
                validations = session.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Session {num + 1}: {validation}")

        if len(self._linkCourseRunTrainer) > 0:
            for trainer in self._linkCourseRunTrainer:
                validations = trainer.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Trainer {num + 1}: {validation}")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "course": {
                "courseReferenceNumber": self._crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"]
                }
            },
            "run": {
                "action": self._action,
                "sequenceNumber": self._sequenceNumber,
                "registrationDates": {
                    "opening": int(self._registrationDates_opening.strftime("%Y%m%d")),
                    "closing": int(self._registrationDates_closing.strftime("%Y%m%d")),
                },
                "courseDates": {
                    "start": int(self._courseDates_start.strftime("%Y%m%d")),
                    "end": int(self._courseDates_end.strftime("%Y%m%d")),
                },
                "scheduleInfoType": {
                    "code": self._scheduleInfoType_code,
                    "description": self._scheduleInfoType_description
                },
                "scheduleInfo": self._scheduleInfo,
                "venue": {
                    "block": self._venue_block,
                    "street": self._venue_street,
                    "floor": self._venue_floor,
                    "unit": self._venue_unit,
                    "building": self._venue_building,
                    "postalCode": self._venue_postalCode,
                    "room": self._venue_room,
                    "wheelChairAccess": self._venue_wheelChairAccess
                },
                "intakeSize": self._intakeSize,
                "threshold": self._threshold,
                "registeredUserCount": self._registeredUserCount,
                "modeOfTraining": self._modeOfTraining,
                "courseAdminEmail": self._courseAdminEmail,
                "courseVacancy": {
                    "code": self._courseVacancy_code,
                    "description": self._courseVacancy_description
                },
                "file": {
                    "Name": self._file_Name,
                    "content": (base64.b64encode(self._file_content.getvalue() if self._file_content else b"")
                                .decode("utf-8")),
                },
                "sessions": list(map(lambda x: x.payload(verify=False), self._sessions)),
                "linkCourseRunTrainer": list(map(lambda x: x.payload(verify=False), self._linkCourseRunTrainer))
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_crid(self, crn: str) -> None:
        if not isinstance(crn, str):
            raise ValueError("Invalid Course Reference ID number")

        self._crid = crn

    def set_sequence_number(self, sequence_number: int) -> None:
        if not isinstance(sequence_number, int):
            raise ValueError("Invalid sequence number")

        self._sequenceNumber = sequence_number

    def set_registrationDates_opening(self, registrationDates_opening: datetime.date) -> None:
        if not isinstance(registrationDates_opening, datetime.date):
            raise ValueError("Invalid opening registration dates")

        self._registrationDates_opening = registrationDates_opening

    def set_registrationDates_closing(self, registrationDates_closing: datetime.date) -> None:
        if not isinstance(registrationDates_closing, datetime.date):
            raise ValueError("Invalid closing registration dates")

        self._registrationDates_closing = registrationDates_closing

    def set_courseDates_start(self, courseDates_start: datetime.date) -> None:
        if not isinstance(courseDates_start, datetime.date):
            raise ValueError("Invalid start course dates")

        self._courseDates_start = courseDates_start

    def set_courseDates_end(self, courseDates_end: datetime.date) -> None:
        if not isinstance(courseDates_end, datetime.date):
            raise ValueError("Invalid end course dates")

        self._courseDates_end = courseDates_end

    def set_scheduleInfoType_code(self, scheduleInfoType_code: str) -> None:
        if not isinstance(scheduleInfoType_code, str):
            raise ValueError("Invalid schedule info type code")

        self._scheduleInfoType_code = scheduleInfoType_code

    def set_scheduleInfoType_description(self, scheduleInfoType_description: str) -> None:
        if not isinstance(scheduleInfoType_description, str):
            raise ValueError("Invalid schedule info type description")

        self._scheduleInfoType_description = scheduleInfoType_description

    def set_scheduleInfo(self, scheduleInfo: str) -> None:
        if not isinstance(scheduleInfo, str):
            raise ValueError("Invalid schedule info")

        self._scheduleInfo = scheduleInfo

    def set_venue_block(self, venue_block: str) -> None:
        if not isinstance(venue_block, str):
            raise ValueError("Invalid venue block")

        self._venue_block = venue_block

    def set_venue_street(self, venue_street: str) -> None:
        if not isinstance(venue_street, str):
            raise ValueError("Invalid venue street address")

        self._venue_street = venue_street

    def set_venue_floor(self, venue_floor: str) -> None:
        if not isinstance(venue_floor, str):
            raise ValueError("Invalid venue floor address")

        self._venue_floor = venue_floor

    def set_venue_unit(self, venue_unit: str) -> None:
        if not isinstance(venue_unit, str):
            raise ValueError("Invalid venue unit")

        self._venue_unit = venue_unit

    def set_venue_building(self, venue_building: str) -> None:
        if not isinstance(venue_building, str):
            raise ValueError("Invalid venue building")

        self._venue_building = venue_building

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        if not isinstance(venue_postalCode, str):
            raise ValueError("Invalid venue postal code")

        self._venue_postalCode = venue_postalCode

    def set_venue_room(self, venue_room: str) -> None:
        if not isinstance(venue_room, str):
            raise ValueError("Invalid venue room")

        self.venue_room = venue_room

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(wheelChairAccess, str) or wheelChairAccess not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid wheel chair access")

        match wheelChairAccess:
            case "Select a value":
                self._venue_wheelChairAccess = None
            case "Yes":
                self._venue_wheelChairAccess = True
            case "No":
                self._venue_wheelChairAccess = False

    def set_intakeSize(self, intakeSize: int) -> None:
        if not isinstance(intakeSize, int):
            raise ValueError("Invalid intake size")

        self._intakeSize = intakeSize

    def set_threshold(self, threshold: int) -> None:
        if not isinstance(threshold, int):
            raise ValueError("Invalid threshold")

        self._threshold = threshold

    def set_registeredUserCount(self, registeredUserCount: int) -> None:
        if not isinstance(registeredUserCount, int):
            raise ValueError("Invalid registered user count")

        self._registeredUserCount = registeredUserCount

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        if not isinstance(modeOfTraining, str):
            raise ValueError("Invalid mode of training")

        self._modeOfTraining = modeOfTraining

    def set_courseAdminEmail(self, courseAdminEmail: str) -> None:
        if not isinstance(courseAdminEmail, str):
            raise ValueError("Invalid course admin email")

        self._courseAdminEmail = courseAdminEmail

    def set_courseVacancy_code(self, courseVacancy_code: str) -> None:
        if not isinstance(courseVacancy_code, str):
            raise ValueError("Invalid course vacancy code")

        self._courseVacancy_code = courseVacancy_code

    def set_courseVacancy_description(self, courseVacancy_description: str) -> None:
        if not isinstance(courseVacancy_description, str):
            raise ValueError("Invalid course vacancy description")

        self._courseVacancy_description = courseVacancy_description

    def set_file_Name(self, file_Name: str) -> None:
        if not isinstance(file_Name, str):
            raise ValueError("Invalid file name")

        self._file_Name = file_Name

    def set_file_content(self, file_content: UploadedFile) -> None:
        if file_content is not None and not isinstance(file_content, UploadedFile):
            raise ValueError("Invalid file content")

        self._file_content = file_content

    def set_sessions(self, sessions: list[RunSessionInfo]) -> None:
        if not isinstance(sessions, list):
            raise ValueError("Invalid list of sessions")

        self._sessions = sessions

    def add_session(self, session: RunSessionInfo) -> None:
        if not isinstance(session, RunSessionInfo):
            raise ValueError("Invalid session")

        self._sessions.append(session)

    def set_linkCourseRunTrainer(self, linkCourseRunTrainer: list) -> None:
        if not isinstance(linkCourseRunTrainer, list):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer = linkCourseRunTrainer

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerInfo) -> None:
        if not isinstance(linkCourseRunTrainer, RunTrainerInfo):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer.append(linkCourseRunTrainer)


class DeleteRunInfo(RunInfo):
    """Encapsulates all information regarding the deletion of a course run"""

    def __init__(self) -> None:
        super().__init__(action="delete")
        self._includeExpired: Literal["Select a value", "Yes", "No"] = None

    def validate(self) -> None | list[str]:
        errors = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No valid Course Reference ID number specified")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "course": {
                "courseReferenceNumber": self._crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"]
                },
                "run": {
                    "action": self._action
                }
            }
        }

        if as_json_str:
            return json.dumps(pl)

        return pl


class AddRunInfo(RunInfo):
    """Encapsulates all information regarding the addition of a course run"""

    def __init__(self):
        super().__init__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No Course Reference ID number specified")

        if self._registrationDates_opening is None:
            errors.append("No opening registration dates specified")

        if self._registrationDates_closing is None:
            errors.append("No closing registration dates specified")

        if self._registrationDates_opening > self._registrationDates_closing:
            errors.append("Registration dates opening should not be after closing date")

        if self._courseDates_start is None:
            errors.append("No start course dates specified")

        if self._courseDates_end is None:
            errors.append("No end course dates specified")

        if self._courseDates_start > self._courseDates_end:
            errors.append("Start course dates should not be after end course date")

        if self._scheduleInfoType_code is None or len(self._scheduleInfoType_code) == 0:
            errors.append("No schedule info type code specified")

        if self._scheduleInfoType_description is None or len(self._scheduleInfoType_description) == 0:
            errors.append("No schedule info type description specified")

        if self._scheduleInfo is None or len(self._scheduleInfo) == 0:
            errors.append("No schedule info specified")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified")

        if self._modeOfTraining is None or len(self._modeOfTraining) == 0:
            errors.append("No mode of training is specified")

        if self._courseAdminEmail is None or len(self._courseAdminEmail) == 0:
            errors.append("No course admin email is specified")

        if self._courseVacancy_code is None or len(self._courseVacancy_code) == 0:
            errors.append("No course vacancy code is specified")

        if self._courseVacancy_description is None or len(self._courseVacancy_description) == 0:
            errors.append("No course vacancy description is specified")

        if len(self._sessions) > 0:
            for session in self._sessions:
                validations = session.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Session {num + 1}: {validation}")

        if len(self._linkCourseRunTrainer) > 0:
            for trainer in self._linkCourseRunTrainer:
                validations = trainer.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Trainer {num + 1}: {validation}")

        if len(errors) > 0:
            return errors
