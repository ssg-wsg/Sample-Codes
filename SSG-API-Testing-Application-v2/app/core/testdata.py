"""
Contains test data to provide to users
"""
from enum import Enum
import streamlit as st

def set_default(widget_key: str, default_value: str):
    '''prefill the value into an unmodified text box'''
    if widget_key not in st.session_state or st.session_state[widget_key] == "":
        st.session_state[widget_key] = default_value

class TestData(Enum):
    """Enum containing all test data"""

    UEN = "199900650G"
    TPCODE = "199900650G-01"
    COURSE_REFERENCE_NUMBER = "TGS-2020000697"
    COURSE_RUN_NUMBER = "835457"
    COURSE_SESSION_NUMBER = "TGS-2020000697-835457-S1"
    TRAINER_ID = "S0808315J"
    TRAINEE_ID = "TGS-2020000697-835457-S1"
    VENUE_POSTAL = "408533"
