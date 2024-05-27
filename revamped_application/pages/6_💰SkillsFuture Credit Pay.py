import streamlit as st

from core.constants import CANCEL_CLAIMS_CODE
from core.models.credit import EncryptPayloadInfo, DecryptPayloadInfo, CancelClaimsInfo, UploadDocumentInfo, \
    DocumentInfo
from core.credit.view_claims import ViewClaims
from core.credit.cancel_claims import CancelClaims
from core.credit.encrypt_payload import EncryptPayload
from core.credit.decrypt_payload import DecryptPayload
from core.credit.upload_document import UploadDocument
from core.constants import PERMITTED_UPLOAD_FILE_TYPE
from utils.http_utils import handle_error
from utils.streamlit_utils import init, display_config

init()

if "claims_request" not in st.session_state:
    st.session_state["claims_request"] = None

st.set_page_config(page_title="SkillsFuture Credit Pay", page_icon="💰")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()

st.header("SkillsFuture Credit Pay")
st.markdown("The SkillsFuture Credit Pay serves to integrate the SkillsFuture Credit claim submission and course "
            "payment with course registration. It allows users to indicate the amount of credits to offset from "
            "the course fee payment during course registration. Please note that individuals must give their "
            "consent for the use of their SkillsFuture Credit information.")
st.info("**This API requires your *requests* to be encrypted, and will return *encrypted responses*!**", icon="ℹ️")

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
    if st.checkbox("Specify Course Details?", key="specify-encryption-course-details"):
        if st.checkbox("Specify Course Run ID?", key="specify-encryption-course-details-course-run-id"):
            encrypt.set_course_run_id(st.text_input(label="Course Run ID",
                                                    key="encryption-course-details-course-run-id",
                                                    help="Unique ID of the course run."))

        encrypt.set_course_id(st.text_input(label="Course ID",
                                            key="encryption-course-details-course-id",
                                            help="Unique ID of the run."))

        encrypt.set_course_fee(st.number_input(label="Course Fee",
                                               key="encryption-course-details-course-fee",
                                               help="Course Fee. Please ensure that the amount is in the currency "
                                                    "format (i.e. with 2 decimal places).",
                                               value=0.00,
                                               min_value=0.00,
                                               step=0.01))
        encrypt.set_start_date(st.date_input(label="Start Date",
                                             key="encryption-course-details-start-date",
                                             help="Start date of the course.",
                                             format="YYYY-MM-DD"))

    st.subheader("Individual Details")
    if st.checkbox("Specify Individual Details?", key="specify-individual-details"):
        encrypt.set_nric(st.text_input(label="NRIC",
                                       key="encryption-individual-nric",
                                       max_chars=9,
                                       help="Refers to the NRIC of the individual submitting the SFC Payment Request."))
        encrypt.set_email(st.text_input(label="Email",
                                        key="encryption-individual-email",
                                        help="Email address of the individual."))
        encrypt.set_home_number(st.text_input(label="Home Number",
                                              key="encryption-individual-home-number",
                                              help="Home number of the individual. This is a mandatory field if "
                                                   "mobile number is not provided."))
        encrypt.set_mobile_number(st.text_input(label="Mobile Number",
                                                key="encryption-individual-mobile-number",
                                                help="Mobile number of the individual. This is a mandatory field if "
                                                     "home number is not provided."))

    st.subheader("Additional Information")
    if st.checkbox("Specify Additional Information?", key="specify-encryption-additional-information"):
        encrypt.set_additional_information(st.text_area(label="Additional Information",
                                                        key="encryption-additional-information",
                                                        help="Any additional information to be provided during SFC "
                                                             "Payment Request submission."))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(encrypt.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="encrypt-button"):
        errors, warnings = encrypt.validate()

        if len(warnings) > 0:
            st.warning(
                "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
            )

        if len(errors) > 0:
            st.error(
                "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
            )
        else:
            enc = EncryptPayload(encrypt)
            request, response = st.tabs(["Request", "Response"])

            with request:
                st.subheader("Request")
                st.code(repr(enc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: enc.execute())

with decryption:
    st.header("SF Credit Claims Payment Request Decryption")
    st.markdown("After the request had been made to submit an SkillsFuture Credit claim, the returned payload "
                "from the response system would be encrypted. Developers should use this API to decrypt the "
                "payload. Consumers can use the decrypted payload's content on their application's transaction "
                "confirmation page.")

    decrypt = DecryptPayloadInfo()
    decrypt.set_request(st.text_area(label="Enter Encrypted Request",
                                     key="decryption-request-payload",
                                     value=(st.session_state["claims_request"]["claimRequestStatus"]
                                            if st.session_state["claims_request"] is not None else ""),
                                     help="The payload consist of the information to be decrypted."))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(decrypt.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="decrypt-button"):
        errors, warnings = decrypt.validate()

        if len(warnings) > 0:
            st.warning(
                "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
            )

        if len(errors) > 0:
            st.error(
                "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
            )
        else:
            dec = DecryptPayload(decrypt)
            request, response = st.tabs(["Request", "Response"])

            with request:
                st.subheader("Request")
                st.code(repr(dec), language="text")

            with response:
                st.subheader("Response")
                st.session_state["claims_request"] = handle_error(lambda: dec.execute(), return_json=True)


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
    upload_doc.set_nric(st.text_input(label="NRIC",
                                      key="upload-document-nric",
                                      max_chars=9))

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
                doc.set_attachment_id(st.text_input(label="Attachment ID",
                                                    key=f"file-attachment-id-{file}",
                                                    help="Refers to the unique ID for each attachment."))
            else:
                doc.set_attachment_id(f"attachment{file}")
                st.info(f"Attachment ID (**{doc.get_attachment_id()}**) is automatically generated!", icon="ℹ️")

            doc.set_file_type(st.selectbox(label="File Type",
                                           key=f"file-type-{file}",
                                           options=PERMITTED_UPLOAD_FILE_TYPE,
                                           format_func=lambda x: x.upper()))
            doc.set_file(st.file_uploader(label="Upload File",
                                          key=f"file-{file}",
                                          accept_multiple_files=False,
                                          type=doc.get_file_type()))
            if doc.has_file():
                st.info(f"File Size is Automatically set to: **{doc.get_formatted_size()}**!", icon="ℹ️")
                doc.set_file_size(doc.get_formatted_size())

            if st.checkbox("Override File Size?", key=f"specify-override-file-size-{file}"):
                doc.set_file_size(st.text_input(label="Override File Size",
                                                key=f"override-file-size-{file}",
                                                value=doc.get_formatted_size()))

            doc.set_file_name(st.text_input(label="File Name",
                                            key=f"file-name-{file}",
                                            value=doc.get_file_name(),
                                            help="Refers to the name of the attached file."))

            upload_doc.add_document(doc)

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(upload_doc.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="upload-button"):
        if claim_id is not None and len(claim_id) == 0:
            st.error("Invalid Claim ID!", icon="🚨")
        else:
            errors, warnings = upload_doc.validate()

            if len(warnings) > 0:
                st.warning(
                    "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
                )

            if len(errors) > 0:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
                )
            else:
                ud = UploadDocument(claim_id, upload_doc)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    st.subheader("Request")
                    st.code(repr(ud), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: ud.execute())

with view:
    st.header("View Claim Details")
    st.markdown("Training Providers can retrieve the details of an individual’s claim by calling this API.")

    nric = st.text_input(label="NRIC",
                         key="view-claims-nric",
                         max_chars=9,
                         help="NRIC of the individual")
    claim_id = st.text_input(label="Claim ID",
                             key="view-claims-claim-id",
                             max_chars=10,
                             help="Unique identifier of the submitted claim. Must be exactly 10 digits.")

    st.divider()
    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="view-button"):
        if len(nric) == 0:
            st.error("Invalid **NRIC** number!", icon="🚨")
        elif len(claim_id) != 10:
            st.error("Invalid **Claims ID**!", icon="🚨")
        else:
            request, response = st.tabs(["Request", "Response"])
            vc = ViewClaims(nric, claim_id)

            with request:
                st.subheader("Request")
                st.code(repr(vc), language="text")

            with response:
                st.subheader("Response")
                handle_error(lambda: vc.execute())

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

    cancel_claims.set_nric(st.text_input(label="NRIC",
                                         key="cancel-claims-nric",
                                         max_chars=9,
                                         help="NRIC of the individual"))
    cancel_claims.set_cancel_claims_code(st.selectbox(label="Select Cancel Claims Code",
                                                      options=CANCEL_CLAIMS_CODE.keys(),
                                                      format_func=lambda x: f"{x}: {CANCEL_CLAIMS_CODE[x]}",
                                                      key="view-claims-cancel-claim-code"))

    st.divider()
    st.subheader("Preview Request Body")
    with st.expander("Request Body"):
        st.json(cancel_claims.payload(verify=False))

    st.subheader("Send Request")
    st.markdown("Click the `Send` button below to send the request to the API!")

    if st.button("Send", key="cancel-button"):
        if len(claim_id) != 10:
            st.error("Invalid **Claims ID**!", icon="🚨")
        else:
            errors, warnings = cancel_claims.validate()

            if len(warnings) > 0:
                st.warning(
                    "**Some warnings are raised with your inputs:**\n\n- " + "\n- ".join(warnings), icon="⚠️"
                )

            if len(errors) > 0:
                st.error(
                    "**Some errors are detected with your inputs:**\n\n- " + "\n- ".join(errors), icon="🚨"
                )
            else:
                cc = CancelClaims(claim_id, cancel_claims)
                request, response = st.tabs(["Request", "Response"])

                with request:
                    st.subheader("Request")
                    st.code(repr(cc), language="text")

                with response:
                    st.subheader("Response")
                    handle_error(lambda: cc.execute())
