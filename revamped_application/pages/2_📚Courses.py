import streamlit as st

from datetime import datetime

from core.courses.delete_course_run import DeleteCourseRun
from core.courses.view_course_run import ViewCourseRun
from core.courses.edit_course_run import EditCourseRun
from core.courses.add_course_run import AddCourseRun
from core.courses.view_course_sessions import ViewCourseSessions
from core.models.course_runs import RunInfo, RunSessionInfo, RunTrainerInfo, DeleteRunInfo, AddRunInfo, \
    RunSessionAddInfo, RunTrainerAddInfo, MODE_OF_TRAINING_MAPPING, ID_TYPE, SALUTATIONS
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

view, add, edit_delete, sessions = st.tabs([
    "View Course Runs", "Add Courses Runs", "Edit/Delete Courses Runs", "View Course Sessions"
])

with view:
    st.header("View Course Runs")
    st.markdown("You can retrieve your course run details based on course reference number and course run ID using "
                "this API.")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-expired")
    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="view_button"):
        if not runs:
            st.error("Key in your course run ID to proceed!")
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
    st.warning("**Add Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

    # ===== BASIC RUN INFO ===== #
    st.subheader("`run` details")
    st.markdown("Note that `registrationDates`, `courseDates`, `scheduleInfoType`, `scheduleInfo`, "
                "`courseVacancy`, `modeOfTraining` and `courseAdminEmail` are required for this add action!")
    # create a store for the parameters to pass into the backend
    add_runinfo = AddRunInfo()
    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-expired-add")
    add_runinfo.set_crid(st.text_input(label="Key in the Course Reference Number",
                                       key="crn_add"))
    add_runinfo.set_sequence_number(st.number_input(
        label="Run Sequence Number",
        value=0,
        help="Defaults to 0",
        key="run-sequence-number-add"
    ))

    st.markdown("#### Registration Dates")
    col1, col2 = st.columns(2)

    with col1:
        add_runinfo.set_registrationDates_opening(st.date_input(label="Opening Date",
                                                                key="opening_date_add",
                                                                help=RunInfo.REGISTRATION_DATE_DESCRIPTION_OPENING))

    with col2:
        add_runinfo.set_registrationDates_closing(st.date_input(label="Closing Date",
                                                                key="closing_date_add",
                                                                help=RunInfo.REGISTRATION_DATE_DESCRIPTION_CLOSING))

    st.markdown("#### Course Dates")
    col1, col2 = st.columns(2)

    with col1:
        add_runinfo.set_courseDates_start(st.date_input(label="Course Start Date",
                                                        key="start_date_add",
                                                        help="Course run start opening dates as YYYYMMDD"))

    with col2:
        add_runinfo.set_courseDates_end(st.date_input(label="Course End Date",
                                                      key="end_date_add",
                                                      help="Course run end opening dates as YYYYMMDD"))

    st.markdown("#### Schedule Info Type")
    add_runinfo.set_scheduleInfoType_code(st.text_input(label="Schedule Code",
                                                        key="schedule_code_add",
                                                        help="Course run schedule info code"))
    add_runinfo.set_scheduleInfoType_description(st.text_area(label="Schedule Description",
                                                              key="schedule_description_add",
                                                              help="Course run schedule info description",
                                                              max_chars=32))

    add_runinfo.set_scheduleInfo(st.text_input(label="Schedule Info",
                                               key="schedule_info_add",
                                               help="String representing Course run schedule info"))

    st.markdown("#### Venue Info")
    if st.checkbox("Specify Venue Block?", key="specify_venue_info_add"):
        add_runinfo.set_venue_block(st.text_input(label="Block",
                                                  key="block_optional_add",
                                                  help="Course run block",
                                                  max_chars=10))

    if st.checkbox("Specify Venue Block?", key="specify_venue_block_add"):
        add_runinfo.set_venue_street(st.text_input(label="Street",
                                                   key="street_optional_add",
                                                   help="Course run street",
                                                   max_chars=32))

    if st.checkbox("Specify Venue Building?", key="specify_venue_building_add"):
        add_runinfo.set_venue_building(st.text_input(label="Building",
                                                     key="building_optional_add",
                                                     help="Course run building",
                                                     max_chars=66))

    if st.checkbox("Specify Wheelchair Accessible?", key="specify_wheelchair_accessible_add"):
        add_runinfo.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                            options=["Select a value", "Yes", "No"],
                                                            key="wheelchair_access_add",
                                                            help="Indication that the course run location is "
                                                                 "wheelchair accessible"))

    add_runinfo.set_venue_floor(st.text_input(label="Floor",
                                              key="floor_add",
                                              help="Course run floor",
                                              max_chars=3))
    add_runinfo.set_venue_unit(st.text_input(label="Unit",
                                             key="unit_add",
                                             help="Course run unit",
                                             max_chars=5))
    add_runinfo.set_venue_postalCode(st.text_input(label="Postal Code",
                                                   key="postalCode_add",
                                                   help="Course run postal code",
                                                   max_chars=6))
    add_runinfo.set_venue_room(st.text_input(label="Room",
                                             key="room_add",
                                             help="Course run room",
                                             max_chars=255))

    st.markdown("#### Course Intake Details")
    if st.checkbox("Specify Intake Size?", key="specify_intake_size_add"):
        add_runinfo.set_intakeSize(st.number_input(label="Intake Size",
                                                   key="intake_size_add",
                                                   value=0,
                                                   min_value=0,
                                                   help="Course run intake size. It represents the max number of pax "
                                                        "for a class"))

    if st.checkbox("Specify Intake Threshold?", key="specify_intake_threshold_add"):
        add_runinfo.set_threshold(st.number_input(label="Threshold",
                                                  key="threshold_add",
                                                  value=0,
                                                  min_value=0,
                                                  help="Course run threshold. Any additional pax that can register above "
                                                       "maximum pax.\ne.g. threshold = `10`, then total allowed "
                                                       "registration pax is `intake size + threshold = 60`"))

    if st.checkbox("Specify Registered User Count?", key="specify_registered_user_count_add"):
        add_runinfo.set_registeredUserCount(st.number_input(label="Registered Users Count",
                                                            key="registered_user_count_add",
                                                            value=0,
                                                            min_value=0,
                                                            help="Course run registered user count. This number cannot "
                                                                 "be more than `intake size + threshold`"))

    st.markdown("#### Course Admin Details")
    add_runinfo.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                key="mode_of_training_add",
                                                options=MODE_OF_TRAINING_MAPPING.keys(),
                                                format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"))
    add_runinfo.set_courseAdminEmail(st.text_input(label="Course Admin Email",
                                                   key="course_admin_email_add",
                                                   help="Course admin email is under course run level "
                                                        "that can receive the email from 'QR code "
                                                        "Attendance Taking', 'Course Atendance with error'"
                                                        " and 'Trainer information not updated'",
                                                   max_chars=255))

    st.markdown("#### Course Vacancy Details")
    add_runinfo.set_courseVacancy_code(st.text_input(label="Vacancy Code",
                                                     key="vacancy_code_add",
                                                     help="Course run vacancy code",
                                                     max_chars=1))
    add_runinfo.set_courseVacancy_description(st.text_input(label="Vacancy Description",
                                                            key="vacancy_description_add",
                                                            help="Course run vacancy description",
                                                            max_chars=128))

    st.markdown("#### File Details")
    if st.checkbox("Specify File Name?", key="specify_file_name_add"):
        add_runinfo.set_file_Name(st.text_input(label="File Name",
                                                key="file_name_add",
                                                help="Physical file name of the course run",
                                                max_chars=255))

    if st.checkbox("Specify File Content?", key="specify_file_content_add"):
        add_runinfo.set_file_content(st.file_uploader(label="File Content",
                                                      key="file_content_add",
                                                      help="File content of the course run in binary",
                                                      accept_multiple_files=False))

    # ===== RUN SESSION INFO ===== #
    st.divider()
    st.subheader("Add `session` details")
    st.markdown("Fill in the course session information here.\n\n"
                "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `endDate` "
                "will be based on the user input. For `modeOfTraining` other than `2` or `4`, course session "
                "`endDate` will be set the same as `startDate`.\n\n"
                "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `startTime` & "
                "`endTime` will be default as from 12:00AM to 11.59PM. For `modeOfTraining` other than `2` or `4`, "
                "course session `startTime` & `endTime` will be based on user input."
                )

    with st.expander("Course Session Details", expanded=False):
        num_sessions: int = st.number_input(label="Key in the number of sessions in the Course Run",
                                            key="num_sessions",
                                            min_value=0,
                                            value=0)

        for i in range(num_sessions):
            runsession: RunSessionInfo = RunSessionAddInfo()

            st.markdown(f"##### Session {i + 1}")
            runsession.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                       options=MODE_OF_TRAINING_MAPPING.keys(),
                                                       format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}",
                                                       key=f"mode_of_training_{i}"))

            col1, col2 = st.columns(2)

            with col1:
                runsession.set_startDate(st.date_input(label="Start date of course session",
                                                       help="YYYYMMDD or YYYY-MM-DD format only",
                                                       key=f"start_date_{i}"))

            if runsession.modeOfTraining in ["2", "4"]:
                with col1:
                    runsession.set_startTime(st.time_input(label="Start time of course session",
                                                           key=f"startTime_add_{i}",
                                                           disabled=True,
                                                           value=datetime(hour=0,
                                                                          minute=0,
                                                                          year=runsession.startDate.year,
                                                                          month=runsession.startDate.month,
                                                                          day=runsession.startDate.day).time()))

                with col2:
                    runsession.set_endDate(st.date_input(label="End date of course session",
                                                         key=f"endDate_add_{i}",
                                                         value=runsession.startDate,
                                                         disabled=True))
                    runsession.set_endTime(st.time_input(label="End time of course session",
                                                         key=f"endTime_add_{i}",
                                                         disabled=True,
                                                         value=datetime(hour=23,
                                                                        minute=59,
                                                                        year=runsession.startDate.year,
                                                                        month=runsession.startDate.month,
                                                                        day=runsession.startDate.day).time()))

                st.info(f"End date of course session is automatically set to **{runsession.startDate}**\n\n"
                        f"Start and end time set to **12:00 AM to 11:59 PM** respectively")
            else:
                with col1:
                    runsession.set_startTime(st.time_input("Start time of course session",
                                                           help="HH:mm:ss/HH:mm format only",
                                                           key=f"startTime_add_{i}"))

                with col2:
                    runsession.set_endDate(st.date_input(label="End date of course session",
                                                         help="YYYYMMDD or YYYY-MM-DD format only",
                                                         key=f"endDate_add_{i}"))
                    runsession.set_endTime(st.time_input("End time of course session",
                                                         help="HH:mm:ss/HH:mm format only",
                                                         key=f"endTime_add_{i}"))

            st.markdown(f"###### Venue")
            if st.checkbox("Specify Venue Block?", key=f"specify_session_venue_block_add_{i}"):
                runsession.set_venue_block(st.text_input(label="Block",
                                                         key=f"block_optional_{i}",
                                                         help="Course run block",
                                                         max_chars=10))

            if st.checkbox("Specify Venue Street", key=f"specify_session_venue_street_add_{i}"):
                runsession.set_venue_street(st.text_input(label="Street",
                                                          key=f"street_optional_{i}",
                                                          help="Course run street",
                                                          max_chars=32))

            if st.checkbox("Specify Venue Building", key=f"specify_session_venue_building_block_add_{i}"):
                runsession.set_venue_building(st.text_input(label="Building",
                                                            key=f"building_optional_{i}",
                                                            help="Course run building",
                                                            max_chars=66))

            if st.checkbox("Specify Venue Wheelchair Accessible?", key=f"specify_venue_wheelchair_accessible_add_{i}"):
                runsession.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                   options=["Select a value", "Yes", "No"],
                                                                   key=f"wheelchair_access_{i}",
                                                                   help="Indication that the course run "
                                                                        "location is wheelchair accessible"))

            if st.checkbox("Specify Primary Venue?", key="specify_venue_primary_add"):
                runsession.set_venue_primaryVenue(st.selectbox(
                    label="Primary Venue",
                    options=["Select a value", "Yes", "No"],
                    help="Indication that the course session is the Primary Venue. If `true`, API will pick the venue "
                         "information from course run and update to session venue",
                    key=f"venue_primary_venue_{i}"))

            runsession.set_venue_floor(st.text_input(label="Floor",
                                                     key=f"floor_{i}",
                                                     help="Course run floor",
                                                     max_chars=3))
            runsession.set_venue_unit(st.text_input(label="Unit",
                                                    key=f"unit_{i}",
                                                    help="Course run unit",
                                                    max_chars=5))
            runsession.set_venue_postalCode(st.text_input(label="Postal Code",
                                                          key=f"postalCode_{i}",
                                                          help="Course run postal code",
                                                          max_chars=6))
            runsession.set_venue_room(st.text_input(label="Room",
                                                    key=f"room_{i}",
                                                    help="Course run room",
                                                    max_chars=255))

            add_runinfo.add_session(runsession)

            if i != num_sessions - 1:
                st.divider()

    # ===== RUN TRAINERS INFO ===== #
    st.subheader("Add `trainer` details")
    st.markdown("If the Trainer type is `1 - Existing`, fill up only the Trainer ID field, and leave the rest empty. "
                "The API will retrieve the details from the TP Profile - Trainer Salutation, Key Domain / "
                "Sector Areas of Practice, Qualification Level, Qualification Description and Experience. The input "
                "details will not be updated to the Trainer profile.\n")
    st.markdown("If the Trainer type is `2 - New`, please fill in all required details. If `inTraningProviderProfile` "
                "is set to `true`, the new added Trainer will be saved into Trainer profile as well as linked to "
                "this specific course run; otherwise this trainer is linked ot this specific course run only.")

    with st.expander("Add Trainer Details", expanded=False):
        num_trainers: int = st.number_input(label="Key in the number of trainers in the Course Run",
                                            key="num_trainers",
                                            min_value=0,
                                            value=0)

        for i in range(num_trainers):
            runtrainer = RunTrainerAddInfo()

            st.markdown(f"##### Trainer {i + 1}")
            runtrainer.set_trainer_type_code(st.text_input(label="Trainer Type",
                                                           key=f"add_trainer_code_{i}",
                                                           max_chars=1))
            runtrainer.set_trainer_type_description(st.text_input(label="Trainer Description",
                                                                  key=f"add_trainer_description_{i}",
                                                                  max_chars=128))

            st.markdown("###### Trainer Particulars")
            if st.checkbox("Specify Trainer Index Number", key=f"specify_trainer_index_number_{i}"):
                runtrainer.set_indexNumber(st.number_input(label="Trainer Index Number",
                                                           min_value=0,
                                                           value=0,
                                                           key=f"add_trainer_index_number_{i}"))

            if st.checkbox("Specify Unique Trainer ID?",
                           key=f"specify_trainer_unique_id_{i}",
                           help="Do not select this field if you are specifying a new Trainer!"):
                runtrainer.set_trainer_id(st.text_input(label="Trainer ID",
                                                        key=f"add_trainer_id_{i}",
                                                        max_chars=50))

            runtrainer.set_trainer_name(st.text_input(label="Trainer Name",
                                                      key=f"add_trainer_name_{i}",
                                                      max_chars=66))
            runtrainer.set_trainer_email(st.text_input(label="Trainer Email",
                                                       key=f"add_trainer_email_{i}",
                                                       max_chars=320))

            st.markdown("###### Trainer ID")
            col1, col2 = st.columns(2)

            with col1:
                runtrainer.set_trainer_idType(st.selectbox(label="Trainer ID Code",
                                                           options=ID_TYPE.keys(),
                                                           format_func=lambda x: f"{x}: {ID_TYPE[x]}",
                                                           help="Trainer ID Type Code",
                                                           key=f"add_trainer_id_code_{i}"))

            with col2:
                runtrainer.set_trainer_idNumber(st.text_input(label="Trainer ID Number",
                                                              key=f"add_trainer_id_number_{i}",
                                                              help="Refers to the NRIC/FIN/Passport number of "
                                                                   "the trainer",
                                                              max_chars=50))

            st.markdown("###### Trainer Roles")
            if st.checkbox("Trainer", key=f"add-trainer-role-{i}"):
                runtrainer.add_trainer_role({
                    "id": 1,
                    "name": "Trainer"
                })
            if st.checkbox("Assessor", key=f"add-assessor-role-{i}"):
                runtrainer.add_trainer_role({
                    "id": 2,
                    "name": "Assessor"
                })

            st.markdown("###### Trainer Profile")
            if st.checkbox("Specify In Training Provider Profile?",
                           key=f"specify-add-training-provider-profile-{i}"):
                runtrainer.set_inTrainingProviderProfile(st.selectbox(label="Set in-training provider profile",
                                                                      options=["Select a value", "Yes", "No"],
                                                                      key=f"in_training_provider_profile_{i}"))

            if st.checkbox("Specify Domain Area of Practice?", key=f"specify-add-domain-area-{i}"):
                runtrainer.set_domainAreaOfPractice(st.text_area(
                    label="Domain Area of Practice",
                    help="This field indicates the Key Domain/Sector Areas of practice of the trainer (required for "
                         "new trainer).",
                    key=f"trainer_domainarea_{i}",
                    max_chars=1000))

            if st.checkbox("Specify Experience?", key=f"specify-add-experience-{i}"):
                runtrainer.set_experience(st.text_input(
                    label="Experience",
                    key=f"experience_{i}",
                    max_chars=1000
                ))

            if st.checkbox("Specify LinkedIn URL?", key=f"specify-add-linkedin-url-{i}"):
                runtrainer.set_linkedInURL(st.text_input(
                    label="LinkedIn URL",
                    key=f"linkedin_url_{i}",
                    max_chars=255
                ))

            if st.checkbox("Specify Salutation ID?", key=f"specify-add-salutation-id-{i}"):
                runtrainer.set_salutationId(st.selectbox(
                    label="Salutations of the Trainer",
                    options=[1, 2, 3, 4, 5, 6],
                    format_func=lambda x: SALUTATIONS[x]
                ))

            st.markdown("###### Photo")
            if st.checkbox("Specify Photo Name?", key=f"specify-add-photo-name-{i}"):
                runtrainer.set_photo_name(st.text_input(label="File Name",
                                                        key=f"file_name_{i}",
                                                        help="Physical file name of the course run",
                                                        max_chars=255))

            if st.checkbox("Specify Photo Content?", key=f"specify-add-photo-content-{i}"):
                runtrainer.set_photo_content(st.file_uploader(
                    label="File Content",
                    key=f"file_content_{i}",
                    help="File content of the course run in binary",
                    accept_multiple_files=False
                ))

            st.divider()
            st.markdown("###### Linked SSEC EQAs")
            linkedssec = st.number_input(
                label="Number of Linked SSEC EQAs",
                key=f"add-linkedSsecEQAs-{i}",
                min_value=0,
                value=0,
            )

            for j in range(linkedssec):
                # create a dict first then fill in
                temp_ssec = {"ssecEQA": {}}

                st.markdown(f"*Linked SSEC EQA {j + 1}*")

                if st.checkbox("Specify SSEC EQA", key=f"add-linkedSsecEQA-{i}-{j}"):
                    temp_ssec["ssecEQA"]["code"] = st.text_input(
                        label="SSEC EQA Code",
                        key=f"linkedSsecEQAs_code_add_{i}_{j}",
                        max_chars=2)

                if st.checkbox("Specify SSEC EQA Description", key=f"add-linkedSsecEQA-description-{i}-{j}"):
                    temp_ssec["description"] = st.text_area(
                        label="Description",
                        help="This field is used to indicate the qualification level of the trainer. For existing "
                             "trainer, please do not input this information.",
                        key=f"linkedSsecEQAs_add_description_{i}_{j}",
                        max_chars=1000)

                runtrainer.add_linkedSsecEQA(temp_ssec)

            add_runinfo.add_linkCourseRunTrainer(runtrainer)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(add_runinfo))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="add_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        else:
            errors = add_runinfo.validate()

            if errors is not None:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors)
                )
            else:
                request, response = st.tabs(["Request", "Response"])

                ac = AddCourseRun(runs, include_expired, add_runinfo)
                resp = None

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
    st.warning("**Edit/Delete Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

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
                           key="run-action-delete")

    if runtype == "delete":
        runinfo = DeleteRunInfo()
    elif runtype == "update":
        runinfo = RunInfo()
    else:
        st.error("Unknown run type selected!")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-expired-edit")
    runinfo.set_crid(st.text_input("Key in the Course Reference Number", key="crn_edit"))
    runs = st.text_input(label="Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-edit")

    if runtype == "update":
        if st.checkbox("Specify Sequence Number?", key="specify-sequence-number"):
            runinfo.set_sequence_number(st.number_input(label="Run Sequence Number",
                                                        value=0,
                                                        help="Defaults to 0",
                                                        key="run-sequence-number-edit"))

        st.markdown("#### Course Admin Details")
        if st.checkbox("Specify Mode of Training?", key="mode-of-training"):
            runinfo.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                    key="mode_of_training_edit",
                                                    options=MODE_OF_TRAINING_MAPPING.keys(),
                                                    format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"))

        if st.checkbox("Specify Course Admin Email?", key="specify-admin-email"):
            runinfo.set_courseAdminEmail(st.text_input(label="Course Admin Email",
                                                       key="course_admin_email",
                                                       help="Course admin email is under course run level "
                                                            "that can receive the email from 'QR code "
                                                            "Attendance Taking', 'Course Atendance with error'"
                                                            " and 'Trainer information not updated'",
                                                       max_chars=255))

        st.markdown("#### Course Vacancy Details")
        if st.checkbox("Specify Course Vacancy?", key="specify-vacancy"):
            runinfo.set_courseVacancy_code(st.text_input(label="Vacancy Code",
                                                         key="vacancy_code",
                                                         help="Course run vacancy code",
                                                         max_chars=1))

            if st.checkbox("Specify Course Vacancy Description?", key="specify-vacancy-description"):
                runinfo.set_courseVacancy_description(st.text_input(label="Vacancy Description",
                                                                    key="vacancy_description",
                                                                    help="Course run vacancy description",
                                                                    max_chars=128))

        st.markdown("#### Registration Dates")
        if st.checkbox("Specify Registration Dates?", key="specify-registrationDates"):
            col1, col2 = st.columns(2)

            with col1:
                runinfo.set_registrationDates_opening(st.date_input(label="Opening Date",
                                                                    key="opening_date",
                                                                    help=RunInfo.REGISTRATION_DATE_DESCRIPTION_OPENING))

            with col2:
                runinfo.set_registrationDates_closing(st.date_input(label="Closing Date",
                                                                    key="closing_date",
                                                                    help=RunInfo.REGISTRATION_DATE_DESCRIPTION_CLOSING))

        st.markdown("#### Course Dates")
        if st.checkbox("Specify Course Dates?", key="specify-courseDates"):
            col1, col2 = st.columns(2)

            with col1:
                runinfo.set_courseDates_start(st.date_input(label="Course Start Date", key="start_date",
                                                            help="Course run start opening dates as YYYYMMDD"))

            with col2:
                runinfo.set_courseDates_end(st.date_input(label="Course End Date",
                                                          key="end_date",
                                                          help="Course run end opening dates as YYYYMMDD"))

        st.markdown("#### Schedule Info Type")
        if st.checkbox("Specify Course Info Type?", key="specify-schedule-info-type"):
            runinfo.set_scheduleInfoType_code(st.text_input(label="Schedule Code",
                                                            key="schedule_code",
                                                            help="Course run schedule info code"))

            if st.checkbox("Specify Schedule Info Type Description?", key="specify-schedule-info-type-description"):
                runinfo.set_scheduleInfoType_description(
                    st.text_area(label="Schedule Description",
                                 key="schedule_description",
                                 help="Course run schedule info description",
                                 max_chars=32))

        if st.checkbox("Specify Schedule Info Description?", key="specify-schedule-info-description"):
            runinfo.set_scheduleInfo(st.text_input(label="Schedule Info",
                                                   key="schedule_info",
                                                   help="String representing Course run schedule info"))

        st.markdown("#### Venue Info")
        if st.checkbox("Specify Venue Info?", key="specify-venue-info"):
            if st.checkbox("Specify Venue Block?", key="specify_venue_block"):
                runinfo.set_venue_block(st.text_input(label="Block",
                                                      key="block_optional",
                                                      help="Course run block",
                                                      max_chars=10))

            if st.checkbox("Specify Venue Street?", key="specify_venue_street"):
                runinfo.set_venue_street(st.text_input(label="Street",
                                                       key="street_optional",
                                                       help="Course run street",
                                                       max_chars=32))

            if st.checkbox("Set Venue Building?", key="set_venue_building"):
                runinfo.set_venue_building(st.text_input(label="Building",
                                                         key="building_optional",
                                                         help="Course run building",
                                                         max_chars=66))

            if st.checkbox("Set Venue Wheelchair Access?", key="set_venue_wheelchair"):
                runinfo.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                options=["Select a value", "Yes", "No"],
                                                                key="wheelchair_access",
                                                                help="Indication that the course run location is "
                                                                     "wheelchair accessible"))

            runinfo.set_venue_floor(st.text_input(label="Floor",
                                                  key="floor",
                                                  help="Course run floor",
                                                  max_chars=3))
            runinfo.set_venue_unit(st.text_input(label="Unit",
                                                 key="unit",
                                                 help="Course run unit",
                                                 max_chars=5))
            runinfo.set_venue_postalCode(st.text_input(label="Postal Code",
                                                       key="postalCode",
                                                       help="Course run postal code",
                                                       max_chars=6))
            runinfo.set_venue_room(st.text_input(label="Room",
                                                 key="room",
                                                 help="Course run room",
                                                 max_chars=255))

        st.markdown("#### Course Intake Details")
        if st.checkbox("Specify Intake Size?", key="specify-intake-size"):
            runinfo.set_intakeSize(st.number_input(label="Intake Size",
                                                   key="intake_size",
                                                   value=0,
                                                   min_value=0,
                                                   help="Course run intake size. It represents the max number of pax "
                                                        "for a class"))
        if st.checkbox("Specify Threshold?", key="specify-threshold"):
            runinfo.set_threshold(st.number_input(label="Threshold",
                                                  key="threshold",
                                                  value=0,
                                                  min_value=0,
                                                  help="Course run threshold. Any additional pax that can register "
                                                       "above maximum pax.\ne.g. threshold = `10`, then total allowed "
                                                       "registration pax is `intake size + threshold = 60`"))

        if st.checkbox("Specify Registered User Count?", key="specify-registered_user_count"):
            runinfo.set_registeredUserCount(st.number_input(label="Registered Users Count",
                                                            key="registered_user_count",
                                                            value=0,
                                                            min_value=0,
                                                            help="Course run registered user count. This number cannot "
                                                                 "be more than `intake size + threshold`"))

        st.markdown("#### File Details")
        if st.checkbox("Specify File Name?", key="specify-file-name"):
            runinfo.set_file_Name(st.text_input(label="File Name",
                                                key="file_name",
                                                help="Physical file name of the course run",
                                                max_chars=255))

        if st.checkbox("Specify File Content?", key="specify-file-content"):
            runinfo.set_file_content(st.file_uploader(label="File Content",
                                                      key="file_content",
                                                      help="File content of the course run in binary",
                                                      accept_multiple_files=False))

        # ===== RUN SESSION INFO ===== #
        st.divider()
        st.subheader("Add `session` details")
        st.markdown("Fill in the course session information here.\n\n"
                    "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `endDate` "
                    "will be based on the user input. For `modeOfTraining` other than `2` or `4`, course session "
                    "`endDate` will be set the same as `startDate`.\n\n"
                    "For `modeOfTraining` in (2-Asynchronous eLearning and 4-On-the-Job), course session `startTime` & "
                    "`endTime` will be default as from 12:00AM to 11.59PM. For `modeOfTraining` other than `2` or `4`, "
                    "course session `startTime` & `endTime` will be based on user input."
                    )

        if st.checkbox("Specify Session Details?", key="specify-session-details"):
            with st.expander("Course Session Details", expanded=False):
                num_sessions: int = st.number_input(label="Key in the number of sessions in the Course Run",
                                                    key="num_sessions_edit",
                                                    min_value=0,
                                                    value=0)

                for i in range(num_sessions):
                    runsession: RunSessionInfo = RunSessionInfo()

                    st.markdown(f"##### Session {i + 1}")
                    if st.checkbox("Specify Session ID?", key=f"specify-session-{i}"):
                        runsession.set_session_id(st.text_input(label="Course session ID",
                                                                key=f"session_id_{i}",
                                                                max_chars=300))

                    if st.checkbox("Sepcify Mode of Training", key=f"specify-modeof_training-{i}"):
                        runsession.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                                   options=MODE_OF_TRAINING_MAPPING.keys(),
                                                                   format_func=(lambda x:
                                                                                f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"),
                                                                   key=f"mode_of_training_{i}"))

                    if st.checkbox("Specify Session Start Date?", key=f"specify-session-start-date-{i}"):
                        runsession.set_startDate(st.date_input(label="Start date of course session",
                                                               help="YYYYMMDD or YYYY-MM-DD format only",
                                                               key=f"start_date_{i}"))

                    if st.checkbox("Specify Session End Date?", key=f"specify-session-end-date-{i}"):
                        runsession.set_endDate(st.date_input(label="End date of course session",
                                                             help="YYYYMMDD or YYYY-MM-DD format only",
                                                             key=f"end_date_{i}"))

                    if st.checkbox("Specify Session Start Time", key=f"specify-session-start-time-{i}"):
                        runsession.set_startTime(st.time_input(label="Start time of course session",
                                                               help="HH:mm:ss/HH:mm format only",
                                                               key=f"start_time_{i}"))

                    if st.checkbox("Specify Session End Time", key=f"specify-session-end-time-{i}"):
                        runsession.set_endTime(st.time_input(label="End time of course session",
                                                             help="HH:mm:ss/HH:mm format only",
                                                             key=f"end_time_{i}"))

                    st.markdown(f"###### Venue")
                    if st.checkbox("Specify Venue", key=f"specify-venue-{i}"):
                        if st.checkbox("Specify Venue Block", key=f"specify-venue-block-{i}"):
                            runsession.set_venue_block(
                                st.text_input(label="Block",
                                              key=f"block_optional_{i}",
                                              help="Course run block",
                                              max_chars=10))

                        if st.checkbox("Specify Venue Street", key=f"specify-venue-street-{i}"):
                            runsession.set_venue_street(st.text_input(label="Street",
                                                                      key=f"street_optional_{i}",
                                                                      help="Course run street",
                                                                      max_chars=32))

                        if st.checkbox("Specify Venue Building", key=f"specify-venue-building-{i}"):
                            runsession.set_venue_building(st.text_input(label="Building",
                                                                        key=f"building_optional_{i}",
                                                                        help="Course run building",
                                                                        max_chars=66))

                        runsession.set_venue_floor(st.text_input(label="Floor",
                                                                 key=f"floor_{i}",
                                                                 help="Course run floor",
                                                                 max_chars=3))
                        runsession.set_venue_unit(st.text_input(label="Unit",
                                                                key=f"unit_{i}",
                                                                help="Course run unit",
                                                                max_chars=5))
                        runsession.set_venue_postalCode(st.text_input(label="Postal Code",
                                                                      key=f"postalCode_{i}",
                                                                      help="Course run postal code",
                                                                      max_chars=6))
                        runsession.set_venue_room(st.text_input(label="Room",
                                                                key=f"room_{i}",
                                                                help="Course run room",
                                                                max_chars=255))

                        if st.checkbox("Specify Wheelchair Access?", key=f"specify-wheelchair-access-{i}"):
                            runsession.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                                               options=["Select a value", "Yes", "No"],
                                                                               key=f"wheelchair_access_{i}",
                                                                               help="Indication that the course "
                                                                                    "run location is wheelchair "
                                                                                    "accessible"))

                        if st.checkbox("Specify Primary Venue?", key=f"specify-primary-venue-{i}"):
                            runsession.set_venue_primaryVenue(st.selectbox(
                                label="Primary Venue",
                                options=["Select a value", "Yes", "No"],
                                help="Indication that the course session is the Primary Venue. If `true`, API "
                                     "will pick the venue information from course run and update to session venue",
                                key=f"venue_primary_venue_{i}"
                            ))

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

        if st.checkbox("Specify Trainer", key="specify-trainer"):
            with st.expander("Add Trainer Details", expanded=False):
                num_trainers: int = st.number_input(label="Key in the number of trainers in the Course Run",
                                                    key="num_trainers_edit",
                                                    min_value=0,
                                                    value=0)

                for i in range(num_trainers):
                    runtrainer = RunTrainerInfo()

                    st.markdown(f"##### Trainer {i + 1}")
                    runtrainer.set_trainer_type_code(st.text_input(label="Trainer Type",
                                                                   key=f"trainer_code_{i}",
                                                                   max_chars=1))
                    runtrainer.set_trainer_type_description(st.text_input(label="Trainer Description",
                                                                          key=f"trainer_description_{i}",
                                                                          max_chars=128))

                    # index number is skipped
                    if st.checkbox("Specify Trainer ID?", key=f"specify-trainer-id-{i}"):
                        runtrainer.set_trainer_id(st.text_input(label="Trainer ID",
                                                                key=f"trainer_id_{i}",
                                                                max_chars=50))

                    st.markdown("###### Trainer Particulars")
                    runtrainer.set_indexNumber(st.number_input(label="Trainer Index",
                                                               min_value=0,
                                                               value=0,
                                                               key=f"trainer_index_number_{i}"))
                    runtrainer.set_trainer_name(st.text_input(label="Trainer Name",
                                                              key=f"trainer_name_{i}",
                                                              max_chars=66))
                    runtrainer.set_trainer_email(st.text_input(label="Trainer Email",
                                                               key=f"trainer_email_{i}",
                                                               max_chars=320))

                    st.markdown("###### Trainer ID")
                    col1, col2 = st.columns(2)

                    with col1:
                        runtrainer.set_trainer_idType(st.selectbox(label="Trainer ID Code",
                                                                   options=ID_TYPE.keys(),
                                                                   format_func=lambda x: f"{x}: {ID_TYPE[x]}",
                                                                   help="Trainer ID Type Code",
                                                                   key=f"trainer_id_code_{i}"))

                    with col2:
                        runtrainer.set_trainer_idNumber(st.text_input(label="Trainer ID Number",
                                                                      key=f"trainer_id_number_{i}",
                                                                      help="Refers to the NRIC/FIN/Passport "
                                                                           "number of the trainer",
                                                                      max_chars=50))

                    st.markdown("###### Trainer Roles")
                    if st.checkbox("Trainer", key=f"select-trainer-role-{i}"):
                        runtrainer.add_trainer_role({
                            "id": 1,
                            "name": "Trainer"
                        })
                    if st.checkbox("Assessor", key=f"select-assessor-roles-{i}"):
                        runtrainer.add_trainer_role({
                            "id": 2,
                            "name": "Assessor"
                        })

                    st.markdown("###### Trainer Profile")
                    if st.checkbox("Specify In Training Provider Profile?",
                                   key=f"specify-training-provider-profile-{i}"):
                        runtrainer.set_inTrainingProviderProfile(st.selectbox(
                            label="Set in-training provider profile",
                            options=["Select a value", "Yes", "No"],
                            key=f"in_training_provider_profile_{i}"))

                    if st.checkbox("Specify Domain Area of Practice?", key=f"specify-domain-area-{i}"):
                        runtrainer.set_domainAreaOfPractice(st.text_area(
                            label="Domain Area of Practice",
                            help="This field indicates the Key Domain/Sector Areas of practice of the trainer "
                                 "(required for new trainer).",
                            key=f"trainer_domainarea_{i}",
                            max_chars=1000))

                    if st.checkbox("Specify Experience?", key=f"specify-experience-{i}"):
                        runtrainer.set_experience(st.text_input(label="Experience",
                                                                key=f"experience_{i}",
                                                                max_chars=1000))

                    if st.checkbox("Specify LinkedIn URL?", key=f"specify-linkedin-url-{i}"):
                        runtrainer.set_linkedInURL(st.text_input(label="LinkedIn URL",
                                                                 key=f"linkedin_url_{i}",
                                                                 max_chars=255))

                    if st.checkbox("Specify Salutation ID?", key=f"specify-salutation-id-{i}"):
                        runtrainer.set_salutationId(st.selectbox(label="Salutations of the Trainer",
                                                                 options=SALUTATIONS.keys(),
                                                                 format_func=lambda x: SALUTATIONS[x]))

                    st.markdown("###### Photo")
                    if st.checkbox("Specify Photo Name?", key=f"specify-photo-name-{i}"):
                        runtrainer.set_photo_name(st.text_input(label="File Name",
                                                                key=f"file_name_{i}",
                                                                help="Physical file name of the course run",
                                                                max_chars=255))

                    if st.checkbox("Specify Photo Content?", key=f"specify-photo-content-{i}"):
                        runtrainer.set_photo_content(st.file_uploader(label="File Content",
                                                                      key=f"file_content_{i}",
                                                                      help="File content of the course run in "
                                                                           "binary",
                                                                      accept_multiple_files=False))

                    st.markdown("###### Linked SSEC EQAs")
                    linkedssec = st.number_input(
                        label="Number of Linked SSEC EQAs",
                        key=f"edit-linkedSsecEQAs-{i}",
                        min_value=0,
                        value=0,
                    )

                    for j in range(linkedssec):
                        # create a dict first then fill in
                        temp_ssec = {"ssecEQA": {}}

                        st.markdown(f"*Linked SSEC EQA {j + 1}*")

                        if st.checkbox("Specify SSEC EQA", key=f"edit-linkedSsecEQA-{i}-{j}"):
                            temp_ssec["ssecEQA"]["code"] = st.text_input(label="SSEC EQA Code",
                                                                         key=f"linkedSsecEQAs_code_edit_{i}_{j}",
                                                                         max_chars=2)

                        if st.checkbox("Specify SSEC EQA Description", key=f"edit-linkedSsecEQA-description-{i}-{j}"):
                            temp_ssec["description"] = st.text_area(label="Description",
                                                                    help="This field is used to indicate the "
                                                                         "qualification level of the trainer. "
                                                                         "For existing trainer, please do not "
                                                                         "input this information.",
                                                                    key=f"linkedSsecEQAs_description_{i}_{j}",
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

    if st.button("Send", key="edit_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        elif not runs:
            st.error("Make sure to fill in your CRN before proceeding!")
        else:
            errors = runinfo.validate()

            if errors is not None:
                st.error(
                    "Some errors are detected with your inputs:\n\n- " + "\n- ".join(errors)
                )
            else:
                request, response = st.tabs(["Request", "Response"])

                ec = None

                if runtype == "update":
                    ec = EditCourseRun(runs, include_expired, runinfo)
                elif runtype == "delete":
                    ec = DeleteCourseRun(runs, include_expired, runinfo)

                resp = None

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
    st.warning("**View Course Sessions requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-sessions-expired")

    crn = st.text_input("Key in the Course Reference Number", key="crn_view_sessions")
    runs = st.text_input("Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-view_sessions")

    month_value, year_value = None, None

    if st.checkbox("Specify Month and Year to retrieve?", key="view-sessions-month-year"):
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
    if st.button("Send", key="view_session_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        else:
            request, response = st.tabs(["Request", "Response"])

            vc = ViewCourseSessions(runs, crn, month_value, year_value, include_expired)
            resp = None

            with request:
                st.subheader("Request")
                st.code(repr(vc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: vc.execute())
