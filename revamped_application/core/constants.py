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


class Vacancy(Enum):
    """Enum representing the different course vacancy codes."""

    AVAILABLE = ("A", "Available")
    FULL = ("F", "Full")
    LIMITED_VACANCY = ("L", "Limited Vacancy")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


# ===== COURSE CONSTANTS ===== #
class Role(Enum):
    """Enum to represent the 2 roles a trainer may have."""

    TRAINER = {
        "id": 1,
        "description": "Trainer"
    }
    ASSESSOR = {
        "id": 2,
        "description": "Assessor"
    }

    def __str__(self):
        return self.value["description"]


class ModeOfTraining(Enum):
    """Enum representing the different modes of training."""

    CLASSROOM = ("1", "Classroom")
    ASYNCHRONOUS_ELEARNING = ("2", "Asynchronous eLearning")
    IN_HOUSE = ("3", "In-house")
    ON_THE_JOB = ("4", "On-the-Job")
    PRACTICAL_PRACTICUM = ("5", "Practical / Practicum")
    SUPERVISED_FIELD = ("6", "Supervised Field")
    TRAINEESHIP = ("7", "Traineeship")
    ASSESSMENT = ("8", "Assessment")
    SYNCHRONOUS_LEARNING = ("9", "Synchronous Learning")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


class IdType(Enum):
    """Enum representing the different subtypes of identification documents in use in Singapore."""

    SINGAPORE_BLUE = ("SB", "Singapore Blue Identification Card")
    SINGAPORE_PINK = ("SP", "Singapore Pink Identification Card")
    FIN_WORK_PERMIT = ("SO", "Fin/Work Permit")
    FOREIGN_PASSPORT = ("FP", "Foreign Passport")
    OTHERS = ("OT", "Others")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


class Salutations(Enum):
    """Enum representing the different salutations."""

    MR = (1, "Mr")
    MS = (2, "Ms")
    MDM = (3, "Mdm")
    MRS = (4, "Mrs")
    DR = (5, "Dr")
    PROF = (6, "Prof")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


class Month(Enum):
    """Enum representing the months of the year."""

    JAN = (1, "Jan")
    FEB = (2, "Feb")
    MAR = (3, "Mar")
    APR = (4, "Apr")
    MAY = (5, "May")
    JUN = (6, "Jun")
    JUL = (7, "Jul")
    AUG = (8, "Aug")
    SEP = (9, "Sep")
    OCT = (10, "Oct")
    NOV = (11, "Nov")
    DEC = (12, "Dec")

    def __str__(self):
        return self.value[1]


# ===== ASSESSMENT CONSTANTS ===== #
class Grade(Enum):
    """Enum represents the overall grade of an assessment."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    def __str__(self):
        return self.value


class Results(Enum):
    """Enum represents the overall result of an assessment."""
    PASS = "Pass"
    FAIL = "Fail"
    EXEMPT = "Exempt"

    def __str__(self):
        return self.value


class IdTypeSummary(Enum):
    """Enum represents the different subtypes of identification documents in use in Singapore."""

    NRIC = "NRIC"
    FIN = "FIN"
    OTHERS = "OTHERS"

    def __str__(self):
        return self.value


class AssessmentUpdateVoidActions(Enum):
    """Enum represents the different actions that can be taken on an assessment."""

    UPDATE = "update"
    VOID = "void"

    def __str__(self):
        return self.value


# ===== ATTENDANCE CONSTANTS ===== #
class Attendance(Enum):
    """Enum represents the different attendance statuses for a trainee."""

    CONFIRMED = ("1", "Confirmed")
    UNCONFIRMED = ("2", "Unconfirmed")
    REJECTED = ("3", "Rejected")
    TP_VOIDED = ("4", "TP Voided")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


class SortField(Enum):
    """Enum represents the different fields that can be sorted by."""

    UPDATED_ON = "updatedOn"
    CREATED_ON = "createdOn"
    ASSESSMENT_DATE = "assessmentDate"

    def __str__(self):
        return self.value


class SortOrder(Enum):
    """Enum represents the different orders that the results can be sorted in."""

    ASCENDING = ("asc", "Ascending")
    DESCENDING = ("desc", "Descending")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


class SurveyLanguage(Enum):
    """Enum represents the different languages that a survey can be conducted in."""

    ENGLISH = ("EL", "English")
    MANDARIN = ("MN", "Mandarin")
    MALAY = ("MY", "Malay")
    TAMIL = ("TM", "Tamil")

    def __str__(self):
        return f"{self.value[0]}: {self.value[1]}"


# ====== ENROLMENT CONSTANTS ===== #
class CollectionStatus(Enum):
    """Enum represents the different statuses of a collection."""

    PENDING_PAYMENT = "Pending Payment"
    PARTIAL_PAYMENT = "Partial Payment"
    FULL_PAYMENT = "Full Payment"

    def __str__(self):
        return self.value


class CancellableCollectionStatus(Enum):
    """Enum represents the statuses of a collection that can be cancelled."""

    PENDING_PAYMENT = "Pending Payment"
    PARTIAL_PAYMENT = "Partial Payment"
    FULL_PAYMENT = "Full Payment"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.value


class SponsorshipType(Enum):
    """Enum represents the different types of sponsorships that can be made."""

    EMPLOYER = "EMPLOYER"
    INDIVIDUAL = "INDIVIDUAL"

    def __str__(self):
        return self.value


class EnrolmentSortField(Enum):
    """Enum represents the different fields that can be sorted by."""

    UPDATED_ON = "updatedOn"
    CREATED_ON = "createdOn"

    def __str__(self):
        return self.value


class EnrolmentStatus(Enum):
    """Enum represents the different statuses of an enrolment."""

    CONFIRMED = "Confirmed"
    REJECTED = "Rejected"

    def __str__(self):
        return self.value


class EnrolmentCourseStatus(Enum):
    """Enum represents the different statuses of a course enrolment."""

    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"

    def __str__(self):
        return self.value
