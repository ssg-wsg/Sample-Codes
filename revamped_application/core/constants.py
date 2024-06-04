"""
Contains all constants and mappings that are used throughout multiple elements in the app

Enums code is inspired by https://stackoverflow.com/questions/12680080/python-enums-with-attributes
"""

from enum import Enum


# ===== BASE CONSTANTS ===== #
class HttpMethod(Enum):
    """Enum representing the permitted types of HTTP requests that can be made."""

    GET = "GET"
    POST = "POST"


class Endpoints(Enum):
    """Enum representing the endpoints that users can connect to."""

    UAT = "https://uat-api.ssg-wsg.sg"
    PRODUCTION = "https://api.ssg-wsg.sg"
    MOCK = "https://mock-api.ssg-wsg.sg"


# ===== COURSES CONSTANTS ===== #
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

ID_TYPE_MAPPING: dict[str, str] = {
    "SB": "Singapore Blue Identification Card",
    "SP": "Singapore Pink Identification Card",
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

NUM2MONTH: dict[int, str] = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

# ===== ASSESSMENT CONSTANTS ===== #
GRADES = ["A", "B", "C", "D", "E", "F"]
RESULTS = ["Pass", "Fail", "Exempt"]
ID_TYPE = ["NRIC", "FIN", "OTHERS"]
ASSESSMENT_UPDATE_VOID_ACTIONS = ["update", "void"]

# ===== ATTENDANCE CONSTANTS ===== #
ATTENDANCE_CODE_MAPPINGS = {
    "1": "Confirmed",
    "2": "Unconfirmed",
    "3": "Rejected",
    "4": "TP Voided"
}
SORT_FIELD = ["updatedOn", "createdOn", "assessmentDate"]
SORT_ORDER = {
    "asc": "Ascending",
    "desc": "Descending"
}

SURVEY_LANGUAGE_MAPPINGS = {
    "EL": "English",
    "MN": "Mandarin",
    "MY": "Malay",
    "TM": "Tamil"
}
