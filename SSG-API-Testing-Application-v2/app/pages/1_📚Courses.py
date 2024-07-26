"""
This page is used to enable access to the Courses API.

There are 4 main processes:
1. View Course Run
    - This tab allows you to enter a Course Run ID and retrieve course run information from the API
2. Add Course Run
    - This tab allows you to create/publish one or more course runs with sessions
3. Edit/Delete Course Run
    - This tab allows you to edit or delete your existing course runs.
4. View Course Sessions
    - This tab allows you to enter a Course Reference ID and a corresponding Course Run ID to retrieve
      course session information from the API

It is important to note that optional fields are always hidden behind a Streamlit checkbox to allow the backend
functions to clean up the request body and send requests that contains only non-null fields.
"""

import streamlit as st

from datetime import datetime, date

from app.core.courses.delete_course_run import DeleteCourseRun
from app.core.courses.view_course_run import ViewCourseRun
from app.core.courses.edit_course_run import EditCourseRun
from app.core.courses.add_course_run import AddCourseRun
from app.core.courses.view_course_sessions import ViewCourseSessions
from app.core.models.course_runs import (EditRunInfo, RunSessionEditInfo, RunTrainerEditInfo,
                                         DeleteRunInfo, AddRunInfo, RunSessionAddInfo,
                                         RunTrainerAddInfo, AddRunIndividualInfo,
                                         LinkedSSECEQA)
from app.core.constants import Month, Vacancy, ModeOfTraining, IdType, Salutations, Role, \
    OptionalSelector, TrainerType
from app.core.system.logger import Logger
from app.utils.http_utils import handle_response, handle_request
from app.utils.streamlit_utils import (init, display_config,
                                       validation_error_handler, does_not_have_keys)
from app.utils.verify import Validators

# initialise necessary variables
init()
LOGGER = Logger("Courses API")

st.set_page_config(page_title="Courses", page_icon="📚")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")

    if st.button("Configs", key="config_display", type="primary"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Courses API")
st.markdown("The Courses API allows you to search, filter and compare different SkillsFuture Credit "
            "eligible courses that have been published on the MySkillsFuture portal! Through this "
            "API you can access details regarding course categories, related courses, popular "
            "courses, featured courses, course brochures, and more! You can also manage your webhook "
            "events and subscriptions via this API!")

st.info(
    "**Add Course Runs and Edit/Delete Course Runs requires your *request payloads* to be encrypted!**\n\n"
    "**View Course Runs and View Course Sessions do not require any encryption!**",
    icon="ℹ️"
)

view, add, edit_delete, sessions = st.tabs([
    "View Course Runs", "Add Course Runs", "Edit/Delete Course Runs", "View Course Sessions"
])

with view:
    st.header("View Course Runs")
    st.markdown("You can retrieve your course run details based on course reference number and course run ID using "
                "this API.")

    st.subheader("Request Parameters")
    include_expired = st.selectbox(label="Include expired courses?",
                                   options=OptionalSelector,
                                   format_func=lambda x: str(x),
                                   help="Indicate whether retrieve expired course or not",
                                   key="view-expired")
    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a parameter for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="view-course-run-id")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-button", type="primary"):
        LOGGER.info("Attempting to send request to View Course Run API...")

        if "url" not in st.session_state or st.session_state["url"] is None:
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif len(runs) == 0:
            LOGGER.error("Missing Course Run ID!")
            st.error("Key in your **Course Run ID** to proceed!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = ViewCourseRun(runs, include_expired)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(vc)

            with response:
                LOGGER.info("Executing request...")
                handle_response(lambda: vc.execute())


with add:
    st.header("Add Course Runs")
    st.markdown("You can use this API to add/publish one or more course runs with sessions.")

    if st.session_state["uen"] is None:
        st.warning("**Add Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    # ===== BASIC RUN INFO ===== #
    st.subheader("`run` details")
    st.markdown("Note that `registrationDates`, `courseDates`, `scheduleInfoType`, `scheduleInfo`, "
                "`courseVacancy`, `modeOfTraining` and `courseAdminEmail` are required for this **add** action!")

    # create a store for the parameters to pass into the backend
    add_runinfo = AddRunInfo()
    include_expired = st.selectbox(label="Include expired courses?",
                                   options=OptionalSelector,
                                   format_func=lambda x: str(x),
                                   help="Indicate whether retrieve expired course or not",
                                   key="add-view-expired")
    add_runinfo.crid = st.text_input(label="Key in the Course Reference Number",
                                     help="Reference number for the course of interest. "
                                          "Encode the course reference number as it may contains "
                                          "some special characters which could be blocked by the Gateway",
                                     placeholder="XX-10000000K-01-TEST 166",
                                     key="add-crn")

    st.subheader("Define Number of Runs to Add")
    num_runs = st.number_input(label="Enter in the number of runs of a course to add",
                               min_value=0,
                               value=1,
                               key="add-num-runs")

    for run in range(num_runs):
        with st.expander(f"Run {run + 1}", expanded=True if run == 0 else False):
            indiv_run = AddRunIndividualInfo()

            st.subheader(f"Run {run + 1}")
            st.info(f"Sequence number is automatically set to {run}!", icon="ℹ️")
            indiv_run.sequence_number = run

            st.markdown("#### Registration Dates")
            col1, col2 = st.columns(2)

            with col1:
                indiv_run.opening_registration_date = st.date_input(
                    label="Opening Date",
                    key=f"add-opening-date-{run}",
                    min_value=date(1900, 1, 1),
                    help="Course run registration opening date as YYYYMMDD format (timezone - UTC+08:00)")

            with col2:
                indiv_run.closing_registration_date = st.date_input(
                    label="Closing Date",
                    key=f"add-closing-date-{run}",
                    min_value=date(1900, 1, 1),
                    help="Course run registration closing date as YYYYMMDD format (timezone - UTC+08:00)")

            st.markdown("#### Course Dates")
            col1, col2 = st.columns(2)

            with col1:
                indiv_run.course_start_date = st.date_input(label="Course Start Date",
                                                            key=f"add-start-date-{run}",
                                                            min_value=date(1900, 1, 1),
                                                            help="Course run start opening dates as YYYYMMDD format "
                                                                 "(timezone - UTC+08:00))")

            with col2:
                indiv_run.course_end_date = st.date_input(label="Course End Date",
                                                          key=f"add-end-date-{run}",
                                                          min_value=date(1900, 1, 1),
                                                          help="Course run end opening dates as YYYYMMDD format "
                                                               "(timezone - UTC+08:00))")

            st.markdown("#### Schedule Info Type")
            indiv_run.schedule_info_type_code = st.text_input(label="Schedule Code",
                                                              key=f"add-schedule-code-{run}",
                                                              help="Course run schedule info code",
                                                              placeholder="01",
                                                              max_chars=2)
            indiv_run.schedule_info_type_description = st.text_area(label="Schedule Description",
                                                                    key=f"add-schedule-description-{run}",
                                                                    help="Course run schedule info description",
                                                                    placeholder="Description",
                                                                    max_chars=32)

            indiv_run.schedule_info = st.text_input(label="Schedule Info",
                                                    key=f"add-schedule-info-{run}",
                                                    help="Course run schedule info",
                                                    placeholder="Sat / 5 Sats / 9am - 6pm",
                                                    max_chars=300)

            st.markdown("#### Venue Info")
            if st.checkbox("Specify Venue Block?", key=f"specify-add-venue-block-info-{run}"):
                indiv_run.block = st.text_input(label="Block",
                                                key=f"add-venue-block-{run}",
                                                help="Course run block",
                                                max_chars=10)

            if st.checkbox("Specify Venue Street?", key=f"specify-add-venue-street-info-{run}"):
                indiv_run.street = st.text_input(label="Street",
                                                 key=f"add-venue-street-{run}",
                                                 help="Course run street",
                                                 max_chars=32)

            if st.checkbox("Specify Venue Building?", key=f"specify-add-venue-building-info-{run}"):
                indiv_run.building = st.text_input(label="Building",
                                                   key=f"add-venue-building-{run}",
                                                   help="Course run building",
                                                   max_chars=66)

            if st.checkbox("Specify Wheelchair Accessible?", key=f"specify-add-wheelchair-accessible-info-{run}"):
                indiv_run.wheel_chair_access = st.selectbox(label="Wheelchair Access",
                                                            options=OptionalSelector,
                                                            format_func=lambda x: str(x),
                                                            key=f"add-venue-wheelchair-accessible-{run}",
                                                            help="Indication that the course run location is "
                                                                 "wheelchair accessible")

            indiv_run.floor = st.text_input(label="Floor",
                                            key=f"add-venue-floor-{run}",
                                            help="Course run floor",
                                            max_chars=3)
            indiv_run.unit = st.text_input(label="Unit",
                                           key=f"add-venue-unit-{run}",
                                           help="Course run unit",
                                           max_chars=5)
            indiv_run.postal_code = st.text_input(label="Postal Code",
                                                  key=f"add-venue-postal-code-{run}",
                                                  help="Course run postal code",
                                                  max_chars=6)
            indiv_run.room = st.text_input(label="Room",
                                           key=f"add-venue-room-{run}",
                                           help="Course run room",
                                           max_chars=255)

            st.markdown("#### Course Intake Details")
            if st.checkbox("Specify Intake Size?", key=f"specify-add-intake-size-info-{run}"):
                indiv_run.intake_size = st.number_input(
                    label="Intake Size",
                    key=f"add-intake-size-{run}",
                    value=0,
                    min_value=0,
                    help="Course run intake size. It represents the max number of pax for a class")

            if st.checkbox("Specify Intake Threshold?", key=f"specify-add-intake-threshold-info-{run}"):
                indiv_run.threshold = st.number_input(
                    label="Threshold",
                    key=f"add-intake-threshold-{run}",
                    value=0,
                    min_value=0,
                    help="Course run threshold. Any additional pax that can register above maximum pax.\n"
                         "e.g. threshold = `10`, then total allowed registration pax is `intake size + "
                         "threshold = 60`")

            if st.checkbox("Specify Registered User Count?", key=f"specify-add-registered-user-count-info-{run}"):
                indiv_run.registered_user_count = st.number_input(
                    label="Registered Users Count",
                    key=f"add-registered-user-count-{run}",
                    value=0,
                    min_value=0,
                    help="Course run registered user count. This number cannot be more than `intake size + threshold`")

            st.markdown("#### Course Admin Details")
            indiv_run.mode_of_training = st.selectbox(label="Mode of Training",
                                                      key=f"add-mode-of-training-{run}",
                                                      help="Mode of training code",
                                                      options=ModeOfTraining,
                                                      format_func=lambda x: str(x))
            indiv_run.course_admin_email = st.text_input(
                label="Course Admin Email",
                key=f"add-course-admin-email-{run}",
                help="Course admin email is under course run level that can receive the email from 'QR code "
                     "Attendance Taking', 'Course Attendance with error' and 'Trainer information not updated'",
                max_chars=255)

            if len(indiv_run.course_admin_email) > 0:
                if not Validators.verify_email(indiv_run.course_admin_email):
                    st.warning(f"Email format is not valid!", icon="⚠️")

            st.markdown("#### Course Vacancy Details")
            indiv_run.course_vacancy = st.selectbox(label="Course Vacancy",
                                                    key=f"add-course-vacancy-{run}",
                                                    options=Vacancy,
                                                    format_func=lambda x: str(x),
                                                    help="Course run vacancy status")

            st.markdown("#### File Details")
            if st.checkbox("Specify File Name?", key=f"specify-add-file-Name-info-{run}"):
                indiv_run.file_name = st.text_input(label="File Name",
                                                    key=f"add-file-name-{run}",
                                                    help="Physical file name of the course run",
                                                    max_chars=255)

            if st.checkbox("Specify File Content?", key=f"specify-add-file-content-info{run}"):
                indiv_run.file_content = st.file_uploader(label="File Content",
                                                          key=f"add-file-content-{run}",
                                                          help="File content of the course run in binary",
                                                          accept_multiple_files=False)

            # ===== RUN SESSION INFO ===== #
            st.divider()
            st.subheader("Add `session` details")
            st.markdown("Fill in the course session information here.\n\n"
                        "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `endDate` "
                        "will be based on the user input. For `modeOfTraining` other than `2` or `4`, course session "
                        "`endDate` will be set the same as `startDate`.\n\n"
                        "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session "
                        "`startTime` & `endTime` will be default as from 12:00AM to 11.59PM. For `modeOfTraining` "
                        "other than `2` or `4`, course session `startTime` & `endTime` will be based on user input."
                        )

            num_sessions: int = st.number_input(label="Key in the number of sessions in the Course Run",
                                                key=f"add-num-session-{run}",
                                                min_value=0,
                                                value=0)

            if num_sessions > 0:
                st.divider()

            for i in range(num_sessions):
                with st.expander(f"Session {i + 1}", expanded=True if i == 0 else False):
                    runsession: RunSessionAddInfo = RunSessionAddInfo()

                    st.markdown(f"##### Session {i + 1}")
                    runsession.mode_of_training = st.selectbox(
                        label="Mode of Training",
                        options=ModeOfTraining,
                        help="Mode of training code",
                        format_func=lambda x: str(x),
                        key=f"add-session-mode-of-training_{i}-{run}")

                    col1, col2 = st.columns(2)
                    with col1:
                        runsession.start_date = st.date_input(label="Start date of course session",
                                                              help="Start date of course session "
                                                                   "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                              min_value=date(1900, 1, 1),
                                                              key=f"add-session-start-date-{i}-{run}")

                    if runsession.is_asynchronous_or_on_the_job():
                        with col1:
                            runsession.start_time = st.time_input(label="Start time of course session",
                                                                  key=f"add-session-start-time-{i}-{run}",
                                                                  help="Start time of course session"
                                                                       "(**HH:mm:ss/HH:mm format only**)",
                                                                  disabled=True,
                                                                  value=datetime(
                                                                      hour=0,
                                                                      minute=0,
                                                                      year=runsession.get_start_date_year(),
                                                                      month=runsession.get_start_date_month(),
                                                                      day=runsession.get_start_date_day())
                                                                  .time())

                        with col2:
                            runsession.end_date = st.date_input(label="End date of course session",
                                                                key=f"add-session-end-date-{i}-{run}",
                                                                min_value=date(1900, 1, 1),
                                                                help="End date of course session "
                                                                     "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                value=runsession.get_start_date(),
                                                                disabled=True)
                            runsession.end_time = st.time_input(label="End time of course session",
                                                                key=f"add-session-end-time-{i}-{run}",
                                                                help="End time of course session"
                                                                     "(**HH:mm:ss/HH:mm format only**)",
                                                                disabled=True,
                                                                value=datetime(hour=23,
                                                                               minute=59,
                                                                               year=runsession.get_start_date_year(),
                                                                               month=runsession.get_start_date_month(),
                                                                               day=runsession.get_start_date_day())
                                                                .time())

                        st.info(f"End date of course session is automatically set to "
                                f"**{runsession.get_start_date()}**\n\nStart and end time set to "
                                f"**12:00 AM to 11:59 PM** respectively", icon="ℹ️")
                    else:
                        with col1:
                            runsession.start_time = st.time_input("Start time of course session",
                                                                  help="Start time of course session"
                                                                       "(**HH:mm:ss/HH:mm format only**)",
                                                                  key=f"add-session-start-time-{i}-{run}")

                        with col2:
                            runsession.end_date = st.date_input(label="End date of course session",
                                                                min_value=date(1900, 1, 1),
                                                                help="End date of course session "
                                                                     "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                key=f"add-session-end-date-{i}-{run}")
                            runsession.end_time = st.time_input("End time of course session",
                                                                help="End time of course session"
                                                                     "(**HH:mm:ss/HH:mm format only**)",
                                                                key=f"add-session-end-time-{i}-{run}")

                    st.markdown(f"###### Venue")
                    if st.checkbox("Specify Venue Block?", key=f"specify-add-session-venue-block-{i}-{run}"):
                        runsession.block = st.text_input(label="Block",
                                                         key=f"add-session-venue-block-{i}-{run}",
                                                         help="Course run block",
                                                         max_chars=10)

                    if st.checkbox("Specify Venue Street", key=f"specify-add-session-venue-street-{i}-{run}"):
                        runsession.street = st.text_input(label="Street",
                                                          key=f"add-session-venue-street-{i}-{run}",
                                                          help="Course run street",
                                                          max_chars=32)

                    if st.checkbox("Specify Venue Building", key=f"specify-add-session-venue-building-{i}-{run}"):
                        runsession.building = st.text_input(label="Building",
                                                            key=f"add-session-venue-building-{i}-{run}",
                                                            help="Course run building",
                                                            max_chars=66)

                    if st.checkbox("Specify Venue Wheelchair Accessible?",
                                   key=f"specify-add-session-venue-wheelchair-{i}-{run}"):
                        runsession.wheel_chair_access = st.selectbox(
                            label="Wheelchair Access",
                            options=OptionalSelector,
                            format_func=lambda x: str(x),
                            key=f"add-session-venue-wheelchair-{i}-{run}",
                            help="Indication that the course run location is wheelchair accessible")

                    if st.checkbox("Specify Primary Venue?", key=f"specify-add-session-primary-venue-{i}-{run}"):
                        runsession.primary_venue = st.selectbox(
                            label="Primary Venue",
                            options=OptionalSelector,
                            format_func=lambda x: str(x),
                            help="Indication that the course session is the Primary Venue. If `Yes`, "
                                 "API will pick the venue information from course run and update to session venue",
                            key=f"add-session-venue-primary-venue-{i}-{run}")

                    runsession.floor = st.text_input(label="Floor",
                                                     key=f"add-session-floor-{i}-{run}",
                                                     help="Course run floor",
                                                     max_chars=3)
                    runsession.unit = st.text_input(label="Unit",
                                                    key=f"add-session-venue-unit-{i}-{run}",
                                                    help="Course run unit",
                                                    max_chars=5)
                    runsession.postal_code = st.text_input(label="Postal Code",
                                                           key=f"add-session-venue-postal-code-{i}-{run}",
                                                           help="Course run postal code",
                                                           max_chars=6)
                    runsession.room = st.text_input(label="Room",
                                                    key=f"add-session-venue-room-{i}-{run}",
                                                    help="Course run room",
                                                    max_chars=255)

                    indiv_run.add_session(runsession)

            # ===== RUN TRAINERS INFO ===== #
            st.subheader("Add `trainer` details")
            st.markdown(
                "If the Trainer type is `1 - Existing`, fill up only the Trainer ID field, and leave the rest empty. "
                "The API will retrieve the details from the TP Profile - Trainer Salutation, Key Domain / "
                "Sector Areas of Practice, Qualification Level, Qualification Description and Experience. The input "
                "details will not be updated to the Trainer profile.\n")
            st.markdown(
                "If the Trainer type is `2 - New`, please fill in all required details. If `inTraningProviderProfile` "
                "is set to `true`, the new added Trainer will be saved into Trainer profile as well as linked to "
                "this specific course run; otherwise this trainer is linked ot this specific course run only.")

            num_trainers: int = st.number_input(label="Key in the number of trainers in the Course Run",
                                                key=f"add-num-trainers-{run}",
                                                min_value=0,
                                                value=0)

            if num_trainers > 0:
                st.divider()

            for i in range(num_trainers):
                with st.expander(f"Trainer {i + 1}", expanded=True if i == 0 else False):
                    runtrainer = RunTrainerAddInfo()

                    st.markdown(f"##### Trainer {i + 1}")
                    code = st.selectbox(label="Trainer Type Code",
                                        options=TrainerType,
                                        format_func=lambda x: str(x),
                                        key=f"add-trainer-type-code-{i}-{run}")

                    runtrainer.trainer_type_code = code.value
                    runtrainer.trainer_type_description = code.name.title()

                    st.markdown("###### Trainer Particulars")
                    if code == TrainerType.EXISTING:
                        runtrainer.trainer_idNumber = st.text_input(label="Trainer ID Number",
                                                                    key=f"add-trainer-id-number-{i}-{run}",
                                                                    help="This refers to the NRIC/FIN/Passport "
                                                                         "number of the trainer.",
                                                                    max_chars=50)
                    elif code == TrainerType.NEW:
                        if st.checkbox("Specify Trainer Index Number",
                                       key=f"specify-add-trainer-index-number-{i}-{run}"):
                            runtrainer.index_number = st.number_input(
                                label="Trainer Index Number",
                                min_value=0,
                                value=0,
                                help="Index Number of the trainer. It is a reference for API if there is more than one "
                                     "trainer in the payload. Can leave as '0'",
                                key=f"add-trainer-index-number-{i}-{run}")

                        if st.checkbox("Specify Unique Trainer ID?",
                                       key=f"add-trainer-unique-trainer-id-{i}-{run}",
                                       help="Do not select this field if you are specifying a new Trainer!"):
                            runtrainer.trainer_id = st.text_input(label="Trainer ID",
                                                                  key=f"add-trainer-unique-id-identifier-{i}-{run}",
                                                                  help="The unique Trainer id for existing trainer. "
                                                                       "For new trainer, leave it blank.",
                                                                  max_chars=50)

                        runtrainer.trainer_name = st.text_input(label="Trainer Name",
                                                                key=f"add-trainer-name-{i}-{run}",
                                                                help="Name of the trainer",
                                                                max_chars=66)
                        runtrainer.trainer_email = st.text_input(label="Trainer Email",
                                                                 key=f"add-trainer-email-{i}-{run}",
                                                                 help="Trainer email address",
                                                                 max_chars=320)
                        if len(runtrainer.trainer_email) > 0:
                            if not Validators.verify_email(runtrainer.trainer_email):
                                st.warning(f"Email format is not valid!", icon="⚠️")

                        st.markdown("###### Trainer ID")
                        col1, col2 = st.columns(2)

                        with col1:
                            runtrainer.trainer_idType = st.selectbox(label="Trainer ID Code",
                                                                     options=IdType,
                                                                     format_func=lambda x: str(x),
                                                                     help="Trainer ID Type Code",
                                                                     key=f"add-trainer-id-code-{i}-{run}")

                        with col2:
                            runtrainer.trainer_idNumber = st.text_input(label="Trainer ID Number",
                                                                        key=f"add-trainer-id-number-{i}-{run}",
                                                                        help="This refers to the NRIC/FIN/Passport "
                                                                             "number of the trainer.",
                                                                        max_chars=50)

                            if runtrainer.trainer_idType != IdType.OTHERS and len(runtrainer.trainer_idNumber) > 0 \
                                    and not Validators.verify_nric(runtrainer.trainer_idNumber):
                                st.warning(f"**ID Number** format may not valid!", icon="⚠️")

                        st.markdown("###### Trainer Roles\n"
                                    "Select one or more of the roles below!")
                        runtrainer.trainer_roles = st.multiselect(
                            label="Select roles for the linked trainer",
                            options=Role,
                            format_func=lambda x: str(x),
                            key=f"specify-add-trainer-role-{i}"
                        )

                        st.markdown("###### Trainer Profile")
                        if st.checkbox("Specify In Training Provider Profile?",
                                       key=f"specify-add-trainer-training-provider-profile-{i}-{run}"):
                            runtrainer.inTrainingProviderProfile = st.selectbox(
                                label="Set in-training provider profile",
                                options=OptionalSelector,
                                format_func=lambda x: str(x),
                                help="This field is used to indicate whether to add the new trainer information to "
                                     "Training Provider's Profile. If the trainer is saved in TP trainers profile, "
                                     "TP can view/update the trainer in trainer maintenance page and select this "
                                     "trainer from trainers list for other course/runs. Next time when link same "
                                     "trainer in add/update course run API, need to indicate this trainer type as "
                                     "'Existing' and put in name & email.",
                                key=f"add-trainer-training-provider-profile-{i}")

                        if st.checkbox("Specify Experience?", key=f"specify-add-trainer-experience-{i}-{run}"):
                            runtrainer.experience = st.text_area(
                                label="Experience",
                                key=f"add-trainer-experience-{i}-{run}",
                                help="Trainer experience",
                                max_chars=1000
                            )

                        if st.checkbox("Specify LinkedIn URL?", key=f"specify-add-trainer-linkedin-{i}-{run}"):
                            runtrainer.linkedInURL = st.text_input(
                                label="LinkedIn URL",
                                key=f"add-trainer-linkedin-{i}-{run}",
                                help="Trainer linkedin URL (optional). For existing trainer, leave this field empty",
                                max_chars=255
                            )

                        runtrainer.domain_area_of_practice = st.text_area(
                            label="Domain Area of Practice",
                            help="This field indicates the Key Domain/Sector Areas of practice of the trainer "
                                 "(required for new trainer). For existing trainer, leave this field empty",
                            key=f"add-trainer-domain-area-{i}-{run}",
                            max_chars=1000)

                        runtrainer.salutationId = st.selectbox(
                            label="Salutations of the Trainer",
                            options=Salutations,
                            format_func=lambda x: str(x),
                            help="This field is used to enter the Salutation of the trainer (required for new "
                                 "trainer). For existing trainer, leave this field empty.",
                            key=f"add-trainer-salutation-id-code-{i}-{run}",
                        )

                        st.markdown("###### Photo")
                        if st.checkbox("Specify Photo Name?", key=f"specify-add-trainer-photo-name-{i}-{run}"):
                            runtrainer.photo_name = st.text_input(label="File Name",
                                                                  key=f"add-trainer-photo-{i}-{run}",
                                                                  help="Physical file name of the course run",
                                                                  max_chars=255)

                        if st.checkbox("Specify Photo Content?", key=f"specify-add-trainer-photo-content-{i}-{run}"):
                            runtrainer.photo_content = st.file_uploader(label="File Content",
                                                                        key=f"add-trainer-photo-content-{i}-{run}",
                                                                        help="File content of the course run encoded "
                                                                             "in base64 format",
                                                                        accept_multiple_files=False)

                        st.markdown("###### Linked SSEC EQAs")
                        st.markdown("This field used to indicate the qualification level of the trainer. For "
                                    "existing trainer, please do not input this information.")
                        linkedssec = st.number_input(label="Number of Linked SSEC EQAs",
                                                     key=f"add-trainer-linkedssec-{i}-{run}",
                                                     min_value=0,
                                                     value=0, )

                        for j in range(linkedssec):
                            # create a dict first then fill in
                            temp_ssec = LinkedSSECEQA()

                            st.markdown(f"*Linked SSEC EQA {j + 1}*")

                            if st.checkbox("Specify SSEC EQA", key=f"specify-add-trainer-linkedssec-{i}-{j}-{run}"):
                                temp_ssec.ssecEQA = st.text_input(
                                    label="SSEC EQA Code",
                                    key=f"add-trainer-linkedssec-{i}-{j}-{run}",
                                    help="SSEC EQA is defined by Department of Statitics Singapore, please refer to "
                                         "[this link](https://www.singstat.gov.sg/standards/standards-and-classi"
                                         "fications/ssec) for more details",
                                    max_chars=2)

                            if st.checkbox("Specify SSEC EQA Description",
                                           key=f"specify-add-trainer-linkedssec-description-{i}-{j}-{run}"):
                                temp_ssec.description = st.text_area(
                                    label="Description",
                                    help="Description of the linked ssec-EQA",
                                    key=f"add-trainer-linkedssec-description-{i}-{j}-{run}",
                                    max_chars=1000)
                            runtrainer.add_linkedSsecEQA(temp_ssec)

                    indiv_run.add_linkCourseRunTrainer(runtrainer)

            add_runinfo.add_run(indiv_run)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(add_runinfo))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="add-button", type="primary") or st.session_state["add-button"]:
        LOGGER.info("Attempting to send request to Add Course Run API...")

        if "url" not in st.session_state or st.session_state["url"] is None:
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your Certificate and Private Key before proceeding!", icon="🚨")
        else:
            errors, warnings = add_runinfo.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                ac = AddCourseRun(include_expired, add_runinfo)

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(ac, require_encryption=True)

                with response:
                    LOGGER.info("Executing request...")
                    handle_response(lambda: ac.execute())


with edit_delete:
    st.header("Edit/Delete Course Runs")
    st.markdown("You can use this API to edit and delete your course runs. Note that this API uses "
                "the **Edit/Delete Course Runs** API to achieve the edit request!")

    if st.session_state["uen"] is None:
        st.warning("**Edit/Delete Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    # ===== BASIC RUN INFO ===== #
    st.subheader("`run` details")
    st.markdown("Note that `registrationDates`, `courseDates`, `scheduleInfoType`, `scheduleInfo`, "
                "`courseVacancy`, `modeOfTraining` are required for this update action!")

    # create a store for the parameters to pass into the backend
    # safe as there are only 2 options for this, and it is filled up later
    runinfo = None

    runtype = st.selectbox(label="Select Action",
                           options=["delete", "update"],
                           format_func=lambda x: x.upper(),
                           help="Action to be performed to the course run, i.e. update or delete",
                           key="edit-run-action")

    if runtype == "delete":
        runinfo = DeleteRunInfo()
    elif runtype == "update":
        runinfo = EditRunInfo()

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=OptionalSelector,
                                   format_func=lambda x: str(x),
                                   help="Indicate whether retrieve expired course or not",
                                   key="edit-view-expired")
    runinfo.crid = st.text_input("Key in the Course Reference Number",
                                 help="Reference number for the course of interest. Encode the course "
                                      "reference number as it may contains some special characters which "
                                      "could be blocked by the Gateway.",
                                 key="crn_edit")

    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="edit-course-run-id")

    if runtype == "update":
        if st.checkbox("Specify Sequence Number?", key="specify-edit-run-sequence-number"):
            runinfo.sequence_number = st.number_input(
                label="Run Sequence Number",
                value=0,
                help="It is a reference for a run if there is more than onerun in the payload. API will "
                     "auto-assign the sequence number according to the sequence of input and return "
                     "message with the sequenceNumber if any error occurs for that particular run. Default as 0",
                key="edit-run-sequence-number")

        st.markdown("#### Course Admin Details")
        if st.checkbox("Specify Mode of Training?", key="specify-edit-mode-of-training"):
            runinfo.mode_of_training = st.selectbox(label="Mode of Training",
                                                    key="edit-mode-of-training",
                                                    options=ModeOfTraining,
                                                    help="Mode of training code",
                                                    format_func=lambda x: str(x))

        runinfo.course_admin_email = st.text_input(label="Course Admin Email",
                                                   key="edit-course-admin-email",
                                                   help="Course admin email is under course run level "
                                                        "that can receive the email from 'QR code "
                                                        "Attendance Taking', 'Course Atendance with error'"
                                                        " and 'Trainer information not updated'",
                                                   max_chars=255)

        if len(runinfo.course_admin_email) > 0:
            if not Validators.verify_email(runinfo.course_admin_email):
                st.warning(f"Email format is not valid!", icon="⚠️")

        st.markdown("#### Course Vacancy Details")
        runinfo.vacancy = st.selectbox(label="Vacancy Code",
                                       key="edit-vacancy",
                                       options=Vacancy,
                                       help="Course run vacancy")

        st.markdown("#### Registration Dates")
        col1, col2 = st.columns(2)

        with col1:
            runinfo.opening_registration_date = st.date_input(label="Opening Date",
                                                              key="edit-opening-date",
                                                              min_value=date(1900, 1, 1),
                                                              help="Course run registration opening date as "
                                                                   "YYYYMMDD format (timezone - UTC+08:00)")

        with col2:
            runinfo.closing_registration_date = st.date_input(label="Closing Date",
                                                              key="edit-closing-date",
                                                              min_value=date(1900, 1, 1),
                                                              help="Course run registration closing date as "
                                                                   "YYYYMMDD format (timezone - UTC+08:00)")

        st.markdown("#### Course Dates")
        col1, col2 = st.columns(2)

        with col1:
            runinfo.course_start_date = st.date_input(label="Course Start Date",
                                                      key="edit-start-date",
                                                      min_value=date(1900, 1, 1),
                                                      help="Course run start opening dates as YYYYMMDD "
                                                           "format (timezone - UTC+08:00))")

        with col2:
            runinfo.course_end_date = st.date_input(label="Course End Date",
                                                    key="edit-end-date",
                                                    min_value=date(1900, 1, 1),
                                                    help="Course run end opening dates as YYYYMMDD format "
                                                         "(timezone - UTC+08:00))")

        st.markdown("#### Schedule Info Type")
        runinfo.schedule_info_type_code = st.text_input(label="Schedule Code",
                                                        key="edit-schedule-info-type-code",
                                                        max_chars=2,
                                                        placeholder="01",
                                                        help="Course run schedule info code")

        runinfo.schedule_info_type_description = st.text_area(label="Schedule Info Type Description",
                                                              key="edit-schedule-info-type-description",
                                                              placeholder="Description",
                                                              help="Course run schedule info description",
                                                              max_chars=32)

        if st.checkbox("Specify Schedule Info Description?", key="specify-edit-schedule-info-description"):
            runinfo.schedule_info = st.text_input(label="Schedule Info",
                                                  key="edit-schedule-info-description",
                                                  help="String representing Course run schedule info")

        st.markdown("#### Venue Info")
        if st.checkbox("Specify Venue Block?", key="specify-edit-venue-block"):
            runinfo.block = st.text_input(label="Block",
                                          key="edit-venue-block",
                                          help="Course run block",
                                          max_chars=10)

        if st.checkbox("Specify Venue Street?", key="specify-edit-venue-street"):
            runinfo.street = st.text_input(label="Street",
                                           key="edit-venue-street",
                                           help="Course run street",
                                           max_chars=32)

        if st.checkbox("Set Venue Building?", key="specify-edit-venue-building"):
            runinfo.building = st.text_input(label="Building",
                                             key="edit-venue-building",
                                             help="Course run building",
                                             max_chars=66)

        if st.checkbox("Set Venue Wheelchair Access?", key="specify-edit-venue-wheelchair"):
            runinfo.wheel_chair_access = st.selectbox(label="Wheelchair Access",
                                                      options=OptionalSelector,
                                                      format_func=lambda x: str(x),
                                                      key="edit-venue-wheelchair",
                                                      help="Indication that the course run location is "
                                                           "wheelchair accessible")

        runinfo.floor = st.text_input(label="Floor",
                                      key="edit-venue-floor",
                                      help="Course run floor",
                                      max_chars=3)
        runinfo.unit = st.text_input(label="Unit",
                                     key="edit-venue-unit",
                                     help="Course run unit",
                                     max_chars=5)
        runinfo.postal_code = st.text_input(label="Postal Code",
                                            key="edit-venue-postal-code",
                                            help="Course run postal code",
                                            max_chars=6)
        runinfo.room = st.text_input(label="Room",
                                     key="edit-venue-room",
                                     help="Course run room",
                                     max_chars=255)

        st.markdown("#### Course Intake Details")
        if st.checkbox("Specify Intake Size?", key="specify-edit-intake-size"):
            runinfo.intake_size = st.number_input(label="Intake Size",
                                                  key="edit-intake-size",
                                                  value=0,
                                                  min_value=0,
                                                  help="Course run intake size. It represents the max number "
                                                       "of pax for a class")
        if st.checkbox("Specify Threshold?", key="specify-edit-threshold"):
            runinfo.threshold = st.number_input(label="Threshold",
                                                key="edit-threshold",
                                                value=0,
                                                min_value=0,
                                                help="Course run threshold. Any additional pax that can register "
                                                     "above maximum pax.\ne.g. threshold = `10`, then total "
                                                     "allowed registration pax is `intake size + "
                                                     "threshold = 60`")

        if st.checkbox("Specify Registered User Count?", key="specify-edit-registered_user_count"):
            runinfo.registered_user_count = st.number_input(label="Registered Users Count",
                                                            key="edit-registered-user-count",
                                                            value=0,
                                                            min_value=0,
                                                            help="Course run registered user count. This number "
                                                                 "cannot be more than `intake size + threshold`")

        st.markdown("#### File Details")
        if st.checkbox("Specify File Name?", key="specify-edit-file-name"):
            runinfo.file_name = st.text_input(label="File Name",
                                              key="edit-file-name",
                                              help="Physical file name of the course run",
                                              max_chars=255)

        if st.checkbox("Specify File Content?", key="specify-edit-file-content"):
            runinfo.file_content = st.file_uploader(label="File Content",
                                                    key="edit-file-content",
                                                    help="File content of the course run in binary",
                                                    accept_multiple_files=False)

        # ===== RUN SESSION INFO ===== #
        st.divider()
        st.subheader("Add `session` details")
        st.markdown("Fill in the course session information here.\n\n"
                    "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `endDate` "
                    "will be based on the user input. For `modeOfTraining` other than `2` or `4`, course session "
                    "`endDate` will be set the same as `startDate`.\n\n"
                    "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session "
                    "`startTime` & `endTime` will be default as from 12:00AM to 11.59PM. For `modeOfTraining` "
                    "other than `2` or `4`, course session `startTime` & `endTime` will be based on user input."
                    )

        if st.checkbox("Specify Session Details?", key="specify-edit-session-details"):
            num_sessions: int = st.number_input(label="Key in the number of sessions in the Course Run",
                                                key="edit-num-sessions",
                                                min_value=0,
                                                value=0)

            for i in range(num_sessions):
                with st.expander(f"Session {i + 1}", expanded=True if i == 0 else False):
                    runsession: RunSessionEditInfo = RunSessionEditInfo()

                    st.markdown(f"##### Session {i + 1}")
                    if st.checkbox("Specify Session ID?", key=f"specify-edit-session-id-{i}"):
                        runsession.session_id = st.text_input(label="Course session ID",
                                                              key=f"edit-session-id-{i}",
                                                              help="Course session ID",
                                                              max_chars=300)

                    if st.checkbox("Specify Mode of Training?", key=f"specify-mode-of_training-{i}"):
                        runsession.mode_of_training = st.selectbox(
                            label="Mode of Training",
                            options=ModeOfTraining,
                            help="Mode of training code",
                            format_func=lambda x: str(x),
                            key=f"edit-mode-of-training-{i}")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.checkbox("Specify Session Start Date?", key=f"specify-edit-session-start-date-{i}"):
                            runsession.start_date = st.date_input(label="Start date of course session",
                                                                  min_value=date(1900, 1, 1),
                                                                  help="Start date of course session "
                                                                       "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                  key=f"edit-session-start-date-{i}")
                        if st.checkbox("Specify Session Start Time?", key=f"specify-edit-session-start-time-{i}"):
                            runsession.start_time = st.time_input(label="Start time of course session",
                                                                  help="Start time of course session"
                                                                       "(**HH:mm:ss/HH:mm format only**)",
                                                                  key=f"edit-session-start-time-{i}")

                    with col2:
                        if st.checkbox("Specify Session End Date?", key=f"specify-edit-session-end-date-{i}"):
                            runsession.end_date = st.date_input(label="End date of course session",
                                                                min_value=date(1900, 1, 1),
                                                                help="End date of course session "
                                                                     "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                key=f"edit-session-end-date-{i}")
                        if st.checkbox("Specify Session End Time?", key=f"specify-edit-session-end-time-{i}"):
                            runsession.end_time = st.time_input(label="End time of course session",
                                                                help="End time of course session"
                                                                     "(**HH:mm:ss/HH:mm format only**)",
                                                                key=f"edit-session-end-time-{i}")

                    st.markdown(f"###### Venue")
                    if st.checkbox("Specify Venue", key=f"specify-edit-session-venue-{i}"):
                        if st.checkbox("Specify Venue Block", key=f"specify-edit-session-venue-block-{i}"):
                            runsession.block = st.text_input(label="Block",
                                                             key=f"edit-venue-block-{i}",
                                                             help="Course run block",
                                                             max_chars=10)

                        if st.checkbox("Specify Venue Street", key=f"specify-edit-session-venue-street-{i}"):
                            runsession.street = st.text_input(label="Street",
                                                              key=f"edit-venue-street-{i}",
                                                              help="Course run street",
                                                              max_chars=32)

                        if st.checkbox("Specify Venue Building", key=f"specify-edit-session-venue-building-{i}"):
                            runsession.building = st.text_input(label="Building",
                                                                key=f"edit-venue-building-{i}",
                                                                help="Course run building",
                                                                max_chars=66)

                        if st.checkbox("Specify Wheelchair Access?",
                                       key=f"specify-edit-session-wheelchair-access-{i}"):
                            runsession.wheel_chair_access = st.selectbox(label="Wheelchair Access",
                                                                         options=OptionalSelector,
                                                                         format_func=lambda x: str(x),
                                                                         key=(f"edit-session-wheelchair-"
                                                                              f"access-{i}"),
                                                                         help="Indication that the course "
                                                                              "run location is wheelchair "
                                                                              "accessible")

                        if st.checkbox("Specify Primary Venue?", key=f"specify-edit-session-primary-venue-{i}"):
                            runsession.primary_venue = st.selectbox(
                                label="Primary Venue",
                                options=OptionalSelector,
                                format_func=lambda x: str(x),
                                help="Indication that the course session is the Primary Venue. If `true`, API "
                                     "will pick the venue information from course run and update to session venue",
                                key=f"edit-session-venue-primary-venue-{i}"
                            )

                        runsession.floor = st.text_input(label="Floor",
                                                         key=f"edit-session-venue-floor{i}",
                                                         help="Course run floor",
                                                         max_chars=3)
                        runsession.unit = st.text_input(label="Unit",
                                                        key=f"edit-session-venue-unit-{i}",
                                                        help="Course run unit",
                                                        max_chars=5)
                        runsession.postal_code = st.text_input(label="Postal Code",
                                                               key=f"edit-session-venue-postal-code-{i}",
                                                               help="Course run postal code",
                                                               max_chars=6)
                        runsession.room = st.text_input(label="Room",
                                                        key=f"edit-session-venue-room-{i}",
                                                        help="Course run room",
                                                        max_chars=255)

                    runinfo.add_session(runsession)

        # ===== RUN TRAINERS INFO ===== #
        st.subheader("Add `trainer` details")
        st.markdown(
            "If the Trainer type is `1 - Existing`, fill up only the Trainer ID field, and leave the rest empty. "
            "The API will retrieve the details from the TP Profile - Trainer Salutation, Key Domain / "
            "Sector Areas of Practice, Qualification Level, Qualification Description and Experience. The input "
            "details will not be updated to the Trainer profile.\n")
        st.markdown(
            "If the Trainer type is `2 - New`, please fill in all required details. If `inTraningProviderProfile` "
            "is set to `true`, the new added Trainer will be saved into Trainer profile as well as linked to "
            "this specific course run; otherwise this trainer is linked ot this specific course run only.")

        if st.checkbox("Specify Trainer", key="specify-num-trainer"):
            num_trainer: int = st.number_input(label="Key in the number of trainers in the Course Run",
                                               key="edit-num-trainers",
                                               min_value=0,
                                               value=0)

            for i in range(num_trainer):
                with st.expander(f"Trainer {i + 1}", expanded=True if i == 0 else False):
                    runtrainer = RunTrainerEditInfo()

                    st.markdown(f"##### Trainer {i + 1}")
                    code = st.selectbox(label="Trainer Type Code",
                                        options=TrainerType,
                                        format_func=lambda x: str(x),
                                        key=f"edit-trainer-code-{i}")

                    runtrainer.trainer_type_code = code.value
                    runtrainer.trainer_type_description = code.name.title()

                    st.markdown("###### Trainer Particulars")
                    if code == TrainerType.EXISTING:
                        runtrainer.trainer_idNumber = st.text_input(label="Trainer ID Number",
                                                                    key=f"edit-trainer-trainer-id-number-{i}",
                                                                    help="This refers to the NRIC/FIN/Passport "
                                                                         "number of the trainer.",
                                                                    max_chars=50)

                        if runtrainer.trainer_idNumber is not None and len(runtrainer.trainer_idNumber) > 0 \
                                and not Validators.verify_nric(runtrainer.trainer_idNumber):
                            st.warning(f"**ID Number** format may not valid!", icon="⚠️")
                    elif code == TrainerType.NEW:
                        if st.checkbox("Specify Trainer Index Number?", key=f"edit-trainer-trainer-index-{i}"):
                            runtrainer.index_number = st.number_input(
                                label="Trainer Index",
                                min_value=0,
                                value=0,
                                help="Index Number of the trainer. It is a reference for API if there is more than one "
                                     "trainer in the payload. Can leave as '0'",
                                key=f"edit-trainer-trainer-index-number-{i}")

                        if st.checkbox("Specify Trainer ID?", key=f"specify-edit-trainer-trainer-id-{i}"):
                            runtrainer.trainer_id = st.text_input(label="Trainer ID",
                                                                  key=f"edit-trainer-trainer-id-{i}",
                                                                  help="The unique Trainer id for existing trainer. "
                                                                       "For new trainer, leave it blank.",
                                                                  max_chars=50)
                        runtrainer.trainer_name = st.text_input(label="Trainer Name",
                                                                key=f"edit-trainer-trainer-name-{i}",
                                                                help="Name of the trainer",
                                                                max_chars=66)
                        runtrainer.trainer_email = st.text_input(label="Trainer Email",
                                                                 key=f"edit-trainer-trainer-email-{i}",
                                                                 help="Trainer email address",
                                                                 max_chars=320)

                        if len(runtrainer.trainer_email) > 0:
                            if not Validators.verify_email(runtrainer.trainer_email):
                                st.warning(f"Email format is not valid!", icon="⚠️")

                        st.markdown("###### Trainer ID")
                        col1, col2 = st.columns(2)

                        with col1:
                            runtrainer.trainer_idType = st.selectbox(label="Trainer ID Code",
                                                                     options=IdType,
                                                                     format_func=lambda x: str(x),
                                                                     help="Trainer ID Type Code",
                                                                     key=f"edit-trainer-trainer-id-code-{i}")

                        with col2:
                            runtrainer.trainer_idNumber = st.text_input(label="Trainer ID Number",
                                                                        key=f"edit-trainer-trainer-id-number-{i}",
                                                                        help="This refers to the NRIC/FIN/Passport "
                                                                             "number of the trainer.",
                                                                        max_chars=50)

                        st.markdown("###### Trainer Roles\n"
                                    "Select one or more of the roles below!")
                        runtrainer.trainer_roles = st.multiselect(
                            label="Select roles for the linked trainer",
                            options=Role,
                            format_func=lambda x: str(x),
                            key=f"specify-edit-trainer-role-{i}"
                        )

                        st.markdown("###### Trainer Profile")
                        if st.checkbox("Specify In Training Provider Profile?",
                                       key=f"specify-edit-trainer-training-provider-profile-{i}"):
                            runtrainer.inTrainingProviderProfile = st.selectbox(
                                label="Set in-training provider profile",
                                options=OptionalSelector,
                                format_func=lambda x: str(x),
                                help="This field is used to indicate whether to add the new trainer information to "
                                     "Training Provider's Profile. If the trainer is saved in TP trainers profile, "
                                     "TP can view/update the trainer in trainer maintenance page and select this "
                                     "trainer from trainers list for other course/runs. Next time when link same "
                                     "trainer in add/update course run API, need to indicate this trainer type as "
                                     "'Existing' and put in name & email.",
                                key=f"edit-trainer-training-provider-profile-{i}")

                        if st.checkbox("Specify Domain Area of Practice?", key=f"specify-edit-trainer-domain-area-{i}"):
                            runtrainer.domain_area_of_practice = st.text_area(
                                label="Domain Area of Practice",
                                help="This field indicates the Key Domain/Sector Areas of practice of the trainer "
                                     "(required for new trainer). For existing trainer, leave this field empty",
                                key=f"edit-trainer-domain-area-{i}",
                                max_chars=1000)

                        if st.checkbox("Specify Experience?", key=f"specify-edit-trainer-experience-{i}"):
                            runtrainer.experience = st.text_area(label="Experience",
                                                                 key=f"edit-trainer-experience-{i}",
                                                                 help="Trainer experience",
                                                                 max_chars=1000)

                        if st.checkbox("Specify LinkedIn URL?", key=f"specify-edit-trainer-linkedin-url-{i}"):
                            runtrainer.linkedInURL = st.text_input(label="LinkedIn URL",
                                                                   key=f"trainer-linkedin-url-{i}",
                                                                   help="Trainer linkedin URL (optional). For "
                                                                        "existing trainer, leave this field empty",
                                                                   max_chars=255)

                        if st.checkbox("Specify Salutation ID?", key=f"specify-edit-trainer-salutation-id-{i}"):
                            runtrainer.salutationId = st.selectbox(label="Salutations of the Trainer",
                                                                   key=f"edit-trainer-salutation-id-{i}",
                                                                   help="This field is used to enter the "
                                                                        "Salutation of the trainer (required for "
                                                                        "new trainer). For existing trainer, "
                                                                        "leave this field empty.",
                                                                   options=Salutations,
                                                                   format_func=lambda x: str(x))

                        st.markdown("###### Photo")
                        if st.checkbox("Specify Photo Name?", key=f"specify-edit-trainer-photo-name-{i}"):
                            runtrainer.photo_name = st.text_input(label="File Name",
                                                                  key=f"edit-trainer-photo-name-{i}",
                                                                  help="Physical file name of the course run",
                                                                  max_chars=255)

                        if st.checkbox("Specify Photo Content?", key=f"specify-edit-trainer-photo-content-{i}"):
                            runtrainer.photo_content = st.file_uploader(label="File Content",
                                                                        key=f"edit-trainer-photo-content-{i}",
                                                                        help="File content of the course run "
                                                                             "encoded in base64 format",
                                                                        accept_multiple_files=False)

                        st.markdown("###### Linked SSEC EQAs")
                        st.markdown("This field used to indicate the qualification level of the trainer. For existing "
                                    "trainer, please do not input this information.")
                        linkedssec = st.number_input(
                            label="Number of Linked SSEC EQAs",
                            key=f"edit-trainer-num-linked-sseceqas-{i}",
                            min_value=0,
                            value=0,
                        )

                        for j in range(linkedssec):
                            temp_ssec = LinkedSSECEQA()

                            st.markdown(f"*Linked SSEC EQA {j + 1}*")

                            if st.checkbox("Specify SSEC EQA", key=f"specify-edit-trainer-linkedSsecEQA-{i}-{j}"):
                                temp_ssec.ssecEQA = st.text_input(label="SSEC EQA Code",
                                                                  help="SSEC EQA is defined by Department "
                                                                       "of Statitics Singapore, please "
                                                                       "refer to [this link](https://www."
                                                                       "singstat.gov.sg/standards/standards"
                                                                       "-and-classifications/ssec) for "
                                                                       "more details",
                                                                  key=f"edit-trainer-linkedSsecEQA-{i}-{j}",
                                                                  max_chars=2)

                            if st.checkbox("Specify SSEC EQA Description",
                                           key=f"specify-edit-linkedSsecEQA-description-{i}-{j}"):
                                temp_ssec.description = st.text_area(label="Description",
                                                                     help="Description of the linked ssec-EQA",
                                                                     key=f"edit-linkedSsecEQA-description-{i}-{j}",
                                                                     max_chars=1000)

                            runtrainer.add_linkedSsecEQA(temp_ssec)

                    runinfo.add_linkCourseRunTrainer(runtrainer)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(runinfo))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="edit-button", type="primary"):
        LOGGER.info("Attempting to send request to Edit/Delete Course Run API...")

        if "url" not in st.session_state or st.session_state["url"] is None:
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif not runs:
            LOGGER.error("Missing Course Run ID, request aborted!")
            st.error("Make sure to fill in your **Course Run ID** before proceeding!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your Certificate and Private Key before proceeding!", icon="🚨")
        else:
            errors, warnings = runinfo.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                ec = None

                if runtype == "update":
                    ec = EditCourseRun(runs, include_expired, runinfo)
                elif runtype == "delete":
                    ec = DeleteCourseRun(runs, include_expired, runinfo)

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(ec, require_encryption=True)

                with response:
                    LOGGER.info("Executing request...")
                    handle_response(lambda: ec.execute())


with sessions:
    st.header("View Course Sessions")
    st.markdown("You can use this API to retrieve course sessions based on the course reference number, course run "
                "ID and the month!")

    if st.session_state["uen"] is None:
        st.warning("**View Course Sessions requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=OptionalSelector,
                                   format_func=lambda x: str(x),
                                   help="Indicate whether retrieve expired course or not",
                                   key="sessions-view-expired")
    crn = st.text_input("Key in the Course Reference Number",
                        help="Reference number for the course of interest. Encode the course reference number "
                             "as it may contains some special characters which could be blocked by the Gateway",
                        key="view-sessions-crn")

    runs = st.text_input("Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="view-sessions-course-run-id")

    month_value, year_value = None, None

    if st.checkbox("Specify Month and Year to retrieve?", key="specify-view-sessions-month-year"):
        month, year = st.columns(2)
        month_value = month.selectbox(label="Select Month value",
                                      options=Month,
                                      format_func=lambda x: str(x),
                                      help="The month of the sessions to retrieve",
                                      key="view-sessions-month")
        year_value = year.number_input(label="Select Year value",
                                       min_value=1900,
                                       max_value=9999,
                                       value=datetime.now().year,
                                       help="The year of the sessions to retrieve",
                                       key="view-sessions-year")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-session-button", type="primary"):
        LOGGER.info("Attempting to send request to View Course Sessions API...")

        if "url" not in st.session_state or st.session_state["url"] is None:
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif not st.session_state["uen"]:
            LOGGER.error("Missing UEN, request aborted!")
            st.error("Make sure to fill in your **UEN** before proceeding!", icon="🚨")
        elif does_not_have_keys():
            LOGGER.error("Missing Certificate or Private Keys!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        elif crn is None or len(crn) == 0:
            st.error("Make sure to fill in the **Course Reference Number** before proceeding!", icon="🚨")
        elif runs is None or len(runs) == 0:
            st.error("Make sure to fill in the **Course Run ID** before proceeding!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vcs = ViewCourseSessions(runs, crn, month_value, year_value, include_expired)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(vcs)

            with response:
                LOGGER.info("Executing request...")
                handle_response(lambda: vcs.execute())
