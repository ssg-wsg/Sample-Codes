"""
Contains test data to provide to users
"""
import datetime
from enum import Enum


class TestData(Enum):
    """Enum containing all test data"""

    UEN = "199900650G"
    TPCODE = "199900650G-01"

    COURSE_REFERENCE_NUMBER = "TGS-2020000697"
    COURSE_RUN_NUMBER = "835457"
    COURSE_SESSION_NUMBER = "TGS-2020000697-835457-S1"
    ENROLMENT_ID = "ENR-2501-000004"
    
    EMAIL = "test@test.com"
    COUNTRYCODE = "+65"
    COUNTRYCODE_INT = 65
    PHONE = "98765432"
    
    CORPPASS = "S1449757I"
    EMPLOYER_UEN = "201000372W"
    EMPLOYER_NAME = "Stephen Chua"

    TRAINEE_ID = "S7020587D"
    TRAINEE_NAME = "Aileen Chong"
    TRAINEE_DOB = datetime.date(1969, 3, 8)
    
    TRAINER_ID = "S0808315J"
    
    VENUE_POSTAL = "408533"

    # Assessments test data
    SKILL_CODE = "ATP-SSM-3007-1.1"
    CONFERRING_INSITITUTE_UEN = "52863847E"
    CONFERRING_INSITITUTE_CODE = "52863847E-01"
    CONFERRING_INSITITUTE_NAME = "test"

    ASSESSMENT_COURSE_RUN = "340121"
    ASSESSMENT_ID = "ASM-2009-161334"
