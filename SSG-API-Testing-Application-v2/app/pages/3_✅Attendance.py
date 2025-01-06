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

from app.core.attendance.course_session_attendance import CourseSessionAttendance
from app.core.attendance.upload_course_session_attendance import (
    UploadCourseSessionAttendance)
from app.core.constants import IdType, Attendance, SurveyLanguage
from app.core.models.attendance import UploadAttendanceInfo
from app.core.system.logger import Logger

from app.utils.http_utils import handle_response, handle_request
from app.utils.streamlit_utils import init, display_config, \
    validation_error_handler, does_not_have_url
from app.utils.verify import Validators

import app.core.system.secrets as Secrets
from app.core.testdata import TestData  # noqa: E402

# initialise necessary variables
init()
LOGGER = Logger("Attendance API")

st.set_page_config(page_title="Attendance", page_icon="✅")

with st.sidebar:
    st.header("View Configs")
    st.markdown(
        "Click the `Configs` button to view your loaded configurations at any time!")

    if st.button("Configs", key="config_display", type="primary"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Attendance API")
st.markdown("The Attendance API allows you effortlessly retrieve and update the course session attendance "
            "of your trainees who are enrolled into your courses!")
st.info("**Course Session Attendance returns *encrypted responses* while the Upload Course Session Attendance "
        "requires encrypted *request payloads*!**", icon="ℹ️")

view, upload = st.tabs(
    ["Course Session Attendance", "Upload Course Session Attendance"])

with view:
    st.header("Course Session Attendance")
    st.markdown("You can use this API to view the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if "uen" not in st.session_state or st.session_state["uen"] is None:
        st.warning("**Course Session Attendance API requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    crn = st.text_input(f"\* Key in the Course Reference Number (Sample data: {TestData.COURSE_REFERENCE_NUMBER.value})",
                        value=TestData.COURSE_REFERENCE_NUMBER.value,
                        key="crn-view-sessions")
    runs = st.text_input(f"\* Enter Course Run ID (Sample data: {TestData.COURSE_RUN_NUMBER.value})",
                         value=TestData.COURSE_RUN_NUMBER.value,
                         help="You will get this value after you add a couse run.\n\n"
                              "The Course Run ID is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-view-attendance")
    session_id = st.text_input(f"\* Enter Session ID (Sample data: {TestData.COURSE_SESSION_NUMBER.value})",
                               value=TestData.COURSE_SESSION_NUMBER.value,
                               help="You can get this using the \"View Course Sessions\" API after adding a couse run.\n\n"
                                    "This field specifies the course session ID to be retrieved; encode this parameter to ensure that "
                                    "special characters will not be blocked by the Gateway",
                               key="session-id-view-attendance")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view_course_session_attendance_button", type="primary"):
        LOGGER.info(
            "Attempting to send request to Retrieve Course Session Attendance API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error(
                "Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error(
                "Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif len(runs) == 0:
            LOGGER.error("Missing Course Run ID, request aborted!")
            st.error(
                "Make sure to specify your **Course Run ID** before proceeding!", icon="🚨")
        elif len(crn) == 0:
            LOGGER.error("Missing Course Reference Number, request aborted!")
            st.error(
                "Make sure to specify your **Course Reference Number** before proceeding!", icon="🚨")
        elif len(session_id) == 0:
            LOGGER.error("Missing Session ID, request aborted!")
            st.error(
                "Make sure to specify your **Session ID** before proceeding!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")



        else:
            request, response = st.tabs(["Request", "Response"])
            vc = CourseSessionAttendance(runs, crn, session_id)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(vc)

            with response:
                LOGGER.info("Executing request with defaults...")
                handle_response(lambda: vc.execute(Secrets.get_cert(),
                                                    Secrets.get_private_key()),
                                Secrets.get_encryption_key())


with upload:
    st.header("Upload Course Session Attendance")
    st.markdown("You can use this API to update the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if "uen" not in st.session_state or st.session_state["uen"] is None:
        st.warning("**Upload Course Session Attendance API requires your UEN to proceed. Make sure that you have "
                   "loaded it up properly under the Home page before proceeding!**", icon="⚠️")

    uploadAttendance = UploadAttendanceInfo()

    uploadAttendance.referenceNumber = st.text_input(label=f"\* Key in the Course Reference Number (Sample data: {TestData.COURSE_REFERENCE_NUMBER.value})",
                                                     value=TestData.COURSE_REFERENCE_NUMBER.value,
                                                     key="crn-upload-attendance-sessions")
    runs = st.text_input(label=f"\* Enter Course Run ID (Sample data: {TestData.COURSE_RUN_NUMBER.value})",
                         value=TestData.COURSE_RUN_NUMBER.value,
                         help="You will get this value after you add a couse run.\n\n"
                              "The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-upload-attendance")
    uploadAttendance.corppassId = st.text_input(label=f"\* Key in your CorpPass Number (Sample data: {TestData.CORPPASS.value})",
                                                value=TestData.CORPPASS.value,
                                                key="corppass-upload-attendance-sessions")
    uploadAttendance.sessionId = st.text_input(label=f"\* Enter Session ID (Sample data: {TestData.COURSE_SESSION_NUMBER.value})",
                                               value=TestData.COURSE_SESSION_NUMBER.value,
                                               help="You can get this using the \"View Course Sessions\" API after adding a couse run.\n\n"
                                                    "The course session ID to be retrieved; encode this parameter "
                                                    "to ensure that special characters will not be blocked by the "
                                                    "Gateway",
                                               key="session_id_upload_attendance")

    st.subheader("Attendance Information")
    uploadAttendance.status_code = st.selectbox(label="Enter the Attendance Status Code",
                                                options=Attendance,
                                                format_func=str,
                                                key="attendance-status-code-upload-attendance")

    st.subheader("Trainee Information")
    col1, col2 = st.columns(2)

    with col1:
        uploadAttendance.trainee_id_type = st.selectbox(label="Enter Trainee ID Type",
                                                        options=IdType,
                                                        format_func=str,
                                                        key="trainee-id-type-upload-attendance")

    with col2:
        uploadAttendance.trainee_id = st.text_input(label=f"\* Enter Trainee ID (Sample data: {TestData.TRAINEE_ID.value})",
                                                    value=TestData.TRAINEE_ID.value,
                                                    help="The ID of the trainee",
                                                    max_chars=50,
                                                    key="trainee-id-upload-attendance")

    if (uploadAttendance.trainee_id_type != IdType.OTHERS
            or uploadAttendance.trainee_id_type != IdType.FOREIGN_PASSPORT) and len(uploadAttendance.trainee_id) \
            and not Validators.verify_nric(uploadAttendance.trainee_id):
        st.warning("**ID Number** may not be valid!", icon="⚠️")

    uploadAttendance.trainee_name = st.text_input(label=f"\* Enter Trainee Name (Sample data: {TestData.TRAINEE_NAME.value})",
                                                  value=TestData.TRAINEE_NAME.value,
                                                  help="Name of the trainee",
                                                  max_chars=66,
                                                  key="trainee-name-upload-attendance")

    if st.checkbox("Specify Trainee Email?", key="specify-trainee-email-upload-attendance"):
        uploadAttendance.trainee_email = st.text_input(label="Enter Trainee Email",
                                                       value=TestData.EMAIL.value,
                                                       help="Email of the trainee; either email or contact number is "
                                                            "necessary",
                                                       max_chars=320,
                                                       key="trainee-email-upload-attendance")

        if len(uploadAttendance.trainee_email) > 0 and not Validators.verify_email(uploadAttendance.trainee_email):
            st.warning("Email format is not valid!", icon="⚠️")

    uploadAttendance.contactNumber_mobile = st.text_input(label="\* Enter Mobile Number of Trainee",
                                                          value=TestData.PHONE.value,
                                                          max_chars=15,
                                                          key="contact-number-mobile-upload-attendance")

    if st.checkbox("Specify Contact Number Area Code?", key="specify-areacode-upload-attendance"):
        uploadAttendance.contactNumber_areacode = st.number_input(label="Enter Mobile Number Area Code",
                                                                  min_value=0,
                                                                  max_value=99999,
                                                                  value=0)

    uploadAttendance.contactNumber_countryCode = st.number_input(label="Enter Mobile Number Country Code",
                                                                 value=TestData.COUNTRYCODE_INT.value,
                                                                 min_value=0,
                                                                 max_value=999)

    st.subheader("Course Information")
    uploadAttendance.numberOfHours = st.number_input(label="Enter number of hours",
                                                     min_value=0.5,
                                                     max_value=8.0,
                                                     step=0.1)

    uploadAttendance.surveyLanguage_code = st.selectbox(
        label="Enter Survey Language",
        options=SurveyLanguage,
        format_func=str,
        key="language-upload-attendance")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(uploadAttendance.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="upload_course_session_attendance_button", type="primary"):
        LOGGER.info(
            "Attempting to send request to Upload Course Session Attendance API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error(
                "Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error(
                "Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif not runs:
            LOGGER.error("Missing Course Run ID, request aborted!")
            st.error(
                "Make sure to fill in your **Course Run ID** before proceeding!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")



        else:
            errors, warnings = uploadAttendance.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                uca = UploadCourseSessionAttendance(runs, uploadAttendance)

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(uca, Secrets.get_encryption_key())

                with response:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: uca.execute(Secrets.get_encryption_key(),
                                                        Secrets.get_cert(),
                                                        Secrets.get_private_key()))
