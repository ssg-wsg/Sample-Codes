"""
Contains classes that help encapsulate data for sending requests to the Course Runs / Sessions APIs.
"""

import base64
import datetime
import json
import streamlit as st

from typing import Optional, Literal
from streamlit.runtime.uploaded_file_manager import UploadedFile
from revamped_application.core.abc.abstract import AbstractRequestInfo
from revamped_application.core.constants import Vacancy, ModeOfTraining, IdType, Salutations, Role
from revamped_application.utils.json_utils import remove_null_fields


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

        if as_json_str:
            return json.dumps(pl)

        return pl


# ===== Session Info ===== #
class RunSessionEditInfo(AbstractRequestInfo):
    """Encapsulates all information regarding a course run's sessions"""

    def __init__(self):
        self._sessionId: Optional[str] = None
        self._startDate: Optional[datetime.date] = None
        self._endDate: Optional[datetime.date] = None
        self._startTime: Optional[datetime.time] = None
        self._endTime: Optional[datetime.time] = None
        self._modeOfTraining: Optional[ModeOfTraining] = None
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

    def set_modeOfTraining(self, modeOfTraining: ModeOfTraining) -> None:
        if not isinstance(modeOfTraining, ModeOfTraining):
            try:
                # needed to ensure that the enums are the same syntactically
                modeOfTraining = ModeOfTraining(modeOfTraining)
            except Exception:
                raise ValueError("Invalid mode of training")

        self._modeOfTraining = modeOfTraining.value[0]

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

        if self._modeOfTraining is None or len(self._modeOfTraining) == 0:
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
        self._salutationId: Optional[Salutations] = None
        self._photo_name: Optional[str] = None
        self._photo_content: Optional[UploadedFile] = None
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
                "roles": self._roles,
                "inTrainingProviderProfile": self._inTrainingProviderProfile,
                "domainAreaOfPractice": self._domainAreaOfPractice,
                "experience": self._experience,
                "linkedInURL": self._linkedInURL,
                "salutationId": self._salutationId,
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

    def set_trainer_idType(self, idType: IdType) -> None:
        if not isinstance(idType, IdType):
            try:
                idType = IdType(idType)
            except Exception:
                raise ValueError("Invalid trainee ID type")

        self._idType_code = idType.value[0]
        self._idType_description = idType.value[1]

    def set_trainer_roles(self, roles: list[Role]) -> None:
        if not isinstance(roles, list):
            raise ValueError("Invalid trainer roles")

        try:
            self._roles = [Role(role).value for role in roles]
        except Exception:
            raise ValueError("Invalid trainer roles")

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

    def set_salutationId(self, salutationId: Salutations) -> None:
        if not isinstance(salutationId, Salutations):
            raise ValueError("Invalid salutation")

        self._salutationId = salutationId.value[0]

    def set_photo_name(self, photo_name: str) -> None:
        if not isinstance(photo_name, str):
            raise ValueError("Invalid photo_name")

        self._photo_name = photo_name

    def set_photo_content(self, photo_content: UploadedFile) -> None:
        if photo_content is not None and not isinstance(photo_content, UploadedFile):
            raise ValueError("Invalid photo_content")

        self._photo_content = photo_content

    def add_linkedSsecEQA(self, linkedSsecEQA: dict) -> None:
        if not isinstance(linkedSsecEQA, dict):
            raise ValueError("Invalid linkedSsecEQA")

        self._linkedSsecEQAs.append(linkedSsecEQA)


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
        self._modeOfTraining: Optional[ModeOfTraining] = None
        self._courseAdminEmail: Optional[str] = None
        self._courseVacancy_code: Literal["A", "F", "L"] = None
        self._courseVacancy_description: Optional[Literal["Available", "Full", "Limited Vacancy"]] = None
        self._file_Name: Optional[str] = None
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
            errors.append("Course Registration Start Date must be before Course Registration End Date!")

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

        self._venue_room = venue_room

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

    def set_modeOfTraining(self, modeOfTraining: ModeOfTraining) -> None:
        if not isinstance(modeOfTraining, ModeOfTraining):
            try:
                # needed to ensure that the enums are the same syntactically
                modeOfTraining = ModeOfTraining(modeOfTraining)
            except Exception:
                raise ValueError("Invalid mode of training")

        self._modeOfTraining = modeOfTraining.value[0]

    def set_courseAdminEmail(self, courseAdminEmail: str) -> None:
        if not isinstance(courseAdminEmail, str):
            raise ValueError("Invalid course admin email")

        self._courseAdminEmail = courseAdminEmail

    def set_courseVacancy(self, vacancy: Vacancy):
        if not isinstance(vacancy, Vacancy):
            try:
                vacancy = Vacancy(vacancy)
            except Exception:
                raise ValueError("Invalid course vacancy")

        self._courseVacancy_code = vacancy.value[0]
        self._courseVacancy_description = vacancy.value[1]

    def set_file_Name(self, file_Name: str) -> None:
        if not isinstance(file_Name, str):
            raise ValueError("Invalid file name")

        self._file_Name = file_Name

    def set_file_content(self, file_content: UploadedFile) -> None:
        if file_content is not None and not isinstance(file_content, UploadedFile):
            raise ValueError("Invalid file content")

        self._file_content = file_content

    def set_sessions(self, sessions: list[RunSessionEditInfo]) -> None:
        if not isinstance(sessions, list):
            raise ValueError("Invalid list of sessions")

        self._sessions = sessions

    def add_session(self, session: RunSessionEditInfo) -> None:
        if not isinstance(session, RunSessionEditInfo):
            raise ValueError("Invalid session")

        self._sessions.append(session)

    def set_linkCourseRunTrainer(self, linkCourseRunTrainer: list) -> None:
        if not isinstance(linkCourseRunTrainer, list):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer = linkCourseRunTrainer

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        if not isinstance(linkCourseRunTrainer, RunTrainerEditInfo):
            raise ValueError("Invalid course run trainer information")

        self._linkCourseRunTrainer.append(linkCourseRunTrainer)


class DeleteRunInfo(EditRunInfo):
    """Encapsulates all information regarding the deletion of a course run"""

    def __init__(self) -> None:
        super().__init__()

    def __eq__(self, other):
        if not isinstance(other, DeleteRunInfo):
            return False

        return self._crid == other._crid

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

    def set_sequence_number(self, sequence_number: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registrationDates_opening(self, registrationDates_opening: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registrationDates_closing(self, registrationDates_closing: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseDates_start(self, courseDates_start: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseDates_end(self, courseDates_end: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfoType_code(self, scheduleInfoType_code: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfoType_description(self, scheduleInfoType_description: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfo(self, scheduleInfo: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_block(self, venue_block: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_street(self, venue_street: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_floor(self, venue_floor: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_unit(self, venue_unit: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_building(self, venue_building: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_room(self, venue_room: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_intakeSize(self, intakeSize: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_threshold(self, threshold: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registeredUserCount(self, registeredUserCount: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseAdminEmail(self, courseAdminEmail: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseVacancy(self, vacancy: Vacancy):
        raise NotImplementedError("This method is not supported!")

    def set_file_Name(self, file_Name: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_file_content(self, file_content: UploadedFile) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_sessions(self, sessions: list[RunSessionEditInfo]) -> None:
        raise NotImplementedError("This method is not supported!")

    def add_session(self, session: RunSessionEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_linkCourseRunTrainer(self, linkCourseRunTrainer: list) -> None:
        raise NotImplementedError("This method is not supported!")

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")


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

    def add_run(self, run: AddRunIndividualInfo) -> None:
        if not isinstance(run, AddRunIndividualInfo):
            raise TypeError("Invalid individual run info")

        self._runs.append(run)

    def set_sequence_number(self, sequence_number: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registrationDates_opening(self, registrationDates_opening: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registrationDates_closing(self, registrationDates_closing: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseDates_start(self, courseDates_start: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseDates_end(self, courseDates_end: datetime.date) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfoType_code(self, scheduleInfoType_code: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfoType_description(self, scheduleInfoType_description: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_scheduleInfo(self, scheduleInfo: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_block(self, venue_block: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_street(self, venue_street: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_floor(self, venue_floor: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_unit(self, venue_unit: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_building(self, venue_building: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_postalCode(self, venue_postalCode: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_room(self, venue_room: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_venue_wheelChairAccess(self, wheelChairAccess: Literal["Select a value", "Yes", "No"]) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_intakeSize(self, intakeSize: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_threshold(self, threshold: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_registeredUserCount(self, registeredUserCount: int) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_modeOfTraining(self, modeOfTraining: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseAdminEmail(self, courseAdminEmail: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_courseVacancy(self, Vacancy: Vacancy):
        raise NotImplementedError("This method is not supported!")

    def set_file_Name(self, file_Name: str) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_file_content(self, file_content: UploadedFile) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_sessions(self, sessions: list[RunSessionEditInfo]) -> None:
        raise NotImplementedError("This method is not supported!")

    def add_session(self, session: RunSessionEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")

    def set_linkCourseRunTrainer(self, linkCourseRunTrainer: list) -> None:
        raise NotImplementedError("This method is not supported!")

    def add_linkCourseRunTrainer(self, linkCourseRunTrainer: RunTrainerEditInfo) -> None:
        raise NotImplementedError("This method is not supported!")
