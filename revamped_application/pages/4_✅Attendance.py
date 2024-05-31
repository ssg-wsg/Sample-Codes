import streamlit as st

from core.attendance.course_session_attendance import CourseSessionAttendance
from core.attendance.upload_course_session_attendance import UploadCourseSessionAttendance
from core.models.attendance import UploadAttendanceInfo
from core.constants import ATTENDANCE_CODE_MAPPINGS, ID_TYPE_MAPPING, SURVEY_LANGUAGE_MAPPINGS, Endpoints
from utils.http_utils import handle_error, handle_request
from utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Attendance", page_icon="✅")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("Attendance API")
st.markdown("The Attendance API allows you effortlessly retrieve and update the course session attendance "
            "of your trainees who are enrolled into your courses!")
st.info("**Retrieve Course Session Attendance API returns *encrypted responses*!**\n\n"
        "**Upload Course Session Attendance API requires your *requests* to be encrypted!**", icon="ℹ️")

view, upload = st.tabs(["Course Session Attendance", "Upload Course Session Attendance"])

with view:
    st.header("Retrieve Course Session Attendance")
    st.markdown("You can use this API to view the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if st.session_state["uen"] is None:
        st.warning("**Course Session Attendance API requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    runs = st.number_input(label="Enter Course Run ID",
                           help="The Course Run Id is used as a parameter for GET Request Call"
                                "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                           value=0,
                           key="course-run-id-view-attendance")
    crn = st.text_input(label="Key in the Course Reference Number",
                        help="Course Reference Number; encode the course reference number as it may contains "
                             "some special characters which could be blocked by the Gateway",
                        key="crn_view_sessions")
    session_id = st.text_input("Enter Session ID",
                               help="The course session ID to be retrieved; encode this parameter to ensure that "
                                    "special characters will not be blocked by the Gateway",
                               key="session_id_view_attendance")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="view_course_session_attendance_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif len(crn) == 0:
            st.error("Make sure to specify your **Course Reference Number** before proceeding!", icon="🚨")
        elif len(session_id) == 0:
            st.error("Make sure to specify your **Session ID** before proceeding!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = CourseSessionAttendance(runs, crn, session_id)

            with request:
                handle_request(vc)

            with response:
                handle_error(lambda: vc.execute(), require_decryption=True)

with upload:
    st.header("Upload Course Session Attendance")
    st.markdown("You can use this API to update the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")

    if st.session_state["uen"] is None:
        st.warning("**Upload Course Session Attendance API requires your UEN to proceed. Make sure that you have "
                   "loaded it up properly under the Home page before proceeding!**", icon="⚠️")

    uploadAttendance = UploadAttendanceInfo()

    runs = st.number_input(label="Enter Course Run ID",
                           help="The Course Run Id is used as a parameter for POST Request Call"
                                "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                           value=0,
                           key="course-run-id-upload-attendance")
    uploadAttendance.set_referenceNumber(st.text_input(label="Key in the Course Reference Number",
                                                       key="crn-upload-attendance-sessions"))
    uploadAttendance.set_corppassId(st.text_input(label="Key in your CorpPass Number",
                                                  key="corppass-upload-attendance-sessions"))
    uploadAttendance.set_sessionId(st.text_input(label="Enter Session ID",
                                                 help="The course session ID to be retrieved; encode this parameter "
                                                      "to ensure that special characters will not be blocked by the "
                                                      "Gateway",
                                                 key="session_id_upload_attendance"))

    st.subheader("Attendance Information")
    uploadAttendance.set_statusCode(st.selectbox(label="Enter the Attendance Status Code",
                                                 help="Attendance taken status code",
                                                 options=ATTENDANCE_CODE_MAPPINGS.keys(),
                                                 format_func=lambda x: f"{x}: {ATTENDANCE_CODE_MAPPINGS[x]}",
                                                 key="attendance-status-code-upload-attendance"))

    st.subheader("Trainee Information")
    col1, col2 = st.columns(2)
    uploadAttendance.set_trainee_id_type(col1.selectbox(label="Enter Trainee ID Type",
                                                        help="Trainee ID type code",
                                                        options=ID_TYPE_MAPPING.keys(),
                                                        format_func=lambda x: f"{x}: {ID_TYPE_MAPPING[x]}",
                                                        key="trainee-id-type-upload-attendance"))

    uploadAttendance.set_trainee_id(col2.text_input(label="Enter Trainee ID",
                                                    help="The ID of the trainee",
                                                    max_chars=100,
                                                    key="trainee-id-upload-attendance"))

    uploadAttendance.set_trainee_name(st.text_input(label="Enter Trainee Name",
                                                    help="Name of the trainee",
                                                    max_chars=66,
                                                    key="trainee-name-upload-attendance"))

    if st.checkbox("Specify Trainee Email?", key="specify-trainee-email-upload-attendance",
                   help="Either email address or contact number is mandatory"):
        uploadAttendance.set_trainee_email(st.text_input(label="Enter Trainee Email",
                                                         help="Email of the trainee; either email or contact number is "
                                                              "necessary",
                                                         max_chars=320,
                                                         key="trainee-email-upload-attendance"))

    col3, col4, col5 = st.columns(3)
    if col3.checkbox("Specify Contact Number Area Code?", key="specify-areacode-upload-attendance"):
        uploadAttendance.set_contactNumber_areacode(col3.number_input(label="Enter Mobile Number Area Code",
                                                                      help="Can leave as `null` if there no area code.",
                                                                      min_value=0,
                                                                      max_value=99999,
                                                                      value=0))

    uploadAttendance.set_contactNumber_countryCode(col4.number_input(label="Enter Mobile Number Country Code",
                                                                     min_value=0,
                                                                     max_value=999,
                                                                     value=65))

    uploadAttendance.set_contactNumber_mobile(col5.text_input(label="Enter Mobile Number of Trainee",
                                                              max_chars=15,
                                                              help="Either email address or contact number is "
                                                                   "mandatory",
                                                              key="contact-number-mobile-upload-attendance"))

    st.subheader("Course Information")
    if st.checkbox("Specify number of hours?", key="hours-upload-attendance",
                   help="No. of Hours or duration on the session attended. "
                        "If the attendance is recorded for a 'On-the-Job' training session, then this field is "
                        "mandatory!"):
        uploadAttendance.set_numberOfHours(st.number_input(label="Enter number of hours",
                                                           min_value=0.5,
                                                           max_value=8.0,
                                                           value=0.5,
                                                           step=0.1))

    uploadAttendance.set_surveyLanguage_code(st.selectbox(
        label="Enter Survey Language",
        options=SURVEY_LANGUAGE_MAPPINGS.keys(),
        format_func=lambda x: SURVEY_LANGUAGE_MAPPINGS[x],
        help="Survey Language code",
        key="language-upload-attendance"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(uploadAttendance.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="upload_course_session_attendance_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!", icon="🚨")
        else:
            errors, warnings = uploadAttendance.validate()

            if len(warnings) > 0:
                st.warning(
                    "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(errors), icon="⚠️"
                )

            if len(errors) > 0:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
                )
            else:
                request, response = st.tabs(["Request", "Response"])
                uca = UploadCourseSessionAttendance(runs, uploadAttendance)

                with request:
                    handle_request(uca, require_encryption=True)

                with response:
                    handle_error(lambda: uca.execute())
