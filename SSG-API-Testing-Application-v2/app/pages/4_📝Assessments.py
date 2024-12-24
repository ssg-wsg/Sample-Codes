"""
This page is used to enable access to the Assessments API.

There are 4 main processes:
1. Create Assessment
    - This tab allows you to create an assessment record for a trainee enrolled in your course
2. Update/Void Assessment
    - This tab allows you to update or void a particular assessment record for a trainee
3. Find Assessment
    - This tab allows you to find assessment records that match the criteria that you have specified
4. Find Assessment
    - This tab allows you to view an assessment record by referencing the Assessment Reference Number
      associated with the assessment record

It is important to note that optional fields are always hidden behind a Streamlit checkbox to allow the backend
functions to clean up the request body and send requests that contains only non-null fields.
"""

import datetime
import os

import streamlit as st

from app.core.assessments.create_assessment import CreateAssessment
from app.core.assessments.update_void_assessment import UpdateVoidAssessment
from app.core.assessments.view_assessment import ViewAssessment
from app.core.assessments.search_assessment import SearchAssessment
from app.core.constants import (Grade, Results, IdTypeSummary, AssessmentUpdateVoidActions,
                                SortField, SortOrder)
from app.core.models.assessments import CreateAssessmentInfo, UpdateVoidAssessmentInfo, \
    SearchAssessmentInfo
from app.core.system.logger import Logger
from app.utils.http_utils import handle_response, handle_request
from app.utils.streamlit_utils import init, display_config, validation_error_handler, \
    does_not_have_url, does_not_have_keys, does_not_have_encryption_key
from app.utils.verify import Validators

from app.core.system.secrets import (
    ENV_NAME_ENCRYPT, ENV_NAME_CERT, ENV_NAME_KEY)

# initialise necessary variables
init()
LOGGER = Logger("Assessments API")

st.set_page_config(page_title="Assessments", page_icon="📝")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")

    if st.button("Configs", key="config_display", type="primary"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Assessments API")
st.markdown("The Assessments API allows you to create, update, void, find and view assessments that are "
            "assigned to your trainees in your courses!")
st.info("**These APIs requires your *requests payloads* to be encrypted and returns *encrypted responses*!**",
        icon="ℹ️")

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
        create_assessment_info.trainingPartner_uen = st.text_input(label="Training Partner UEN",
                                                                   key="create-assessment-tp-uen",
                                                                   value=("" if st.session_state["uen"] is None
                                                                          else st.session_state["uen"]),
                                                                   max_chars=12)

    create_assessment_info.trainingPartner_code = st.text_input(label="Enter the Training Partner Code",
                                                                max_chars=15,
                                                                help="Code for the training partner conducting the "
                                                                     "course for which the assessment result is "
                                                                     "being submitted",
                                                                key="create-assessment-training-partner-code")
    st.subheader("Course Info")
    create_assessment_info.course_referenceNumber = st.text_input(label="Enter the Course Reference Number",
                                                                  max_chars=100,
                                                                  help="The course reference number as in the "
                                                                       "Training Partners Gateway course registry",
                                                                  key="create-assessment-reference-number")
    create_assessment_info.course_runId = st.text_input(label="Enter the Course Run ID",
                                                        max_chars=20,
                                                        help="The ID for the course run",
                                                        key="create-assessment-run-id")

    st.subheader("Trainee Info")
    col1, col2 = st.columns(2)
    create_assessment_info.trainee_idType = col1.selectbox(label="Enter the Trainee ID Type",
                                                           options=IdTypeSummary,
                                                           format_func=lambda x: x.value,
                                                           help="This describes the type of ID provided",
                                                           key="create-assessment-trainee-id-type")
    create_assessment_info.trainee_id = col2.text_input(label="Enter the Trainee ID Number",
                                                        max_chars=20,
                                                        help="This is the individual's government-issued "
                                                             "ID number",
                                                        key="create-assessment-trainee-id")

    if create_assessment_info.trainee_idType != IdTypeSummary.OTHERS and len(create_assessment_info.trainee_id) > 0 \
            and not Validators.verify_nric(create_assessment_info.trainee_id):
        st.warning(f"**ID Number** may not be valid!", icon="⚠️")

    create_assessment_info.trainee_fullName = st.text_input(label="Enter the Trainee Full Name",
                                                            max_chars=200,
                                                            help="This is the individual's full name",
                                                            key="create-assessment-trainee-full-name")

    st.subheader("Assessment Info")
    col3, col4 = st.columns(2)
    if col3.checkbox("Specify Grade?", key="specify-create-grade"):
        create_assessment_info.grade = col3.selectbox(label="Select Grade",
                                                      options=Grade,
                                                      format_func=lambda x: x.value,
                                                      help="A grade, entered as A-F",
                                                      key="create-assessment-grade")

    if col4.checkbox("Specify Score?", key="specify-create-score"):
        create_assessment_info.score = col4.number_input(label="Select Score",
                                                         min_value=0,
                                                         value=0,
                                                         help="A numerical score or percentage, entered "
                                                              "as a whole number",
                                                         key="create-assessment-score")

    if col3.checkbox("Specify Skill Code?", key="specify-create-assessment-skill-code"):
        create_assessment_info.skillCode = col3.text_input(label="Enter the Skill Code",
                                                           max_chars=30,
                                                           help="The competency or skill code assessed for the "
                                                                "course, derived from the course data in the "
                                                                "Training Partners Gateway",
                                                           key="create-assessment-skill-code")

    if col4.checkbox("Specify Conferring Institute Code?", key="specify-create-assessment-conferring-institute-code"):
        create_assessment_info.conferringInstitute_code = col4.text_input(label="Enter the Conferring Institute Code",
                                                                          help="This field refers to the UEN/branch "
                                                                               "code of the supporting assessment TP "
                                                                               "for the results. If left blank, the "
                                                                               "trainingProvider.code is set as the "
                                                                               "default value!")

    create_assessment_info.result = st.selectbox(label="Select Result",
                                                 options=Results,
                                                 format_func=lambda x: str(x),
                                                 help="The outcome of the assessment, specified as pass or fail",
                                                 key="create-assessment-result")
    create_assessment_info.assessmentDate = st.date_input(label="Select Assessment Date",
                                                          min_value=datetime.date(1900, 1, 1),
                                                          help="Date the assessment was conducted",
                                                          key="create-assessment-date")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(create_assessment_info.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="edit-button", type="primary"):
        LOGGER.info("Attempting to send request to Create Assessment API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        
        elif not st.session_state["default_secrets"] and does_not_have_encryption_key():
            LOGGER.error("Invalid AES-256 encryption key provided!")
            st.error("Invalid **AES-256 Encryption Key** provided!", icon="🚨")

        elif st.session_state["default_secrets"] and not st.session_state["secret_fetched"]:
            LOGGER.error(
                "User chose to use defaults but defaults are not set!")
            st.error(
                "There are no default secrets set, please provide your own secrets.", icon="🚨")

        elif not st.session_state["default_secrets"] and does_not_have_keys():
            LOGGER.error(
                "Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        
        else:
            errors, warnings = create_assessment_info.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                ec = CreateAssessment(create_assessment_info)

                with request:
                    LOGGER.info("Showing preview of request...")
                    if st.session_state["default_secrets"]:
                        handle_request(ec, os.environ.get(
                            ENV_NAME_ENCRYPT, ''))
                    else:
                        handle_request(ec, st.session_state["encryption_key"])

                with response:
                    # pass in the correct secrets based on user choice
                    if st.session_state["default_secrets"]:
                        LOGGER.info("Executing request with defaults...")
                        handle_response(lambda: ec.execute(os.environ.get(ENV_NAME_ENCRYPT, ''),
                                                           os.environ.get(ENV_NAME_CERT, ''),
                                                           os.environ.get(ENV_NAME_KEY, '')),
                                        os.environ.get(ENV_NAME_ENCRYPT, ''))
                    else:
                        LOGGER.info("Executing request with user's secrets...")
                        handle_response(lambda: ec.execute(st.session_state["encryption_key"],
                                                           st.session_state["cert_pem"],
                                                           st.session_state["key_pem"]),
                                        st.session_state["encryption_key"])


with update_void:
    st.header("Update/Void Assessment")
    st.markdown("You can use this API to update or void an assessment record for trainees enrolled in your courses.")

    update_void_assessment = UpdateVoidAssessmentInfo()
    update_void_assessment.action = st.selectbox(label="Select Action to Perform",
                                                 options=AssessmentUpdateVoidActions,
                                                 format_func=lambda x: str(x).upper(),
                                                 help="Select UPDATE to update an assessment record, and "
                                                      "VOID to void an assessment record",
                                                 key="update-void-assessment-action")

    st.subheader("Course Info")
    assessment_ref_num = st.text_input(label="Enter the Assessment Reference Number",
                                       max_chars=100,
                                       help="Assessment reference number in the "
                                            "Training Partners Gateway",
                                       key="update-void-assessment-reference-number")

    if update_void_assessment.is_update():
        st.subheader("Trainee Info")
        if st.checkbox("Update Trainee Full Name?", key="update-void-trainee-info"):
            update_void_assessment.trainee_fullName = st.text_input(label="Enter the Trainee Full Name",
                                                                    max_chars=200,
                                                                    help="The individual's full name",
                                                                    key="update-void-assessment-trainee-full-name")

        st.subheader("Assessment Info")
        col1, col2, col3 = st.columns(3)
        if col1.checkbox("Update Grade?", key="update-void-grade"):
            update_void_assessment.grade = col1.selectbox(label="Select Grade",
                                                          options=Grade,
                                                          format_func=lambda x: x.value,
                                                          help="The letter grade of the assessment, entered as A-F, "
                                                               "if applicable",
                                                          key="update-void-assessment-grade")

        if col2.checkbox("Update Score?", key="update-void-score"):
            update_void_assessment.score = col2.number_input(label="Select Score",
                                                             min_value=0,
                                                             value=0,
                                                             help="The numerical score or percentage score of the "
                                                                  "assessment, entered as a whole number, "
                                                                  "if applicable",
                                                             key="update-void-assessment-score")

        if col3.checkbox("Update Assessment Result?", key="update-void-assessment-results"):
            update_void_assessment.result = col3.selectbox(label="Select Result",
                                                           options=Results,
                                                           format_func=lambda x: str(x),
                                                           help="The outcome of the assessment, specified as pass, "
                                                                "fail or exempt",
                                                           key="update-void-assessment-result")

        if st.checkbox("Update Skill Code?", key="will-update-void-assessment-skill-code"):
            update_void_assessment.skillCode = st.text_input(label="Enter the Skill Code",
                                                             max_chars=30,
                                                             help="The competency or skill code assessed for the "
                                                                  "course, derived from the course data in the "
                                                                  "Training Partners Gateway",
                                                             key="update-void-assessment-skill-code")

        if st.checkbox("Update Assessment Date?", key="will-update-void-assessment-date"):
            update_void_assessment.assessmentDate = st.date_input(label="Select Assessment Date",
                                                                  min_value=datetime.date(1900, 1, 1),
                                                                  help="Date the assessment was conducted",
                                                                  key="update-void-assessment-date")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(update_void_assessment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="update-void-button", type="primary"):
        LOGGER.info("Attempting to send request to Update/Void Assessment API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif len(assessment_ref_num) == 0:
            LOGGER.error("Missing Assessment Reference Number!")
            st.error("Make sure that you have entered in your **Assessment Reference Number** before proceeding!",
                     icon="🚨")
        
        elif not st.session_state["default_secrets"] and does_not_have_encryption_key():
            LOGGER.error("Invalid AES-256 encryption key provided!")
            st.error("Invalid **AES-256 Encryption Key** provided!", icon="🚨")

        elif st.session_state["default_secrets"] and not st.session_state["secret_fetched"]:
            LOGGER.error(
                "User chose to use defaults but defaults are not set!")
            st.error(
                "There are no default secrets set, please provide your own secrets.", icon="🚨")

        elif not st.session_state["default_secrets"] and does_not_have_keys():
            LOGGER.error(
                "Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
            
        else:
            errors, warnings = update_void_assessment.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                uva = UpdateVoidAssessment(assessment_ref_num, update_void_assessment)

                with request:
                    LOGGER.info("Showing preview of request...")
                    if st.session_state["default_secrets"]:
                        handle_request(uva, os.environ.get(
                            ENV_NAME_ENCRYPT, ''))
                    else:
                        handle_request(uva, st.session_state["encryption_key"])

                with response:
                    # pass in the correct secrets based on user choice
                    if st.session_state["default_secrets"]:
                        LOGGER.info("Executing request with defaults...")
                        handle_response(lambda: uva.execute(os.environ.get(ENV_NAME_ENCRYPT, ''),
                                                           os.environ.get(ENV_NAME_CERT, ''),
                                                           os.environ.get(ENV_NAME_KEY, '')),
                                        os.environ.get(ENV_NAME_ENCRYPT, ''))
                    else:
                        LOGGER.info("Executing request with user's secrets...")
                        handle_response(lambda: uva.execute(st.session_state["encryption_key"],
                                                           st.session_state["cert_pem"],
                                                           st.session_state["key_pem"]),
                                        st.session_state["encryption_key"])


with find:
    st.header("Find Assessments")
    st.markdown("You can use this API to find/search/query for an assessment record.")
    search_assessment = SearchAssessmentInfo()

    st.subheader("Query Parameters")
    col1, col2 = st.columns(2)

    if col1.checkbox("Specify Last Update Date From?", key="search-last-update-date-from"):
        search_assessment.lastUpdateDateTo = col1.date_input(label="Select Last Update Date",
                                                             help="Last update date of records from",
                                                             key="search-last-update-date-from-input")

    if col2.checkbox("Specify Last Update Date To?", key="search-last-update-date-to"):
        search_assessment.lastUpdateDateFrom = col2.date_input(label="Select Last Update Date",
                                                               help="Last update date of records to",
                                                               key="search-last-update-date-to-input")

    if col1.checkbox("Specify Sort By Field?", key="search-sort-by-field"):
        search_assessment.sortBy_field = col1.selectbox(label="Select Sort By Field",
                                                        options=SortField,
                                                        format_func=lambda x: str(x),
                                                        help="Field to sort by. Available fields:\n"
                                                             "- 'updatedOn'\n"
                                                             "- 'createdOn'\n"
                                                             "- 'assessmentDate'\n",
                                                        key="search-sort-by-field-input")

    if col2.checkbox("Specify Sort Order?", key="search-sort-order"):
        search_assessment.sortBy_order = col2.selectbox(label="Select Sort Order",
                                                        options=SortOrder,
                                                        format_func=lambda x: str(x),
                                                        help="Sort order",
                                                        key="search-sort-by-order-input")

    search_assessment.page = st.number_input(label="Page Number",
                                             min_value=0,
                                             value=0,
                                             help="Page number of page displayed, starting from 0",
                                             key="search-page-number")
    search_assessment.pageSize = st.number_input(label="Page Size",
                                                 min_value=1,
                                                 max_value=100,
                                                 help="The number of items to be displayed on one page.",
                                                 key="search-page-size")

    st.subheader("Assessment Query Parameters")
    if st.checkbox("Specify Course Run ID?", key="search-course-run-id"):
        search_assessment.courseRunId = st.text_input(label="Select Course Run ID",
                                                      help="The ID for the course run, configured in My SkillsFuture",
                                                      key="search-course-run-id-input",
                                                      max_chars=20)

    if st.checkbox("Specify Course Reference Number?", key="search-course-reference-number"):
        search_assessment.courseReferenceNumber = st.text_input(label="Select Course Reference Number",
                                                                max_chars=50,
                                                                help="The course reference number of the course in "
                                                                     "the Training Partners Gateway course registry",
                                                                key="search-course-reference-number-input")

    if st.checkbox("Specify Trainee ID?", key="search-trainee-id"):
        search_assessment.trainee_id_ = st.text_input(label="Select Trainee ID Number",
                                                      max_chars=20,
                                                      help="Government-issued ID number",
                                                      key="search-trainee-id-input")

    if st.checkbox("Specify Enrolment Reference Number?", key="search-enrolment-reference-number"):
        search_assessment.enrolment_referenceNumber = st.text_input(label="Select Enrolment Reference Number",
                                                                    help="The reference number of the associated "
                                                                         "enrolment in the Training Partners "
                                                                         "Gateway, if applicable",
                                                                    key="search-enrolment-reference-number-input")

    if st.checkbox("Specify Skill Code?", key="search-skill-code"):
        search_assessment.skillCode = st.text_input(label="Enter the Skill Code",
                                                    max_chars=30,
                                                    help="The competency or skill code assessed for the course, "
                                                         "derived from the course data in the Training Partners "
                                                         "Gateway",
                                                    key="search-skill-code-input")

    st.subheader("Training Partner Parameters")
    search_assessment.trainingPartner_uen = st.text_input(label="Enter the Training Partner UEN",
                                                          max_chars=12,
                                                          value=("" if st.session_state["uen"] is None
                                                                 else st.session_state["uen"]),
                                                          help="UEN of the training partner organisation "
                                                               "conducting the course for which the assessment "
                                                               "result is being submitted")

    search_assessment.trainingPartner_code = st.text_input(label="Enter the Training Partner Code",
                                                           max_chars=15,
                                                           help="Code for the training partner conducting the "
                                                                "course for which the trainee is enrolled",
                                                           key="search-training-partner-code-input")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(search_assessment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="search-button", type="primary"):
        LOGGER.info("Attempting to send request to Search Assessment API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        
        elif not st.session_state["default_secrets"] and does_not_have_encryption_key():
            LOGGER.error("Invalid AES-256 encryption key provided!")
            st.error("Invalid **AES-256 Encryption Key** provided!", icon="🚨")

        elif st.session_state["default_secrets"] and not st.session_state["secret_fetched"]:
            LOGGER.error(
                "User chose to use defaults but defaults are not set!")
            st.error(
                "There are no default secrets set, please provide your own secrets.", icon="🚨")

        elif not st.session_state["default_secrets"] and does_not_have_keys():
            LOGGER.error(
                "Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
            
        else:
            errors, warnings = search_assessment.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                sa = SearchAssessment(search_assessment)

                with request:
                    LOGGER.info("Showing preview of request...")
                    if st.session_state["default_secrets"]:
                        handle_request(sa, os.environ.get(
                            ENV_NAME_ENCRYPT, ''))
                    else:
                        handle_request(sa, st.session_state["encryption_key"])

                with response:
                    # pass in the correct secrets based on user choice
                    if st.session_state["default_secrets"]:
                        LOGGER.info("Executing request with defaults...")
                        handle_response(lambda: sa.execute(os.environ.get(ENV_NAME_ENCRYPT, ''),
                                                           os.environ.get(ENV_NAME_CERT, ''),
                                                           os.environ.get(ENV_NAME_KEY, '')),
                                        os.environ.get(ENV_NAME_ENCRYPT, ''))
                    else:
                        LOGGER.info("Executing request with user's secrets...")
                        handle_response(lambda: sa.execute(st.session_state["encryption_key"],
                                                           st.session_state["cert_pem"],
                                                           st.session_state["key_pem"]),
                                        st.session_state["encryption_key"])


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

    if st.button("Send", key="view-assessment-button", type="primary"):
        LOGGER.info("Attempting to send request to View Assessment API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif arn is None or len(arn) == 0:
            LOGGER.error("No Assessment Reference Number provide! Request aborted...")
            st.error("Please enter in the **Assessment Reference Number**!", icon="🚨")
        
        elif not st.session_state["default_secrets"] and does_not_have_encryption_key():
            LOGGER.error("Invalid AES-256 encryption key provided!")
            st.error("Invalid **AES-256 Encryption Key** provided!", icon="🚨")

        elif st.session_state["default_secrets"] and not st.session_state["secret_fetched"]:
            LOGGER.error(
                "User chose to use defaults but defaults are not set!")
            st.error(
                "There are no default secrets set, please provide your own secrets.", icon="🚨")

        elif not st.session_state["default_secrets"] and does_not_have_keys():
            LOGGER.error(
                "Missing Certificate or Private Keys, request aborted!")
            st.error("Make sure that you have uploaded your **Certificate and Private Key** before proceeding!",
                     icon="🚨")
        
        else:
            request, response = st.tabs(["Request", "Response"])
            va = ViewAssessment(arn)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(va)

            with response:
                # pass in the correct secrets based on user choice
                if st.session_state["default_secrets"]:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: va.execute(os.environ.get(ENV_NAME_ENCRYPT, ''),
                                                        os.environ.get(ENV_NAME_CERT, ''),
                                                        os.environ.get(ENV_NAME_KEY, '')),
                                    os.environ.get(ENV_NAME_ENCRYPT, ''))
                else:
                    LOGGER.info("Executing request with user's secrets...")
                    handle_response(lambda: va.execute(st.session_state["encryption_key"],
                                                        st.session_state["cert_pem"],
                                                        st.session_state["key_pem"]),
                                    st.session_state["encryption_key"])
