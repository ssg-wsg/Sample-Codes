import streamlit as st

from revamped_application.core.attendance.course_session_attendance import CourseSessionAttendance
from revamped_application.core.attendance.upload_course_session_attendance import UploadCourseSessionAttendance
from revamped_application.core.models.attendance import UploadAttendanceInfo

from revamped_application.utils.http_utils import handle_error
from revamped_application.utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Attendance", page_icon="✅")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("Attendance API")
st.markdown("The Attendance API allows you effortlessly retrieve and update the course session attendance "
            "of your trainees who are enrolled into your courses!")
st.info("**This API requires your requests and data to be encrypted!**")

view, upload = st.tabs(["Course Session Attendance", "Upload Course Session Attendance"])

with view:
    st.header("Course Session Attendance")
    st.markdown("You can use this API to view the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")
    st.warning("**Course Session Attendance API requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-attendance")
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
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        elif len(runs) == 0:
            st.error("Make sure to specify your Course Run ID before proceeding!")
        elif len(crn) == 0:
            st.error("Make sure to specify your Course Reference Number before proceeding!")
        elif len(session_id) == 0:
            st.error("Make sure to specify your Session ID before proceeding!")
        else:
            request, response = st.tabs(["Request", "Response"])

            vc = CourseSessionAttendance(runs, crn, session_id, include_expired)

            with request:
                st.subheader("Request")
                st.code(repr(vc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: vc.execute())

with upload:
    st.header("Upload Course Session Attendance")
    st.markdown("You can use this API to update the attendance of the trainees who are enrolled into your course for "
                "a particular course session.")
    st.warning("**Upload Course Session Attendance API requires your UEN to proceed. Make sure that you have "
               "loaded it up properly under the Home page before proceeding!**")

    uploadAttendance = UploadAttendanceInfo()

    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-upload-attendance")
    uploadAttendance.set_referenceNumber(st.text_input(label="Key in the Course Reference Number",
                                                       key="crn-upload-attendance-sessions"))
    uploadAttendance.set_corppassId(st.text_input(label="Key in your Corppass Number",
                                                  key="corppass-upload-attendance-sessions"))
    uploadAttendance.set_sessionId(st.text_input(label="Enter Session ID",
                                                 help="The course session ID to be retrieved; encode this parameter "
                                                      "to ensure that special characters will not be blocked by the "
                                                      "Gateway",
                                                 key="session_id_upload_attendance"))

    st.subheader("Attendance Information")
    uploadAttendance.set_statusCode(st.selectbox(label="Enter the Attendance Status Code",
                                                 options=["1", "2", "3", "4"],
                                                 format_func=lambda x: UploadAttendanceInfo.ATTENDANCE_CODE_MAPPINGS[x],
                                                 key="attendance-status-code-upload-attendance"))

    st.subheader("Trainee Information")
    uploadAttendance.set_trainee_id(st.text_input(label="Enter Trainee ID",
                                                  help="The ID of the trainee",
                                                  max_chars=100,
                                                  key="trainee-id-upload-attendance"))
    uploadAttendance.set_trainee_name(st.text_input(label="Enter Trainee Name",
                                                    help="Name of the trainee",
                                                    max_chars=66,
                                                    key="trainee-name-upload-attendance"))

    if st.checkbox("Specify Trainee Email?", key="specify-trainee-email-upload-attendance"):
        uploadAttendance.set_trainee_email(st.text_input(label="Enter Trainee Email",
                                                         help="Email of the trainee; either email or contact number is "
                                                              "necessary",
                                                         max_chars=320,
                                                         key="trainee-email-upload-attendance"))
    uploadAttendance.set_trainee_id_type(st.selectbox(label="Enter Trainee ID Type",
                                                      options=UploadAttendanceInfo.ID_TYPE_MAPPINGS.keys(),
                                                      format_func=lambda x: UploadAttendanceInfo.ID_TYPE_MAPPINGS[x],
                                                      key="trainee-id-type-upload-attendance"))
    uploadAttendance.set_contactNumber_mobile(st.text_input(label="Enter Mobile Number of Trainee",
                                                            max_chars=15,
                                                            key="contact-number-mobile-upload-attendance"))

    if st.checkbox("Specify Contact Number Area Code?", key="specify-areacode-upload-attendance"):
        uploadAttendance.set_contactNumber_areacode(st.number_input(label="Enter Mobile Number Area Code",
                                                                    min_value=0,
                                                                    max_value=99999,
                                                                    value=0))

    uploadAttendance.set_contactNumber_countryCode(st.number_input(label="Enter Mobile Number Country Code",
                                                                   min_value=0,
                                                                   max_value=999,
                                                                   value=65))

    st.subheader("Course Information")
    if st.checkbox("Specify number of hours?", key="hours-upload-attendance"):
        uploadAttendance.set_numberOfHours(st.number_input(label="Enter number of hours",
                                                           min_value=0.5,
                                                           max_value=8.0,
                                                           step=0.1))

    uploadAttendance.set_surveyLanguage_code(st.selectbox(
        label="Enter Survey Language",
        options=UploadAttendanceInfo.SURVEY_LANGUAGE_MAPPINGS.keys(),
        format_func=lambda x: UploadAttendanceInfo.SURVEY_LANGUAGE_MAPPINGS[x],
        key="language-upload-attendance"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(uploadAttendance.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="upload_course_session_attendance_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        elif not runs:
            st.error("Make sure to fill in your Course Run ID before proceeding!")
        else:
            errors = uploadAttendance.validate()

            if errors is not None:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors)
                )
            else:
                request, response = st.tabs(["Request", "Response"])

                uca = UploadCourseSessionAttendance(runs, uploadAttendance)

                with request:
                    st.subheader("Request")
                    st.code(repr(uca), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: uca.execute())
