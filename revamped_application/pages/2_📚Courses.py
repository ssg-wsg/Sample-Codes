import streamlit as st

from datetime import datetime

from core.courses.delete_course_run import DeleteCourseRun
from core.courses.view_course_run import ViewCourseRun
from core.courses.edit_course_run import EditCourseRun
from core.models.course_runs import RunInfo, RunSessionInfo, RunTrainerInfo, DeleteRunInfo, \
    MODE_OF_TRAINING_MAPPING, ID_TYPE, SALUTATIONS
from utils.http import handle_error
from utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Courses")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()


st.header("Courses API")
st.markdown("The Courses API allows you to search, filter and compare different SkillsFuture Credit "
            "eligible courses that have been published on the MySkillsFuture portal! Through this "
            "API you can access details regarding course categories, related courses, popular "
            "courses, featured courses, course brochures, and more! You can also manage your webhook "
            "events and subscriptions via this API!")

view, add, delete, edit, sessions = st.tabs([
    "View Course Runs", "Add Courses Runs", "Delete Courses Runs", "Edit Courses Runs", "View Course Sessions"
])

with view:
    st.subheader("View Course Runs")
    st.markdown("You can retrieve your course run details based on course reference number and course run ID using "
                "this API!")

    include_expired = st.checkbox("Include expired courses?", key="view-expired")
    runs = st.text_input("Enter Course Run ID",
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
    pass

with delete:
    st.header("Delete Course Runs")
    st.markdown("You can use this API to delete course run with sessions. Note that this API uses "
                "the **Edit Course Runs** API to achieve the deletion request!")
    st.warning("**Delete Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

    del_runinfo = DeleteRunInfo()

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-expired-delete")
    del_runinfo.set_crid(st.text_input("Key in the Course Run Number", key="crn_delete"))
    runs = st.text_input("Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-delete")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")
    if st.button("Send", key="delete_button"):
        if not st.session_state["uen"]:
            st.error("Make sure to fill in your UEN before proceeding!")
        elif not runs:
            st.error("Make sure to fill in your CRN or Course Run ID before proceeding!")
        else:
            errors = del_runinfo.validate()

            if errors is not None:
                st.error(
                    "Some errors are detected with your inputs:\n" + "\n".join(errors)
                )
            else:
                request, response = st.tabs(["Request", "Response"])

                ec = DeleteCourseRun(runs, include_expired, del_runinfo)
                resp = None

                with request:
                    st.subheader("Request")
                    st.code(repr(ec), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: ec.execute())

with edit:
    st.header("Edit Course Runs")
    st.markdown("You can use this API to edit your course runs. Note that this API uses "
                "the **Edit Course Runs** API to achieve the edit request!")
    st.warning("**Edit Course Runs requires your UEN to proceed. Make sure that you have loaded it up "
               "properly under the Home page before proceeding!**")

    # ===== BASIC RUN INFO ===== #
    st.subheader("`run` details")
    st.markdown("Note that `registrationDates`, `courseDates`, `scheduleInfoType`, `scheduleInfo`, "
                "`courseVacancy`, `modeOfTraining` are required for this update action!")
    # create a store for the parameters to pass into the backend
    runinfo = RunInfo()

    include_expired = st.selectbox(label="Include expired courses?",
                                   options=["Select a value", "Yes", "No"],
                                   key="view-expired-edit")
    runinfo.set_crid(st.text_input("Key in the Course Run Number", key="crn_edit"))
    runs = st.text_input("Enter Course Run ID",
                         help="The Course Run Id is used as a URL for GET Request Call"
                              "Example: https://api.ssg-wsg.sg/courses/runs/{runId}",
                         key="course-run-id-edit")
    runinfo.set_sequence_number(st.number_input(
        label="Run Sequence Number",
        value=0,
        help="Defaults to 0"
    ))

    st.markdown("#### Registration Dates")
    runinfo.set_registrationDates_opening(st.date_input(label="Opening Date", key="opening_date",
                                                        help=RunInfo.REGISTRATION_DATE_DESCRIPTION_OPENING))
    runinfo.set_registrationDates_closing(st.date_input(label="Closing Date", key="closing_date",
                                                        help=RunInfo.REGISTRATION_DATE_DESCRIPTION_CLOSING))

    st.markdown("#### Course Dates")
    runinfo.set_courseDates_start(st.date_input(label="Course Start Date", key="start_date",
                                                help="Course run start opening dates as YYYYMMDD"))
    runinfo.set_courseDates_end(st.date_input(label="Course End Date", key="end_date",
                                              help="Course run end opening dates as YYYYMMDD"))

    st.markdown("#### Schedule Info Type")
    runinfo.set_scheduleInfoType_code(st.text_input(label="Schedule Code", key="schedule_code",
                                                    help="Course run schedule info code"))
    runinfo.set_scheduleInfoType_description(st.text_area("Schedule Description", key="schedule_description",
                                                          help="Course run schedule info description",
                                                          max_chars=32))

    runinfo.set_scheduleInfo(st.text_input(label="Schedule Info", key="schedule_info",
                                           help="String representing Course run schedule info"))

    st.markdown("#### Venue Info")
    runinfo.set_venue_block(st.text_input(label="Block", key="block_optional", help="Course run block",
                                          max_chars=10))
    runinfo.set_venue_street(st.text_input(label="Street", key="street_optional", help="Course run street",
                                           max_chars=32))
    runinfo.set_venue_floor(st.text_input(label="Floor", key="floor", help="Course run floor", max_chars=3))
    runinfo.set_venue_unit(st.text_input(label="Unit", key="unit", help="Course run unit", max_chars=5))
    runinfo.set_venue_building(st.text_input(label="Building", key="building_optional", help="Course run building",
                                             max_chars=66))
    runinfo.set_venue_postalCode(st.text_input(label="Postal Code", key="postalCode", help="Course run postal code",
                                               max_chars=6))
    runinfo.set_venue_room(st.text_input(label="Room", key="room", help="Course run room", max_chars=255))
    runinfo.set_venue_wheelChairAccess(st.selectbox("Wheelchair Access",
                                                    options=["Select a value", "Yes", "No"],
                                                    key="wheelchair_access",
                                                    help="Indication that the course run location is wheelchair "
                                                         "accessible"))

    st.markdown("#### Course Intake Details")
    runinfo.set_intakeSize(st.number_input("Intake Size",
                                           key="intake_size",
                                           value=0,
                                           min_value=0,
                                           help="Course run intake size. It represents the max number of pax "
                                                "for a class"))
    runinfo.set_threshold(st.number_input("Threshold",
                                          key="threshold",
                                          value=0,
                                          min_value=0,
                                          help="Course run threshold. Any additional pax that can register above "
                                               "maximum pax.\ne.g. threshold = `10`, then total allowed "
                                               "registration pax is `intake size + threshold = 60`"))
    runinfo.set_registeredUserCount(st.number_input("Registered Users Count",
                                                    key="registered_user_count",
                                                    value=0,
                                                    min_value=0,
                                                    help="Course run registered user count. This number cannot "
                                                         "be more than `intake size + threshold`"))

    st.markdown("#### Course Admin Details")
    runinfo.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                            options=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                                            format_func=lambda x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}"))
    runinfo.set_courseAdminEmail(st.text_input(label="Course Admin Email", key="course_admin_email",
                                               help="Course admin email is under course run level "
                                                    "that can receive the email from 'QR code "
                                                    "Attendance Taking', 'Course Atendance with error'"
                                                    " and 'Trainer information not updated'",
                                               max_chars=255))

    st.markdown("#### Course Vacancy Details")
    runinfo.set_courseVacancy_code(st.text_input(label="Vacancy Code", key="vacancy_code",
                                                 help="Course run vacancy code",
                                                 max_chars=1))
    runinfo.set_courseVacancy_description(st.text_input(label="Vacancy Description",
                                                        key="vacancy_description",
                                                        help="Course run vacancy description",
                                                        max_chars=128))

    st.markdown("#### File Details")
    runinfo.set_file_Name(st.text_input(label="File Name", key="file_name", help="Physical file name of the course run",
                                        max_chars=255))
    runinfo.set_file_content(st.file_uploader(
        label="File Content",
        key="file_content",
        help="File content of the course run in binary",
        accept_multiple_files=False
    ))

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
        num_sessions: int = st.number_input("Key in the number of sessions in the Course Run",
                                            key="num_sessions",
                                            min_value=0,
                                            value=0)

        for i in range(num_sessions):
            runsession: RunSessionInfo = RunSessionInfo("update")

            st.markdown(f"##### Session {i + 1}")
            runsession.set_session_id(st.text_input(label="Course session ID", key=f"session_id_{i}",
                                                    max_chars=300))
            runsession.set_modeOfTraining(st.selectbox(label="Mode of Training",
                                                       options=["1", "2", "3", "4", "5", "6", "7", "8", "9"],
                                                       format_func=lambda
                                                           x: f"{x}: {MODE_OF_TRAINING_MAPPING[x]}",
                                                       key=f"mode_of_training_{i}"))
            runsession.set_startDate(st.date_input("Start date of course session",
                                                   help="YYYYMMDD or YYYY-MM-DD format only",
                                                   key=f"start_date_{i}"))

            if runsession.modeOfTraining in ["2", "4"]:
                runsession.set_endDate(runsession.startDate)
                runsession.set_startTime(datetime(hour=0, minute=0, year=runsession.startDate.year,
                                                  month=runsession.startDate.month, day=runsession.startDate.day)
                                         .time())
                runsession.set_endTime(datetime(hour=23, minute=59, year=runsession.startDate.year,
                                                month=runsession.startDate.month, day=runsession.startDate.day)
                                       .time())
                runsession.set_endTime(st.time_input("End time of course session",
                                                     help="HH:mm:ss/HH:mm format only",
                                                     key=f"end_time_{i}"))
                st.info(f"End date of course session is automatically set to **{runsession.startDate}**")
                st.info(f"Start and end time set to **12:00 AM to 11:59 PM** respectively")
            else:
                runsession.set_endDate(st.date_input("End date of course session",
                                                     help="YYYYMMDD or YYYY-MM-DD format only",
                                                     key=f"end_date_{i}"))
                runsession.set_startTime(st.time_input("Start time of course session",
                                                       help="HH:mm:ss/HH:mm format only",
                                                       key=f"start_time_{i}"))
                runsession.set_endTime(st.time_input("End time of course session",
                                                     help="HH:mm:ss/HH:mm format only",
                                                     key=f"end_time_{i}"))

            st.markdown(f"###### Venue")
            runsession.set_venue_block(st.text_input(label="Block", key=f"block_optional_{i}", help="Course run block",
                                                     max_chars=10))
            runsession.set_venue_street(st.text_input(label="Street", key=f"street_optional_{i}",
                                                      help="Course run street", max_chars=32))
            runsession.set_venue_floor(st.text_input(label="Floor", key=f"floor_{i}", help="Course run floor",
                                                     max_chars=3))
            runsession.set_venue_unit(st.text_input(label="Unit", key=f"unit_{i}", help="Course run unit",
                                                    max_chars=5))
            runsession.set_venue_building(st.text_input(label="Building", key=f"building_optional_{i}",
                                                        help="Course run building", max_chars=66))
            runsession.set_venue_postalCode(st.text_input(label="Postal Code", key=f"postalCode_{i}",
                                                          help="Course run postal code", max_chars=6))
            runsession.set_venue_room(st.text_input(label="Room", key=f"room_{i}", help="Course run room",
                                                    max_chars=255))
            runsession.set_venue_wheelChairAccess(st.selectbox(label="Wheelchair Access",
                                                               options=["Select a value", "Yes", "No"],
                                                               key=f"wheelchair_access_{i}",
                                                               help="Indication that the course run "
                                                                    "location is wheelchair accessible"))
            runsession.set_venue_primaryVenue(st.selectbox(
                label="Primary Venue",
                options=["Select a value", "Yes", "No"],
                help="Indication that the course session is the Primary Venue. If `true`, API will pick the venue "
                     "information from course run and update to session venue",
                key=f"venue_primary_venue_{i}"
            ))

            runinfo.add_session(runsession)

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
        num_trainers: int = st.number_input("Key in the number of trainers in the Course Run",
                                            key="num_trainers",
                                            min_value=0,
                                            value=0)

        for i in range(num_trainers):
            runtrainer = RunTrainerInfo("update")

            st.markdown(f"##### Trainer {i + 1}")
            runtrainer.set_trainer_type_code(st.selectbox(
                label="Trainer Type",
                options=["1", "2"],
                help="1 for Existing, 2 for New",
                format_func=lambda x: "1: Existing" if x == "1" else "2: New",
                key=f"trainer_code_{i}"
            ))
            runtrainer.set_trainer_type_description(st.text_input(
                label="Trainer Description",
                key=f"trainer_description_{i}",
                max_chars=128
            ))
            runtrainer.set_trainer_id(st.text_input(
                label="Trainer ID",
                key=f"trainer_id_{i}",
                max_chars=50
            ))

            if runtrainer.is_new_trainer():
                st.markdown("###### Trainer Particulars")
                runtrainer.set_indexNumber(st.number_input(
                    label="Trainer Index",
                    min_value=0,
                    value=0,
                    key=f"trainer_index_number_{i}",
                ))
                runtrainer.set_trainer_name(st.text_input(
                    label="Trainer Name",
                    key=f"trainer_name_{i}",
                    max_chars=66
                ))
                runtrainer.set_trainer_email(st.text_input(
                    label="Trainer Email",
                    key=f"trainer_email_{i}",
                    max_chars=320
                ))

                st.markdown("###### Trainer ID")
                runtrainer.set_trainer_idNumber(st.text_input(
                    label="Trainer ID Number",
                    key=f"trainer_id_number_{i}",
                    help="Refers to the NRIC/FIN/Passport number of the trainer",
                    max_chars=50
                ))
                runtrainer.set_trainer_idType(st.selectbox(
                    label="Trainer ID Code",
                    options=["SB", "SP", "SO", "FP", "OT"],
                    format_func=lambda x: f"{x}: {ID_TYPE[x]}",
                    help="Trainer ID Type Code",
                    key=f"trainer_id_code_{i}"
                ))

                st.info(f"**Trainer ID Type Description:** {runtrainer.idType_description}")

                st.divider()
                st.markdown("###### Trainer Roles")
                num_roles = st.number_input(
                    label="Number of roles to add for Trainer",
                    min_value=0,
                    value=0,
                    key=f"trainer_roles_number_{i}"
                )

                for j in range(num_roles):
                    st.markdown(f"**Role {j + 1}**")
                    temp_role = {
                        "id": st.number_input(
                            "Role ID",
                            key=f"trainer_roles_id_number_{i}_{j}",
                            value=0
                        ),
                        "name": st.text_input(
                            "Role Description",
                            key=f"trainer_roles_name_{i}_{j}",
                            help="Trainer Role description"
                        )
                    }

                    runtrainer.add_trainer_role(temp_role)

                st.divider()
                runtrainer.set_inTrainingProviderProfile(st.selectbox(
                    label="Set in-training provider profile",
                    options=["Select a value", "Yes", "No"],
                    key=f"in_training_provider_profile_{i}"))
                runtrainer.set_domainAreaOfPractice(st.text_area(
                    "Domain Area of Practice",
                    help="This field indicates the Key Domain/Sector Areas of practice of the trainer (required for "
                         "new trainer).",
                    key=f"trainer_domainarea_{i}",
                    max_chars=1000))
                runtrainer.set_experience(st.text_input(
                    "Experience",
                    key=f"experience_{i}",
                    max_chars=1000
                ))
                runtrainer.set_linkedInURL(st.text_input(
                    "LinkedIn URL",
                    key=f"linkedin_url_{i}",
                    max_chars=255
                ))
                runtrainer.set_salutationId(st.selectbox(
                    label="Salutations of the Trainer",
                    options=[1, 2, 3, 4, 5, 6],
                    format_func=lambda x: SALUTATIONS[x]
                ))

                st.markdown(f"*Photo*")
                runtrainer.set_photo_name(st.text_input(label="File Name",
                                                        key=f"file_name_{i}",
                                                        help="Physical file name of the course run",
                                                        max_chars=255))
                runtrainer.set_photo_content(st.file_uploader(
                    label="File Content",
                    key=f"file_content_{i}",
                    help="File content of the course run in binary",
                    accept_multiple_files=False
                ))

                st.divider()
                linkedssec = st.number_input(
                    label="Number of Linked SSEC EQAs",
                    key="linkedSsecEQAs",
                    min_value=0,
                    value=0,
                )

                for j in range(linkedssec):
                    # create a dict first then fill in
                    temp_ssec = {"ssecEQA": {}}

                    st.markdown(f"*Linked SSEC EQA {j + 1}*")
                    temp_ssec["description"] = st.text_area(
                        "Description",
                        help="This field is used to indicate the qualification level of the trainer. For existing "
                             "trainer, please do not input this information.",
                        key=f"linkedSsecEQAs_description_{i}_{j}",
                        max_chars=1000
                    )
                    temp_ssec["code"] = st.text_input(
                        "SSEC EQA Code",
                        key=f"linkedSsecEQAs_code_{i}_{j}",
                        max_chars=2
                    )
                    runtrainer.add_linkedSsecEQA(temp_ssec)

            runinfo.add_linkCourseRunTrainer(runtrainer)

    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(repr(runinfo))

    st.divider()
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
                    "Some errors are detected with your inputs:\n" + "\n".join(errors)
                )
            else:
                request, response = st.tabs(["Request", "Response"])

                ec = EditCourseRun(runs, include_expired, runinfo)
                resp = None

                with request:
                    st.subheader("Request")
                    st.code(repr(ec), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: ec.execute())

with sessions:
    pass
