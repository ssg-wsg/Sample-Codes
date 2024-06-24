"""
This page is used to enable access to the Attendance API. The Attendance API is a subset of the Courses API, and
can be found in the same page as the other Courses-related APIs.

There are 2 main processes:
1. (View) Course Session Attendance
    - This tab allows you to key in your Course Run ID, Assessment Reference Number and Session ID to retrieve
      the course session attendance of a particular course run and session.
2. Upload Course Session Attendance
    - This tab allows you to upload information regarding the attendance of a trainee for a particular course run
      and course session to record their attendance.

It is important to note that optional fields are always hidden behind a Streamlit checkbox to allow the backend
functions to clean up the request body and send requests that contains only non-null fields.
"""

import streamlit as st

from revamped_application.core.attendance.course_session_attendance import CourseSessionAttendance
from revamped_application.core.attendance.upload_course_session_attendance import UploadCourseSessionAttendance
from revamped_application.core.constants import IdType, Attendance, SurveyLanguage
from revamped_application.core.models.attendance import UploadAttendanceInfo
from revamped_application.core.system.logger import Logger

from revamped_application.utils.http_utils import handle_response, handle_request
from revamped_application.utils.streamlit_utils import init, display_config, validation_error_handler, \
    does_not_have_keys
from revamped_application.utils.verify import Validators

# initialise necessary variables
init()
LOGGER = Logger("Attendance API")

st.set_page_config(page_title="Attendance", page_icon="✅")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")
    if st.button("Configs", key="config_display"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Attendance API")
st.markdown("The Attendance API allows you effortlessly retrieve and update the course session attendance "
            "of your trainees who are enrolled into your courses!")
st.info("**This API requires your requests and data to be encrypted!**", icon="ℹ️")

view, upload = st.tabs(["Course Session Attendance", "Upload Course Session Attendance"])

with view:
    st.header("Course Session Attendance")
    st.markdown("You can use this API to view the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if "uen" not in st.session_state or st.session_state["uen"] is None:
        st.warning("**Course Session Attendance API requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    runs = st.text_input("Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-view-attendance")
    crn = st.text_input("Key in the Assessment Reference Number", key="crn_view_sessions")
    session_id = st.text_input("Enter Session ID",
                               help="The course session ID to be retrieved; encode this parameter to ensure that "
                                    "special characters will not be blocked by the Gateway",
                               key="session_id_view_attendance")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="view_course_session_attendance_button"):
        LOGGER.info("Attempting to send request to Retrieve Course Session Attendance API...")

        if not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif len(runs) == 0:
            LOGGER.error("Missing Course Run ID, request aborted!")
            st.error("Make sure to specify your **Course Run ID** before proceeding!", icon="🚨")
        elif len(crn) == 0:
            LOGGER.error("Missing Course Reference Number, request aborted!")
            st.error("Make sure to specify your **Course Reference Number** before proceeding!", icon="🚨")
        elif len(session_id) == 0:
            LOGGER.error("Missing Session ID, request aborted!")
            st.error("Make sure to specify your **Session ID** before proceeding!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = CourseSessionAttendance(runs, crn, session_id)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(vc)

            with response:
                LOGGER.info("Executing request...")
                handle_response(lambda: vc.execute())

with upload:
    st.header("Upload Course Session Attendance")
    st.markdown("You can use this API to update the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if "uen" not in st.session_state or st.session_state["uen"] is None:
        st.warning("**Upload Course Session Attendance API requires your UEN to proceed. Make sure that you have "
                   "loaded it up properly under the Home page before proceeding!**", icon="⚠️")

    uploadAttendance = UploadAttendanceInfo()

    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-upload-attendance")
    uploadAttendance.referenceNumber = st.text_input(label="Key in the Course Reference Number",
                                                     key="crn-upload-attendance-sessions")
    uploadAttendance.corppassId = st.text_input(label="Key in your CorpPass Number",
                                                key="corppass-upload-attendance-sessions")
    uploadAttendance.sessionId = st.text_input(label="Enter Session ID",
                                               help="The course session ID to be retrieved; encode this parameter "
                                                    "to ensure that special characters will not be blocked by the "
                                                    "Gateway",
                                               key="session_id_upload_attendance")

    st.subheader("Attendance Information")
    uploadAttendance.status_code = st.selectbox(label="Enter the Attendance Status Code",
                                                options=Attendance,
                                                format_func=lambda x: str(x),
                                                key="attendance-status-code-upload-attendance")

    st.subheader("Trainee Information")
    col1, col2 = st.columns(2)

    with col1:
        uploadAttendance.trainee_id_type = st.selectbox(label="Enter Trainee ID Type",
                                                        options=IdType,
                                                        format_func=lambda x: str(x),
                                                        key="trainee-id-type-upload-attendance")

    with col2:
        uploadAttendance.trainee_id = st.text_input(label="Enter Trainee ID",
                                                    help="The ID of the trainee",
                                                    max_chars=50,
                                                    key="trainee-id-upload-attendance")

    uploadAttendance.trainee_name = st.text_input(label="Enter Trainee Name",
                                                  help="Name of the trainee",
                                                  max_chars=66,
                                                  key="trainee-name-upload-attendance")

    if st.checkbox("Specify Trainee Email?", key="specify-trainee-email-upload-attendance"):
        uploadAttendance.trainee_email = st.text_input(label="Enter Trainee Email",
                                                       help="Email of the trainee; either email or contact number is "
                                                            "necessary",
                                                       max_chars=320,
                                                       key="trainee-email-upload-attendance")

        if len(uploadAttendance.trainee_email) > 0:
            if not Validators.verify_email(uploadAttendance.trainee_email):
                st.warning(f"Email format is not valid!", icon="⚠️")

    uploadAttendance.contactNumber_mobile = st.text_input(label="Enter Mobile Number of Trainee",
                                                          max_chars=15,
                                                          key="contact-number-mobile-upload-attendance")

    if st.checkbox("Specify Contact Number Area Code?", key="specify-areacode-upload-attendance"):
        uploadAttendance.contactNumber_areacode = st.number_input(label="Enter Mobile Number Area Code",
                                                                  min_value=0,
                                                                  max_value=99999,
                                                                  value=0)

    uploadAttendance.contactNumber_countryCode = st.number_input(label="Enter Mobile Number Country Code",
                                                                 min_value=0,
                                                                 max_value=999,
                                                                 value=65)

    st.subheader("Course Information")
    if st.checkbox("Specify number of hours?", key="hours-upload-attendance"):
        uploadAttendance.numberOfHours = st.number_input(label="Enter number of hours",
                                                         min_value=0.5,
                                                         max_value=8.0,
                                                         step=0.1)

    uploadAttendance.surveyLanguage_code = st.selectbox(
        label="Enter Survey Language",
        options=SurveyLanguage,
        format_func=lambda x: str(x),
        key="language-upload-attendance")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(uploadAttendance.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="upload_course_session_attendance_button"):
        LOGGER.info("Attempting to send request to Upload Course Session Attendance API...")
        if not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif not runs:
            LOGGER.error("Missing Course Run ID, request aborted!")
            st.error("Make sure to fill in your **Course Run ID** before proceeding!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        else:
            errors, warnings = uploadAttendance.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                uca = UploadCourseSessionAttendance(runs, uploadAttendance)

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(uca)

                with response:
                    LOGGER.info("Executing request...")
                    handle_response(lambda: uca.execute())
