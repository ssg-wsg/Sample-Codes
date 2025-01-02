"""
This page is used to enable access to the SkillsFuture Credit Pay API.

There are 5 main processes:
1. Encryption
    - This tab allows you to create a claims request, and obtain the encrypted API response that will be used in
      the sending of a form POST request to the SFC UAT Endpoint
2. Decryption
    - This tab allows you to decrypt the response from the above form POST request
3. Upload Supporting Documents
    - This tab allows you to upload any supporting documents for making a claims request
4. View Claims
    - This tab allows you to view the details of an existing claims request
5. Cancel Claims
    - This tab allows you to cancel a claims request

It is important to note that optional fields are always hidden behind a Streamlit checkbox to allow the backend
functions to clean up the request body and send requests that contains only non-null fields.
"""

import datetime
import os

import streamlit as st

from app.core.models.credit import (EncryptPayloadInfo, DecryptPayloadInfo, CancelClaimsInfo,
                                    UploadDocumentInfo, DocumentInfo)
from app.core.credit.view_claims import ViewClaims
from app.core.credit.cancel_claims import CancelClaims
from app.core.credit.encrypt_payload import EncryptPayload
from app.core.credit.decrypt_payload import DecryptPayload
from app.core.credit.upload_document import UploadDocument
from app.core.constants import CancelClaimsCode, PermittedFileUploadType
from app.core.system.logger import Logger
from app.utils.http_utils import handle_response, handle_request
from app.utils.streamlit_utils import init, display_config, validation_error_handler, does_not_have_url
from app.utils.verify import Validators

import app.core.system.secrets as Secrets

init()
LOGGER = Logger("SkillsFuture Credit Pay")

st.set_page_config(page_title="SkillsFuture Credit Pay", page_icon="💰")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")

    if st.button("Configs", key="config_display", type="primary"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("SkillsFuture Credit Pay API")
st.markdown("The SkillsFuture Credit Pay API serves to integrate the SkillsFuture Credit claim submission and course "
            "payment with course registration. It allows users to indicate the amount of credits to offset from "
            "the course fee payment during course registration. Please note that individuals must give their "
            "consent for the use of their SkillsFuture Credit information.")
st.info("**This API requires your *requests payloads* to be encrypted, and will return *encrypted responses*!**",
        icon="ℹ️")

encryption, decryption, upload, view, cancel = st.tabs([
    "Encryption", "Decryption", "Upload Supporting Documents", "View Claims", "Cancel Claims"
])

with encryption:
    st.header("SF Credit Claims Payment Request Encryption")
    st.markdown("As part of the efforts to make the data exchange secure, developers must encrypt the payload "
                "before making the browser form post to submit claims. Any payloads that are not encrypted will "
                "not be accepted by the system.")

    encrypt = EncryptPayloadInfo()

    st.subheader("Course Details")
    if st.checkbox("Specify Course Run ID?", key="specify-encryption-course-details-course-run-id"):
        encrypt.course_run_id = st.text_input(label="Course Run ID",
                                              key="encryption-course-details-course-run-id",
                                              help="Unique ID of the course run.")

    encrypt.course_id = st.text_input(label="Course ID",
                                      key="encryption-course-details-course-id",
                                      help="Unique ID of the run.")

    encrypt.course_fee = st.number_input(label="Course Fee",
                                         key="encryption-course-details-course-fee",
                                         help="Course Fee. Please ensure that the amount is in the currency "
                                              "format (i.e. with 2 decimal places).",
                                         value=0.00,
                                         min_value=0.00,
                                         step=0.01)
    encrypt.start_date = st.date_input(label="Start Date",
                                       min_value=datetime.date(1900, 1, 1),
                                       key="encryption-course-details-start-date",
                                       help="Start date of the course.",
                                       format="YYYY-MM-DD")

    st.subheader("Individual Details")
    encrypt.nric = st.text_input(label="NRIC",
                                 key="encryption-individual-nric",
                                 max_chars=9,
                                 help="Refers to the NRIC of the individual submitting the SFC Payment Request.")

    if len(encrypt.nric) > 0 and not Validators.verify_nric(encrypt.nric):
        st.warning("NRIC format is not valid!", icon="⚠️")

    encrypt.email = st.text_input(label="Email",
                                  key="encryption-individual-email",
                                  help="Email address of the individual.")

    if len(encrypt.email) > 0 and not Validators.verify_email(encrypt.email):
        st.warning("Email format is not valid!", icon="⚠️")

    encrypt.home_number = st.text_input(label="Home Number",
                                        key="encryption-individual-home-number",
                                        help="Home number of the individual. This is a mandatory field if "
                                             "mobile number is not provided.")
    encrypt.mobile_number = st.text_input(label="Mobile Number",
                                          key="encryption-individual-mobile-number",
                                          help="Mobile number of the individual. This is a mandatory field if "
                                               "home number is not provided.")

    st.subheader("Additional Information")
    if st.checkbox("Specify Additional Information?", key="specify-encryption-additional-information"):
        encrypt.additional_information = st.text_area(label="Additional Information",
                                                      key="encryption-additional-information",
                                                      help="Any additional information to be provided during SFC "
                                                           "Payment Request submission.")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(encrypt.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="encrypt-button", type="primary"):
        LOGGER.info("Attempting to send request to SF Credit Claims Payment Request Encryption API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")

        else:
            errors, warnings = encrypt.validate()

            if validation_error_handler(errors, warnings):
                enc = EncryptPayload(encrypt)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(enc, Secrets.get_encryption_key())

                with response:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: enc.execute(Secrets.get_encryption_key(),
                                                        os.environ.get(
                                                            ENV_NAME_CERT, ''),
                                                        Secrets.get_private_key()),
                                    Secrets.get_encryption_key()
                                    )

    st.divider()
    st.subheader("Form POST Encrypted Payload")
    st.markdown("After obtaining the encrypted payload, download the HTML form below, open it within your browser, "
                "and paste the encrypted payload into the field in the HTML form.")

    st.download_button(
        "Download HTML Form",
        data="""
<h1>SkillsFuture Credit Payment Request Form</h1>
<p>Enter in the encrypted payload below and click "Submit" to send the request to the API!</p>
<form action="https://uat.sfc.myskillsfuture.gov.sg/sfc2-ind/api/individual/sfcpayment/claim/submit/gateway"
       method="post" target="_blank">
     <textarea id="encryptedPayload" name="encryptedPayload" rows="10" cols="100"></textarea>
     <br>
     <input type="submit" href="#" formtarget="_blank" value="Submit">
 </form>
        """,
        file_name="form.html",
        mime="text/html",
        key="download-html-form",
        help="Click to download the HTML form for submission!",
        on_click=lambda: LOGGER.info("Downloading HTML form for submission..."),
        type="primary")
    
    st.write("Below is the form if you do not wish to download it")
    st.write("""
<h1>SkillsFuture Credit Payment Request Form</h1>
<p>Enter in the encrypted payload below and click "Submit" to send the request to the API!</p>
<form action="https://uat.sfc.myskillsfuture.gov.sg/sfc2-ind/api/individual/sfcpayment/claim/submit/gateway"
       method="post" target="_blank">
     <textarea id="encryptedPayload" name="encryptedPayload" rows="10" cols="100"></textarea>
     <br>
     <input type="submit" href="#" formtarget="_blank" value="Submit">
 </form>
""", unsafe_allow_html=True)

with decryption:
    st.header("SF Credit Claims Payment Request Decryption")
    st.markdown("After the request had been made to submit an SkillsFuture Credit claim, the returned payload "
                "from the response system would be encrypted. Developers should use this API to decrypt the "
                "payload. Consumers can use the decrypted payload's content on their application's transaction "
                "confirmation page.")

    decrypt = DecryptPayloadInfo()
    decrypt.encrypted_request = st.text_area(label="Enter Encrypted Request",
                                             key="decryption-request-payload",
                                             help="The payload consist of the information to be decrypted.")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(decrypt.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="decrypt-button", type="primary"):
        LOGGER.info("Attempting to send request to SF Credit Claims Payment Request Decryption API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")

        else:
            errors, warnings = decrypt.validate()

            if validation_error_handler(errors, warnings):
                dec = DecryptPayload(decrypt)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(dec, Secrets.get_encryption_key())

                with response:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: dec.execute(Secrets.get_encryption_key(),
                                                        os.environ.get(
                                                            ENV_NAME_CERT, ''),
                                                        Secrets.get_private_key()),
                                    Secrets.get_encryption_key())

with upload:
    st.header("Upload Supporting Documents")
    st.markdown("As part of the business process, supporting documents are required to substantiate the SkillsFuture "
                "Credit claim submission. Developers can use this API to automatically upload the relevant documents "
                "when a claim submission is made.\n\n"
                "Claims that are not substantiated with the documents will be rejected. This procedure is "
                "essential as it is an important stage in the SkillsFuture Credit claims process.\n\n"
                "Developers or end users can upload using the stated file formats for the supporting documents. "
                "The allowed file formats are pdf, doc, docx, tif, jpg, jpeg, png, xls, xlsm, xlsx.\n\n"
                "For more technical details, do visit [https://github.com/SSG-WSG](https://github.com/SSG-WSG)")

    upload_doc = UploadDocumentInfo()
    st.subheader("Claimant Details")
    claim_id = st.text_input(label="Claim ID",
                             key="upload-claim-id",
                             help="Unique identifier of the submitted claim.")
    upload_doc.nric = st.text_input(label="NRIC",
                                    key="upload-document-nric",
                                    max_chars=9)

    if len(upload_doc.nric) > 0 and not Validators.verify_nric(upload_doc.nric):
        st.warning("NRIC format is not valid!", icon="⚠️")

    st.subheader("Supporting Documents")
    st.markdown("Specify your file type before uploading the file. Fields such as the file name and file size will be"
                "automatically populated for you!")

    num_files = st.number_input(label="Specify Number of Documents",
                                min_value=0,
                                help="Indicate the total number of files that you wish to upload as the supporting "
                                     "documents for a particular claims!")

    for file in range(num_files):
        with st.expander(f"File {file + 1}", expanded=file == 0):
            st.subheader(f"File {file + 1}")
            doc = DocumentInfo()

            if st.checkbox("Specify Attachment ID?", key=f"specify-file-attachment-id-{file}",
                           help="If not specified, attachment ID will be automatically generated!"):
                doc.attachment_id = st.text_input(label="Attachment ID",
                                                  key=f"file-attachment-id-{file}",
                                                  help="Refers to the unique ID for each attachment.")
            else:
                doc.attachment_id = f"attachment{file}"
                st.info(f"Attachment ID (**{doc.attachment_id}**) is automatically generated!", icon="ℹ️")

            doc.file_type = st.selectbox(label="File Type",
                                         key=f"file-type-{file}",
                                         options=PermittedFileUploadType,
                                         format_func=lambda x: x.value)
            doc.attachment_bytes = st.file_uploader(label="Upload File",
                                                    key=f"file-{file}",
                                                    accept_multiple_files=False,
                                                    type=doc.file_type.value)
            if doc.has_file():
                st.info(f"File Size is Automatically set to: **{doc.get_formatted_size()}**!", icon="ℹ️")
                doc.file_size = doc.get_formatted_size()

            if st.checkbox("Override File Size?", key=f"specify-override-file-size-{file}"):
                doc.file_size = st.text_input(label="Override File Size",
                                              key=f"override-file-size-{file}",
                                              value=doc.get_formatted_size())

            doc.file_name = st.text_input(label="File Name",
                                          key=f"file-name-{file}",
                                          value=doc.file_name,
                                          help="Refers to the name of the attached file.")

            upload_doc.add_document(doc)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(upload_doc.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="upload-button", type="primary"):
        LOGGER.info("Attempting to send request to Upload Supporting Documents API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif claim_id is None or (claim_id is not None and len(claim_id) == 0):
            LOGGER.error("No Claim ID provided!")
            st.error("Invalid Claim ID!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")

        else:
            errors, warnings = upload_doc.validate()

            if validation_error_handler(errors, warnings):
                ud = UploadDocument(claim_id, upload_doc)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    LOGGER.info("Showing preview of request...")
                    handle_request(ud, Secrets.get_encryption_key())

                with response:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: ud.execute(Secrets.get_encryption_key(),
                                                        os.environ.get(
                                                            ENV_NAME_CERT, ''),
                                                        Secrets.get_private_key()),
                                    Secrets.get_encryption_key())


with view:
    st.header("View Claim Details")
    st.markdown("Training Providers can retrieve the details of an individual’s claim by calling this API.")

    nric = st.text_input(label="NRIC",
                         key="view-claims-nric",
                         max_chars=9,
                         help="NRIC of the individual")

    if len(nric) > 0 and not Validators.verify_nric(nric):
        st.warning("**NRIC format** is not valid!", icon="⚠️")

    claim_id = st.text_input(label="Claim ID",
                             key="view-claims-claim-id",
                             max_chars=10,
                             help="Unique identifier of the submitted claim. Must be exactly 10 digits.")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-button", type="primary"):
        LOGGER.info("Attempting to send request to View SF Credit Claims API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif len(nric) == 0:
            st.error("Invalid **NRIC** number!", icon="🚨")
        elif len(claim_id) != 10:
            st.error("Invalid **Claims ID**!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")
            
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = ViewClaims(nric, claim_id)

            with request:
                LOGGER.info("Showing preview of request...")
                handle_request(vc)

            with response:
                LOGGER.info("Executing request with defaults...")
                handle_response(lambda: vc.execute(os.environ.get(
                                                        ENV_NAME_CERT, ''),
                                                    Secrets.get_private_key()),
                                Secrets.get_encryption_key())

with cancel:
    st.header("Cancel Claim")
    st.markdown("To give end users and developers more flexibility in managing claim submissions, this API "
                "is available for cancellation of submitted claims. Developers can automate the cancellation "
                "process for end users by consuming this API. Claims that have yet to be approved can be "
                "cancelled by this API.\n\n"
                "For more technical details, do visit [https://github.com/SSG-WSG](https://github.com/SSG-WSG)")
    cancel_claims = CancelClaimsInfo()

    claim_id = st.text_input(label="Claim ID",
                             key="cancel-claims-claim-id",
                             max_chars=10,
                             help="Unique identifier of the submitted claim. Must be exactly 10 digits.")

    cancel_claims.nric = st.text_input(label="NRIC",
                                       key="cancel-claims-nric",
                                       max_chars=9,
                                       help="NRIC of the individual")

    if len(cancel_claims.nric) > 0 and not Validators.verify_nric(cancel_claims.nric):
        st.warning("NRIC format is not valid!", icon="⚠️")

    cancel_claims.cancel_claims_code = st.selectbox(label="Select Cancel Claims Code",
                                                    options=CancelClaimsCode,
                                                    format_func=lambda x: str(x),
                                                    key="view-claims-cancel-claim-code")

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(cancel_claims.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="cancel-button", type="primary"):
        LOGGER.info("Attempting to send request to Cancel SF Credit Claims API...")

        if does_not_have_url():
            LOGGER.error("Missing Endpoint URL!")
            st.error("Missing Endpoint URL! Navigate to the Home page to set up the URL!", icon="🚨")
        elif len(claim_id) != 10:
            st.error("Invalid **Claims ID**!", icon="🚨")

        elif not st.session_state["secret_fetched"]:
            LOGGER.error(
                "There are no default secrets loaded!")
            st.error(
                "There are no default secrets set, please try to refetch them via the config button in the side bar.", icon="🚨")

        else:
            if validation_error_handler(*(cancel_claims.validate())):
                cc = CancelClaims(claim_id, cancel_claims)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    handle_request(cc)

                with response:
                    LOGGER.info("Executing request with defaults...")
                    handle_response(lambda: cc.execute(Secrets.get_encryption_key(),
                                                        os.environ.get(
                                                            ENV_NAME_CERT, ''),
                                                        Secrets.get_private_key()),
                                    Secrets.get_encryption_key())
