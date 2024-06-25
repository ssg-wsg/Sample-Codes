"""
Contains classes that help encapsulate data for sending requests to the Course Runs / Sessions APIs.
"""

import base64
import datetime
import json
import streamlit as st

from typing import Optional, Literal, Annotated

from email_validator import validate_email, EmailSyntaxError
from streamlit.runtime.uploaded_file_manager import UploadedFile
from core.abc.abstract import AbstractRequestInfo
from core.constants import Vacancy, ModeOfTraining, IdType, Salutations, Role, OptionalSelector
from utils.json_utils import remove_null_fields


class LinkedSSECEQA(AbstractRequestInfo):
    """
    Class to represent a Linked SSEC EQA entry.

    Values taken from https://www.singstat.gov.sg/-/media/files/standards_and_classifications/educational_
    classification/classification-of-lea-eqa-and-fos-ssec-2020.ashx.
    """

    VALID_SSECEQA_MAPPINGS = {
        '0': 'NO FORMAL QUALIFICATION / PRE-PRIMARY / LOWER PRIMARY',
        '01': 'Never attended school',
        '02': 'Pre-Primary (i.e. Nursery, Kindergarten 1, Kindergarten 2)',
        '03': 'Primary education without Primary School Leaving Examination (PSLE) / '
        'Primary School Proficiency Examination (PSPE) certificate or equivalent',
        '04': 'Certificate in BEST 1-3',
        '1': 'PRIMARY',
        '11': 'Primary School Leaving Examination (PSLE) / Primary School Proficiency '
        'Examination (PSPE) certificate or equivalent',
        '12': 'Certificate in BEST 4',
        '13': 'At least 3 achievements for different Workplace Literacy or Numeracy '
        '(WPLN) skills at Level 1 or 2',
        '2': 'LOWER SECONDARY',
        '21': "Secondary education without any subject pass at GCE 'O'/'N' Level or equivalent",
        '22': 'Certificate in WISE 1-3',
        '23': 'Basic vocational certificate (including ITE Basic Vocational Training)',
        '24': 'At least 3 achievements for different Workplace Literacy or Numeracy '
        '(WPLN) skills at Level 3 or 4',
        '3': 'SECONDARY',
        '31': "At least 1 subject pass at GCE 'N' Level",
        '32': "At least 1 subject pass at GCE 'O' Level",
        '33': 'National ITE Certificate (Intermediate) or equivalent (including National '
        'Technical Certificate (NTC) Grade 3, Certificate of Vocational Training, '
        'BCA Builder Certificate)',
        '34': 'ITE Skills Certificate (ISC) or equivalent (including Certificate of '
        'Competency, Certificate in Service Skills)',
        '35': 'At least 3 achievements for different Workplace Literacy or Numeracy '
        '(WPLN) skills at Level 5 and above',
        '39': 'Other secondary education/certificates or equivalent',
        '4': 'POST-SECONDARY (NON-TERTIARY): GENERAL AND VOCATIONAL',
        '41': "At least 1 subject pass at GCE 'A'/'H2' Level or equivalent (general)",
        '42': 'National ITE Certificate (Nitec) or equivalent (including Post Nitec '
        'Certificate,Specialist Nitec, Certificate in Office Skills,'
        'National Technical Certificate (NTC) Grade 2, National Certificate in Nursing,'
        'BCA Advanced Builder Certificate)',
        '43': 'Higher Nitec or equivalent (including Certificate in Business Skills,'
        'Industrial Technician Certificate)',
        '44': 'Master Nitec or equivalent (including NTC Grade 1)',
        '45': 'WSQ Certificate or equivalent',
        '46': 'WSQ Higher Certificate or equivalent',
        '47': 'WSQ Advanced Certificate or equivalent',
        '48': 'Other post-secondary (non-tertiary; general) qualifications or equivalent '
        '(including International Baccalaureate / NUS High School Diploma)',
        '49': 'Other post-secondary (non-tertiary; vocational) certificates/qualifications '
        'or equivalent (including SIM certificate)',
        '5': 'POLYTECHNIC DIPLOMA',
        '51': 'Polytechnic diploma',
        '52': 'Polytechnic post-diploma (including polytechnic advanced/specialist/'
        'management/graduate diploma, diploma (conversion))',
        '6': 'PROFESSIONAL QUALIFICATION AND OTHER DIPLOMA',
        '61': 'ITE diploma',
        '62': 'Other locally or externally developed diploma (including NIE diploma, '
        'SIM diploma, LASALLE diploma, NAFA diploma)',
        '63': 'Qualification awarded by professional bodies (including ACCA, CFA)',
        '64': 'WSQ diploma',
        '65': 'WSQ specialist diploma',
        '69': 'Other post-diploma qualifications or equivalent',
        '7': "BACHELOR'S OR EQUIVALENT",
        '71': 'First degree or equivalent',
        '72': 'Long first degree or equivalent',
        '8': "POSTGRADUATE DIPLOMA/CERTIFICATE (EXCLUDING MASTER'S AND DOCTORATE)",
        '81': 'Postgraduate diploma/certificate (including NIE postgraduate diploma)',
        '82': 'WSQ graduate certificate',
        '83': 'WSQ graduate diploma',
        '9': "MASTER'S AND DOCTORATE OR EQUIVALENT",
        '91': "Master's degree or equivalent",
        '92': 'Doctoral degree or equivalent',
        'N': 'MODULAR CERTIFICATION (NON-AWARD COURSES / NON-FULL QUALIFICATIONS)',
        'N1': 'At least 1 WSQ Statement of Attainment or ITE modular certificate at '
        'post-secondary level (non-tertiary) or equivalent',
        'N2': 'At least 1 WSQ Statement of Attainment or other modular certificate at '
        'diploma level or equivalent (including polytechnic post-diploma certificate)',
        'N3': 'At least 1 WSQ Statement of Attainment or other modular certificate at degree '
        'level or equivalent',
        'N4': 'At least 1 WSQ Statement of Attainment or other modular certificate at '
        'postgraduate level or equivalent',
        'N9': 'Other statements of attainment, modular certificates or equivalent',
        'X': 'NOT REPORTED',
        'XX': 'Not reported'
    }

    def __init__(self):
        self._description: str = None
        self._ssecEQA: str = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, LinkedSSECEQA):
            return False

        return (
            self._description == other._description
            and self._ssecEQA == other._ssecEQA
        )

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str):
            raise ValueError("Invalid description")

        self._description = description

    @property
    def ssecEQA(self):
        return self._ssecEQA

    @ssecEQA.setter
    def ssecEQA(self, ssecEQA: str):
        if not isinstance(ssecEQA, str):
            raise ValueError("Invalid SSEC EQA")

        self._ssecEQA = ssecEQA

    def validate(self) -> None | tuple[list[str], list[str]]:
        errors, warnings = [], []

        if self._ssecEQA is None or len(self._ssecEQA) == 0:
            warnings.append("No SSEC EQA code specified!")

        if self._description is None or len(self._description) == 0:
            warnings.append("No SSEC EQA description specified!")

        if self._ssecEQA not in LinkedSSECEQA.VALID_SSECEQA_MAPPINGS:
            errors.append("Invalid SSEC EQA code specified!")

        if self._description not in LinkedSSECEQA.VALID_SSECEQA_MAPPINGS.values():
            warnings.append("Invalid SSEC EQA description specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "description": self._description,
            "ssecEQA": {
                "code": self._ssecEQA,
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl


# ===== Session Info ===== #
class RunSessionEditInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course run's sessions"""

    def __init__(self):
        self._sessionId: Annotated[Optional[str], "string($varchar(300))"] = None
        self._startDate: Annotated[Optional[datetime.date], "Formatted as YYYYMMDD or YYYY-MM-DD"] = None
        self._endDate: Annotated[Optional[datetime.date], "Formatted as YYYYMMDD or YYYY-MM-DD"] = None
        self._startTime: Annotated[Optional[datetime.time], "Formatted as HH:mm:ss or HH:mm"] = None
        self._endTime: Annotated[Optional[datetime.time], "Formatted as HH:mm:ss or HH:mm"] = None
        self._modeOfTraining: Annotated[Optional[ModeOfTraining], "string($varchar(4))"] = None
        self._venue_block: Annotated[Optional[str], "string($varchar(10))"] = None
        self._venue_street: Annotated[Optional[str], "string($varchar(32))"] = None
        self._venue_floor: Annotated[str, "string($varchar(3))"] = None
        self._venue_unit: Annotated[str, "string($varchar(5))"] = None
        self._venue_building: Annotated[Optional[str], "string($varchar(66))"] = None
        self._venue_postalCode: Annotated[str, "string($varchar(6))"] = None
        self._venue_room: Annotated[str, "string($varchar(255))"] = None
        self._venue_wheelChairAccess: OptionalSelector = None
        self._venue_primaryVenue: OptionalSelector = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, RunSessionEditInfo):
            return False

        return (
            self._sessionId == other._sessionId
            and self._startDate == other._startDate
            and self._endDate == other._endDate
            and self._startTime == other._startTime
            and self._endTime == other._endTime
            and self._modeOfTraining == other._modeOfTraining
            and self._venue_block == other._venue_block
            and self._venue_street == other._venue_street
            and self._venue_floor == other._venue_floor
            and self._venue_unit == other._venue_unit
            and self._venue_building == other._venue_building
            and self._venue_postalCode == other._venue_postalCode
            and self._venue_room == other._venue_room
            and self._venue_wheelChairAccess == other._venue_wheelChairAccess
            and self._venue_primaryVenue == other._venue_primaryVenue
        )

    @property
    def session_id(self):
        return self._sessionId

    @session_id.setter
    def session_id(self, session_id: str):
        if not isinstance(session_id, str):
            raise ValueError("Invalid session id")

        self._sessionId = session_id

    @property
    def start_date(self):
        return self._startDate

    @start_date.setter
    def start_date(self, start_date: datetime.date):
        if not isinstance(start_date, datetime.date):
            raise ValueError("Invalid start date")

        self._startDate = start_date

    @property
    def end_date(self):
        return self._endDate

    @end_date.setter
    def end_date(self, end_date: datetime.date):
        if not isinstance(end_date, datetime.date):
            raise ValueError("Invalid end date")

        self._endDate = end_date

    @property
    def start_time(self):
        return self._startTime

    @start_time.setter
    def start_time(self, start_time: datetime.time):
        if not isinstance(start_time, datetime.time):
            raise ValueError("Invalid start time")

        self._startTime = start_time

    @property
    def end_time(self):
        return self._endTime

    @end_time.setter
    def end_time(self, end_time: datetime.time):
        if not isinstance(end_time, datetime.time):
            raise ValueError("Invalid end time")

        self._endTime = end_time

    @property
    def mode_of_training(self):
        return self._modeOfTraining

    @mode_of_training.setter
    def mode_of_training(self, mode_of_training: ModeOfTraining):
        if not isinstance(mode_of_training, ModeOfTraining):
            try:
                mode_of_training = ModeOfTraining(mode_of_training)
            except Exception:
                raise ValueError("Invalid mode of training")

        self._modeOfTraining = mode_of_training

    @property
    def block(self):
        return self._venue_block

    @block.setter
    def block(self, block: str):
        if not isinstance(block, str):
            raise ValueError("Invalid venue block")

        self._venue_block = block

    @property
    def street(self):
        return self._venue_street

    @street.setter
    def street(self, street: str):
        if not isinstance(street, str):
            raise ValueError("Invalid venue street")

        self._venue_street = street

    @property
    def floor(self):
        return self._venue_floor

    @floor.setter
    def floor(self, floor: str):
        if not isinstance(floor, str):
            raise ValueError("Invalid venue floor")

        self._venue_floor = floor

    @property
    def unit(self):
        return self._venue_unit

    @unit.setter
    def unit(self, unit: str):
        if not isinstance(unit, str):
            raise ValueError("Invalid venue unit")

        self._venue_unit = unit

    @property
    def building(self):
        return self._venue_building

    @building.setter
    def building(self, building: str):
        if not isinstance(building, str):
            raise ValueError("Invalid venue building")

        self._venue_building = building

    @property
    def postal_code(self):
        return self._venue_postalCode

    @postal_code.setter
    def postal_code(self, postal_code: str):
        if not isinstance(postal_code, str):
            raise ValueError("Invalid venue postal code")

        self._venue_postalCode = postal_code

    @property
    def room(self):
        return self._venue_room

    @room.setter
    def room(self, room: str):
        if not isinstance(room, str):
            raise ValueError("Invalid venue room")

        self._venue_room = room

    @property
    def wheel_chair_access(self):
        return self._venue_wheelChairAccess

    @wheel_chair_access.setter
    def wheel_chair_access(self, wheelChairAccess: OptionalSelector):
        if not isinstance(wheelChairAccess, OptionalSelector):
            try:
                wheelChairAccess = OptionalSelector(wheelChairAccess)
            except Exception:
                raise ValueError("Invalid wheelchair access indicator")

        self._venue_wheelChairAccess = wheelChairAccess

    @property
    def primary_venue(self):
        return self._venue_primaryVenue

    @primary_venue.setter
    def primary_venue(self, primaryVenue: OptionalSelector):
        if not isinstance(primaryVenue, OptionalSelector):
            try:
                primaryVenue = OptionalSelector(primaryVenue)
            except Exception:
                raise ValueError("Invalid primary venue indicator")

        self._venue_primaryVenue = primaryVenue

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._venue_floor is not None and len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is not None and len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is not None and len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is not None and len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        if self._startDate is not None and self._endDate is not None and self._startDate > self._endDate:
            errors.append("Start Date of Session cannot be after the End Date!")

        if self._startTime is not None and self._endTime is not None and self._startTime > self._endTime:
            errors.append("Start Time of Session cannot be after the End Time!")

        # optional parameter verification
        if self._sessionId is not None and len(self._sessionId) == 0:
            warnings.append("Session ID is empty but Session ID was marked as specified!")

        if self._venue_block is not None and len(self._venue_block) == 0:
            warnings.append("Venue Block is empty but Venue Block was marked as specified!")

        if self._venue_street is not None and len(self._venue_street) == 0:
            warnings.append("Venue Street is empty but Venue Street was marked as specified!")

        if self._venue_building is not None and len(self._venue_building) == 0:
            warnings.append("Venue Building is empty but Venue Building was marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "action": "update",
            "sessionId": self._sessionId,
            "startDate": self._startDate.strftime("%Y%m%d") if self._startDate is not None else None,
            "endDate": self._endDate.strftime("%Y%m%d") if self._endDate is not None else None,
            "startTime": self._startTime.strftime("%H:%M") if self._startTime is not None else None,
            "endTime": self._endTime.strftime("%H:%M") if self._endTime is not None else None,
            "modeOfTraining": self._modeOfTraining.value[0] if self._modeOfTraining is not None else None,
            "venue": {
                "block": self._venue_block,
                "street": self._venue_street,
                "floor": self._venue_floor,
                "unit": self._venue_unit,
                "building": self._venue_building,
                "postalCode": self._venue_postalCode,
                "room": self._venue_room,
                "wheelChairAccess": (self._venue_wheelChairAccess.value[1]
                                     if self._venue_wheelChairAccess is not None else None),
                "primaryVenue": (self._venue_primaryVenue.value[1]
                                 if self._venue_primaryVenue is not None else None),
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def get_start_date(self) -> datetime.date:
        return self._startDate if self._startDate else None

    def get_start_date_year(self) -> int:
        return self._startDate.year if self._startDate else None

    def get_end_date_year(self) -> int:
        return self._endDate.year if self._endDate else None

    def get_start_date_month(self) -> int:
        return self._startDate.month if self._startDate else None

    def get_end_date_month(self) -> int:
        return self._endDate.month if self._endDate else None

    def get_start_date_day(self) -> int:
        return self._startDate.day if self._startDate else None

    def get_end_date_day(self) -> int:
        return self._endDate.day if self._endDate else None

    def is_asynchronous_or_on_the_job(self) -> bool:
        return self._modeOfTraining == ModeOfTraining.ASYNCHRONOUS_ELEARNING or \
            self._modeOfTraining == ModeOfTraining.ON_THE_JOB


class RunSessionAddInfo(RunSessionEditInfo):
    """Encapsulates all information regarding adding a session to a course run"""

    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, RunSessionAddInfo):
            return False

        return (
            self._sessionId == other._sessionId
            and self._startDate == other._startDate
            and self._endDate == other._endDate
            and self._startTime == other._startTime
            and self._endTime == other._endTime
            and self._modeOfTraining == other._modeOfTraining
            and self._venue_block == other._venue_block
            and self._venue_street == other._venue_street
            and self._venue_floor == other._venue_floor
            and self._venue_unit == other._venue_unit
            and self._venue_building == other._venue_building
            and self._venue_postalCode == other._venue_postalCode
            and self._venue_room == other._venue_room
            and self._venue_wheelChairAccess == other._venue_wheelChairAccess
            and self._venue_primaryVenue == other._venue_primaryVenue
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._startDate is None:
            errors.append("No start date is specified!")

        if self._endDate is None:
            errors.append("No end date is specified!")

        if self._startDate is not None and self._endDate is not None and self._startDate > self._endDate:
            errors.append("Start date must be before end date")

        if self._startTime is None:
            errors.append("No start time is specified!")

        if self._endTime is None:
            errors.append("No end time is specified!")

        if self._startTime is not None and self._endTime is not None and self._startTime > self._endTime:
            errors.append("Starting time must be before ending time")

        if self._modeOfTraining is None:
            errors.append("No mode of training is specified!")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        # optional parameter verification
        if self._venue_block is not None and len(self._venue_block) == 0:
            warnings.append("Venue Block is empty even though Venue Block is marked as specified!")

        if self._venue_street is not None and len(self._venue_street) == 0:
            warnings.append("Venue Street is empty even though Venue Street is marked as specified!")

        if self._venue_building is not None and len(self._venue_building) == 0:
            warnings.append("Venue Building is empty though Venue Building is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False):
        pl = super().payload(verify=verify, as_json_str=False)
        del pl["action"]

        if "sessionId" in pl:
            del pl["sessionId"]

        if as_json_str:
            return json.dumps(pl)

        return pl


# ===== Trainer Info ===== #
class RunTrainerEditInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a trainer in a course run"""

    def __init__(self):
        self._trainerType_code: Annotated[Literal["1", "2"], "string($varchar(1))"] = None
        self._trainerType_description: Annotated[str, "string($varchar(128))"] = None
        self._indexNumber: Optional[int] = None
        self._id: Annotated[Optional[str], "string($uniqueidentifier)"] = None
        self._name: Annotated[str, "string($varchar(66))"] = None
        self._email: Annotated[str, "string($varchar(320))"] = None
        self._idNumber: Annotated[str, "string($varchar(50))"] = None
        self._idType_code: Annotated[IdType.value[0], "	string($varchar(2))"] = None
        self._idType_description: Annotated[IdType.value[1], "	string($varchar(128))"] = None
        self._roles: list[Role] = []
        self._inTrainingProviderProfile: OptionalSelector = None
        self._domainAreaOfPractice: Annotated[Optional[str], "string($varchar(1000))"] = None
        self._experience: Annotated[Optional[str], "string($varchar(1000))"] = None
        self._linkedInURL: Annotated[Optional[str], "string($varchar(255))"] = None
        self._salutationId: Optional[Salutations] = None
        self._photo_name: Annotated[Optional[str], "string($varchar(255))"] = None
        self._photo_content: Annotated[Optional[UploadedFile], "string($nvarbinary(max))"] = None
        self._linkedSsecEQAs: Optional[list[dict]] = []

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, RunTrainerEditInfo):
            return False

        return (
            self._trainerType_code == other._trainerType_code
            and self._trainerType_description == other._trainerType_description
            and self._indexNumber == other._indexNumber
            and self._id == other._id
            and self._name == other._name
            and self._email == other._email
            and self._idNumber == other._idNumber
            and self._idType_code == other._idType_code
            and self._idType_description == other._idType_description
            and (
                len(self._roles) == len(other._roles)
                and all(map(lambda x: x[0] == x[1], zip(self._roles, other._roles)))
            )
            and self._inTrainingProviderProfile == other._inTrainingProviderProfile
            and self._domainAreaOfPractice == other._domainAreaOfPractice
            and self._experience == other._experience
            and self._linkedInURL == other._linkedInURL
            and self._salutationId == other._salutationId
            and self._photo_name == other._photo_name
            and self._photo_content == other._photo_content
            and (
                len(self._linkedSsecEQAs) == len(other._linkedSsecEQAs)
                and all(map(lambda x: x[0] == x[1], zip(self._linkedSsecEQAs, other._linkedSsecEQAs)))
            )
        )

    @property
    def trainer_type_code(self):
        return self._trainerType_code

    @trainer_type_code.setter
    def trainer_type_code(self, trainer_type: str):
        if not isinstance(trainer_type, str):
            raise ValueError("Invalid trainer type")

        self._trainerType_code = trainer_type

    @property
    def trainer_type_description(self):
        return self._trainerType_description

    @trainer_type_description.setter
    def trainer_type_description(self, trainer_type_description: str):
        if not isinstance(trainer_type_description, str):
            raise ValueError("Invalid trainer type description")

        self._trainerType_description = trainer_type_description

    @property
    def index_number(self):
        return self._indexNumber

    @index_number.setter
    def index_number(self, indexNumber: int):
        if not isinstance(indexNumber, int):
            raise ValueError("Invalid indexNumber")

        self._indexNumber = indexNumber

    @property
    def trainer_id(self):
        return self._id

    @trainer_id.setter
    def trainer_id(self, id: str):
        if not isinstance(id, str):
            raise ValueError("Invalid trainer id")

        self._id = id

    @property
    def trainer_name(self):
        return self._name

    @trainer_name.setter
    def trainer_name(self, name: str):
        if not isinstance(name, str):
            raise ValueError("Invalid trainer name")

        self._name = name

    @property
    def trainer_email(self):
        return self._email

    @trainer_email.setter
    def trainer_email(self, email: str):
        if not isinstance(email, str):
            raise ValueError("Invalid trainer email")

        self._email = email

    @property
    def trainer_idNumber(self):
        return self._idNumber

    @trainer_idNumber.setter
    def trainer_idNumber(self, idNumber: str):
        if not isinstance(idNumber, str):
            raise ValueError("Invalid trainer idNumber")

        self._idNumber = idNumber

    @property
    def trainer_idType(self):
        return IdType((self._idType_code, self._idType_description))

    @trainer_idType.setter
    def trainer_idType(self, idType: IdType):
        if not isinstance(idType, IdType):
            try:
                idType = IdType(idType)
            except Exception:
                raise ValueError("Invalid trainee ID type")

        self._idType_code = idType.value[0]
        self._idType_description = idType.value[1]

    @property
    def trainer_roles(self):
        return self._roles

    @trainer_roles.setter
    def trainer_roles(self, roles: list[Role]):
        if not isinstance(roles, list):
            raise ValueError("Invalid trainer roles")

        for role in roles:
            try:
                Role(role)
            except Exception:
                raise ValueError("Invalid trainer roles")

        self._roles = roles

    @property
    def inTrainingProviderProfile(self):
        return self._inTrainingProviderProfile

    @inTrainingProviderProfile.setter
    def inTrainingProviderProfile(self, inTrainingProviderProfile: OptionalSelector):
        if not isinstance(inTrainingProviderProfile, OptionalSelector):
            try:
                inTrainingProviderProfile = OptionalSelector(inTrainingProviderProfile)
            except Exception:
                raise ValueError("Invalid inTrainingProviderProfile")

        self._inTrainingProviderProfile = inTrainingProviderProfile

    @property
    def domain_area_of_practice(self):
        return self._domainAreaOfPractice

    @domain_area_of_practice.setter
    def domain_area_of_practice(self, domainAreaOfPractice: str):
        if not isinstance(domainAreaOfPractice, str):
            raise ValueError("Invalid domainAreaOfPractice")

        self._domainAreaOfPractice = domainAreaOfPractice

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, experience: str):
        if not isinstance(experience, str):
            raise ValueError("Invalid experience")

        self._experience = experience

    @property
    def linkedInURL(self):
        return self._linkedInURL

    @linkedInURL.setter
    def linkedInURL(self, linkedInURL: str):
        if not isinstance(linkedInURL, str):
            raise ValueError("Invalid linkedInURL")

        self._linkedInURL = linkedInURL

    @property
    def salutationId(self):
        return self._salutationId

    @salutationId.setter
    def salutationId(self, salutationId: Salutations):
        if not isinstance(salutationId, Salutations):
            raise ValueError("Invalid salutation")

        self._salutationId = salutationId

    @property
    def photo_name(self):
        return self._photo_name

    @photo_name.setter
    def photo_name(self, photo_name: str):
        if not isinstance(photo_name, str):
            raise ValueError("Invalid photo_name")

        self._photo_name = photo_name

    @property
    def photo_content(self):
        return self._photo_content

    @photo_content.setter
    def photo_content(self, photo_content: UploadedFile):
        if photo_content is not None and not isinstance(photo_content, UploadedFile):
            raise ValueError("Invalid photo_content")

        self._photo_content = photo_content

    def add_linkedSsecEQA(self, linkedSsecEQA: LinkedSSECEQA):
        """Method to add a Linked SSEC EQA record to this object."""

        if not isinstance(linkedSsecEQA, LinkedSSECEQA):
            raise ValueError("Invalid linkedSsecEQA")

        # the object is converted to a dict as the object itself is not JSON-serializable
        self._linkedSsecEQAs.append(linkedSsecEQA.payload(verify=False))

    @property
    def linkedSsecEQAs(self):
        # the object is converted to a dict as the object itself is not JSON-serializable
        return list(map(lambda x: LinkedSSECEQA(x), self._linkedSsecEQAs))

    @linkedSsecEQAs.setter
    def linkedSsecEQAs(self, linkedSsecEQAs: list[LinkedSSECEQA]):
        if not isinstance(linkedSsecEQAs, list):
            raise ValueError("Invalid linkedSsecEQA")

        if not all(map(lambda x: isinstance(x, LinkedSSECEQA), linkedSsecEQAs)):
            raise ValueError("Invalid linkedSsecEQA")

        # the object is converted to a dict as the object itself is not JSON-serializable
        self._linkedSsecEQAs = list(map(lambda x: x.payload(verify=False), linkedSsecEQAs))

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._trainerType_code is None or len(self._trainerType_code) == 0:
            errors.append("No Trainer Type Code specified!")

        if self._trainerType_description is None or len(self._trainerType_description) == 0:
            errors.append("No Trainer Type Description specified!")

        if self._name is None or len(self._name) == 0:
            errors.append("No Trainer Name specified!")

        if self._email is None or len(self._email) == 0:
            errors.append("No Trainer Email specified!")

        if self._email is not None and len(self._email) > 0:
            try:
                validate_email(self._email)
            except EmailSyntaxError:
                errors.append("Trainer Email specified is not of the correct format!")

        if self._idNumber is None or len(self._idNumber) == 0:
            errors.append("No Trainer ID number specified!")

        if self._idType_code is None or len(self._idType_code) == 0:
            errors.append("No Trainer ID type specified!")

        if self._idType_description is None or len(self._idType_description) == 0:
            errors.append("No Trainer ID description specified!")

        if self._roles is None or len(self._roles) == 0:
            errors.append("No Trainer Roles specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
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
                "roles": [x.value for x in self._roles],
                "inTrainingProviderProfile": (self._inTrainingProviderProfile.value[1]
                                              if self._inTrainingProviderProfile is not None else None),
                "domainAreaOfPractice": self._domainAreaOfPractice,
                "experience": self._experience,
                "linkedInURL": self._linkedInURL,
                "salutationId": self._salutationId.value[0] if self._salutationId is not None else None,
                "photo": {
                    "name": self._photo_name,
                    "content": (base64.b64encode(
                        self._photo_content.getvalue()).decode("utf-8") if self._photo_content else None)
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


class RunTrainerAddInfo(RunTrainerEditInfo):
    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, RunTrainerAddInfo):
            return False

        return (
            self._trainerType_code == other._trainerType_code
            and self._trainerType_description == other._trainerType_description
            and self._indexNumber == other._indexNumber
            and self._id == other._id
            and self._name == other._name
            and self._email == other._email
            and self._idNumber == other._idNumber
            and self._idType_code == other._idType_code
            and self._idType_description == other._idType_description
            and (
                len(self._roles) == len(other._roles)
                and all(map(lambda x: x[0] == x[1], zip(self._roles, other._roles)))
            )
            and self._inTrainingProviderProfile == other._inTrainingProviderProfile
            and self._domainAreaOfPractice == other._domainAreaOfPractice
            and self._experience == other._experience
            and self._linkedInURL == other._linkedInURL
            and self._salutationId == other._salutationId
            and self._photo_name == other._photo_name
            and self._photo_content == other._photo_content
            and (
                len(self._linkedSsecEQAs) == len(other._linkedSsecEQAs)
                and all(map(lambda x: x[0] == x[1], zip(self._linkedSsecEQAs, other._linkedSsecEQAs)))
            )
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._trainerType_code is None or len(self._trainerType_code) == 0:
            errors.append("No trainerType code specified!")

        if self._trainerType_description is None or len(self._trainerType_description) == 0:
            errors.append("No trainerType description specified!")

        if self._name is None or len(self._name) == 0:
            errors.append("No name specified!")

        if self._email is None or len(self._email) == 0:
            errors.append("No email specified!")

        if self._email is not None and len(self._email) > 0:
            try:
                validate_email(self._email)
            except EmailSyntaxError:
                errors.append("Trainer Email specified is not of the correct format!")

        if self._idNumber is None or len(self._idNumber) == 0:
            errors.append("No ID number specified!")

        if self._idType_code is None or len(self._idType_code) == 0:
            errors.append("No ID type code specified!")

        if self._idType_description is None or len(self._idType_description) == 0:
            errors.append("No ID Type Description specified!")

        if self._roles is None or len(self._roles) == 0:
            errors.append("No roles specified!")

        # optional parameters verification
        if self._id is not None and len(self._id) == 0:
            warnings.append("Index Number is empty even though Index Number is marked as specified!")

        if self._domainAreaOfPractice is not None and len(self._domainAreaOfPractice) == 0:
            warnings.append("Domain Area of Practice is empty even though Domain Area of Practice is marked as "
                            "specified!")

        if self._experience is not None and len(self._experience) == 0:
            warnings.append("Experience is empty even though Experience is marked as specified!")

        if self._linkedInURL is not None and len(self._linkedInURL) == 0:
            warnings.append("LinkedIn URL is empty even though LinkedIn URL is marked as specified!")

        if self._photo_name is not None and len(self._photo_name) == 0:
            warnings.append("Photo Name is empty but Photo Name is marked as specified!")

        if self._photo_name is not None and self._photo_content is None:
            warnings.append("Photo Name is specified but there is no photo file uploaded!")

        if self._photo_name is None and self._photo_content is not None:
            warnings.append("Photo Content is specified but there is no photo file name!")

        for i, ssec in enumerate(self._linkedSsecEQAs):
            if "description" in ssec and ssec["description"] is not None and len(ssec["description"]) == 0:
                warnings.append(f"[SSEC EQA {i + 1}]: SSEC EQA Description is empty even though SSEC EQA Description "
                                f"is marked as specified!")

            if "ssecEQA" in ssec and "code" in ssec["ssecEQA"] and ssec["ssecEQA"]["code"] is not None and \
                    len(ssec["ssecEQA"]["code"]) == 0:
                warnings.append(f"[SSEC EQA {i + 1}]: SSEC EQA Code is empty even though SSEC EQA Code is marked "
                                f"as specified!")

        return errors, warnings


# ===== Run Info ===== #
class EditRunInfo(AbstractRequestInfo):
    """Encapsulates all information regarding the editing of a course run"""

    def __init__(self):
        self._crid: str = None
        self._sequenceNumber: Optional[int] = None
        self._registrationDates_opening: Annotated[datetime.date, "Number formatted as YYYYMMDD"] = None
        self._registrationDates_closing: Annotated[datetime.date, "Number formatted as YYYYMMDD"] = None
        self._courseDates_start: Annotated[datetime.date, "Number formatted as YYYYMMDD"] = None
        self._courseDates_end: Annotated[datetime.date, "String formatted as YYYYMMDD"] = None
        self._scheduleInfoType_code: Annotated[str, "string($varchar(2))"] = None
        self._scheduleInfoType_description: Annotated[Optional[str], "string($varchar(32))"] = None
        self._scheduleInfo: Annotated[Optional[str], "string($nvarchar(max))"] = None
        self._venue_block: Annotated[Optional[str], "string($varchar(10))"] = None
        self._venue_street: Annotated[Optional[str], "string($varchar(32))"] = None
        self._venue_floor: Annotated[str, "string($varchar(3))"] = None
        self._venue_unit: Annotated[str, "string($varchar(5))"] = None
        self._venue_building: Annotated[Optional[str], "string($varchar(66))"] = None
        self._venue_postalCode: Annotated[str, "string($varchar(6))"] = None
        self._venue_room: Annotated[str, "string($varchar(255))"] = None
        self._venue_wheelChairAccess: OptionalSelector = None
        self._intakeSize: Optional[int] = None
        self._threshold: Optional[int] = None
        self._registeredUserCount: Optional[int] = None
        self._modeOfTraining: Optional[ModeOfTraining] = None
        self._courseAdminEmail: Annotated[Optional[str], "string($varchar(255))"] = None
        self._courseVacancy_code: Annotated[str, "string($varchar(1))"] = None
        self._courseVacancy_description: Annotated[Optional[str], "string($varchar(128))"] = None
        self._file_Name: Annotated[Optional[str], "string($varchar(255))"] = None
        self._file_content: Optional[UploadedFile] = None
        self._sessions: Optional[list[RunSessionEditInfo]] = []
        self._linkCourseRunTrainer: Optional[list[RunTrainerEditInfo]] = []

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, EditRunInfo):
            return False

        return (
            self._crid == other._crid
            and self._sequenceNumber == other._sequenceNumber
            and self._registrationDates_opening == other._registrationDates_opening
            and self._registrationDates_closing == other._registrationDates_closing
            and self._courseDates_start == other._courseDates_start
            and self._courseDates_end == other._courseDates_end
            and self._scheduleInfoType_code == other._scheduleInfoType_code
            and self._scheduleInfoType_description == other._scheduleInfoType_description
            and self._scheduleInfo == other._scheduleInfo
            and self._venue_block == other._venue_block
            and self._venue_street == other._venue_street
            and self._venue_floor == other._venue_floor
            and self._venue_unit == other._venue_unit
            and self._venue_building == other._venue_building
            and self._venue_postalCode == other._venue_postalCode
            and self._venue_room == other._venue_room
            and self._venue_wheelChairAccess == other._venue_wheelChairAccess
            and self._intakeSize == other._intakeSize
            and self._threshold == other._threshold
            and self._registeredUserCount == other._registeredUserCount
            and self._modeOfTraining == other._modeOfTraining
            and self._courseAdminEmail == other._courseAdminEmail
            and self._courseVacancy_code == other._courseVacancy_code
            and self._courseVacancy_description == other._courseVacancy_description
            and self._file_Name == other._file_Name
            and self._file_content == other._file_content
            and (
                len(self._sessions) == len(other._sessions)
                and all(map(lambda x: x[0] == x[1], zip(self._sessions, other._sessions)))
            )
            and (
                len(self._linkCourseRunTrainer) == len(other._linkCourseRunTrainer)
                and all(map(lambda x: x[0] == x[1], zip(self._linkCourseRunTrainer, other._linkCourseRunTrainer)))
            )
        )

    @property
    def crid(self):
        return self._crid

    @crid.setter
    def crid(self, crn: str):
        if not isinstance(crn, str):
            raise ValueError("Invalid Course Reference ID number")

        self._crid = crn

    @property
    def vacancy(self):
        return Vacancy((self._courseVacancy_code, self._courseVacancy_description))

    @vacancy.setter
    def vacancy(self, vacancy: Vacancy):
        if not isinstance(vacancy, Vacancy):
            try:
                vacancy = Vacancy(vacancy)
            except Exception:
                raise ValueError("Invalid Vacancy code")

        self._courseVacancy_code = vacancy.value[0]
        self._courseVacancy_description = vacancy.value[1]

    @property
    def sequence_number(self):
        return self._sequenceNumber

    @sequence_number.setter
    def sequence_number(self, sequence_number: int):
        if not isinstance(sequence_number, int):
            raise ValueError("Invalid sequence number")

        self._sequenceNumber = sequence_number

    @property
    def opening_registration_date(self):
        return self._registrationDates_opening

    @opening_registration_date.setter
    def opening_registration_date(self, opening_registration_date: datetime.date):
        if not isinstance(opening_registration_date, datetime.date):
            raise ValueError("Invalid opening registration dates")

        self._registrationDates_opening = opening_registration_date

    @property
    def closing_registration_date(self):
        return self._registrationDates_closing

    @closing_registration_date.setter
    def closing_registration_date(self, closing_registration_date: datetime.date):
        if not isinstance(closing_registration_date, datetime.date):
            raise ValueError("Invalid closing registration dates")

        self._registrationDates_closing = closing_registration_date

    @property
    def course_start_date(self):
        return self._courseDates_start

    @course_start_date.setter
    def course_start_date(self, course_start_date: datetime.date):
        if not isinstance(course_start_date, datetime.date):
            raise ValueError("Invalid course start date")

        self._courseDates_start = course_start_date

    @property
    def course_end_date(self):
        return self._courseDates_end

    @course_end_date.setter
    def course_end_date(self, course_end_date: datetime.date):
        if not isinstance(course_end_date, datetime.date):
            raise ValueError("Invalid course end date")

        self._courseDates_end = course_end_date

    @property
    def schedule_info_type_code(self):
        return self._scheduleInfoType_code

    @schedule_info_type_code.setter
    def schedule_info_type_code(self, schedule_info_type_code: str):
        if not isinstance(schedule_info_type_code, str):
            raise ValueError("Invalid schedule info type code")

        self._scheduleInfoType_code = schedule_info_type_code

    @property
    def schedule_info_type_description(self):
        return self._scheduleInfoType_description

    @schedule_info_type_description.setter
    def schedule_info_type_description(self, schedule_info_type_description: str):
        if not isinstance(schedule_info_type_description, str):
            raise ValueError("Invalid schedule info type description")

        self._scheduleInfoType_description = schedule_info_type_description

    @property
    def schedule_info(self):
        return self._scheduleInfo

    @schedule_info.setter
    def schedule_info(self, schedule_info: str):
        if not isinstance(schedule_info, str):
            raise ValueError("Invalid schedule info")

        self._scheduleInfo = schedule_info

    @property
    def block(self):
        return self._venue_block

    @block.setter
    def block(self, block: str):
        if not isinstance(block, str):
            raise ValueError("Invalid venue block")

        self._venue_block = block

    @property
    def street(self):
        return self._venue_street

    @street.setter
    def street(self, street: str):
        if not isinstance(street, str):
            raise ValueError("Invalid venue street")

        self._venue_street = street

    @property
    def floor(self):
        return self._venue_floor

    @floor.setter
    def floor(self, floor: str):
        if not isinstance(floor, str):
            raise ValueError("Invalid venue floor")

        self._venue_floor = floor

    @property
    def unit(self):
        return self._venue_unit

    @unit.setter
    def unit(self, unit: str):
        if not isinstance(unit, str):
            raise ValueError("Invalid venue unit")

        self._venue_unit = unit

    @property
    def building(self):
        return self._venue_building

    @building.setter
    def building(self, building: str):
        if not isinstance(building, str):
            raise ValueError("Invalid venue building")

        self._venue_building = building

    @property
    def postal_code(self):
        return self._venue_postalCode

    @postal_code.setter
    def postal_code(self, postal_code: str):
        if not isinstance(postal_code, str):
            raise ValueError("Invalid venue postal code")

        self._venue_postalCode = postal_code

    @property
    def room(self):
        return self._venue_room

    @room.setter
    def room(self, room: str):
        if not isinstance(room, str):
            raise ValueError("Invalid venue room")

        self._venue_room = room

    @property
    def wheel_chair_access(self):
        return self._venue_wheelChairAccess

    @wheel_chair_access.setter
    def wheel_chair_access(self, wheelChairAccess: OptionalSelector):
        if not isinstance(wheelChairAccess, OptionalSelector):
            try:
                wheelChairAccess = OptionalSelector(wheelChairAccess)
            except Exception:
                raise ValueError("Invalid wheelchair access indicator")

        self._venue_wheelChairAccess = wheelChairAccess

    @property
    def intake_size(self):
        return self._intakeSize

    @intake_size.setter
    def intake_size(self, intake_size: int):
        if not isinstance(intake_size, int):
            raise ValueError("Invalid intake size")

        self._intakeSize = intake_size

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        if not isinstance(threshold, int):
            raise ValueError("Invalid threshold")

        self._threshold = threshold

    @property
    def registered_user_count(self):
        return self._registeredUserCount

    @registered_user_count.setter
    def registered_user_count(self, registered_user_count: int):
        if not isinstance(registered_user_count, int):
            raise ValueError("Invalid registered user count")

        self._registeredUserCount = registered_user_count

    @property
    def mode_of_training(self):
        return self._modeOfTraining

    @mode_of_training.setter
    def mode_of_training(self, mode_of_training: ModeOfTraining):
        if not isinstance(mode_of_training, ModeOfTraining):
            try:
                # needed to ensure that the enums are the same syntactically
                mode_of_training = ModeOfTraining(mode_of_training)
            except Exception:
                raise ValueError("Invalid mode of training")

        self._modeOfTraining = mode_of_training

    @property
    def course_admin_email(self):
        return self._courseAdminEmail

    @course_admin_email.setter
    def course_admin_email(self, course_admin_email: str):
        if not isinstance(course_admin_email, str):
            raise ValueError("Invalid course admin email")

        self._courseAdminEmail = course_admin_email

    @property
    def course_vacancy_code(self):
        return self._courseVacancy_code

    @course_vacancy_code.setter
    def course_vacancy_code(self, course_vacancy_code: Vacancy.__members__):
        if not isinstance(course_vacancy_code, str) or course_vacancy_code not in Vacancy.__members__:
            raise ValueError("Invalid course vacancy code")

        self._courseVacancy_code = course_vacancy_code

    @property
    def course_vacancy_description(self):
        return self._courseVacancy_description

    @course_vacancy_description.setter
    def course_vacancy_description(self, course_vacancy_description: Vacancy):
        if not isinstance(course_vacancy_description, str) or course_vacancy_description not in Vacancy:
            raise ValueError("Invalid course vacancy description")

        self._courseVacancy_description = course_vacancy_description

    @property
    def course_vacancy(self):
        return Vacancy((self._courseVacancy_code, self._courseVacancy_description))

    @course_vacancy.setter
    def course_vacancy(self, course_vacancy: Vacancy):
        if not isinstance(course_vacancy, Vacancy):
            try:
                course_vacancy = Vacancy(course_vacancy)
            except Exception:
                raise ValueError("Invalid course vacancy")

        self._courseVacancy_code = course_vacancy.value[0]
        self._courseVacancy_description = course_vacancy.value[1]

    @property
    def file_name(self):
        return self._file_Name

    @file_name.setter
    def file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise ValueError("Invalid file name")

        self._file_Name = file_name

    @property
    def file_content(self):
        return self._file_content

    @file_content.setter
    def file_content(self, file_content: UploadedFile):
        if file_content is not None and not isinstance(file_content, UploadedFile):
            raise ValueError("Invalid file content")

        self._file_content = file_content

    @property
    def sessions(self):
        return self._sessions

    @sessions.setter
    def sessions(self, sessions: list[RunSessionEditInfo]):
        if not isinstance(sessions, list):
            raise ValueError("Invalid list of sessions")

        self._sessions = sessions

    def add_session(self, session: RunSessionEditInfo) -> None:
        if not isinstance(session, RunSessionEditInfo):
            raise ValueError("Invalid session")

        self._sessions.append(session)

    @property
    def linked_course_run_trainers(self):
        return self._linkCourseRunTrainer

    @linked_course_run_trainers.setter
    def linked_course_run_trainers(self, linked_course_run_trainers: list[RunTrainerEditInfo]):
        if not isinstance(linked_course_run_trainers, list):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer = linked_course_run_trainers

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        if not isinstance(linkCourseRunTrainer, RunTrainerEditInfo):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer.append(linkCourseRunTrainer)

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No Course Reference ID specified!")

        if self._registrationDates_opening is not None and self._registrationDates_closing is None:
            errors.append("If Opening Registration Date is specified, then the Closing Registration Date must be "
                          "specified!")

        if self._registrationDates_closing is not None and self._registrationDates_opening is None:
            errors.append("If Closing Registration Date is specified, then the Opening Registration Date must be "
                          "specified!")

        if self._registrationDates_opening is not None and self._registrationDates_closing is not None and \
                self._registrationDates_opening > self._registrationDates_closing:
            errors.append("Registration dates opening date must be before closing date!")

        if self._courseDates_start is not None and self._courseDates_end is None:
            errors.append("If Course Start Date is specified, then the Course End Date must be "
                          "specified!")

        if self._courseDates_end is not None and self._courseDates_start is None:
            errors.append("If Course End Date is specified, then the Course Start Date must be "
                          "specified!")

        if self._courseDates_start is not None and self._courseDates_end is not None and \
                self._courseDates_start > self._courseDates_end:
            errors.append("Course Start Date must be before Course End Date!")

        if self._scheduleInfoType_code is not None and len(self._scheduleInfoType_code) == 0:
            errors.append("No Course Run Schedule Info Code specified")

        if self._venue_floor is not None and len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is not None and len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is not None and len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is not None and len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        if self._courseVacancy_code is not None and len(self._courseVacancy_code) == 0:
            errors.append("No course vacancy code is specified")

        if self._courseAdminEmail is not None and len(self._courseAdminEmail) > 0:
            try:
                validate_email(self._courseAdminEmail)
            except EmailSyntaxError:
                errors.append("Course Admin Email specified is not of the correct format!")

        # optional parameter verification
        if self._courseAdminEmail is not None and len(self._courseAdminEmail) == 0:
            warnings.append("Course Admin Email is empty even though Course Admin Email is marked as specified!")

        if self._scheduleInfoType_description is not None and len(self._scheduleInfoType_description) == 0:
            warnings.append("Schedule Info Type Description is empty but Schedule Info Type "
                            "Description is marked as specified!")

        if self._scheduleInfo is not None and len(self._scheduleInfo) == 0:
            warnings.append("Schedule Info is empty but Schedule Info is marked as specified!")

        if self._venue_block is not None and len(self._venue_block) == 0:
            warnings.append("Venue Block is empty but Venue Block is marked as specified!")

        if self._venue_street is not None and len(self._venue_street) == 0:
            warnings.append("Venue Street is empty but Venue Street is marked as specified!")

        if self._venue_building is not None and len(self._venue_building) == 0:
            warnings.append("Venue Building is empty but Venue Building is marked as specified!")

        if self._file_Name is not None and len(self._file_Name) == 0:
            warnings.append("File Name is empty but File Name is marked as specified!")

        if self._file_Name is not None and self._file_content is None:
            warnings.append("File Name is specified but there is no file uploaded!")

        if self._courseVacancy_description is not None and len(self._courseVacancy_description) == 0:
            warnings.append("Course Description is empty but Course Description is marked as specified!")

        if self._file_Name is None and self._file_content is not None:
            warnings.append("File Content is specified but there is no file name!")

        for i, session in enumerate(self._sessions):
            err, war = session.validate()

            for e in err:
                errors.append(f"**Session {i + 1}**: {e}")

            for w in war:
                warnings.append(f"**Session {i + 1}**: {w}")

        for i, trainer in enumerate(self._linkCourseRunTrainer):
            err, war = trainer.validate()

            for e in err:
                errors.append(f"**Trainer {i + 1}**: {e}")

            for w in war:
                warnings.append(f"**Trainer {i + 1}**: {w}")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "course": {
                "courseReferenceNumber": self._crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"] if "uen" in st.session_state else None
                }
            },
            "run": {
                "action": "update",
                "sequenceNumber": self._sequenceNumber,
                "registrationDates": {
                    "opening": (int(self._registrationDates_opening.strftime("%Y%m%d"))
                                if self._registrationDates_opening is not None else None),
                    "closing": (int(self._registrationDates_closing.strftime("%Y%m%d"))
                                if self._registrationDates_closing is not None else None),
                },
                "courseDates": {
                    "start": (int(self._courseDates_start.strftime("%Y%m%d"))
                              if self._courseDates_start is not None else None),
                    "end": (int(self._courseDates_end.strftime("%Y%m%d"))
                            if self._courseDates_end is not None else None),
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
                    "wheelChairAccess": (self._venue_wheelChairAccess.value[1] if
                                         self._venue_wheelChairAccess is not None else None)
                },
                "intakeSize": self._intakeSize,
                "threshold": self._threshold,
                "registeredUserCount": self._registeredUserCount,
                "modeOfTraining": self._modeOfTraining.value[0] if self.mode_of_training is not None else None,
                "courseAdminEmail": self._courseAdminEmail,
                "courseVacancy": {
                    "code": self._courseVacancy_code,
                    "description": self._courseVacancy_description
                },
                "file": {
                    "Name": self._file_Name,
                    "content": (base64.b64encode(
                        self._file_content.getvalue()).decode() if self._file_content else None),
                },
                "sessions": list(map(lambda x: x.payload(verify=False), self._sessions)),
                "linkCourseRunTrainer": list(map(lambda x: x.payload(verify=False), self._linkCourseRunTrainer))
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl


class DeleteRunInfo(EditRunInfo):
    """Encapsulates all information regarding the deletion of a course run"""

    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, DeleteRunInfo):
            return False

        return self._crid == other._crid

    @property
    def crid(self):
        return self._crid

    @crid.setter
    def crid(self, crn: str):
        if not isinstance(crn, str):
            raise ValueError("Invalid Course Reference ID number")

        self._crid = crn

    @property
    def sequence_number(self):
        raise NotImplementedError("This method is not supported!")

    @sequence_number.setter
    def sequence_number(self, sequence_number: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def opening_registration_date(self):
        raise NotImplementedError("This method is not supported!")

    @opening_registration_date.setter
    def opening_registration_date(self, opening_registration_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def closing_registration_date(self):
        raise NotImplementedError("This method is not supported!")

    @closing_registration_date.setter
    def closing_registration_date(self, closing_registration_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_start_date(self):
        raise NotImplementedError("This method is not supported!")

    @course_start_date.setter
    def course_start_date(self, course_start_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_end_date(self):
        raise NotImplementedError("This method is not supported!")

    @course_end_date.setter
    def course_end_date(self, course_end_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info_type_code(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info_type_code.setter
    def schedule_info_type_code(self, schedule_info_type_code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info_type_description(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info_type_description.setter
    def schedule_info_type_description(self, schedule_info_type_description: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info.setter
    def schedule_info(self, schedule_info: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def block(self):
        raise NotImplementedError("This method is not supported!")

    @block.setter
    def block(self, block: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def street(self):
        raise NotImplementedError("This method is not supported!")

    @street.setter
    def street(self, street: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def floor(self):
        raise NotImplementedError("This method is not supported!")

    @floor.setter
    def floor(self, floor: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def unit(self):
        raise NotImplementedError("This method is not supported!")

    @unit.setter
    def unit(self, unit: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def building(self):
        raise NotImplementedError("This method is not supported!")

    @building.setter
    def building(self, building: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def postal_code(self):
        raise NotImplementedError("This method is not supported!")

    @postal_code.setter
    def postal_code(self, postal_code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def room(self):
        raise NotImplementedError("This method is not supported!")

    @room.setter
    def room(self, room: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def wheel_chair_access(self):
        raise NotImplementedError("This method is not supported!")

    @wheel_chair_access.setter
    def wheel_chair_access(self, wheelChairAccess: OptionalSelector):
        raise NotImplementedError("This method is not supported!")

    @property
    def intake_size(self):
        raise NotImplementedError("This method is not supported!")

    @intake_size.setter
    def intake_size(self, intake_size: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def threshold(self):
        raise NotImplementedError("This method is not supported!")

    @threshold.setter
    def threshold(self, threshold: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def registered_user_count(self):
        raise NotImplementedError("This method is not supported!")

    @registered_user_count.setter
    def registered_user_count(self, registered_user_count: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def mode_of_training(self):
        raise NotImplementedError("This method is not supported!")

    @mode_of_training.setter
    def mode_of_training(self, mode_of_training: ModeOfTraining):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_admin_email(self):
        raise NotImplementedError("This method is not supported!")

    @course_admin_email.setter
    def course_admin_email(self, course_admin_email: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy_code(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy_code.setter
    def course_vacancy_code(self, course_vacancy_code: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy_description(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy_description.setter
    def course_vacancy_description(self, course_vacancy_description: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy.setter
    def course_vacancy(self, course_vacancy: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def file_name(self):
        raise NotImplementedError("This method is not supported!")

    @file_name.setter
    def file_name(self, file_name: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def file_content(self):
        raise NotImplementedError("This method is not supported!")

    @file_content.setter
    def file_content(self, file_content: UploadedFile):
        raise NotImplementedError("This method is not supported!")

    @property
    def sessions(self):
        raise NotImplementedError("This method is not supported!")

    @sessions.setter
    def sessions(self, sessions: list[RunSessionEditInfo]):
        raise NotImplementedError("This method is not supported!")

    def add_session(self, session: RunSessionEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    @property
    def linked_course_run_trainers(self):
        raise NotImplementedError("This method is not supported!")

    @linked_course_run_trainers.setter
    def linked_course_run_trainers(self, linked_course_run_trainers: list[RunTrainerEditInfo]):
        raise NotImplementedError("This method is not supported!")

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No valid Course Reference ID number specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "course": {
                "courseReferenceNumber": self._crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"] if "uen" in st.session_state else None
                },
                "run": {
                    "action": "delete"
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl


class AddRunIndividualInfo(EditRunInfo):
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, AddRunIndividualInfo):
            return False

        return (
            self._sequenceNumber == other._sequenceNumber
            and self._registrationDates_opening == other._registrationDates_opening
            and self._registrationDates_closing == other._registrationDates_closing
            and self._courseDates_start == other._courseDates_start
            and self._courseDates_end == other._courseDates_end
            and self._scheduleInfoType_code == other._scheduleInfoType_code
            and self._scheduleInfoType_description == other._scheduleInfoType_description
            and self._scheduleInfo == other._scheduleInfo
            and self._venue_block == other._venue_block
            and self._venue_street == other._venue_street
            and self._venue_floor == other._venue_floor
            and self._venue_unit == other._venue_unit
            and self._venue_building == other._venue_building
            and self._venue_postalCode == other._venue_postalCode
            and self._venue_room == other._venue_room
            and self._venue_wheelChairAccess == other._venue_wheelChairAccess
            and self._intakeSize == other._intakeSize
            and self._threshold == other._threshold
            and self._registeredUserCount == other._registeredUserCount
            and self._modeOfTraining == other._modeOfTraining
            and self._courseAdminEmail == other._courseAdminEmail
            and self._courseVacancy_code == other._courseVacancy_code
            and self._courseVacancy_description == other._courseVacancy_description
            and self._file_Name == other._file_Name
            and self._file_content == other._file_content
            and (
                len(self._sessions) == len(other._sessions)
                and all(map(lambda x: x[0] == x[1], zip(self._sessions, other._sessions)))
            )
            and (
                len(self._linkCourseRunTrainer) == len(other._linkCourseRunTrainer)
                and all(map(lambda x: x[0] == x[1],
                            zip(self._linkCourseRunTrainer, other._linkCourseRunTrainer)))
            )
        )

    @property
    def sequence_number(self):
        return self._sequenceNumber

    @sequence_number.setter
    def sequence_number(self, sequence_number: int):
        if not isinstance(sequence_number, int):
            raise ValueError("Invalid sequence number")

        self._sequenceNumber = sequence_number

    @property
    def opening_registration_date(self):
        return self._registrationDates_opening

    @opening_registration_date.setter
    def opening_registration_date(self, opening_registration_date: datetime.date):
        if not isinstance(opening_registration_date, datetime.date):
            raise ValueError("Invalid opening registration dates")

        self._registrationDates_opening = opening_registration_date

    @property
    def closing_registration_date(self):
        return self._registrationDates_closing

    @closing_registration_date.setter
    def closing_registration_date(self, closing_registration_date: datetime.date):
        if not isinstance(closing_registration_date, datetime.date):
            raise ValueError("Invalid closing registration dates")

        self._registrationDates_closing = closing_registration_date

    @property
    def course_start_date(self):
        return self._courseDates_start

    @course_start_date.setter
    def course_start_date(self, course_start_date: datetime.date):
        if not isinstance(course_start_date, datetime.date):
            raise ValueError("Invalid course start date")

        self._courseDates_start = course_start_date

    @property
    def course_end_date(self):
        return self._courseDates_end

    @course_end_date.setter
    def course_end_date(self, course_end_date: datetime.date):
        if not isinstance(course_end_date, datetime.date):
            raise ValueError("Invalid course end date")

        self._courseDates_end = course_end_date

    @property
    def schedule_info_type_code(self):
        return self._scheduleInfoType_code

    @schedule_info_type_code.setter
    def schedule_info_type_code(self, schedule_info_type_code: str):
        if not isinstance(schedule_info_type_code, str):
            raise ValueError("Invalid schedule info type code")

        self._scheduleInfoType_code = schedule_info_type_code

    @property
    def schedule_info_type_description(self):
        return self._scheduleInfoType_description

    @schedule_info_type_description.setter
    def schedule_info_type_description(self, schedule_info_type_description: str):
        if not isinstance(schedule_info_type_description, str):
            raise ValueError("Invalid schedule info type description")

        self._scheduleInfoType_description = schedule_info_type_description

    @property
    def schedule_info(self):
        return self._scheduleInfo

    @schedule_info.setter
    def schedule_info(self, schedule_info: str):
        if not isinstance(schedule_info, str):
            raise ValueError("Invalid schedule info")

        self._scheduleInfo = schedule_info

    @property
    def block(self):
        return self._venue_block

    @block.setter
    def block(self, block: str):
        if not isinstance(block, str):
            raise ValueError("Invalid venue block")

        self._venue_block = block

    @property
    def street(self):
        return self._venue_street

    @street.setter
    def street(self, street: str):
        if not isinstance(street, str):
            raise ValueError("Invalid venue street")

        self._venue_street = street

    @property
    def floor(self):
        return self._venue_floor

    @floor.setter
    def floor(self, floor: str):
        if not isinstance(floor, str):
            raise ValueError("Invalid venue floor")

        self._venue_floor = floor

    @property
    def unit(self):
        return self._venue_unit

    @unit.setter
    def unit(self, unit: str):
        if not isinstance(unit, str):
            raise ValueError("Invalid venue unit")

        self._venue_unit = unit

    @property
    def building(self):
        return self._venue_building

    @building.setter
    def building(self, building: str):
        if not isinstance(building, str):
            raise ValueError("Invalid venue building")

        self._venue_building = building

    @property
    def postal_code(self):
        return self._venue_postalCode

    @postal_code.setter
    def postal_code(self, postal_code: str):
        if not isinstance(postal_code, str):
            raise ValueError("Invalid venue postal code")

        self._venue_postalCode = postal_code

    @property
    def room(self):
        return self._venue_room

    @room.setter
    def room(self, room: str):
        if not isinstance(room, str):
            raise ValueError("Invalid venue room")

        self._venue_room = room

    @property
    def wheel_chair_access(self):
        return self._venue_wheelChairAccess

    @wheel_chair_access.setter
    def wheel_chair_access(self, wheelChairAccess: OptionalSelector):
        if not isinstance(wheelChairAccess, OptionalSelector):
            try:
                wheelChairAccess = OptionalSelector(wheelChairAccess)
            except Exception:
                raise ValueError("Invalid wheelchair access indicator")

        self._venue_wheelChairAccess = wheelChairAccess

    @property
    def intake_size(self):
        return self._intakeSize

    @intake_size.setter
    def intake_size(self, intake_size: int):
        if not isinstance(intake_size, int):
            raise ValueError("Invalid intake size")

        self._intakeSize = intake_size

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, threshold: int):
        if not isinstance(threshold, int):
            raise ValueError("Invalid threshold")

        self._threshold = threshold

    @property
    def registered_user_count(self):
        return self._registeredUserCount

    @registered_user_count.setter
    def registered_user_count(self, registered_user_count: int):
        if not isinstance(registered_user_count, int):
            raise ValueError("Invalid registered user count")

        self._registeredUserCount = registered_user_count

    @property
    def mode_of_training(self):
        return self._modeOfTraining

    @mode_of_training.setter
    def mode_of_training(self, mode_of_training: ModeOfTraining):
        if not isinstance(mode_of_training, ModeOfTraining):
            try:
                # needed to ensure that the enums are the same syntactically
                mode_of_training = ModeOfTraining(mode_of_training)
            except Exception:
                raise ValueError("Invalid mode of training")

        self._modeOfTraining = mode_of_training

    @property
    def course_admin_email(self):
        return self._courseAdminEmail

    @course_admin_email.setter
    def course_admin_email(self, course_admin_email: str):
        if not isinstance(course_admin_email, str):
            raise ValueError("Invalid course admin email")

        self._courseAdminEmail = course_admin_email

    @property
    def course_vacancy_code(self):
        return self._courseVacancy_code

    @course_vacancy_code.setter
    def course_vacancy_code(self, course_vacancy_code: Vacancy):
        if not isinstance(course_vacancy_code, Vacancy):
            try:
                course_vacancy_code = Vacancy(course_vacancy_code)
            except Exception:
                raise ValueError("Invalid course vacancy code")

        self._courseVacancy_code = course_vacancy_code.value[0]

    @property
    def course_vacancy_description(self):
        return self._courseVacancy_description

    @course_vacancy_description.setter
    def course_vacancy_description(self, course_vacancy_description: Vacancy):
        if not isinstance(course_vacancy_description, Vacancy):
            try:
                course_vacancy_description = Vacancy(course_vacancy_description)
            except Exception:
                raise ValueError("Invalid course vacancy description")

        self._courseVacancy_description = course_vacancy_description.value[1]

    @property
    def course_vacancy(self):
        return Vacancy((self._courseVacancy_code, self._courseVacancy_description))

    @course_vacancy.setter
    def course_vacancy(self, course_vacancy: Vacancy):
        if not isinstance(course_vacancy, Vacancy):
            try:
                course_vacancy = Vacancy(course_vacancy)
            except Exception:
                raise ValueError("Invalid course vacancy")

        self._courseVacancy_code = course_vacancy.value[0]
        self._courseVacancy_description = course_vacancy.value[1]

    @property
    def file_name(self):
        return self._file_Name

    @file_name.setter
    def file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise ValueError("Invalid file name")

        self._file_Name = file_name

    @property
    def file_content(self):
        return self._file_content

    @file_content.setter
    def file_content(self, file_content: UploadedFile):
        if file_content is not None and not isinstance(file_content, UploadedFile):
            raise ValueError("Invalid file content")

        self._file_content = file_content

    @property
    def sessions(self):
        return self._sessions

    @sessions.setter
    def sessions(self, sessions: list[RunSessionEditInfo]):
        if not isinstance(sessions, list):
            raise ValueError("Invalid list of sessions")

        self._sessions = sessions

    def add_session(self, session: RunSessionEditInfo) -> None:
        if not isinstance(session, RunSessionEditInfo):
            raise ValueError("Invalid session")

        self._sessions.append(session)

    @property
    def linked_course_run_trainers(self):
        return self._linkCourseRunTrainer

    @linked_course_run_trainers.setter
    def linked_course_run_trainers(self, linked_course_run_trainers: list[RunTrainerEditInfo]):
        if not isinstance(linked_course_run_trainers, list):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer = linked_course_run_trainers

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        if not isinstance(linkCourseRunTrainer, RunTrainerEditInfo):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer.append(linkCourseRunTrainer)

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._registrationDates_opening is None:
            errors.append("No opening registration dates specified!")

        if self._registrationDates_closing is None:
            errors.append("No closing registration dates specified!")

        if self._registrationDates_opening is not None and self._registrationDates_closing is not None and \
                self._registrationDates_opening > self._registrationDates_closing:
            errors.append("Registration dates opening should not be after closing date")

        if self._courseDates_start is None:
            errors.append("No start course dates specified!")

        if self._courseDates_end is None:
            errors.append("No end course dates specified!")

        if self._courseDates_start is not None and self._courseDates_end is not None and \
                self._courseDates_start > self._courseDates_end:
            errors.append("Start course dates should not be after end course date")

        if self._scheduleInfoType_code is None or len(self._scheduleInfoType_code) == 0:
            errors.append("No schedule info type code specified!")

        if self._scheduleInfoType_description is None or len(self._scheduleInfoType_description) == 0:
            errors.append("No schedule info type description specified!")

        if self._scheduleInfo is None or len(self._scheduleInfo) == 0:
            errors.append("No schedule info specified!")

        if self._venue_floor is None or len(self._venue_floor) == 0:
            errors.append("No venue floor is specified!")

        if self._venue_unit is None or len(self._venue_unit) == 0:
            errors.append("No venue unit is specified!")

        if self._venue_postalCode is None or len(self._venue_postalCode) == 0:
            errors.append("No venue postal code is specified!")

        if self._venue_room is None or len(self._venue_room) == 0:
            errors.append("No venue room is specified!")

        if self._modeOfTraining is None:
            errors.append("No mode of training is specified!")

        if self._courseAdminEmail is None or len(self._courseAdminEmail) == 0:
            errors.append("No course admin email is specified!")

        if self._courseAdminEmail is not None and len(self._courseAdminEmail) > 0:
            try:
                validate_email(self._courseAdminEmail)
            except EmailSyntaxError:
                errors.append("Course Admin Email specified is not of the correct format!")

        if self._courseVacancy_code is None or len(self._courseVacancy_code) == 0:
            errors.append("No course vacancy code is specified!")

        if self._courseVacancy_description is None or len(self._courseVacancy_description) == 0:
            errors.append("No course vacancy description is specified!")

        # optional param validation
        if self._venue_block is not None and len(self._venue_block) == 0:
            warnings.append("Venue Block is empty but Venue Block is marked as specified!")

        if self._venue_street is not None and len(self._venue_street) == 0:
            warnings.append("Venue Street is empty but Venue Street is marked as specified!")

        if self._venue_building is not None and len(self._venue_building) == 0:
            warnings.append("Venue Building is empty but Venue Building is marked as specified!")

        if self._file_Name is not None and len(self._file_Name) == 0:
            warnings.append("File Name is empty but File Name is marked as specified!")

        if self._file_Name is not None and self._file_content is None:
            warnings.append("File Name is specified but there is no file uploaded!")

        if self._file_Name is None and self._file_content is not None:
            warnings.append("File Content is specified but there is no file name!")

        for i, session in enumerate(self._sessions):
            err, war = session.validate()

            for e in err:
                errors.append(f"*Session {i + 1}*: {e}")

            for w in war:
                warnings.append(f"*Session {i + 1}*: {w}")

        for i, trainer in enumerate(self._linkCourseRunTrainer):
            err, war = trainer.validate()

            for e in err:
                errors.append(f"*Trainer {i + 1}*: {e}")

            for w in war:
                warnings.append(f"*Trainer {i + 1}*: {w}")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "sequenceNumber": self._sequenceNumber,
            "registrationDates": {
                "opening": (int(self._registrationDates_opening.strftime("%Y%m%d"))
                            if self._registrationDates_opening is not None else None),
                "closing": (int(self._registrationDates_closing.strftime("%Y%m%d"))
                            if self._registrationDates_closing is not None else None),
            },
            "courseDates": {
                "start": (int(self._courseDates_start.strftime("%Y%m%d"))
                          if self._courseDates_start is not None else None),
                "end": (int(self._courseDates_end.strftime("%Y%m%d"))
                        if self._courseDates_end is not None else None),
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
                "wheelChairAccess": (self._venue_wheelChairAccess.value[1]
                                     if self._venue_wheelChairAccess is not None else None)
            },
            "intakeSize": self._intakeSize,
            "threshold": self._threshold,
            "registeredUserCount": self._registeredUserCount,
            "modeOfTraining": self._modeOfTraining.value[0] if self._modeOfTraining is not None else None,
            "courseAdminEmail": self._courseAdminEmail,
            "courseVacancy": {
                "code": self._courseVacancy_code,
                "description": self._courseVacancy_description
            },
            "file": {
                "Name": self._file_Name,
                "content": (base64.b64encode(
                    self._file_content.getvalue()).decode() if self._file_content else None),
            },
            "sessions": list(map(lambda x: x.payload(verify=False), self._sessions)),
            "linkCourseRunTrainer": list(map(lambda x: x.payload(verify=False), self._linkCourseRunTrainer))
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_crid(self, crn: str) -> None:
        raise NotImplementedError("This method is not supported!")


class AddRunInfo(EditRunInfo):
    """Encapsulates all information regarding the addition of a course run"""

    def __init__(self):
        super().__init__()
        self._runs: list[AddRunIndividualInfo] = []

    def __eq__(self, other):
        if not isinstance(other, AddRunInfo):
            return False

        return (
            self._crid == other._crid
            and len(self._runs) == len(other._runs)
            and all(map(lambda x: x[0] == x[1], zip(self._runs, other._runs)))
        )

    def add_run(self, run: AddRunIndividualInfo) -> None:
        if not isinstance(run, AddRunIndividualInfo):
            raise TypeError("Invalid individual run info")

        self._runs.append(run)

    @property
    def runs(self):
        return self._runs

    @runs.setter
    def runs(self, runs: list[AddRunIndividualInfo]):
        if not isinstance(runs, list):
            raise ValueError("Invalid list of runs")

        self._runs = runs

    @property
    def crid(self):
        return self._crid

    @crid.setter
    def crid(self, crn: str):
        if not isinstance(crn, str):
            raise ValueError("Invalid Course Reference ID number")

        self._crid = crn

    @property
    def sequence_number(self):
        raise NotImplementedError("This method is not supported!")

    @sequence_number.setter
    def sequence_number(self, sequence_number: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def opening_registration_date(self):
        raise NotImplementedError("This method is not supported!")

    @opening_registration_date.setter
    def opening_registration_date(self, opening_registration_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def closing_registration_date(self):
        raise NotImplementedError("This method is not supported!")

    @closing_registration_date.setter
    def closing_registration_date(self, closing_registration_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_start_date(self):
        raise NotImplementedError("This method is not supported!")

    @course_start_date.setter
    def course_start_date(self, course_start_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_end_date(self):
        raise NotImplementedError("This method is not supported!")

    @course_end_date.setter
    def course_end_date(self, course_end_date: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info_type_code(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info_type_code.setter
    def schedule_info_type_code(self, schedule_info_type_code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info_type_description(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info_type_description.setter
    def schedule_info_type_description(self, schedule_info_type_description: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def schedule_info(self):
        raise NotImplementedError("This method is not supported!")

    @schedule_info.setter
    def schedule_info(self, schedule_info: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def block(self):
        raise NotImplementedError("This method is not supported!")

    @block.setter
    def block(self, block: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def street(self):
        raise NotImplementedError("This method is not supported!")

    @street.setter
    def street(self, street: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def floor(self):
        raise NotImplementedError("This method is not supported!")

    @floor.setter
    def floor(self, floor: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def unit(self):
        raise NotImplementedError("This method is not supported!")

    @unit.setter
    def unit(self, unit: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def building(self):
        raise NotImplementedError("This method is not supported!")

    @building.setter
    def building(self, building: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def postal_code(self):
        raise NotImplementedError("This method is not supported!")

    @postal_code.setter
    def postal_code(self, postal_code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def room(self):
        raise NotImplementedError("This method is not supported!")

    @room.setter
    def room(self, room: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def wheel_chair_access(self):
        raise NotImplementedError("This method is not supported!")

    @wheel_chair_access.setter
    def wheel_chair_access(self, wheelChairAccess: OptionalSelector):
        raise NotImplementedError("This method is not supported!")

    @property
    def intake_size(self):
        raise NotImplementedError("This method is not supported!")

    @intake_size.setter
    def intake_size(self, intake_size: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def threshold(self):
        raise NotImplementedError("This method is not supported!")

    @threshold.setter
    def threshold(self, threshold: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def registered_user_count(self):
        raise NotImplementedError("This method is not supported!")

    @registered_user_count.setter
    def registered_user_count(self, registered_user_count: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def mode_of_training(self):
        raise NotImplementedError("This method is not supported!")

    @mode_of_training.setter
    def mode_of_training(self, mode_of_training: ModeOfTraining):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_admin_email(self):
        raise NotImplementedError("This method is not supported!")

    @course_admin_email.setter
    def course_admin_email(self, course_admin_email: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy_code(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy_code.setter
    def course_vacancy_code(self, course_vacancy_code: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy_description(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy_description.setter
    def course_vacancy_description(self, course_vacancy_description: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_vacancy(self):
        raise NotImplementedError("This method is not supported!")

    @course_vacancy.setter
    def course_vacancy(self, course_vacancy: Vacancy):
        raise NotImplementedError("This method is not supported!")

    @property
    def file_name(self):
        raise NotImplementedError("This method is not supported!")

    @file_name.setter
    def file_name(self, file_name: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def file_content(self):
        raise NotImplementedError("This method is not supported!")

    @file_content.setter
    def file_content(self, file_content: UploadedFile):
        raise NotImplementedError("This method is not supported!")

    @property
    def sessions(self):
        raise NotImplementedError("This method is not supported!")

    @sessions.setter
    def sessions(self, sessions: list[RunSessionEditInfo]):
        raise NotImplementedError("This method is not supported!")

    def add_session(self, session: RunSessionEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    @property
    def linked_course_run_trainers(self):
        raise NotImplementedError("This method is not supported!")

    @linked_course_run_trainers.setter
    def linked_course_run_trainers(self, linked_course_run_trainers: list[RunTrainerEditInfo]):
        raise NotImplementedError("This method is not supported!")

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._crid is None or len(self._crid) == 0:
            errors.append("No Course Reference ID number specified!")

        for i, run in enumerate(self._runs):
            err, war = run.validate()

            for e in err:
                errors.append(f"**Run {i + 1}**: {e}")

            for w in war:
                warnings.append(f"**Run {i + 1}**: {w}")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "course": {
                "courseReferenceNumber": self._crid,
                "trainingProvider": {
                    "uen": st.session_state["uen"] if "uen" in st.session_state else None
                }
            },
            "runs": [x.payload(verify=False) for x in self._runs]
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl
