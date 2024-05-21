import streamlit as st

from core.models.attendance import UploadAttendanceInfo

from utils.http_utils import handle_error
from utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Enrolment", page_icon="🏫")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("Enrolment API")
st.markdown("The Enrolment API allows you enroll your trainees to your courses!")
st.info("To scroll through the different tabs below, you can hold `Shift` and scroll with your mouse scroll, or you "
        "can use the arrow keys to navigate between the tabs!")

create, update, delete, search, view, update_fee = st.tabs([
    "Create Enrolment", "Update Enrolment", "Delete Enrolment", "Search Enrolment", "View Enrolment",
    "Update Enrolment Fee Collection"
])

with create:
    pass

with update:
    pass

with delete:
    pass

with search:
    pass

with view:
    pass

with update_fee:
    pass
