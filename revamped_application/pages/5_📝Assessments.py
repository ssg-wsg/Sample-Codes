import streamlit as st

from core.assessments.create_assessment import CreateAssessment
from core.assessments.update_void_assessment import UpdateVoidAssessment
from core.assessments.view_assessment import ViewAssessment
from core.assessments.search_assessment import SearchAssessment
from core.constants import GRADES, RESULTS, ID_TYPE, ASSESSMENT_UPDATE_VOID_ACTIONS, SORT_FIELD, \
    SORT_ORDER
from core.models.assessments import CreateAssessmentInfo, UpdateVoidAssessmentInfo, \
    SearchAssessmentInfo
from utils.http_utils import handle_error
from utils.streamlit_utils import init, display_config

init()

st.set_page_config(page_title="Assessments", page_icon="📝")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("Assessments")
st.markdown("The Assessments API allows you to create, update, void, find and view assessments that are "
            "assigned to your trainees in your courses!")
st.info("**These APIs requires your *requests* to be encrypted and returns *encrypted responses*!**", icon="ℹ️")

create, update_void, find, view = st.tabs([
    "Create Assessment", "Update/Void Assessment", "Find Assessment", "View Assessment"
])

with create:
    st.header("Create Assessment")
    st.markdown("You can use this API to create an assessment record for trainees enrolled in your courses.")
    if st.session_state["uen"] is None:
        st.warning("**Create Assessment requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    create_assessment_info = CreateAssessmentInfo()
    if st.checkbox("Override Training Partner UEN?", key="specify-create-assessment-tp-uen",
                   help="If specified, this will override the UEN provided under the Home page!"):
        create_assessment_info.set_trainingPartner_uen(st.text_input(label="Training Partner UEN",
                                                                     key="create-assessment-tp-uen",
                                                                     max_chars=12))

    st.subheader("Course Info")
    create_assessment_info.set_course_runId(st.text_input(label="Enter the Course Run ID",
                                                          max_chars=20,
                                                          help="The ID for the course run",
                                                          key="create-assessment-run-id"))
    create_assessment_info.set_course_referenceNumber(st.text_input(label="Enter the Course Reference Number",
                                                                    max_chars=100,
                                                                    help="The course reference number as in the "
                                                                         "Training Partners Gateway course registry",
                                                                    key="create-assessment-reference-number"))

    st.subheader("Trainee Info")
    col1, col2 = st.columns(2)
    create_assessment_info.set_trainee_id_type(col1.selectbox(label="Enter the Trainee ID Type",
                                                              options=ID_TYPE,
                                                              help="This describes the type of ID provided",
                                                              key="create-assessment-trainee-id-type"))
    create_assessment_info.set_trainee_id(col2.text_input(label="Enter the Trainee ID Number",
                                                          max_chars=20,
                                                          help="This is the individual's government-issued "
                                                               "ID number",
                                                          key="create-assessment-trainee-id"))
    create_assessment_info.set_trainee_fullName(st.text_input(label="Enter the Trainee Full Name",
                                                              max_chars=200,
                                                              help="This is the individual's full name",
                                                              key="create-assessment-trainee-full-name"))

    st.subheader("Assessment Info")
    col3, col4 = st.columns(2)
    if col3.checkbox("Specify Grade?", key="specify-create-grade"):
        create_assessment_info.set_grade(col3.selectbox(label="Select Grade",
                                                        options=GRADES,
                                                        help="A grade, entered as A-F",
                                                        key="create-assessment-grade"))

    if col4.checkbox("Specify Score?", key="specify-create-score"):
        create_assessment_info.set_score(col4.number_input(label="Select Score",
                                                           min_value=0,
                                                           value=0,
                                                           help="A numerical score or percentage, entered "
                                                                "as a whole number",
                                                           key="create-assessment-score"))

    if col3.checkbox("Specify Skill Code?", key="specify-create-assessment-skill-code"):
        create_assessment_info.set_skillCode(col3.text_input(label="Enter the Skill Code",
                                                             max_chars=30,
                                                             help="The competency or skill code assessed for the "
                                                                  "course, derived from the course data in the "
                                                                  "Training Partners Gateway",
                                                             key="create-assessment-skill-code"))

    if col4.checkbox("Specify Conferring Institute Code?", key="specify-create-assessment-conferring-institute-code"):
        create_assessment_info.set_conferringInstitute_code(col4.text_input(label="Enter the Conferring Institute Code",
                                                                            help="This field refers to the UEN/branch "
                                                                                 "code of the supporting assessment TP "
                                                                                 "for the results. If left blank, the "
                                                                                 "trainingProvider.code is set as the "
                                                                                 "default value!"))

    create_assessment_info.set_result(st.selectbox(label="Select Result",
                                                   options=RESULTS,
                                                   help="The outcome of the assessment, specified as pass or fail",
                                                   key="create-assessment-result"))
    create_assessment_info.set_assessmentDate(st.date_input(label="Select Assessment Date",
                                                            help="Date the assessment was conducted",
                                                            key="create-assessment-date"))
    create_assessment_info.set_trainingPartner_code(st.text_input(label="Enter the Training Partner Code",
                                                                  max_chars=12,
                                                                  help="Code for the training partner conducting the "
                                                                       "course for which the assessment result is "
                                                                       "being submitted",
                                                                  key="create-assessment-training-partner-code"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(create_assessment_info.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="edit-button"):
        errors, warnings = create_assessment_info.validate()

        if len(warnings) > 0:
            st.warning(
                "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
            )

        if len(errors) > 0:
            st.error(
                "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
            )
        else:
            request, response = st.tabs(["Request", "Response"])
            ec = CreateAssessment(create_assessment_info)

            with request:
                st.subheader("Request")
                st.code(repr(ec), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: ec.execute())

with update_void:
    st.header("Update/Void Assessment")
    st.markdown("You can use this API to update or void an assessment record for trainees enrolled in your courses.")

    update_void_assessment = UpdateVoidAssessmentInfo()
    update_void_assessment.set_action(st.selectbox(label="Select Action to Perform",
                                                   options=ASSESSMENT_UPDATE_VOID_ACTIONS,
                                                   format_func=lambda x: x.upper(),
                                                   help="Select UPDATE to update an assessment record, and "
                                                        "VOID to void an assessment record",
                                                   key="update-void-assessment-action"))

    st.subheader("Course Info")
    update_void_assessment.set_assessment_referenceNumber(st.text_input(label="Enter the Assessment Reference Number",
                                                                        max_chars=100,
                                                                        help="Assessment reference number in the "
                                                                             "Training Partners Gateway",
                                                                        key="update-void-assessment-reference-number"))

    if update_void_assessment.is_update():
        st.subheader("Trainee Info")
        if st.checkbox("Update Trainee Full Name?", key="update-void-trainee-info"):
            update_void_assessment.set_trainee_fullName(st.text_input(label="Enter the Trainee Full Name",
                                                                      max_chars=200,
                                                                      help="The individual's full name",
                                                                      key="update-void-assessment-trainee-full-name"))

        st.subheader("Assessment Info")
        col1, col2, col3 = st.columns(3)
        if col1.checkbox("Update Grade?", key="update-void-grade"):
            update_void_assessment.set_grade(col1.selectbox(label="Select Grade",
                                                            options=GRADES,
                                                            help="The letter grade of the assessment, entered as A-F, "
                                                                 "if applicable",
                                                            key="update-void-assessment-grade"))

        if col2.checkbox("Update Score?", key="update-void-score"):
            update_void_assessment.set_score(col2.number_input(label="Select Score",
                                                               min_value=0,
                                                               value=0,
                                                               help="The numerical score or percentage score of the "
                                                                    "assessment, entered as a whole number, "
                                                                    "if applicable",
                                                               key="update-void-assessment-score"))

        if col3.checkbox("Update Assessment Result?", key="update-void-assessment-results"):
            update_void_assessment.set_result(col3.selectbox(label="Select Result",
                                                             options=RESULTS,
                                                             help="The outcome of the assessment, specified as pass, "
                                                                  "fail or exempt",
                                                             key="update-void-assessment-result"))

        if st.checkbox("Update Skill Code?", key="will-update-void-assessment-skill-code"):
            update_void_assessment.set_skillCode(st.text_input(label="Enter the Skill Code",
                                                               max_chars=30,
                                                               help="The competency or skill code assessed for the "
                                                                    "course, derived from the course data in the "
                                                                    "Training Partners Gateway",
                                                               key="update-void-assessment-skill-code"))

        if st.checkbox("Update Assessment Date?", key="will-update-void-assessment-date"):
            update_void_assessment.set_assessmentDate(st.date_input(label="Select Assessment Date",
                                                                    help="Date the assessment was conducted",
                                                                    key="update-void-assessment-date"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(update_void_assessment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="update-void-button"):
        errors, warnings = update_void_assessment.validate()

        if len(warnings) > 0:
            st.warning(
                "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
            )

        if len(errors) > 0:
            st.error(
                "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
            )
        else:
            request, response = st.tabs(["Request", "Response"])
            uva = UpdateVoidAssessment(update_void_assessment)

            with request:
                st.subheader("Request")
                st.code(repr(uva), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: uva.execute())

with find:
    st.header("Find Assessments")
    st.markdown("You can use this API to find/search/query for an assessment record.")
    search_assessment = SearchAssessmentInfo()

    st.subheader("Query Parameters")
    col1, col2 = st.columns(2)

    if col1.checkbox("Specify Last Update Date From?", key="search-last-update-date-from"):
        search_assessment.set_lastUpdateDateFrom(col1.date_input(label="Select Last Update Date",
                                                                 help="Last update date of records from",
                                                                 key="search-last-update-date-from-input"))

    if col2.checkbox("Specify Last Update Date To?", key="search-last-update-date-to"):
        search_assessment.set_lastUpdateDateTo(col2.date_input(label="Select Last Update Date",
                                                               help="Last update date of records to",
                                                               key="search-last-update-date-to-input"))

    if col1.checkbox("Specify Sort By Field?", key="search-sort-by-field"):
        search_assessment.set_sortBy_field(col1.selectbox(label="Select Sort By Field",
                                                          options=SORT_FIELD,
                                                          help="Field to sort by. Available fields:\n"
                                                               "- 'updatedOn'\n"
                                                               "- 'createdOn'\n"
                                                               "- 'assessmentDate'\n",
                                                          key="search-sort-by-field-input"))

    if col2.checkbox("Specify Sort Order?", key="search-sort-order"):
        search_assessment.set_sortBy_order(col2.selectbox(label="Select Sort Order",
                                                          options=SORT_ORDER.keys(),
                                                          help="Sort order",
                                                          format_func=lambda x: f"{x}: {SORT_ORDER[x]}",
                                                          key="search-sort-by-order-input"))

    search_assessment.set_page(st.number_input(label="Page Number",
                                               min_value=0,
                                               value=0,
                                               help="Page number of page displayed, starting from 0",
                                               key="search-page-number"))
    search_assessment.set_pageSize(st.number_input(label="Page Size",
                                                   min_value=1,
                                                   max_value=100,
                                                   help="The number of items to be displayed on one page.",
                                                   key="search-page-size"))

    st.subheader("Assessment Query Parameters")
    if st.checkbox("Specify Course Run ID?", key="search-course-run-id"):
        search_assessment.set_courseRunId(st.text_input(label="Select Course Run ID",
                                                        help="The ID for the course run, configured in My SkillsFuture",
                                                        key="search-course-run-id-input",
                                                        max_chars=20))

    if st.checkbox("Specify Course Reference Number?", key="search-course-reference-number"):
        search_assessment.set_courseReferenceNumber(st.text_input(label="Select Course Reference Number",
                                                                  max_chars=50,
                                                                  help="The course reference number of the course in "
                                                                       "the Training Partners Gateway course registry",
                                                                  key="search-course-reference-number-input"))

    if st.checkbox("Specify Trainee ID?", key="search-trainee-id"):
        search_assessment.set_trainee_id(st.text_input(label="Select Trainee ID Number",
                                                       max_chars=20,
                                                       help="Government-issued ID number",
                                                       key="search-trainee-id-input"))

    if st.checkbox("Specify Enrolment Reference Number?", key="search-enrolment-reference-number"):
        search_assessment.set_enrolment_referenceNumber(st.text_input(label="Select Enrolment Reference Number",
                                                                      help="The reference number of the associated "
                                                                           "enrolment in the Training Partners "
                                                                           "Gateway, if applicable",
                                                                      key="search-enrolment-reference-number-input"))

    if st.checkbox("Specify Skill Code?", key="search-skill-code"):
        search_assessment.set_skillCode(st.text_input(label="Enter the Skill Code",
                                                      max_chars=30,
                                                      help="The competency or skill code assessed for the course, "
                                                           "derived from the course data in the Training Partners "
                                                           "Gateway",
                                                      key="search-skill-code-input"))

    st.subheader("Training Partner Parameters")
    if st.checkbox("Specify Training Partner UEN?", key="search-training-partner-uen",
                   help="If this is enabled, it will **override the default UEN provided** in the Home page!"):
        search_assessment.set_trainingPartner_uen(st.text_input(label="Enter the Training Partner UEN",
                                                                max_chars=12,
                                                                help="UEN of the training partner organisation "
                                                                     "conducting the course for which the assessment "
                                                                     "result is being submitted"))

    if st.checkbox("Specify Training Partner Code?", key="search-training-partner-code"):
        search_assessment.set_trainingPartner_code(st.text_input(label="Enter the Training Partner Code",
                                                                 max_chars=15,
                                                                 help="Code for the training partner conducting the "
                                                                      "course for which the trainee is enrolled",
                                                                 key="search-training-partner-code-input"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(search_assessment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="search-button"):
        errors, warnings = search_assessment.validate()

        if len(warnings) > 0:
            st.warning(
                "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
            )

        if len(errors) > 0:
            st.error(
                "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
            )
        else:
            request, response = st.tabs(["Request", "Response"])
            sa = SearchAssessment(search_assessment)

            with request:
                st.subheader("Request")
                st.code(repr(sa), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: sa.execute())

with view:
    st.header("View Assessment")
    st.markdown("You can use this API to view an assessment record for trainees enrolled in your courses.")

    arn = st.text_input(label="Enter the Assessment Reference Number",
                        max_chars=100,
                        help="Assessment reference number",
                        key="view-assessment-reference-number")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-assessment-button"):
        if arn is None or len(arn) == 0:
            st.error("Please enter in the **Assessment Reference Number**!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            va = ViewAssessment(arn)

            with request:
                st.subheader("Request")
                st.code(repr(va), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: va.execute())
