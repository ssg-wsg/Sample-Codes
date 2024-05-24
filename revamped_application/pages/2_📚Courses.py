import streamlit as st

from datetime import datetime

from core.courses.delete_course_run import DeleteCourseRun
from core.courses.view_course_run import ViewCourseRun
from core.courses.edit_course_run import EditCourseRun
from core.courses.add_course_run import AddCourseRun
from core.courses.view_course_sessions import ViewCourseSessions
from core.models.course_runs import RunInfo, RunSessionInfo, RunTrainerInfo, DeleteRunInfo, AddRunInfo, \
    RunSessionAddInfo, RunTrainerAddInfo, AddRunIndividualInfo, MODE_OF_TRAINING_MAPPING, ID_TYPE, SALUTATIONS
from utils.http import handle_error
from utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Courses", page_icon="📚")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("Courses API")
st.markdown("The Courses API allows you to search, filter and compare different SkillsFuture Credit "
            "eligible courses that have been published on the MySkillsFuture portal! Through this "
            "API you can access details regarding course categories, related courses, popular "
            "courses, featured courses, course brochures, and more! You can also manage your webhook "
            "events and subscriptions via this API!")

info_container = st.info(
    "**Add Course Runs and Edit/Delete Course Runs requires your *requests* to be encrypted!**\n\n"
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

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   help="Indicate whether retrieve expired course or not",
                                   key="view-expired")
    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a parameter for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="view-course-run-id")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="view-button"):
        if not runs:
            st.error("Key in your course run ID to proceed!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = ViewCourseRun(runs, include_expired)

            with request:
                st.subheader("Request")
                st.code(repr(vc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: vc.execute())

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
                                   options=["Select a value", "Yes", "No"],
                                   help="Indicate whether retrieve expired course or not",
                                   key="add-expired")
    add_runinfo.set_crid(st.text_input(label="Key in the Course Reference Number",
                                       help="Reference number for the course of interest. "
                                            "Encode the course reference number as it may contains "
                                            "some special characters which could be blocked by the Gateway",
                                       key="add-crn"))

    st.subheader("Define Number of Runs to Add")
    num_runs = st.number_input(label="Enter in the number of runs of a course to add",
                               min_value=1,
                               value=1,
                               key="add-num-runs")

    for run in range(num_runs):
        with st.expander(f"Run {run + 1}", expanded=True if run == 0 else False):
            indiv_run = AddRunIndividualInfo()

            st.subheader(f"Run {run + 1}")
            st.info(f"Sequence number is automatically set to {run}!", icon="ℹ️")
            indiv_run.set_sequence_number(run)

            st.markdown("#### Registration Dates")
            col1, col2 = st.columns(2)

            with col1:
                indiv_run.set_registrationDates_opening(st.date_input(
                    label="Opening Date",
                    key=f"add-opening-date-{run}",
                    help="Course run registration opening date as YYYYMMDD format (timezone - UTC+08:00)"))

            with col2:
                indiv_run.set_registrationDates_closing(st.date_input(
                    label="Closing Date",
                    key=f"add-closing-date-{run}",
                    help="Course run registration closing date as YYYYMMDD format (timezone - UTC+08:00)"))

            st.markdown("#### Course Dates")
            col1, col2 = st.columns(2)

            with col1:
                indiv_run.set_courseDates_start(st.date_input(label="Course Start Date",
                                                              key=f"add-start-date-{run}",
                                                              help="Course run start opening dates as YYYYMMDD format "
                                                                   "(timezone - UTC+08:00))"))

            with col2:
                indiv_run.set_courseDates_end(st.date_input(label="Course End Date",
                                                            key=f"add-end-date-{run}",
                                                            help="Course run end opening dates as YYYYMMDD format "
                                                                 "(timezone - UTC+08:00))"))

            st.markdown("#### Schedule Info Type")
            indiv_run.set_scheduleInfoType_code(st.text_input(label="Schedule Code",
                                                              key=f"add-schedule-code-{run}",
                                                              help="Course run schedule info code"))
            indiv_run.set_scheduleInfoType_description(st.text_area(label="Schedule Description",
                                                                    key=f"add-schedule-description-{run}",
                                                                    help="Course run schedule info description",
                                                                    max_chars=32))

            indiv_run.set_scheduleInfo(st.text_input(label="Schedule Info",
                                                     key=f"add-schedule-info-{run}",
                                                     help="Course run schedule info"))

            st.markdown("#### Venue Info")
            if st.checkbox("Specify Venue Block?", key=f"specify-add-venue-block-info-{run}"):
                indiv_run.set_venue_block(st.text_input(label="Block",
                                                        key=f"add-venue-block-{run}",
                                                        help="Course run block",
                                                        max_chars=10))

            if st.checkbox("Specify Venue Street?", key=f"specify-add-venue-street-info-{run}"):
                indiv_run.set_venue_street(st.text_input(label="Street",
                                                         key=f"add-venue-street-{run}",
                                                         help="Course run street",
                                                         max_chars=32))

            if st.checkbox("Specify Venue Building?", key=f"specify-add-venue-building-info-{run}"):
                indiv_run.set_venue_building(st.text_input(label="Building",
                                                           key=f"add-venue-building-{run}",
                                                           help="Course run building",
                                                           max_chars=66))

            if st.checkbox("Specify Wheelchair Accessible?", key=f"specify-add-wheelchair-accessible-info-{run}"):
                indiv_run.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                  options=["Select a value", "Yes", "No"],
                                                                  key=f"add-venue-wheelchair-accessible-{run}",
                                                                  help="Indication that the course run location is "
                                                                       "wheelchair accessible"))

            indiv_run.set_venue_floor(st.text_input(label="Floor",
                                                    key=f"add-venue-floor-{run}",
                                                    help="Course run floor",
                                                    max_chars=3))
            indiv_run.set_venue_unit(st.text_input(label="Unit",
                                                   key=f"add-venue-unit-{run}",
                                                   help="Course run unit",
                                                   max_chars=5))
            indiv_run.set_venue_postalCode(st.text_input(label="Postal Code",
                                                         key=f"add-venue-postal-code-{run}",
                                                         help="Course run postal code",
                                                         max_chars=6))
            indiv_run.set_venue_room(st.text_input(label="Room",
                                                   key=f"add-venue-room-{run}",
                                                   help="Course run room",
                                                   max_chars=255))

            st.markdown("#### Course Intake Details")
            if st.checkbox("Specify Intake Size?", key=f"specify-add-intake-size-info-{run}"):
                indiv_run.set_intakeSize(st.number_input(
                    label="Intake Size",
                    key=f"add-intake-size-{run}",
                    value=0,
                    min_value=0,
                    help="Course run intake size. It represents the max number of pax for a class"))

            if st.checkbox("Specify Intake Threshold?", key=f"specify-add-intake-threshold-info-{run}"):
                indiv_run.set_threshold(st.number_input(
                    label="Threshold",
                    key=f"add-intake-threshold-{run}",
                    value=0,
                    min_value=0,
                    help="Course run threshold. Any additional pax that can register above maximum pax.\n"
                         "e.g. threshold = `10`, then total allowed registration pax is `intake size + "
                         "threshold = 60`"))

            if st.checkbox("Specify Registered User Count?", key=f"specify-add-registered-user-count-info-{run}"):
                indiv_run.set_registeredUserCount(st.number_input(
                    label="Registered Users Count",
                    key=f"add-registered-user-count-{run}",
                    value=0,
                    min_value=0,
                    help="Course run registered user count. This number cannot be more than `intake size + threshold`"))

            st.markdown("#### Course Admin Details")
            indiv_run.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                      key=f"add-mode-of-training-{run}",
                                                      help="Mode of training code",
                                                      options=MODE_OF_TRAINING_MAPPING.keys(),
                                                      format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"))
            indiv_run.set_courseAdminEmail(st.text_input(
                label="Course Admin Email",
                key=f"add-course-admin-email-{run}",
                help="Course admin email is under course run level that can receive the email from 'QR code "
                     "Attendance Taking', 'Course Atendance with error' and 'Trainer information not updated'",
                max_chars=255))

            st.markdown("#### Course Vacancy Details")
            indiv_run.set_courseVacancy_code(st.text_input(label="Vacancy Code",
                                                           key=f"add-course-vacancy-code-{run}",
                                                           help="Course run vacancy code",
                                                           max_chars=1))
            indiv_run.set_courseVacancy_description(st.text_input(label="Vacancy Description",
                                                                  key=f"add-course-vacancy-description-{run}",
                                                                  help="Course run vacancy description",
                                                                  max_chars=128))

            st.markdown("#### File Details")
            if st.checkbox("Specify File Name?", key=f"specify-add-file-Name-info-{run}"):
                indiv_run.set_file_Name(st.text_input(label="File Name",
                                                      key=f"add-file-name-{run}",
                                                      help="Physical file name of the course run",
                                                      max_chars=255))

            if st.checkbox("Specify File Content?", key=f"specify-add-file-content-info{run}"):
                indiv_run.set_file_content(st.file_uploader(label="File Content",
                                                            key=f"add-file-content-{run}",
                                                            help="File content of the course run in binary",
                                                            accept_multiple_files=False))

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
                runsession: RunSessionAddInfo = RunSessionAddInfo()

                st.markdown(f"##### Session {i + 1}")
                runsession.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                           options=MODE_OF_TRAINING_MAPPING.keys(),
                                                           help="Mode of training code",
                                                           format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}",
                                                           key=f"add-session-mode-of-training_{i}-{run}"))

                col1, col2 = st.columns(2)
                with col1:
                    runsession.set_startDate(st.date_input(label="Start date of course session",
                                                           help="Start date of course session "
                                                                "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                           key=f"add-session-start-date-{i}-{run}"))

                if runsession.is_asynchronous_or_on_the_job():
                    with col1:
                        runsession.set_startTime(st.time_input(label="Start time of course session",
                                                               key=f"add-session-start-time-{i}-{run}",
                                                               help="Start time of course session"
                                                                    "(**HH:mm:ss/HH:mm format only**)",
                                                               disabled=True,
                                                               value=datetime(hour=0,
                                                                              minute=0,
                                                                              year=runsession.get_start_date_year(),
                                                                              month=runsession.get_start_time_month(),
                                                                              day=runsession.get_start_time_day())
                                                               .time()))

                    with col2:
                        runsession.set_endDate(st.date_input(label="End date of course session",
                                                             key=f"add-session-end-date-{i}-{run}",
                                                             help="End date of course session "
                                                                  "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                             value=runsession.get_start_date(),
                                                             disabled=True))
                        runsession.set_endTime(st.time_input(label="End time of course session",
                                                             key=f"add-session-end-time-{i}-{run}",
                                                             help="End time of course session"
                                                                  "(**HH:mm:ss/HH:mm format only**)",
                                                             disabled=True,
                                                             value=datetime(hour=23,
                                                                            minute=59,
                                                                            year=runsession.get_start_date_year(),
                                                                            month=runsession.get_start_time_month(),
                                                                            day=runsession.get_start_time_day())
                                                             .time()))

                    st.info(f"End date of course session is automatically set to **{runsession.get_start_date()}**\n\n"
                            f"Start and end time set to **12:00 AM to 11:59 PM** respectively", icon="ℹ️")
                else:
                    with col1:
                        runsession.set_startTime(st.time_input("Start time of course session",
                                                               help="Start time of course session"
                                                                    "(**HH:mm:ss/HH:mm format only**)",
                                                               key=f"add-session-start-time-{i}-{run}"))

                    with col2:
                        runsession.set_endDate(st.date_input(label="End date of course session",
                                                             help="End date of course session "
                                                                  "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                             key=f"add-session-end-date-{i}-{run}"))
                        runsession.set_endTime(st.time_input("End time of course session",
                                                             help="End time of course session"
                                                                  "(**HH:mm:ss/HH:mm format only**)",
                                                             key=f"add-session-end-time-{i}-{run}"))

                st.markdown(f"###### Venue")
                if st.checkbox("Specify Venue Block?", key=f"specify-add-session-venue-block-{i}-{run}"):
                    runsession.set_venue_block(st.text_input(label="Block",
                                                             key=f"add-session-venue-block-{i}-{run}",
                                                             help="Course run block",
                                                             max_chars=10))

                if st.checkbox("Specify Venue Street", key=f"specify-add-session-venue-street-{i}-{run}"):
                    runsession.set_venue_street(st.text_input(label="Street",
                                                              key=f"add-session-venue-street-{i}-{run}",
                                                              help="Course run street",
                                                              max_chars=32))

                if st.checkbox("Specify Venue Building", key=f"specify-add-session-venue-building-{i}-{run}"):
                    runsession.set_venue_building(st.text_input(label="Building",
                                                                key=f"add-session-venue-building-{i}-{run}",
                                                                help="Course run building",
                                                                max_chars=66))

                if st.checkbox("Specify Venue Wheelchair Accessible?",
                               key=f"specify-add-session-venue-wheelchair-{i}-{run}"):
                    runsession.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                       options=["Select a value", "Yes", "No"],
                                                                       key=f"add-session-venue-wheelchair-{i}-{run}",
                                                                       help="Indication that the course run "
                                                                            "location is wheelchair accessible"))

                if st.checkbox("Specify Primary Venue?", key=f"specify-add-session-primary-venue-{i}-{run}"):
                    runsession.set_venue_primaryVenue(st.selectbox(
                        label="Primary Venue",
                        options=["Select a value", "Yes", "No"],
                        help="Indication that the course session is the Primary Venue. If `Yes`, "
                             "API will pick the venue information from course run and update to session venue",
                        key=f"add-session-venue-primary-venue-{i}-{run}"))

                runsession.set_venue_floor(st.text_input(label="Floor",
                                                         key=f"add-session-floor-{i}-{run}",
                                                         help="Course run floor",
                                                         max_chars=3))
                runsession.set_venue_unit(st.text_input(label="Unit",
                                                        key=f"add-session-venue-unit-{i}-{run}",
                                                        help="Course run unit",
                                                        max_chars=5))
                runsession.set_venue_postalCode(st.text_input(label="Postal Code",
                                                              key=f"add-session-venue-postal-code-{i}-{run}",
                                                              help="Course run postal code",
                                                              max_chars=6))
                runsession.set_venue_room(st.text_input(label="Room",
                                                        key=f"add-session-venue-room-{i}-{run}",
                                                        help="Course run room",
                                                        max_chars=255))

                if i != num_sessions - 1:
                    st.divider()

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
                runtrainer = RunTrainerAddInfo()

                st.markdown(f"##### Trainer {i + 1}")
                runtrainer.set_trainer_type_code(st.text_input(label="Trainer Type",
                                                               key=f"add-trainer-type-{i}-{run}",
                                                               help="Trainer type code",
                                                               max_chars=1))
                runtrainer.set_trainer_type_description(st.text_input(label="Trainer Description",
                                                                      key=f"add-trainer-type-description-{i}-{run}",
                                                                      help="Trainer description",
                                                                      max_chars=128))

                st.markdown("###### Trainer Particulars")
                if st.checkbox("Specify Trainer Index Number", key=f"specify-add-trainer-index-number-{i}-{run}"):
                    runtrainer.set_indexNumber(st.number_input(
                        label="Trainer Index Number",
                        min_value=0,
                        value=0,
                        help="Index Number of the trainer. It is a reference for API if there is more than one "
                             "trainer in the payload. Can leave as '0'",
                        key=f"add-trainer-index-number-{i}-{run}"))

                if st.checkbox("Specify Unique Trainer ID?",
                               key=f"add-trainer-unique-trainer-id-{i}-{run}",
                               help="Do not select this field if you are specifying a new Trainer!"):
                    runtrainer.set_trainer_id(st.text_input(label="Trainer ID",
                                                            key=f"add-trainer-unique-id-identifier-{i}-{run}",
                                                            help="The unique Trainer id for existing trainer. "
                                                                 "For new trainer, leave it blank.",
                                                            max_chars=50))

                runtrainer.set_trainer_name(st.text_input(label="Trainer Name",
                                                          key=f"add-trainer-name-{i}-{run}",
                                                          help="Name of the trainer",
                                                          max_chars=66))
                runtrainer.set_trainer_email(st.text_input(label="Trainer Email",
                                                           key=f"add-trainer-email-{i}-{run}",
                                                           help="Trainer email address",
                                                           max_chars=320))

                st.markdown("###### Trainer ID")
                col1, col2 = st.columns(2)

                with col1:
                    runtrainer.set_trainer_idType(st.selectbox(label="Trainer ID Code",
                                                               options=ID_TYPE.keys(),
                                                               format_func=lambda x: f"{x}: {ID_TYPE[x]}",
                                                               help="Trainer ID Type Code",
                                                               key=f"add-trainer-id-code-{i}-{run}"))

                with col2:
                    runtrainer.set_trainer_idNumber(st.text_input(label="Trainer ID Number",
                                                                  key=f"add-trainer-id-number-{i}-{run}",
                                                                  help="This refers to the NRIC/FIN/Passport number "
                                                                       "of the trainer.",
                                                                  max_chars=50))

                st.markdown("###### Trainer Roles")
                if st.checkbox("Trainer", key=f"specify-add-trainer-role-trainer-{i}-{run}",
                               help="Trainer role of the linked trainer"):
                    runtrainer.add_trainer_role({
                        "id": 1,
                        "name": "Trainer"
                    })
                if st.checkbox("Assessor", key=f"specify-add-trainer-assessor-{i}-{run}",
                               help="Assessor role of the linked trainer"):
                    runtrainer.add_trainer_role({
                        "id": 2,
                        "name": "Assessor"
                    })

                st.markdown("###### Trainer Profile")
                if st.checkbox("Specify In Training Provider Profile?",
                               key=f"specify-add-trainer-training-provider-profile-{i}-{run}"):
                    runtrainer.set_inTrainingProviderProfile(st.selectbox(
                        label="Set in-training provider profile",
                        options=["Select a value", "Yes", "No"],
                        help="This field is used to indicate whether to add the new trainer information to "
                             "Training Provider's Profile. If the trainer is saved in TP trainers profile, "
                             "TP can view/update the trainer in trainer maintenance page and select this trainer "
                             "from trainers list for other course/runs. Next time when link same trainer in "
                             "add/update course run API, need to indicate this trainer type as 'Existing' "
                             "and put in name & email.",
                        key=f"add-trainer-training-provider-profile-{i}"))

                if st.checkbox("Specify Domain Area of Practice?", key=f"specify-add-trainer-domain-area-{i}-{run}"):
                    runtrainer.set_domainAreaOfPractice(st.text_area(
                        label="Domain Area of Practice",
                        help="This field indicates the Key Domain/Sector Areas of practice of the trainer "
                             "(required for new trainer). For existing trainer, leave this field empty",
                        key=f"add-trainer-domain-area-{i}-{run}",
                        max_chars=1000))

                if st.checkbox("Specify Experience?", key=f"specify-add-trainer-experience-{i}-{run}"):
                    runtrainer.set_experience(st.text_input(
                        label="Experience",
                        key=f"add-trainer-experience-{i}-{run}",
                        help="Trainer experience",
                        max_chars=1000
                    ))

                if st.checkbox("Specify LinkedIn URL?", key=f"specify-add-trainer-linkedin-{i}-{run}"):
                    runtrainer.set_linkedInURL(st.text_input(
                        label="LinkedIn URL",
                        key=f"add-trainer-linkedin-{i}-{run}",
                        help="Trainer linkedin URL (optional). For existing trainer, leave this field empty",
                        max_chars=255
                    ))

                if st.checkbox("Specify Salutation ID?", key=f"specify-add-trainer-salutation-{i}-{run}"):
                    runtrainer.set_salutationId(st.selectbox(
                        label="Salutations of the Trainer",
                        options=SALUTATIONS.keys(),
                        format_func=lambda x: SALUTATIONS[x],
                        help="This field is used to enter the Salutation of the trainer (required for new trainer). "
                             "For existing trainer, leave this field empty.",
                        key=f"add-trainer-salutation-id-code-{i}-{run}",
                    ))

                st.markdown("###### Photo")
                if st.checkbox("Specify Photo Name?", key=f"specify-add-trainer-photo-name-{i}-{run}"):
                    runtrainer.set_photo_name(st.text_input(label="File Name",
                                                            key=f"add-trainer-photo-{i}-{run}",
                                                            help="Physical file name of the course run",
                                                            max_chars=255))

                if st.checkbox("Specify Photo Content?", key=f"specify-add-trainer-photo-content-{i}-{run}"):
                    runtrainer.set_photo_content(st.file_uploader(label="File Content",
                                                                  key=f"add-trainer-photo-content-{i}-{run}",
                                                                  help="File content of the course run encoded in "
                                                                       "base64 format",
                                                                  accept_multiple_files=False))

                st.markdown("###### Linked SSEC EQAs")
                st.markdown("This field used to indicate the qualification level of the trainer. For existing trainer, "
                            "please do not input this information.")
                linkedssec = st.number_input(label="Number of Linked SSEC EQAs",
                                             key=f"add-trainer-linkedssec-{i}-{run}",
                                             min_value=0,
                                             value=0, )

                for j in range(linkedssec):
                    # create a dict first then fill in
                    temp_ssec = {"ssecEQA": {}}

                    st.markdown(f"*Linked SSEC EQA {j + 1}*")

                    if st.checkbox("Specify SSEC EQA", key=f"specify-add-trainer-linkedssec-{i}-{j}-{run}"):
                        temp_ssec["ssecEQA"]["code"] = st.text_input(
                            label="SSEC EQA Code",
                            key=f"add-trainer-linkedssec-{i}-{j}-{run}",
                            help="SSEC EQA is defined by Department of Statitics Singapore, please refer to "
                                 "[this link](https://www.singstat.gov.sg/standards/standards-and-classifications/"
                                 "ssec) for more details",
                            max_chars=2)

                    if st.checkbox("Specify SSEC EQA Description",
                                   key=f"specify-add-trainer-linkedssec-description-{i}-{j}-{run}"):
                        temp_ssec["description"] = st.text_area(
                            label="Description",
                            help="Description of the linked ssec-EQA",
                            key=f"add-trainer-linkedssec-description-{i}-{j}-{run}",
                            max_chars=1000)

                    runtrainer.add_linkedSsecEQA(temp_ssec)

                if i != num_trainers - 1:
                    st.divider()

                indiv_run.add_linkCourseRunTrainer(runtrainer)

            add_runinfo.add_run(indiv_run)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(add_runinfo))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="add-button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!", icon="🚨")
        else:
            errors, warnings = add_runinfo.validate()

            if len(errors) > 0:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
                )
            else:
                if len(warnings) > 0:
                    st.warning(
                        "**Some warnings are raised with your inputs:**\n\n- " + "\n".join(warnings), icon="⚠️"
                    )

                    request, response = st.tabs(["Request", "Response"])
                    ac = AddCourseRun(include_expired, add_runinfo)

                    with request:
                        st.subheader("Request")
                        st.code(repr(ac), language="text")

                    with response:
                        st.subheader("Response")
                        handle_error(lambda: ac.execute())

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
        runinfo = RunInfo()

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   help="Indicate whether retrieve expired course or not",
                                   key="edit-expired")
    runinfo.set_crid(st.text_input("Key in the Course Reference Number",
                                   help="Reference number for the course of interest. Encode the course "
                                        "reference number as it may contains some special characters which "
                                        "could be blocked by the Gateway.",
                                   key="crn_edit"))

    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="edit-course-run-id")

    if runtype == "update":
        if st.checkbox("Specify Sequence Number?", key="specify-edit-run-sequence-number"):
            runinfo.set_sequence_number(st.number_input(
                label="Run Sequence Number",
                value=0,
                help="It is a reference for a run if there is more than onerun in the payload. API will "
                     "auto-assign the sequence number according to the sequence of input and return "
                     "message with the sequenceNumber if any error occurs for that particular run. Default as 0",
                key="edit-run-sequence-number"))

        st.markdown("#### Course Admin Details")
        if st.checkbox("Specify Mode of Training?", key="specify-edit-mode-of-training"):
            runinfo.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                    key="edit-mode-of-training",
                                                    options=MODE_OF_TRAINING_MAPPING.keys(),
                                                    help="Mode of training code",
                                                    format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"))

        if st.checkbox("Specify Course Admin Email?", key="specify-edit-course-admin-email"):
            runinfo.set_courseAdminEmail(st.text_input(label="Course Admin Email",
                                                       key="edit-course-admin-email",
                                                       help="Course admin email is under course run level "
                                                            "that can receive the email from 'QR code "
                                                            "Attendance Taking', 'Course Atendance with error'"
                                                            " and 'Trainer information not updated'",
                                                       max_chars=255))

        st.markdown("#### Course Vacancy Details")
        if st.checkbox("Specify Course Vacancy?", key="specify-edit-vacancy-code"):
            runinfo.set_courseVacancy_code(st.text_input(label="Vacancy Code",
                                                         key="edit-vacancy-code",
                                                         help="Course run vacancy code",
                                                         max_chars=1))

            if st.checkbox("Specify Course Vacancy Description?", key="specify-edit-vacancy-description"):
                runinfo.set_courseVacancy_description(st.text_input(label="Vacancy Description",
                                                                    key="edit-vacancy-description",
                                                                    help="Course run vacancy description",
                                                                    max_chars=128))

        st.markdown("#### Registration Dates")
        if st.checkbox("Specify Registration Dates?", key="specify-edit-registrationDates"):
            col1, col2 = st.columns(2)

            with col1:
                runinfo.set_registrationDates_opening(st.date_input(label="Opening Date",
                                                                    key="edit-opening-date",
                                                                    help="Course run registration opening date as "
                                                                         "YYYYMMDD format (timezone - UTC+08:00)"))

            with col2:
                runinfo.set_registrationDates_closing(st.date_input(label="Closing Date",
                                                                    key="edit-closing-date",
                                                                    help="Course run registration closing date as "
                                                                         "YYYYMMDD format (timezone - UTC+08:00)"))

        st.markdown("#### Course Dates")
        if st.checkbox("Specify Course Dates?", key="specify-edit-courseDates"):
            col1, col2 = st.columns(2)

            with col1:
                runinfo.set_courseDates_start(st.date_input(label="Course Start Date",
                                                            key="edit-start-date",
                                                            help="Course run start opening dates as YYYYMMDD "
                                                                 "format (timezone - UTC+08:00))"))

            with col2:
                runinfo.set_courseDates_end(st.date_input(label="Course End Date",
                                                          key="edit-end-date",
                                                          help="Course run end opening dates as YYYYMMDD format "
                                                               "(timezone - UTC+08:00))"))

        st.markdown("#### Schedule Info Type")
        if st.checkbox("Specify Course Info Type?", key="specify-edit-schedule-info-type"):
            runinfo.set_scheduleInfoType_code(st.text_input(label="Schedule Code",
                                                            key="edit-schedule-info-type-code",
                                                            help="Course run schedule info code"))

            if st.checkbox("Specify Schedule Info Type Description?",
                           key="specify-edit-schedule-info-type-description"):
                runinfo.set_scheduleInfoType_description(
                    st.text_area(label="Schedule Description",
                                 key="edit-schedule-info-type-description",
                                 help="Course run schedule info description",
                                 max_chars=32))

        if st.checkbox("Specify Schedule Info Description?", key="specify-edit-schedule-info-description"):
            runinfo.set_scheduleInfo(st.text_input(label="Schedule Info",
                                                   key="edit-schedule-info-description",
                                                   help="String representing Course run schedule info"))

        st.markdown("#### Venue Info")
        if st.checkbox("Specify Venue Info?", key="specify-edit-venue-info"):
            if st.checkbox("Specify Venue Block?", key="specify-edit-venue-block"):
                runinfo.set_venue_block(st.text_input(label="Block",
                                                      key="edit-venue-block",
                                                      help="Course run block",
                                                      max_chars=10))

            if st.checkbox("Specify Venue Street?", key="specify-edit-venue-street"):
                runinfo.set_venue_street(st.text_input(label="Street",
                                                       key="edit-venue-street",
                                                       help="Course run street",
                                                       max_chars=32))

            if st.checkbox("Set Venue Building?", key="specify-edit-venue-building"):
                runinfo.set_venue_building(st.text_input(label="Building",
                                                         key="edit-venue-building",
                                                         help="Course run building",
                                                         max_chars=66))

            if st.checkbox("Set Venue Wheelchair Access?", key="specify-edit-venue-wheelchair"):
                runinfo.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                options=["Select a value", "Yes", "No"],
                                                                key="edit-venue-wheelchair",
                                                                help="Indication that the course run location is "
                                                                     "wheelchair accessible"))

            runinfo.set_venue_floor(st.text_input(label="Floor",
                                                  key="edit-venue-floor",
                                                  help="Course run floor",
                                                  max_chars=3))
            runinfo.set_venue_unit(st.text_input(label="Unit",
                                                 key="edit-venue-unit",
                                                 help="Course run unit",
                                                 max_chars=5))
            runinfo.set_venue_postalCode(st.text_input(label="Postal Code",
                                                       key="edit-venue-postal-code",
                                                       help="Course run postal code",
                                                       max_chars=6))
            runinfo.set_venue_room(st.text_input(label="Room",
                                                 key="edit-venue-room",
                                                 help="Course run room",
                                                 max_chars=255))

        st.markdown("#### Course Intake Details")
        if st.checkbox("Specify Intake Size?", key="specify-edit-intake-size"):
            runinfo.set_intakeSize(st.number_input(label="Intake Size",
                                                   key="edit-intake-size",
                                                   value=0,
                                                   min_value=0,
                                                   help="Course run intake size. It represents the max number "
                                                        "of pax for a class"))
        if st.checkbox("Specify Threshold?", key="specify-edit-threshold"):
            runinfo.set_threshold(st.number_input(label="Threshold",
                                                  key="edit-threshold",
                                                  value=0,
                                                  min_value=0,
                                                  help="Course run threshold. Any additional pax that can register "
                                                       "above maximum pax.\ne.g. threshold = `10`, then total "
                                                       "allowed registration pax is `intake size + "
                                                       "threshold = 60`"))

        if st.checkbox("Specify Registered User Count?", key="specify-edit-registered_user_count"):
            runinfo.set_registeredUserCount(st.number_input(label="Registered Users Count",
                                                            key="edit-registered-user-count",
                                                            value=0,
                                                            min_value=0,
                                                            help="Course run registered user count. This number "
                                                                 "cannot be more than `intake size + threshold`"))

        st.markdown("#### File Details")
        if st.checkbox("Specify File Name?", key="specify-edit-file-name"):
            runinfo.set_file_Name(st.text_input(label="File Name",
                                                key="edit-file-name",
                                                help="Physical file name of the course run",
                                                max_chars=255))

        if st.checkbox("Specify File Content?", key="specify-edit-file-content"):
            runinfo.set_file_content(st.file_uploader(label="File Content",
                                                      key="edit-file-content",
                                                      help="File content of the course run in binary",
                                                      accept_multiple_files=False))

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
            with st.expander("Course Session Details", expanded=False):
                num_sessions: int = st.number_input(label="Key in the number of sessions in the Course Run",
                                                    key="edit-num-sessions",
                                                    min_value=0,
                                                    value=0)

                if num_sessions > 0:
                    st.divider()

                for i in range(num_sessions):
                    runsession: RunSessionInfo = RunSessionInfo()

                    st.markdown(f"##### Session {i + 1}")
                    if st.checkbox("Specify Session ID?", key=f"specify-edit-session-id-{i}"):
                        runsession.set_session_id(st.text_input(label="Course session ID",
                                                                key=f"edit-session-id-{i}",
                                                                help="Course session ID",
                                                                max_chars=300))

                    if st.checkbox("Sepcify Mode of Training?", key=f"specify-mode-of_training-{i}"):
                        runsession.set_modeOfTraining(st.selectbox(
                            label="Mode of Training",
                            options=MODE_OF_TRAINING_MAPPING.keys(),
                            help="Mode of training code",
                            format_func=(lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"),
                            key=f"edit-mode-of-training-{i}"))

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.checkbox("Specify Session Start Date?", key=f"specify-edit-session-start-date-{i}"):
                            runsession.set_startDate(st.date_input(label="Start date of course session",
                                                                   help="Start date of course session "
                                                                        "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                   key=f"edit-session-start-date-{i}"))
                        if st.checkbox("Specify Session Start Time?", key=f"specify-edit-session-start-time-{i}"):
                            runsession.set_startTime(st.time_input(label="Start time of course session",
                                                                   help="Start time of course session"
                                                                        "(**HH:mm:ss/HH:mm format only**)",
                                                                   key=f"edit-session-start-time-{i}"))

                    with col2:
                        if st.checkbox("Specify Session End Date?", key=f"specify-edit-session-end-date-{i}"):
                            runsession.set_endDate(st.date_input(label="End date of course session",
                                                                 help="End date of course session "
                                                                      "(**YYYYMMDD or YYYY-MM-DD format only**)",
                                                                 key=f"edit-session-end-date-{i}"))
                        if st.checkbox("Specify Session End Time?", key=f"specify-edit-session-end-time-{i}"):
                            runsession.set_endTime(st.time_input(label="End time of course session",
                                                                 help="End time of course session"
                                                                      "(**HH:mm:ss/HH:mm format only**)",
                                                                 key=f"edit-session-end-time-{i}"))

                    st.markdown(f"###### Venue")
                    if st.checkbox("Specify Venue", key=f"specify-edit-session-venue-{i}"):
                        if st.checkbox("Specify Venue Block", key=f"specify-edit-session-venue-block-{i}"):
                            runsession.set_venue_block(
                                st.text_input(label="Block",
                                              key=f"edit-venue-block-{i}",
                                              help="Course run block",
                                              max_chars=10))

                        if st.checkbox("Specify Venue Street", key=f"specify-edit-session-venue-street-{i}"):
                            runsession.set_venue_street(st.text_input(label="Street",
                                                                      key=f"edit-venue-street-{i}",
                                                                      help="Course run street",
                                                                      max_chars=32))

                        if st.checkbox("Specify Venue Building", key=f"specify-edit-session-venue-building-{i}"):
                            runsession.set_venue_building(st.text_input(label="Building",
                                                                        key=f"edit-venue-building-{i}",
                                                                        help="Course run building",
                                                                        max_chars=66))

                        runsession.set_venue_floor(st.text_input(label="Floor",
                                                                 key=f"edit-session-venue-floor{i}",
                                                                 help="Course run floor",
                                                                 max_chars=3))
                        runsession.set_venue_unit(st.text_input(label="Unit",
                                                                key=f"edit-session-venue-unit-{i}",
                                                                help="Course run unit",
                                                                max_chars=5))
                        runsession.set_venue_postalCode(st.text_input(label="Postal Code",
                                                                      key=f"edit-session-venue-postal-code-{i}",
                                                                      help="Course run postal code",
                                                                      max_chars=6))
                        runsession.set_venue_room(st.text_input(label="Room",
                                                                key=f"edit-session-venue-room-{i}",
                                                                help="Course run room",
                                                                max_chars=255))

                        if st.checkbox("Specify Wheelchair Access?",
                                       key=f"specify-edit-session-wheelchair-access-{i}"):
                            runsession.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                               options=["Select a value", "Yes",
                                                                                        "No"],
                                                                               key=f"edit-session-wheelchair-"
                                                                                   f"access-{i}",
                                                                               help="Indication that the course "
                                                                                    "run location is wheelchair "
                                                                                    "accessible"))

                        if st.checkbox("Specify Primary Venue?", key=f"specify-edit-session-primary-venue-{i}"):
                            runsession.set_venue_primaryVenue(st.selectbox(
                                label="Primary Venue",
                                options=["Select a value", "Yes", "No"],
                                help="Indication that the course session is the Primary Venue. If `true`, API "
                                     "will pick the venue information from course run and update to session venue",
                                key=f"edit-session-venue-primary-venue-{i}"
                            ))

                    if i != num_sessions - 1:
                        st.divider()

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
            with st.expander("Add Trainer Details", expanded=False):
                num_trainers: int = st.number_input(label="Key in the number of trainers in the Course Run",
                                                    key="num-trainers",
                                                    min_value=0,
                                                    value=0)

                if num_trainers > 0:
                    st.divider()

                for i in range(num_trainers):
                    runtrainer = RunTrainerInfo()

                    st.markdown(f"##### Trainer {i + 1}")
                    runtrainer.set_trainer_type_code(st.text_input(label="Trainer Type",
                                                                   key=f"edit-trainer-trainer-code-{i}",
                                                                   help="Trainer type code",
                                                                   max_chars=1))
                    runtrainer.set_trainer_type_description(st.text_input(label="Trainer Description",
                                                                          key=f"trainer_description_{i}",
                                                                          help="Trainer description",
                                                                          max_chars=128))

                    if st.checkbox("Specify Trainer Index Number?", key=f"edit-trainer-trainer-index-{i}"):
                        runtrainer.set_indexNumber(st.number_input(
                            label="Trainer Index",
                            min_value=0,
                            value=0,
                            help="Index Number of the trainer. It is a reference for API if there is more than one "
                                 "trainer in the payload. Can leave as '0'",
                            key=f"edit-trainer-trainer-index-number-{i}"))

                    if st.checkbox("Specify Trainer ID?", key=f"specify-edit-trainer-trainer-id-{i}"):
                        runtrainer.set_trainer_id(st.text_input(label="Trainer ID",
                                                                key=f"edit-trainer-trainer-id-{i}",
                                                                help="The unique Trainer id for existing trainer. "
                                                                     "For new trainer, leave it blank.",
                                                                max_chars=50))

                    st.markdown("###### Trainer Particulars")
                    runtrainer.set_trainer_name(st.text_input(label="Trainer Name",
                                                              key=f"edit-trainer-trainer-name-{i}",
                                                              help="Name of the trainer",
                                                              max_chars=66))
                    runtrainer.set_trainer_email(st.text_input(label="Trainer Email",
                                                               key=f"edit-trainer-trainer-email-{i}",
                                                               help="Trainer email address",
                                                               max_chars=320))

                    st.markdown("###### Trainer ID")
                    col1, col2 = st.columns(2)

                    with col1:
                        runtrainer.set_trainer_idType(st.selectbox(label="Trainer ID Code",
                                                                   options=ID_TYPE.keys(),
                                                                   format_func=lambda x: f"{x}: {ID_TYPE[x]}",
                                                                   help="Trainer ID Type Code",
                                                                   key=f"edit-trainer-trainer-id-code-{i}"))

                    with col2:
                        runtrainer.set_trainer_idNumber(st.text_input(label="Trainer ID Number",
                                                                      key=f"edit-trainer-trainer-id-number-{i}",
                                                                      help="This refers to the NRIC/FIN/Passport "
                                                                           "number of the trainer.",
                                                                      max_chars=50))

                    st.markdown("###### Trainer Roles")
                    if st.checkbox("Trainer", key=f"specify-edit-trainer-trainer-role-{i}",
                                   help="Trainer role of the linked trainer"):
                        runtrainer.add_trainer_role({
                            "id": 1,
                            "name": "Trainer"
                        })
                    if st.checkbox("Assessor", key=f"specify-edit-trainer-assessor-roles-{i}",
                                   help="Assessor role of the linked trainer"):
                        runtrainer.add_trainer_role({
                            "id": 2,
                            "name": "Assessor"
                        })

                    st.markdown("###### Trainer Profile")
                    if st.checkbox("Specify In Training Provider Profile?",
                                   key=f"specify-edit-trainer-training-provider-profile-{i}"):
                        runtrainer.set_inTrainingProviderProfile(st.selectbox(
                            label="Set in-training provider profile",
                            options=["Select a value", "Yes", "No"],
                            help="This field is used to indicate whether to add the new trainer information to "
                                 "Training Provider's Profile. If the trainer is saved in TP trainers profile, "
                                 "TP can view/update the trainer in trainer maintenance page and select this "
                                 "trainer from trainers list for other course/runs. Next time when link same "
                                 "trainer in add/update course run API, need to indicate this trainer type as "
                                 "'Existing' and put in name & email.",
                            key=f"edit-trainer-training-provider-profile-{i}"))

                    if st.checkbox("Specify Domain Area of Practice?", key=f"specify-edit-trainer-domain-area-{i}"):
                        runtrainer.set_domainAreaOfPractice(st.text_area(
                            label="Domain Area of Practice",
                            help="This field indicates the Key Domain/Sector Areas of practice of the trainer "
                                 "(required for new trainer). For existing trainer, leave this field empty",
                            key=f"edit-trainer-domain-area-{i}",
                            max_chars=1000))

                    if st.checkbox("Specify Experience?", key=f"specify-edit-trainer-experience-{i}"):
                        runtrainer.set_experience(st.text_input(label="Experience",
                                                                key=f"edit-trainer-experience-{i}",
                                                                help="Trainer experience",
                                                                max_chars=1000))

                    if st.checkbox("Specify LinkedIn URL?", key=f"specify-edit-trainer-linkedin-url-{i}"):
                        runtrainer.set_linkedInURL(st.text_input(label="LinkedIn URL",
                                                                 key=f"trainer-linkedin-url-{i}",
                                                                 help="Trainer linkedin URL (optional). For "
                                                                      "existing trainer, leave this field empty",
                                                                 max_chars=255))

                    if st.checkbox("Specify Salutation ID?", key=f"specify-edit-trainer-salutation-id-{i}"):
                        runtrainer.set_salutationId(st.selectbox(label="Salutations of the Trainer",
                                                                 key=f"edit-trainer-salutation-id-{i}",
                                                                 help="This field is used to enter the "
                                                                      "Salutation of the trainer (required for "
                                                                      "new trainer). For existing trainer, "
                                                                      "leave this field empty.",
                                                                 options=SALUTATIONS.keys(),
                                                                 format_func=lambda x: SALUTATIONS[x]))

                    st.markdown("###### Photo")
                    if st.checkbox("Specify Photo Name?", key=f"specify-edit-trainer-photo-name-{i}"):
                        runtrainer.set_photo_name(st.text_input(label="File Name",
                                                                key=f"edit-trainer-photo-name-{i}",
                                                                help="Physical file name of the course run",
                                                                max_chars=255))

                    if st.checkbox("Specify Photo Content?", key=f"specify-edit-trainer-photo-content-{i}"):
                        runtrainer.set_photo_content(st.file_uploader(label="File Content",
                                                                      key=f"edit-trainer-photo-content-{i}",
                                                                      help="File content of the course run "
                                                                           "encoded in base64 format",
                                                                      accept_multiple_files=False))

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
                        # create a dict first then fill in
                        temp_ssec = {"ssecEQA": {}}

                        st.markdown(f"*Linked SSEC EQA {j + 1}*")

                        if st.checkbox("Specify SSEC EQA", key=f"specify-edit-trainer-linkedSsecEQA-{i}-{j}"):
                            temp_ssec["ssecEQA"]["code"] = st.text_input(label="SSEC EQA Code",
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
                            temp_ssec["description"] = st.text_area(label="Description",
                                                                    help="Description of the linked ssec-EQA",
                                                                    key=f"edit-linkedSsecEQA-description-{i}-{j}",
                                                                    max_chars=1000)

                        runtrainer.add_linkedSsecEQA(temp_ssec)

                    if i != num_trainers - 1:
                        st.divider()

                    runinfo.add_linkCourseRunTrainer(runtrainer)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(runinfo))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="edit-button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!", icon="🚨")
        elif not runs:
            st.error("Make sure to fill in your CRN before proceeding!", icon="🚨")
        else:
            errors, warnings = runinfo.validate()

            if len(errors) > 0:
                st.error(
                    "Some errors are detected with your inputs:\n\n- " + "\n- ".join(errors), icon="🚨"
                )
            else:
                if len(warnings) > 0:
                    st.warning(
                        "Some warnings are raised with your inputs:\n\n- " + "\n- ".join(warnings), icon="⚠️"
                    )

                request, response = st.tabs(["Request", "Response"])
                ec = None

                if runtype == "update":
                    ec = EditCourseRun(runs, include_expired, runinfo)
                elif runtype == "delete":
                    ec = DeleteCourseRun(runs, include_expired, runinfo)

                with request:
                    st.subheader("Request")
                    st.code(repr(ec), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: ec.execute())

with sessions:
    st.header("View Course Sessions")
    st.markdown("You can use this API to retrieve course sessions based on the course reference number, course run "
                "ID and the month!")

    if st.session_state["uen"] is None:
        st.warning("**View Course Sessions requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   help="Indicate whether retrieve expired course or not",
                                   key="view-sessions-expired")
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
                                      options=ViewCourseSessions.NUM2MONTH.keys(),
                                      format_func=lambda x: ViewCourseSessions.NUM2MONTH[x],
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
    if st.button("Send", key="view-session-button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = ViewCourseSessions(runs, crn, month_value, year_value, include_expired)

            with request:
                st.subheader("Request")
                st.code(repr(vc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: vc.execute())
