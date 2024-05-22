import base64
import datetime
import json
import streamlit as st

from typing import Optional, Literal
from streamlit.runtime.uploaded_file_manager import UploadedFile

from core.abc.abstract_course import ABCCourseInfo

MODE_OF_TRAINING_MAPPING: dict = {
    "1": "Classroom",
    "2": "Asynchronous eLearning",
    "3": "In-house",
    "4": "On-the-Job",
    "5": "Practical / Practicum",
    "6": "Supervised Field",
    "7": "Traineeship",
    "8": "Assessment",
    "9": "Synchronous Learning"
}

ID_TYPE: dict[str, str] = {
    "SB": "Singapore Blue",
    "SP": "Singapore Pink",
    "SO": "Fin/Work Permit",
    "FP": "Foreign Passport",
    "OT": "Others"
}

SALUTATIONS: dict[int, str] = {
    1: "Mr",
    2: "Ms",
    3: "Mdm,",
    4: "Mrs",
    5: "Dr",
    6: "Prof"
}


# ===== Session Info ===== #
class RunSessionInfo(ABCCourseInfo):
    """Encapsulates all information regarding a course run's sessions"""

    def __init__(self):
        self.sessionId: Optional[str] = None
        self.startDate: Optional[datetime.date] = None
        self.endDate: Optional[datetime.date] = None
        self.startTime: Optional[datetime.time] = None
        self.endTime: Optional[datetime.time] = None
        self.modeOfTraining: Optional[Literal["1", "2", "3", "4", "5", "6", "7", "8", "9"]] = None
        self.venue_block: Optional[str] = None
        self.venue_street: Optional[str] = None
        self.venue_floor: str = None
        self.venue_unit: str = None
        self.venue_building: Optional[str] = None
        self.venue_postalCode: str = None
        self.venue_room: str = None
        self.venue_wheelChairAccess: Optional[bool] = None
        self.venue_primaryVenue: Optional[bool] = None

    def __repr__(self):
        return self.payload(as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self.venue_floor is None or len(self.venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self.venue_unit is None or len(self.venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self.venue_postalCode is None or len(self.venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self.venue_room is None or len(self.venue_room) == 0:
            errors.append("No venue room is specified!")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False) -> dict | str:
        pl = {
            "action": "update",
            "sessionId": self.sessionId,
            "startDate": self.startDate.strftime("%Y%m%d") if self.startDate is not None else None,
            "endDate": self.endDate.strftime("%Y%m%d") if self.endDate is not None else None,
            "startTime": self.startTime.strftime("%H:%M:%S") if self.startTime is not None else None,
            "endTime": self.endTime.strftime("%H:%M:%S") if self.endTime is not None else None,
            "modeOfTraining": self.modeOfTraining,
            "venue": {
                "block": self.venue_block,
                "street": self.venue_street,
                "floor": self.venue_floor,
                "unit": self.venue_unit,
                "building": self.venue_building,
                "postalCode": self.venue_postalCode,
                "room": self.venue_room,
                "wheelChairAccess": self.venue_wheelChairAccess,
                "primaryVenue": self.venue_primaryVenue,
            }
        }

        if as_json_str:
            return json.dumps(pl)

        return pl

    def is_require_venue(self) -> bool:
        return self.modeOfTraining is None and self.modeOfTraining != "2" and self.modeOfTraining != "4"

    def set_session_id(self, session_id: str) -> None:
        if not isinstance(session_id, str):
            raise ValueError("Invalid session id")

        self.sessionId = session_id

    def set_startDate(self, startDate: datetime.date) -> None:
        if not isinstance(startDate, datetime.date):
            raise ValueError("Invalid start date")

        self.startDate = startDate

    def set_endDate(self, endDate: datetime.date) -> None:
        if endDate is not None and not isinstance(endDate, datetime.date):
            raise ValueError("Invalid end date")

        self.endDate = endDate

    def set_startTime(self, startTime: datetime.time) -> None:
        if not isinstance(startTime, datetime.time):
            raise ValueError("Invalid start time")

        self.startTime = startTime

    def set_endTime(self, endTime: datetime.time) -> None:
        if not isinstance(endTime, datetime.time):
            raise ValueError("Invalid end time")

        self.endTime = endTime

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        if not isinstance(modeOfTraining, str) or modeOfTraining not in [
            "1", "2", "3", "4", "5", "6", "7", "8", "9"
        ]:
            raise ValueError("Invalid mode of training")
        self.modeOfTraining = modeOfTraining

    def set_venue_block(self, venue_block: str) -> None:
        if not isinstance(venue_block, str):
            raise ValueError("Invalid venue block")

        self.venue_block = venue_block

    def set_venue_street(self, venue_street: str) -> None:
        if not isinstance(venue_street, str):
            raise ValueError("Invalid venue street")

        self.venue_street = venue_street

    def set_venue_floor(self, venue_floor: str) -> None:
        if not isinstance(venue_floor, str):
            raise ValueError("Invalid venue floor")

        self.venue_floor = venue_floor

    def set_venue_unit(self, venue_unit: str) -> None:
        if not isinstance(venue_unit, str):
            raise ValueError("Invalid venue unit")

        self.venue_unit = venue_unit

    def set_venue_building(self, venue_building: str) -> None:
        if not isinstance(venue_building, str):
            raise ValueError("Invalid venue building")

        self.venue_building = venue_building

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        if not isinstance(venue_postalCode, str):
            raise ValueError("Invalid venue postal code")

        self.venue_postalCode = venue_postalCode

    def set_venue_room(self, venue_room: str) -> None:
        if not isinstance(venue_room, str):
            raise ValueError("Invalid venue room")

        self.venue_room = venue_room

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(wheelChairAccess, str) or wheelChairAccess not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid wheel chair access indicator")

        match wheelChairAccess:
            case "Select a value":
                self.venue_wheelChairAccess = None
            case "Yes":
                self.venue_wheelChairAccess = True
            case "No":
                self.venue_wheelChairAccess = False

    def set_venue_primaryVenue(self, primaryVenue: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(primaryVenue, str) or primaryVenue not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid primary venue indicator")

        match primaryVenue:
            case "Select a value":
                self.venue_primaryVenue = None
            case "Yes":
                self.venue_primaryVenue = True
            case "No":
                self.venue_primaryVenue = False


class RunSessionAddInfo(RunSessionInfo):
    def __init__(self) -> None:
        super().__init__()

    def validate(self) -> None | list[str]:
        errors = []

        if self.startDate is None:
            errors.append("No start date is specified")

        if self.endDate is None:
            errors.append("No end date is specified")

        if self.startDate > self.endDate:
            errors.append("Start date must be before end date")

        if self.startTime is None:
            errors.append("No start time is specified")

        if self.endTime is None:
            errors.append("No end time is specified")

        if self.startTime > self.endTime:
            errors.append("Starting time must be before ending time")

        if self.modeOfTraining is None or len(self.modeOfTraining) == 0:
            errors.append("No mode of training is specified")

        if self.venue_floor is None or len(self.venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self.venue_unit is None or len(self.venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self.venue_postalCode is None or len(self.venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self.venue_room is None or len(self.venue_room) == 0:
            errors.append("No venue room is specified!")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False):
        pl = super().payload(as_json_str=False)
        pl["action"] = "add"

        if as_json_str:
            return json.dumps(pl)

        return pl


# ===== Trainer Info ===== #
class RunTrainerInfo(ABCCourseInfo):
    """Encapsulates all information regarding a trainer in a course run"""

    def __init__(self):
        self.trainerType_code: str = None
        self.trainerType_description: str = None
        self.indexNumber: Optional[int] = None
        self.id: Optional[str] = None
        self.name: str = None
        self.email: str = None
        self.idNumber: str = None
        self.idType_code: Literal["SB", "SP", "SO", "FP", "OT"] = None
        self.idType_description: Literal["Singapore Pink Identification Card",
                                         "Singapore Blue Identification Card",
                                         "FIN/Work Permit",
                                         "Foreign Passport",
                                         "Others"] = None
        self.roles: list[dict] = []
        self.inTrainingProviderProfile: Optional[bool] = None
        self.domainAreaOfPractice: Optional[str] = None
        self.experience: Optional[str] = None
        self.linkedInURL: Optional[str] = None
        self.salutationId: Optional[Literal[1, 2, 3, 4, 5, 6]] = None
        self.photo_name: Optional[str] = None
        self.photo_content: Optional[UploadedFile] = None
        self.linkedSsecEQAs: Optional[list[dict]] = []

    def __repr__(self):
        return self.payload()

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self.trainerType_code is None or len(self.trainerType_code) == 0:
            errors.append("No trainerType code specified")

        if self.trainerType_description is None or len(self.trainerType_description) == 0:
            errors.append("No trainerType description specified")

        if self.name is None or len(self.name) == 0:
            errors.append("No name specified")

        if self.email is None or len(self.email) == 0:
            errors.append("No email specified")

        if self.idNumber is None or len(self.idNumber) == 0:
            errors.append("No Trainer ID number specified")

        if self.idType_code is None or self.idType_description is None or len(self.idType_description) == 0 or \
                len(self.idType_code) == 0:
            errors.append("No Trainer ID type specified")

        if self.roles is None or len(self.roles) == 0:
            errors.append("No roles specified")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False) -> dict | str:
        pl = {
            "trainer": {
                "trainerType": {
                    "code": self.trainerType_code,
                    "description": self.trainerType_description,
                },
                "indexNumber": self.indexNumber,
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "idNumber": self.idNumber,
                "idType": {
                    "code": self.idType_code,
                    "description": self.idType_description,
                },
                "roles": self.roles,
                "inTrainingProviderProfile": self.inTrainingProviderProfile,
                "domainAreaOfPractice": self.domainAreaOfPractice,
                "experience": self.experience,
                "linkedInURL": self.linkedInURL,
                "salutationId": self.salutationId,
                "photo": {
                    "name": self.photo_name,
                    "content": (base64.b64encode(self.photo_content.getvalue() if self.photo_content else b"")
                                .decode("utf-8"))
                },
                "linkedSsecEQAs": self.linkedSsecEQAs
            }
        }

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_trainer_type_code(self, trainer_type: str) -> None:
        if not isinstance(trainer_type, str):
            raise ValueError("Invalid trainer type")

        self.trainerType_code = trainer_type

    def set_trainer_type_description(self, trainer_type_description: str) -> None:
        if not isinstance(trainer_type_description, str):
            raise ValueError("Invalid trainer type description")

        self.trainerType_description = trainer_type_description

    def set_indexNumber(self, indexNumber: int) -> None:
        if not isinstance(indexNumber, int):
            raise ValueError("Invalid indexNumber")

        self.indexNumber = indexNumber

    def set_trainer_id(self, id: str) -> None:
        if not isinstance(id, str):
            raise ValueError("Invalid trainer id")

        self.id = id

    def set_trainer_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("Invalid trainer name")

        self.name = name

    def set_trainer_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise ValueError("Invalid trainer email")

        self.email = email

    def set_trainer_idNumber(self, idNumber: str) -> None:
        if not isinstance(idNumber, str):
            raise ValueError("Invalid trainer idNumber")

        self.idNumber = idNumber

    def set_trainer_idType(self, idType: Literal["SB", "SP", "SO", "FP", "OT"]) -> None:
        if not isinstance(idType, str) or idType not in ["SB", "SP", "SO", "FP", "OT"]:
            raise ValueError("Invalid trainer idType")

        self.idType_code = idType
        self.idType_description = ID_TYPE[idType]

    def set_trainer_roles(self, roles: list[dict]) -> None:
        if not isinstance(roles, list):
            raise ValueError("Invalid trainer roles")

        self.roles = roles

    def add_trainer_role(self, role: dict) -> None:
        if not isinstance(role, dict):
            raise ValueError("Invalid trainer role")

        self.roles.append(role)

    def set_inTrainingProviderProfile(self, inTrainingProviderProfile: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(inTrainingProviderProfile, str) or \
                inTrainingProviderProfile not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid In Training Provider Profile indicator")

        match inTrainingProviderProfile:
            case "Select a value":
                self.inTrainingProviderProfile = None
            case "Yes":
                self.inTrainingProviderProfile = True
            case "No":
                self.inTrainingProviderProfile = False

    def set_domainAreaOfPractice(self, domainAreaOfPractice: str) -> None:
        if not isinstance(domainAreaOfPractice, str):
            raise ValueError("Invalid domainAreaOfPractice")

        self.domainAreaOfPractice = domainAreaOfPractice

    def set_experience(self, experience: str) -> None:
        if not isinstance(experience, str):
            raise ValueError("Invalid experience")

        self.experience = experience

    def set_linkedInURL(self, linkedInURL: str) -> None:
        if not isinstance(linkedInURL, str):
            raise ValueError("Invalid linkedInURL")

        self.linkedInURL = linkedInURL

    def set_salutationId(self, salutationId: int) -> None:
        if not isinstance(salutationId, int):
            raise ValueError("Invalid salutationId")

        self.salutationId = salutationId

    def set_photo_name(self, photo_name: str) -> None:
        if not isinstance(photo_name, str):
            raise ValueError("Invalid photo_name")

        self.photo_name = photo_name

    def set_photo_content(self, photo_content: UploadedFile) -> None:
        if photo_content is not None and not isinstance(photo_content, UploadedFile):
            raise ValueError("Invalid photo_content")

        self.photo_content = photo_content

    def set_linkedSsecEQAs(self, linkedSsecEQAs: list[dict]) -> None:
        if not isinstance(linkedSsecEQAs, list):
            raise ValueError("Invalid linkedSsecEQAs")

        self.linkedSsecEQAs = linkedSsecEQAs

    def add_linkedSsecEQA(self, linkedSsecEQA: dict) -> None:
        if not isinstance(linkedSsecEQA, dict):
            raise ValueError("Invalid linkedSsecEQA")

        self.linkedSsecEQAs.append(linkedSsecEQA)


class RunTrainerAddInfo(RunTrainerInfo):
    def __init__(self) -> None:
        super().__init__()

    def validate(self) -> None | list[str]:
        errors = []

        if self.trainerType_code is None or len(self.trainerType_code) == 0:
            errors.append("No trainerType code specified")

        if self.trainerType_description is None or len(self.trainerType_description) == 0:
            errors.append("No trainerType description specified")

        if self.name is None or len(self.name) == 0:
            errors.append("No name specified")

        if self.email is None or len(self.email) == 0:
            errors.append("No email specified")

        if self.idNumber is None or len(self.idNumber) == 0:
            errors.append("No id number specified")

        if self.idType_code is None or self.idType_description is None or len(self.idType_description) == 0 or \
                len(self.idType_code) == 0:
            errors.append("No id type code specified")

        if self.roles is None or len(self.roles) == 0:
            errors.append("No roles specified")

        if len(errors) > 0:
            return errors


# ===== Run Info ===== #
class RunInfo(ABCCourseInfo):
    """Encapsulates all information regarding the editing of a single course run"""

    ACTION_DESCRIPTION = "Action to be performed to the course run, i.e. update or delete"
    SEQUENCE_NUMBER_DESCRIPTION = "Sequence number, defaults to 0"
    REGISTRATION_DATE_DESCRIPTION_OPENING = ("Course run registration opening date as YYYYMMDD format, "
                                             "timezone -> UTC+08:00")
    REGISTRATION_DATE_DESCRIPTION_CLOSING = ("Course run registration opening date as YYYYMMDD format, "
                                             "timezone -> UTC+08:00")

    def __init__(self):
        self.crid: str = None
        self.sequenceNumber: Optional[int] = None
        self.registrationDates_opening: Optional[datetime.date] = None
        self.registrationDates_closing: Optional[datetime.date] = None
        self.courseDates_start: Optional[datetime.date] = None
        self.courseDates_end: Optional[datetime.date] = None
        self.scheduleInfoType_code: Optional[str] = None
        self.scheduleInfoType_description: Optional[str] = None
        self.scheduleInfo: Optional[str] = None
        self.venue_block: Optional[str] = None
        self.venue_street: Optional[str] = None
        self.venue_floor: Optional[str] = None
        self.venue_unit: Optional[str] = None
        self.venue_building: Optional[str] = None
        self.venue_postalCode: Optional[str] = None
        self.venue_room: Optional[str] = None
        self.venue_wheelChairAccess: Optional[bool] = None
        self.intakeSize: Optional[int] = None
        self.threshold: Optional[int] = None
        self.registeredUserCount: Optional[int] = None
        self.modeOfTraining: Optional[str] = None
        self.courseAdminEmail: Optional[str] = None
        self.courseVacancy_code: Optional[str] = None
        self.courseVacancy_description: Optional[str] = None
        self.file_Name: Optional[str] = None
        self.file_content: Optional[UploadedFile] = None
        self.sessions: Optional[list[RunSessionInfo]] = []
        self.linkCourseRunTrainer: Optional[list] = []

    def __repr__(self):
        return self.payload(as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self.crid is None or len(self.crid) == 0:
            errors.append("No Course Reference ID specified!")

        if len(self.sessions) > 0:
            for session in self.sessions:
                validations = session.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Session {num + 1}: {validation}")

        if len(self.linkCourseRunTrainer) > 0:
            for trainer in self.linkCourseRunTrainer:
                validations = trainer.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Trainer {num + 1}: {validation}")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False) -> dict | str:
        pl = {
            "course": {
                "courseReferenceNumber": self.crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"]
                }
            },
            "run": {
                "action": "update",
                "sequenceNumber": self.sequenceNumber,
                "registrationDates": {
                    "opening": (int(self.registrationDates_opening.strftime("%Y%m%d"))
                                if self.registrationDates_opening is not None else None),
                    "closing": (int(self.registrationDates_closing.strftime("%Y%m%d"))
                                if self.registrationDates_closing is not None else None),
                },
                "courseDates": {
                    "start": (int(self.courseDates_start.strftime("%Y%m%d"))
                              if self.courseDates_start is not None else None),
                    "end": (int(self.courseDates_end.strftime("%Y%m%d"))
                            if self.courseDates_end is not None else None),
                },
                "scheduleInfoType": {
                    "code": self.scheduleInfoType_code,
                    "description": self.scheduleInfoType_description
                },
                "scheduleInfo": self.scheduleInfo,
                "venue": {
                    "block": self.venue_block,
                    "street": self.venue_street,
                    "floor": self.venue_floor,
                    "unit": self.venue_unit,
                    "building": self.venue_building,
                    "postalCode": self.venue_postalCode,
                    "room": self.venue_room,
                    "wheelChairAccess": self.venue_wheelChairAccess
                },
                "intakeSize": self.intakeSize,
                "threshold": self.threshold,
                "registeredUserCount": self.registeredUserCount,
                "modeOfTraining": self.modeOfTraining,
                "courseAdminEmail": self.courseAdminEmail,
                "courseVacancy": {
                    "code": self.courseVacancy_code,
                    "description": self.courseVacancy_description
                },
                "file": {
                    "Name": self.file_Name,
                    "content": (base64.b64encode(self.file_content.getvalue() if self.file_content else b"")
                                .decode("utf-8")),
                },
                "sessions": list(map(lambda x: x.payload(), self.sessions)),
                "linkCourseRunTrainer": list(map(lambda x: x.payload(), self.linkCourseRunTrainer))
            }
        }

        if as_json_str:
            return json.dumps(pl)

        return pl

    def is_require_venue(self) -> bool:
        return self.modeOfTraining is None and self.modeOfTraining != "2" and self.modeOfTraining != "4"

    def set_crid(self, crn: str) -> None:
        if not isinstance(crn, str):
            raise ValueError("Invalid Course Reference ID number")

        self.crid = crn

    def set_sequence_number(self, sequence_number: int) -> None:
        if not isinstance(sequence_number, int):
            raise ValueError("Invalid sequence number")

        self.sequenceNumber = sequence_number

    def set_registrationDates_opening(self, registrationDates_opening: datetime.date) -> None:
        if not isinstance(registrationDates_opening, datetime.date):
            raise ValueError("Invalid opening registration dates")

        self.registrationDates_opening = registrationDates_opening

    def set_registrationDates_closing(self, registrationDates_closing: datetime.date) -> None:
        if not isinstance(registrationDates_closing, datetime.date):
            raise ValueError("Invalid closing registration dates")

        self.registrationDates_closing = registrationDates_closing

    def set_courseDates_start(self, courseDates_start: datetime.date) -> None:
        if not isinstance(courseDates_start, datetime.date):
            raise ValueError("Invalid start course dates")

        self.courseDates_start = courseDates_start

    def set_courseDates_end(self, courseDates_end: datetime.date) -> None:
        if not isinstance(courseDates_end, datetime.date):
            raise ValueError("Invalid end course dates")

        self.courseDates_end = courseDates_end

    def set_scheduleInfoType_code(self, scheduleInfoType_code: str) -> None:
        if not isinstance(scheduleInfoType_code, str):
            raise ValueError("Invalid schedule info type code")

        self.scheduleInfoType_code = scheduleInfoType_code

    def set_scheduleInfoType_description(self, scheduleInfoType_description: str) -> None:
        if not isinstance(scheduleInfoType_description, str):
            raise ValueError("Invalid schedule info type description")

        self.scheduleInfoType_description = scheduleInfoType_description

    def set_scheduleInfo(self, scheduleInfo: str) -> None:
        if not isinstance(scheduleInfo, str):
            raise ValueError("Invalid schedule info")

        self.scheduleInfo = scheduleInfo

    def set_venue_block(self, venue_block: str) -> None:
        if not isinstance(venue_block, str):
            raise ValueError("Invalid venue block")

        self.venue_block = venue_block

    def set_venue_street(self, venue_street: str) -> None:
        if not isinstance(venue_street, str):
            raise ValueError("Invalid venue street address")

        self.venue_street = venue_street

    def set_venue_floor(self, venue_floor: str) -> None:
        if not isinstance(venue_floor, str):
            raise ValueError("Invalid venue floor address")

        self.venue_floor = venue_floor

    def set_venue_unit(self, venue_unit: str) -> None:
        if not isinstance(venue_unit, str):
            raise ValueError("Invalid venue unit")

        self.venue_unit = venue_unit

    def set_venue_building(self, venue_building: str) -> None:
        if not isinstance(venue_building, str):
            raise ValueError("Invalid venue building")

        self.venue_building = venue_building

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        if not isinstance(venue_postalCode, str):
            raise ValueError("Invalid venue postal code")

        self.venue_postalCode = venue_postalCode

    def set_venue_room(self, venue_room: str) -> None:
        if not isinstance(venue_room, str):
            raise ValueError("Invalid venue room")

        self.venue_room = venue_room

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        if not isinstance(wheelChairAccess, str) or wheelChairAccess not in ["Select a value", "Yes", "No"]:
            raise ValueError("Invalid wheel chair access")

        match wheelChairAccess:
            case "Select a value":
                self.venue_wheelChairAccess = None
            case "Yes":
                self.venue_wheelChairAccess = True
            case "No":
                self.venue_wheelChairAccess = False

    def set_intakeSize(self, intakeSize: int) -> None:
        if not isinstance(intakeSize, int):
            raise ValueError("Invalid intake size")

        self.intakeSize = intakeSize

    def set_threshold(self, threshold: int) -> None:
        if not isinstance(threshold, int):
            raise ValueError("Invalid threshold")

        self.threshold = threshold

    def set_registeredUserCount(self, registeredUserCount: int) -> None:
        if not isinstance(registeredUserCount, int):
            raise ValueError("Invalid registered user count")

        self.registeredUserCount = registeredUserCount

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        if not isinstance(modeOfTraining, str):
            raise ValueError("Invalid mode of training")

        self.modeOfTraining = modeOfTraining

    def set_courseAdminEmail(self, courseAdminEmail: str) -> None:
        if not isinstance(courseAdminEmail, str):
            raise ValueError("Invalid course admin email")

        self.courseAdminEmail = courseAdminEmail

    def set_courseVacancy_code(self, courseVacancy_code: str) -> None:
        if not isinstance(courseVacancy_code, str):
            raise ValueError("Invalid course vacancy code")

        self.courseVacancy_code = courseVacancy_code

    def set_courseVacancy_description(self, courseVacancy_description: str) -> None:
        if not isinstance(courseVacancy_description, str):
            raise ValueError("Invalid course vacancy description")

        self.courseVacancy_description = courseVacancy_description

    def set_file_Name(self, file_Name: str) -> None:
        if not isinstance(file_Name, str):
            raise ValueError("Invalid file name")

        self.file_Name = file_Name

    def set_file_content(self, file_content: UploadedFile) -> None:
        if file_content is not None and not isinstance(file_content, UploadedFile):
            raise ValueError("Invalid file content")

        self.file_content = file_content

    def set_sessions(self, sessions: list[RunSessionInfo]) -> None:
        if not isinstance(sessions, list):
            raise ValueError("Invalid list of sessions")

        self.sessions = sessions

    def add_session(self, session: RunSessionInfo) -> None:
        if not isinstance(session, RunSessionInfo):
            raise ValueError("Invalid session")

        self.sessions.append(session)

    def set_linkCourseRunTrainer(self, linkCourseRunTrainer: list) -> None:
        if not isinstance(linkCourseRunTrainer, list):
            raise ValueError("Invalid course run trainer information")

        self.linkCourseRunTrainer = linkCourseRunTrainer

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerInfo) -> None:
        if not isinstance(linkCourseRunTrainer, RunTrainerInfo):
            raise ValueError("Invalid course run trainer information")

        self.linkCourseRunTrainer.append(linkCourseRunTrainer)


class DeleteRunInfo(RunInfo):
    """Encapsulates all information regarding the deletion of a course run"""

    def __init__(self) -> None:
        super().__init__()
        self.includeExpired: Literal["Select a value", "Yes", "No"] = None

    def validate(self) -> None | list[str]:
        errors = []

        if self.crid is None or len(self.crid) == 0:
            errors.append("No valid Course Reference ID number specified")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False) -> dict | str:
        pl = {
            "course": {
                "courseReferenceNumber": self.crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"]
                },
                "run": {
                    "action": "delete"
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

        if self.crid is None or len(self.crid) == 0:
            errors.append("No Course Reference ID number specified")

        if self.registrationDates_opening is None:
            errors.append("No opening registration dates specified")

        if self.registrationDates_closing is None:
            errors.append("No closing registration dates specified")

        if self.registrationDates_opening > self.registrationDates_closing:
            errors.append("Registration dates opening should not be after closing date")

        if self.courseDates_start is None:
            errors.append("No start course dates specified")

        if self.courseDates_end is None:
            errors.append("No end course dates specified")

        if self.courseDates_start > self.courseDates_end:
            errors.append("Start course dates should not be after end course date")

        if self.scheduleInfoType_code is None or len(self.scheduleInfoType_code) == 0:
            errors.append("No schedule info type code specified")

        if self.scheduleInfoType_description is None or len(self.scheduleInfoType_description) == 0:
            errors.append("No schedule info type description specified")

        if self.scheduleInfo is None or len(self.scheduleInfo) == 0:
            errors.append("No schedule info specified")

        if self.venue_floor is None or len(self.venue_floor) == 0:
            errors.append("No venue floor is specified")

        if self.venue_unit is None or len(self.venue_unit) == 0:
            errors.append("No venue unit is specified")

        if self.venue_postalCode is None or len(self.venue_postalCode) == 0:
            errors.append("No venue postal code is specified")

        if self.venue_room is None or len(self.venue_room) == 0:
            errors.append("No venue room is specified")

        if self.modeOfTraining is None or len(self.modeOfTraining) == 0:
            errors.append("No mode of training is specified")

        if self.courseAdminEmail is None or len(self.courseAdminEmail) == 0:
            errors.append("No course admin email is specified")

        if self.courseVacancy_code is None or len(self.courseVacancy_code) == 0:
            errors.append("No course vacancy code is specified")

        if self.courseVacancy_description is None or len(self.courseVacancy_description) == 0:
            errors.append("No course vacancy description is specified")

        if len(self.sessions) > 0:
            for session in self.sessions:
                validations = session.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Session {num + 1}: {validation}")

        if len(self.linkCourseRunTrainer) > 0:
            for trainer in self.linkCourseRunTrainer:
                validations = trainer.validate()

                for num, validation in enumerate(validations):
                    errors.append(f"Trainer {num + 1}: {validation}")

        if len(errors) > 0:
            return errors

    def payload(self, as_json_str: bool = False) -> dict | str:
        pl = {
            "course": {
                "courseReferenceNumber": self.crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"]
                }
            },
            "runs": [
                {
                    "sequenceNumber": self.sequenceNumber,
                    "registrationDates": {
                        "opening": (int(self.registrationDates_opening.strftime("%Y%m%d"))
                                    if self.registrationDates_opening is not None else None),
                        "closing": (int(self.registrationDates_closing.strftime("%Y%m%d"))
                                    if self.registrationDates_closing is not None else None),
                    },
                    "courseDates": {
                        "start": (int(self.courseDates_start.strftime("%Y%m%d"))
                                  if self.courseDates_start is not None else None),
                        "end": (int(self.courseDates_end.strftime("%Y%m%d"))
                                if self.courseDates_end is not None else None),
                    },
                    "scheduleInfoType": {
                        "code": self.scheduleInfoType_code,
                        "description": self.scheduleInfoType_description
                    },
                    "scheduleInfo": self.scheduleInfo,
                    "venue": {
                        "block": self.venue_block,
                        "street": self.venue_street,
                        "floor": self.venue_floor,
                        "unit": self.venue_unit,
                        "building": self.venue_building,
                        "postalCode": self.venue_postalCode,
                        "room": self.venue_room,
                        "wheelChairAccess": self.venue_wheelChairAccess
                    },
                    "intakeSize": self.intakeSize,
                    "threshold": self.threshold,
                    "registeredUserCount": self.registeredUserCount,
                    "modeOfTraining": self.modeOfTraining,
                    "courseAdminEmail": self.courseAdminEmail,
                    "courseVacancy": {
                        "code": self.courseVacancy_code,
                        "description": self.courseVacancy_description
                    },
                    "file": {
                        "Name": self.file_Name,
                        "content": (base64.b64encode(self.file_content.getvalue() if self.file_content else b"")
                                    .decode("utf-8")),
                    },
                    "sessions": list(map(lambda x: x.payload(), self.sessions)),
                    "linkCourseRunTrainer": list(map(lambda x: x.payload(), self.linkCourseRunTrainer))
                }
            ]
        }

        if as_json_str:
            return json.dumps(pl)

        return pl
