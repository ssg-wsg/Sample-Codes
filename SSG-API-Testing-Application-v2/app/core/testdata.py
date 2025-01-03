"""
Contains test data to provide to users
"""
import datetime
from enum import Enum
import streamlit as st

def set_default(widget_key: str, default_value):
    # '''prefill the value into an unmodified text box'''
    # if widget_key not in st.session_state or not st.session_state[widget_key]:
    #     st.session_state[widget_key] = default_value
    pass

class TestData(Enum):
    """Enum containing all test data"""

    UEN = "199900650G"
    TPCODE = "199900650G-01"
    COURSE_REFERENCE_NUMBER = "TGS-2020000697"
    COURSE_RUN_NUMBER = "835457"
    COURSE_SESSION_NUMBER = "TGS-2020000697-835457-S1"
    
    EMAIL = "test@test.com"
    COUNTRYCODE = "+65"
    PHONE = "98765432"
    
    CORPPASS = "S1449757I"
    EMPLOYER_UEN = "201000372W"
    EMPLOYER_NAME = "Stephen Chua"

    TRAINEE_ID = "S0808315J"
    TRAINEE_NAME = "Aileen Chong"
    TRAINEE_DOB = datetime.date(1970, 6, 19) # 1970/06/19
    TRAINER_ID = "S0808315J"
    
    VENUE_POSTAL = "408533"

