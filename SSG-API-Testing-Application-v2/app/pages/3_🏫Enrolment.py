import datetime

import streamlit as st

from app.core.models.enrolment import (CreateEnrolmentInfo, UpdateEnrolmentInfo,
                                       CancelEnrolmentInfo, UpdateEnrolmentFeeCollectionInfo,
                                       SearchEnrolmentInfo)
from app.core.enrolment.create_enrolment import CreateEnrolment
from app.core.enrolment.view_enrolment import ViewEnrolment
from app.core.enrolment.update_enrolment import UpdateEnrolment
from app.core.enrolment.cancel_enrolment import CancelEnrolment
from app.core.enrolment.search_enrolment import SearchEnrolment
from app.core.enrolment.update_enrolment_fee_collection import UpdateEnrolmentFeeCollection
from app.core.constants import (IdTypeSummary, CollectionStatus, CancellableCollectionStatus,
                                SponsorshipType, EnrolmentSortField, SortOrder,
                                EnrolmentCourseStatus)
from app.utils.http_utils import handle_request, handle_response
from app.utils.streamlit_utils import init, display_config, validation_error_handler
from app.utils.verify import Validators

init()

st.set_page_config(page_title="Enrolment", page_icon="🏫")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")
    if st.button("Configs", key="config_display"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Enrolment API")
st.markdown("Integration with the Enrolment APIs enable enrolment records to be updated on the Training Partners "
            "Gateway. It facilitates enrolment of a trainee to a course run and allows the updating, cancellation, "
            "searching and viewing of enrolment records!")
st.info("**This API requires your *request payloads* to be encrypted and will return *encrypted responses*!**",
        icon="ℹ️")
st.info("To scroll through the different tabs below, you can hold `Shift` and scroll with your mouse scroll, or you "
        "can use the arrow keys to navigate between the tabs!", icon="ℹ️")

create, update, cancel, search, view, update_fee = st.tabs([
    "Create Enrolment", "Update Enrolment", "Cancel Enrolment", "Search Enrolment", "View Enrolment",
    "Update Enrolment Fee Collection"
])


with create:
    st.header("Create Enrolment")
    st.markdown("Create enrolment records, as well as updating, cancelling and searching of existing enrolment "
                "records!")

    create_enrolment = CreateEnrolmentInfo()

    if st.session_state["uen"] is None:
        st.warning("**Create Enrolment requires your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    st.subheader("Course Info")
    if st.checkbox("Specify Course Run ID?", key="specify-enrolment-course-run-id"):
        create_enrolment.course_run_id = st.text_input(label="Course Run ID",
                                                       help="SSG-generated Unique ID for the course run",
                                                       key="enrolment-course-run-id",
                                                       max_chars=20)
    create_enrolment.course_referenceNumber = st.text_input(label="Course Reference Number",
                                                            help="SSG-generated Unique reference number for the "
                                                                 "course",
                                                            key="enrolment-course-reference-number",
                                                            max_chars=100)

    st.subheader("Trainee Info")
    col1, col2 = st.columns(2)
    create_enrolment.trainee_idType = col1.selectbox(label="Trainee ID Type",
                                                     options=IdTypeSummary,
                                                     format_func=lambda x: x.value,
                                                     help="Trainee ID Type",
                                                     key="enrolment-id-type")
    create_enrolment.trainee_id = col2.text_input(label="Trainee ID",
                                                  help="Trainee's government-issued ID number",
                                                  key="enrolment-trainee-id")

    st.markdown("#### Payment Info")
    if st.checkbox("Specify Fee Discount Amount?", key="specify-enrolment-trainee-fees-discount-amount"):
        create_enrolment.trainee_fees_discountAmount = st.number_input(label="Trainee Fees Discount",
                                                                       value=0.00,
                                                                       step=0.01,
                                                                       min_value=0.00,
                                                                       help="Amount of discount the training "
                                                                            "partner is deducting from course "
                                                                            "fees",
                                                                       key="enrolment-trainee-fees-discount-"
                                                                           "amount")

    create_enrolment.trainee_fees_collectionStatus = st.selectbox(label="Trainee Fees Collection Status",
                                                                  options=CollectionStatus,
                                                                  format_func=lambda x: x.value,
                                                                  help="Status of the trainee's or employer's "
                                                                       "payment of the course fees to the "
                                                                       "training partner",
                                                                  key="enrolment-trainee-fees-collection-status")

    st.markdown("#### Employer Info")
    if st.checkbox("Specify Employer UEN?", key="specify-enrolment-employer-uen"):
        uen = st.text_input(label="Employer UEN",
                            max_chars=50,
                            help="Employer organisation's UEN",
                            key="enrolment-employer-uen")

        if len(uen) > 0 and not Validators.verify_uen(uen):
            st.warning("**Employer UEN** is not a valid UEN!", icon="⚠️")

        create_enrolment.employer_uen = uen

    if st.checkbox("Specify Employer Full Name?", key="specify-enrolment-employer-contact-full-name"):
        create_enrolment.employer_fullName = st.text_input(
            label="Employer Full Name",
            max_chars=50,
            help="The employer contact's person name",
            key="enrolment-employer-contact-full-name")

    if st.checkbox("Specify Employer Email Address?", key="specify-enrolment-employer-contact-email-address"):
        create_enrolment.employer_emailAddress = st.text_input(
            label="Employer Email Address",
            max_chars=100,
            help="The employer contact's email address",
            key="enrolment-employer-contact-email-address")

        if len(create_enrolment.employer_emailAddress) > 0:
            if not Validators.verify_email(create_enrolment.employer_emailAddress):
                st.warning(f"Email format is not valid!", icon="⚠️")

    col1, col2, col3 = st.columns(3)

    if col1.checkbox("Specify Employer Phone Number Area Code?",
                     key="specify-enrolment-employer-contact-number-area-code"):
        create_enrolment.employer_areaCode = col1.text_input(
            label="Employer Contact Number Area Code",
            max_chars=10,
            help="Area code of phone number",
            key="enrolment-employer-contact-number-area-code")

    if col2.checkbox("Specify Employer Phone Number Country Code",
                     key="specify-enrolment-employer-contact-number-country-code"):
        create_enrolment.employer_countryCode = col2.text_input(
            label="Employer Contact Number Country",
            max_chars=5,
            help="Country code of the phone number",
            key="enrolment-employer-contact-number-country-code")

    if col3.checkbox("Specify Employer Phone Number?", key="specify-enrolment-employer-contact-phone-number"):
        create_enrolment.employer_phoneNumber = col3.text_input(
            label="Employer Phone Number",
            max_chars=20,
            help="The phone number",
            key="enrolment-employer-contact-number-phone-number")

    st.markdown("#### Trainee Particulars")
    if st.checkbox("Specify Trainee Full Name?", key="specify-enrolment-trainee-full-name"):
        create_enrolment.trainee_fullName = st.text_input(
            label="Trainee Full Name",
            max_chars=200,
            help="The trainee's full name",
            key="enrolment-trainee-full-name")
    create_enrolment.trainee_dateOfBirth = st.date_input(label="Trainee Date of Birth",
                                                         min_value=datetime.date(1900, 1, 1),
                                                         help="Trainee Date of Birth",
                                                         key="enrolment-trainee-date-of-birth")
    create_enrolment.trainee_emailAddress = st.text_input(label="Trainee Email Address",
                                                          max_chars=100,
                                                          help="The trainee's email address",
                                                          key="enrolment-trainee-email-address")
    if len(create_enrolment.trainee_emailAddress) > 0:
        if not Validators.verify_email(create_enrolment.trainee_emailAddress):
            st.warning(f"Email format is not valid!", icon="⚠️")

    col1, col2, col3 = st.columns(3)

    if col1.checkbox("Specify Trainee Phone Number Area Code",
                     key="specify-enrolment-trainee-phone-number-area-code"):
        create_enrolment.trainee_contactNumber_areaCode = col1.text_input(label="Trainee Area Code",
                                                                          max_chars=10,
                                                                          help="Area code of the phone number",
                                                                          key="enrolment-trainee-phone-number-area-"
                                                                              "code")

    create_enrolment.trainee_contactNumber_countryCode = col2.text_input(label="Trainee Country Code",
                                                                         max_chars=5,
                                                                         help="Country code of the phone number",
                                                                         key="enrolment-trainee-phone-number-"
                                                                             "country-code")

    create_enrolment.trainee_contactNumber_phoneNumber = col3.text_input(label="Trainee Phone Number",
                                                                         max_chars=20,
                                                                         help="The phone number",
                                                                         key="enrolment-trainee-phone-number-"
                                                                             "phone-number")

    if st.checkbox("Specify Trainee Date of Enrolment?", key="specify-enrolment-trainee-date-of-enrolment"):
        create_enrolment.trainee_enrolmentDate = st.date_input(label="Trainee Date of Enrolment",
                                                               min_value=datetime.date(1900, 1, 1),
                                                               help="Trainee Date of Enrolment",
                                                               key="enrolment-trainee-date-of-enrolment")

    create_enrolment.trainee_sponsorshipType = st.selectbox(label="Trainee Sponsorship Type",
                                                            options=SponsorshipType,
                                                            format_func=lambda x: x.value,
                                                            key="enrolment-trainee-sponsorship-type")

    st.subheader("Training Partner Info")
    uen = st.text_input(label="Training Partner UEN",
                        key="enrolment-training-partner-uen",
                        value=st.session_state["uen"] if "uen" in st.session_state else "",
                        max_chars=12)

    if uen is not None and len(uen) > 0 and not Validators.verify_uen(uen):
        st.warning("**Training Provider UEN** is not a valid UEN!", icon="⚠️")
    elif uen is not None and len(uen) > 0 and Validators.verify_nric(uen):
        create_enrolment.trainingPartner_uen = uen

    create_enrolment.trainingPartner_code = st.text_input(label="Training Partner Code",
                                                          max_chars=15,
                                                          help="Code for the training partner conducting the course "
                                                               "for which the trainee is enrolled",
                                                          key="enrolment-training-partner-code")
    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(create_enrolment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="create-button"):
        if not st.session_state["uen"] and not create_enrolment.has_overridden_uen():
            st.error("Make sure to fill in your UEN via the **Home page** or via the **Specify Training Partner UEN**"
                     " before proceeding!", icon="🚨")
        else:
            errors, warnings = create_enrolment.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                ce = CreateEnrolment(create_enrolment)

                with request:
                    handle_request(ce, require_encryption=True)

                with response:
                    handle_response(lambda: ce.execute(), require_decryption=True)


with update:
    st.header("Update Enrolment")
    st.markdown("SSG will allow the creation of enrolment records, as well as updating, cancelling and searching of "
                "existing enrolment records")

    update_enrolment = UpdateEnrolmentInfo()

    update_enrolment.course_run_id = st.text_input(label="Course Run ID",
                                                   help="SSG-generated Unique ID for the course run",
                                                   key="update-enrolment-course-run-id",
                                                   max_chars=20)
    enrolment_reference_num = st.text_input(label="Enrolment Reference Number",
                                            help="SSG enrolment reference number",
                                            key="update-enrolment-enrolment-reference-number")

    st.subheader("Course Info")
    st.markdown("#### Payment Info")
    if st.checkbox("Specify Fees Discount?", key="specify-update-enrolment-trainee-fees-discount-amount"):
        update_enrolment.trainee_fees_discountAmount = st.number_input(label="Trainee Fees Discount",
                                                                       value=0.00,
                                                                       step=0.01,
                                                                       min_value=0.00,
                                                                       help="Amount of discount the training "
                                                                            "partner is deducting from course fees",
                                                                       key="update-enrolment-trainee-fees-"
                                                                           "discount-amount")

    if st.checkbox("Specify Fee Collection Status?", key="specify-update-enrolment-trainee-fees-collection-status"):
        update_enrolment.trainee_fees_collectionStatus = st.selectbox(label="Trainee Fees Collection Status",
                                                                      options=CancellableCollectionStatus,
                                                                      format_func=lambda x: x.value,
                                                                      help="Status of the trainee's or employer's "
                                                                           "payment of the course fees to the "
                                                                           "training partner",
                                                                      key="update-enrolment-trainee-fees-"
                                                                          "collection-status")

    st.markdown("#### Employer Info")
    if st.checkbox("Specify Employer Full Name?", key="specify-update-enrolment-employer-contact-full-name"):
        update_enrolment.employer_fullName = st.text_input(
            label="Employer Full Name",
            max_chars=50,
            help="The employer contact's person name",
            key="update-enrolment-employer-contact-full-name")

    if st.checkbox("Specify Employer Email Address?", key="specify-update-enrolment-employer-contact-email-address"):
        update_enrolment.employer_emailAddress = st.text_input(
            label="Employer Email Address",
            max_chars=100,
            help="The employer contact's email address",
            key="update-enrolment-employer-contact-email-address")

        if len(update_enrolment.employer_emailAddress) > 0:
            if not Validators.verify_email(update_enrolment.employer_emailAddress):
                st.warning(f"Email format is not valid!", icon="⚠️")

    col1, col2, col3 = st.columns(3)

    if col1.checkbox("Specify Employer Phone Number Area Code?",
                     key="specify-update-enrolment-employer-contact-number-area-code"):
        update_enrolment.employer_areaCode = col1.text_input(
            label="Employer Contact Number Area Code",
            max_chars=10,
            help="Area code of phone number",
            key="update-enrolment-employer-contact-number-area-code")

    if col2.checkbox("Specify Employer Phone Number Country Code",
                     key="specify-update-enrolment-employer-contact-number-country-code"):
        update_enrolment.employer_countryCode = col2.text_input(
            label="Employer Contact Number Country",
            max_chars=5,
            help="Country code of the phone number",
            key="update-enrolment-employer-contact-number-country-code")

    if col3.checkbox("Specify Employer Phone Number?", key="specify-update-enrolment-employer-contact-phone-number"):
        update_enrolment.employer_phoneNumber = col3.text_input(
            label="Employer Phone Number",
            max_chars=20,
            help="The phone number",
            key="update-enrolment-employer-contact-number-phone-number")

    st.markdown("#### Trainee Particulars")
    if st.checkbox("Specify Trainee Email Address?", key="specify-update-enrolment-trainee-email-address"):
        update_enrolment.trainee_emailAddress = st.text_input(label="Trainee Email Address",
                                                              max_chars=100,
                                                              help="The trainee's email address",
                                                              key="update-enrolment-trainee-email-address")

        if len(update_enrolment.trainee_emailAddress) > 0:
            if not Validators.verify_email(update_enrolment.trainee_emailAddress):
                st.warning(f"Email format is not valid!", icon="⚠️")

    col1, col2, col3 = st.columns(3)
    if col1.checkbox("Specify Trainee Phone Number Area Code",
                     key="specify-update-enrolment-trainee-phone-number-area-code"):
        update_enrolment.trainee_contactNumber_areaCode = col1.text_input(label="Trainee Phone Number Area Code",
                                                                          max_chars=10,
                                                                          help="Area code of the phone number",
                                                                          key="update-enrolment-trainee-phone-number"
                                                                              "-area-code")
    if col2.checkbox("Specify Trainee Phone Number Country Code",
                     key="specify-update-enrolment-trainee-phone-number-country-code"):
        update_enrolment.trainee_contactNumber_countryCode = col2.text_input(label="Trainee Contact Number Country",
                                                                             max_chars=5,
                                                                             help="Country code of the phone number",
                                                                             key="update-enrolment-trainee-phone-"
                                                                                 "number-country-code")

    if col3.checkbox("Specify Trainee Phone Number Country Code",
                     key="specify-update-enrolment-trainee-phone-number-phone-number"):
        update_enrolment.trainee_contactNumber_phoneNumber = col3.text_input(label="Trainee Phone Number",
                                                                             max_chars=20,
                                                                             help="The phone number",
                                                                             key="update-enrolment-trainee-phone-"
                                                                                 "number-phone-number")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(update_enrolment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="update-button"):
        if len(enrolment_reference_num) == 0:
            st.error("Make sure to fill in your enrolment reference number before proceeding!", icon="🚨")
        else:
            errors, warnings = update_enrolment.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                ue = UpdateEnrolment(enrolment_reference_num, update_enrolment)

                with request:
                    handle_request(ue, require_encryption=True)

                with response:
                    handle_response(lambda: ue.execute(), require_decryption=True)


with cancel:
    st.header("Cancel Enrolment")
    st.markdown("SSG will allow the creation of enrolment records, as well as updating, cancelling and searching of "
                "existing enrolment records")

    cancel_enrolment = CancelEnrolmentInfo()
    enrolment_reference_num = st.text_input(label="Enrolment Reference Number",
                                            help="SSG enrolment reference number",
                                            key="cancel-enrolment-enrolment-reference-number")

    cancel_enrolment.course_run_id = st.text_input(label="Course Run ID",
                                                   help="SSG Course Run ID",
                                                   key="cancel-enrolment-course-run-id")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(cancel_enrolment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="cancel-button"):
        if len(enrolment_reference_num) == 0:
            st.error("Make sure to fill in your **Enrolment Reference Number** before proceeding!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])

            errors, warnings = cancel_enrolment.validate()

            if validation_error_handler(errors, warnings):
                cancel_en = CancelEnrolment(enrolment_reference_num, cancel_enrolment)

                with request:
                    handle_request(cancel_en, require_encryption=True)

                with response:
                    handle_response(lambda: cancel_en.execute(), require_decryption=True)


with search:
    st.header("Search Enrolment")
    st.markdown("SSG will allow the creation of enrolment records, as well as updating, cancelling and searching "
                "of existing enrolment records")

    if st.session_state["uen"] is None:
        st.warning("**Search Enrolment may require your UEN to proceed. Make sure that you have loaded it up "
                   "properly under the Home page before proceeding!**", icon="⚠️")

    search_enrolment = SearchEnrolmentInfo()

    st.subheader("Meta Info")
    col1, col2 = st.columns(2)

    with col1:
        if st.checkbox("Specify Last Updated Date From?", key="specify-search-enrolment-last-updated-from"):
            search_enrolment.lastUpdateDateFrom = st.date_input(label="Last Updated Date From",
                                                                key="search-enrolment-last-updated-from",
                                                                min_value=datetime.date(1900, 1, 1),
                                                                format="YYYY-MM-DD",
                                                                help="This parameter is mandatory if retrieveType is "
                                                                     "DELTA. This will return records with last "
                                                                     "update date same or greater than this "
                                                                     "input value. Format YYYY-MM-DD.")

    with col2:
        if st.checkbox("Specify Last Updated Date To?", key="specify-search-enrolment-last-updated-to"):
            search_enrolment.lastUpdateDateTo = st.date_input(label="Last Updated Date To",
                                                              key="search-enrolment-last-updated-to",
                                                              min_value=datetime.date(1900, 1, 1),
                                                              format="YYYY-MM-DD",
                                                              help="Optional parameter. This will return records up "
                                                                   "till the specified date. Format YYYY-MM-DD.")

    st.subheader("Sort By Info")
    col3, col4 = st.columns(2)

    with col3:
        if st.checkbox("Specify Sort By Field?", key="specify-search-enrolment-sort-by-field"):
            search_enrolment.sortBy_field = st.selectbox(label="Sort By Field",
                                                         options=EnrolmentSortField,
                                                         format_func=lambda x: x.value,
                                                         help="Field to sort by. Available fields -updatedOn, "
                                                              "-createdOn. Will default to updatedOn if null",
                                                         key="search-enrolment-sort-by-field")

    with col4:
        if st.checkbox("Specify Sort By Order?", key="specify-search-enrolment-sort-by-order"):
            search_enrolment.sortBy_order = st.selectbox(label="Sort By Order",
                                                         options=SortOrder,
                                                         format_func=lambda x: str(x),
                                                         help="Sort order. Ascending - asc, Descending - desc. "
                                                              "Will default to desc if null",
                                                         key="search-enrolment-sort-by-order")

    st.subheader("Enrolment Info")
    if st.checkbox("Specify Course Run ID?", key="specify-search-enrolment-course-run-id"):
        search_enrolment.course_run_id = st.text_input(label="Course Run ID",
                                                       key="search-enrolment-course-run-id",
                                                       help="The ID for the course run",
                                                       max_chars=20)

    if st.checkbox("Specify Enrolment Reference Number?", key="specify-search-enrolment-enrolment-reference-number"):
        search_enrolment.course_referenceNumber = st.text_input(label="Enrolment Reference Number",
                                                                key="search-enrolment-enrolment-reference-number",
                                                                help="The Enrolment Reference Number",
                                                                max_chars=100)

    if st.checkbox("Specify Enrolment Status?", key="specify-search-enrolment-status"):
        search_enrolment.course_status = st.selectbox(label="Enrolment Status",
                                                      options=EnrolmentCourseStatus,
                                                      format_func=lambda x: x.value,
                                                      key="search-enrolment-status",
                                                      help="Status of enrolment records to be searched")

    col5, col6 = st.columns(2)
    with col5:
        if st.checkbox("Specify Trainee ID Type?", key="specify-search-enrolment-trainee-id-type"):
            search_enrolment.trainee_idType = st.selectbox(label="Trainee ID Type",
                                                           options=IdTypeSummary,
                                                           key="search-enrolment-trainee-id-type",
                                                           help="Trainee's ID type")

    with col6:
        if st.checkbox("Specify Trainee ID?", key="specify-search-enrolment-trainee-id"):
            search_enrolment.trainee_id = st.text_input(label="Trainee ID",
                                                        key="search-enrolment-trainee-id",
                                                        help="Trainee's government-issued ID number",
                                                        max_chars=20)

    if st.checkbox("Specify Fee Collection Status?", key="specify-search-enrolment-fee-collection-status"):
        search_enrolment.trainee_fees_feeCollectionStatus = st.selectbox(label="Fee Collection Status",
                                                                         options=CancellableCollectionStatus,
                                                                         format_func=lambda x: x.value,
                                                                         key="search-enrolment-fee-collection-status",
                                                                         help="Status of the trainee's or employer's "
                                                                              "payment of the course fees "
                                                                              "to the training partner")

    if st.checkbox("Specify Employee UEN?", key="specify-search-enrolment-employee-uen"):
        uen = st.text_input(label="Employee UEN",
                            key="search-enrolment-employee-uen",
                            max_chars=50,
                            help="Employer organisation's UEN number")

        if len(uen) > 0 and not Validators.verify_uen(uen):
            st.warning("**Employer UEN** is not a valid UEN!", icon="⚠️")

        search_enrolment.employer_uen = uen

    if st.checkbox("Specify Enrolment Date?", key="specify-search-enrolment-date"):
        search_enrolment.trainee_enrolmentDate = st.date_input(label="Enrolment Date",
                                                               min_value=datetime.date(1900, 1, 1),
                                                               key="search-enrolment-date",
                                                               format="YYYY-MM-DD",
                                                               help="Enrolment date")

    if st.checkbox("Specify Sponsorship Type?", key="specify-search-enrolment-sponsorship-type"):
        search_enrolment.trainee_sponsorshipType = st.selectbox(label="Sponsorship Type",
                                                                options=SponsorshipType,
                                                                format_func=lambda x: x.value,
                                                                help="Trainee's sponsorship type",
                                                                key="search-enrolment-sponsorship-type")

    if st.checkbox("Specify Training Partner UEN?", key="specify-search-enrolment-training-partner-uen",
                   help="If specified, this will override the UEN number provided under the Home page!"):
        uen = st.text_input(
            label="Training Partner UEN",
            max_chars=12,
            help="UEN of the training partner organisation conducting the course for "
                 "which the trainee is enrolled. Must match UEN passed in the header.\n\n"
                 "If unspecified, the default loaded training partner UEN will be used.",
            key="search-enrolment-training-partner-uen")

        if len(uen) > 0 and not Validators.verify_uen(uen):
            st.warning("**Training Partner UEN** is not a valid UEN!", icon="⚠️")

        search_enrolment.trainingPartner_uen = uen

    search_enrolment.trainingPartner_code = st.text_input(label="Training Partner Code",
                                                          key="search-enrolment-training-partner-code",
                                                          max_chars=15,
                                                          help="Code for the training partner conducting the "
                                                               "course for which the trainee is enrolled")

    st.subheader("Query Parameters Info")
    if st.checkbox("Specify Query Parameters?", key="specify-query-parameters"):
        search_enrolment.page = st.number_input(label="Page",
                                                min_value=0,
                                                value=0,
                                                key="search-enrolment-page-number",
                                                help="Page number of page displayed, starting from 0")

    search_enrolment.page_size = st.number_input(label="Page Size",
                                                 min_value=1,
                                                 max_value=100,
                                                 value=20,
                                                 key="search-enrolment-page-size",
                                                 help="The number of items to be displayed on one page.")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(search_enrolment.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="search-button"):
        if st.session_state["uen"] is None and not search_enrolment.has_overridden_uen():
            st.error("Make sure to fill in your UEN via the **Home page** or via the **Specify Training Partner UEN**"
                     " before proceeding!", icon="🚨")
        else:
            errors, warnings = search_enrolment.validate()

            if validation_error_handler(errors, warnings):
                request, response = st.tabs(["Request", "Response"])
                se = SearchEnrolment(search_enrolment)

                with request:
                    handle_request(se, require_encryption=True)

                with response:
                    handle_response(lambda: se.execute(), require_decryption=True)


with view:
    st.header("View Enrolment")
    st.markdown("SSG will allow the creation of enrolment records, as well as updating, cancelling and searching "
                "of existing enrolment records")

    st.subheader("Reference Number")
    ref_num = st.text_input(label="Enter Enrolment Record Reference Number",
                            help="SSG-generated unique reference number for the enrolment record",
                            key="view-enrolment-reference-number")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-button"):
        if len(ref_num) == 0:
            st.error("Please enter a valid **Enrolment Record Reference Number**!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            ve = ViewEnrolment(ref_num)

            with request:
                handle_request(ve)

            with response:
                handle_response(lambda: ve.execute(), require_decryption=True)


with update_fee:
    st.header("Update Enrolment Fee Collection")
    st.markdown("SSG will allow the creation of enrolment records, as well as updating, cancelling and searching "
                "of existing enrolment records")

    update_enrolment_fee_collection = UpdateEnrolmentFeeCollectionInfo()
    enrolment_reference_num = st.text_input(label="Enrolment Reference Number",
                                            help="SSG enrolment reference number",
                                            key="update-enrolment-fee-collection-enrolment-reference-number")

    update_enrolment_fee_collection.trainee_fees_collectionStatus = (
        st.selectbox(label="Trainee Fees Collection Status",
                     options=CancellableCollectionStatus,
                     format_func=lambda x: x.value,
                     help="Status of the trainee's or employer's payment of the course fees to the training "
                          "partner",
                     key="update-enrolment-fee-collection-trainee-fees-collection-status")
    )

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(update_enrolment_fee_collection.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="update-fee-button"):
        if len(enrolment_reference_num) == 0:
            st.error("Make sure to fill in your **Enrolment Reference Number** before proceeding!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            errors, warnings = update_enrolment_fee_collection.validate()

            if validation_error_handler(errors, warnings):
                eufc = UpdateEnrolmentFeeCollection(enrolment_reference_num, update_enrolment_fee_collection)

                with request:
                    handle_request(eufc, require_encryption=True)

                with response:
                    handle_response(lambda: eufc.execute(), require_decryption=True)
