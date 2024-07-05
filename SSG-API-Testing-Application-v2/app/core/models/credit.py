import datetime
import json
import base64

from typing import Optional, Sequence, Annotated

from app.core.abc.abstract import AbstractRequestInfo
from app.core.constants import CancelClaimsCode, PermittedFileUploadType
from streamlit.runtime.uploaded_file_manager import UploadedFile
from app.utils.json_utils import remove_null_fields
from app.utils.verify import Validators


class EncryptPayloadInfo(AbstractRequestInfo):
    def __init__(self):
        self._course_id: Annotated[str, "Unique Course ID"] = None
        self._course_fee: Annotated[float, "Must be in the currency format (2 d.p.)"] = None
        self._course_run_id: Annotated[Optional[str], "Unique Course Run ID"] = None
        self._startDate: Annotated[datetime.date, "Start date of course"] = None
        self._nric: Annotated[str, "NRIC string of length 9"] = None
        self._email: Annotated[str, "Email string"] = None
        self._homeNumber: Annotated[str, "Mandatory if mobile number is not provided"] = None
        self._mobileNumber: Annotated[str, "Mandatory if home number is not provided"] = None
        self._additionalInformation: Annotated[Optional[str], "Additional info to be provided"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, EncryptPayloadInfo):
            return False

        return (
            self._course_id == other._course_id
            and self._course_fee == other._course_fee
            and self._course_run_id == other._course_run_id
            and self._startDate == other._startDate
            and self._nric == other._nric
            and self._email == other._email
            and self._homeNumber == other._homeNumber
            and self._mobileNumber == other._mobileNumber
            and self._additionalInformation == other._additionalInformation
        )

    def validate(self) -> tuple[list[str], list[str]]:
        warnings = []
        errors = []

        if self._nric is None or len(self._nric) != 9 or not Validators.verify_nric(self._nric):
            errors.append("No valid NRIC number is provided!")

        if self._email is None or len(self._email) == 0 or not Validators.verify_email(self._email):
            errors.append("No valid email address is provided!")

        if self._course_id is not None and len(self._course_id) == 0:
            errors.append("No valid Course ID is provided!")

        if self._email is not None and len(self._email) == 0:
            errors.append("No valid Email is provided!")

        if self._homeNumber is not None and len(self._homeNumber) == 0 and \
                self._mobileNumber is not None and len(self._mobileNumber) == 0:
            errors.append("Either Home Number or Mobile Number must be provided!")

        if self._course_run_id is not None and len(self._course_run_id) == 0:
            warnings.append("Course Run ID is empty even though it was marked as specified!")

        if self._additionalInformation is not None and len(self._additionalInformation) == 0:
            warnings.append("Additional Information is empty even though it was marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "claimRequest": {
                "course": {
                    "id": self._course_id,
                    "fee": "{:.2f}".format(self._course_fee) if self._course_fee is not None else None,
                    "runId": self._course_run_id,
                    "startDate": self._startDate.strftime("%Y-%m-%d") if self._startDate is not None else None,
                },
                "individual": {
                    "nric": self._nric,
                    "email": self._email,
                    "homeNumber": self._homeNumber,
                    "mobileNumber": self._mobileNumber
                },
                "additionalInformation": self._additionalInformation
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl, indent=4)

        return pl

    @property
    def course_id(self):
        return self._course_id

    @course_id.setter
    def course_id(self, course_id: str):
        if not isinstance(course_id, str):
            raise ValueError("Invalid Course ID")

        self._course_id = course_id

    @property
    def course_fee(self):
        return self._course_fee

    @course_fee.setter
    def course_fee(self, course_fee: float):
        if not isinstance(course_fee, float):
            raise ValueError("Invalid Course Fee")

        self._course_fee = float(course_fee)

    @property
    def course_run_id(self):
        return self._course_run_id

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        if not isinstance(course_run_id, str):
            raise ValueError("Invalid Course Run ID")

        self._course_run_id = course_run_id

    @property
    def start_date(self):
        return self._startDate

    @start_date.setter
    def start_date(self, start_date: datetime.date):
        if not isinstance(start_date, datetime.date):
            raise ValueError

        self._startDate = start_date

    @property
    def nric(self):
        return self._nric

    @nric.setter
    def nric(self, nric: str):
        if not isinstance(nric, str):
            raise ValueError("Invalid NRIC number")

        self._nric = nric

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if not isinstance(email, str):
            raise ValueError("Invalid email")

        self._email = email

    @property
    def home_number(self):
        return self._homeNumber

    @home_number.setter
    def home_number(self, home_number: str):
        if not isinstance(home_number, str):
            raise ValueError("Invalid home number")

        self._homeNumber = home_number

    @property
    def mobile_number(self):
        return self._mobileNumber

    @mobile_number.setter
    def mobile_number(self, mobile_number: str):
        if not isinstance(mobile_number, str):
            raise ValueError("Invalid mobile number")

        self._mobileNumber = mobile_number

    @property
    def additional_information(self):
        return self._additionalInformation

    @additional_information.setter
    def additional_information(self, additional_information: str):
        if not isinstance(additional_information, str):
            raise ValueError("Invalid additional information")

        self._additionalInformation = additional_information


class DecryptPayloadInfo(AbstractRequestInfo):
    def __init__(self):
        self._encrypted_request: Annotated[str, "Payload to decrypt"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, DecryptPayloadInfo):
            return False

        return self._encrypted_request == other._encrypted_request

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._encrypted_request is not None and len(self._encrypted_request) == 0:
            warnings.append("Encrypted Request is empty even though it was marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "claimRequestStatus": self._encrypted_request
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def encrypted_request(self):
        return self._encrypted_request

    @encrypted_request.setter
    def encrypted_request(self, encrypted_request: str):
        if not isinstance(encrypted_request, str):
            raise ValueError("Invalid encrypted request")

        self._encrypted_request = encrypted_request


class DocumentInfo(AbstractRequestInfo):
    def __init__(self):
        self._fileName: Annotated[str, "Name of the attached file"] = None
        self._fileSize: Annotated[str, "Size of attached file, auto-inferred if not provided"] = None
        self._fileType: PermittedFileUploadType = None
        self._attachmentId: Annotated[Optional[str], "Unique ID for each attachment"] = None
        self._attachmentBytes: Annotated[UploadedFile, "Base64 encoded value of the file contents"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, DocumentInfo):
            return False

        return (
            self._fileName == other._fileName
            and self._fileSize == other._fileSize
            and self._fileType == other._fileType
            and self._attachmentId == other._attachmentId
            and self._attachmentBytes == other._attachmentBytes
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._fileName is not None and len(self._fileName) == 0:
            errors.append("File name cannot be empty!")

        if self._fileSize is not None and len(self._fileSize) == 0:
            errors.append("File size cannot be empty!")

        if self._fileType is None:
            errors.append("File type cannot be empty!")

        if self._attachmentBytes is None:
            errors.append("No document uploaded!")

        if self._attachmentBytes is not None and len(self._attachmentBytes.getvalue()) == 0:
            errors.append("Document uploaded is empty even though it was marked as specified!")

        if self._attachmentId is not None and len(self._attachmentId) == 0:
            warnings.append("Attachment ID is empty even though it was marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()
            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "fileName": self._fileName,
            "fileSize": self._fileSize,
            "fileType": self._fileType.value if self._fileType is not None else None,
            "attachmentId": self._attachmentId,
            "attachmentBytes": (base64.b64encode(self._attachmentBytes.getvalue()).decode("utf-8")
                                if self._attachmentBytes else None),
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def file_name(self):
        return self._fileName if self._fileName is not None else ""

    @file_name.setter
    def file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise ValueError("Invalid file name")

        self._fileName = file_name

    @property
    def file_size(self):
        return self._fileSize

    @file_size.setter
    def file_size(self, file_size: str):
        if not isinstance(file_size, str):
            raise ValueError("Invalid file size")

        self._fileSize = file_size

    @property
    def file_type(self):
        return self._fileType

    @file_type.setter
    def file_type(self, file_type: PermittedFileUploadType):
        if not isinstance(file_type, PermittedFileUploadType):
            raise ValueError("Invalid file type")

        self._fileType = file_type

    @property
    def attachment_id(self):
        return self._attachmentId

    @attachment_id.setter
    def attachment_id(self, attachment_id: str):
        if not isinstance(attachment_id, str):
            raise ValueError("Invalid attachment ID")

        self._attachmentId = attachment_id

    @property
    def attachment_bytes(self):
        return self._attachmentBytes

    @attachment_bytes.setter
    def attachment_bytes(self, attachment_bytes: UploadedFile):
        if attachment_bytes is not None and not isinstance(attachment_bytes, UploadedFile):
            raise ValueError("Invalid attachment bytes")

        self._attachmentBytes = attachment_bytes

    def get_file_size(self) -> float:
        """Returns the size of the file in MB, if uploaded"""

        if self._attachmentBytes is not None:
            return round(len(self._attachmentBytes.getvalue()) / (10 ** 6), 3)

        return 0

    def get_formatted_size(self) -> str:
        """Returns the size of the file as a formatted string"""

        if self._attachmentBytes is not None:
            return f"{self.get_file_size()} MB"

        return ""

    def has_file(self) -> bool:
        return self._attachmentBytes is not None


class UploadDocumentInfo(AbstractRequestInfo):
    def __init__(self):
        self._nric: Annotated[str, "Must be a NRIC number"] = None
        self._documents: Annotated[list[DocumentInfo], "List of DocumentInfo objects"] = []

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, UploadDocumentInfo):
            return False

        return (
            self._nric == other._nric
            and all(map(lambda x: x[0] == x[1], zip(self._documents, other._documents)))
        )

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._nric is None or (self._nric is not None and len(self._nric) != 9):
            errors.append("No valid NRIC number was specified!")

        for i, doc in enumerate(self._documents):
            err, war = doc.validate()

            for e in err:
                errors.append(f"**File {i + 1}**: {e}")

            for w in war:
                warnings.append(f"**File {i + 1}**: {w}")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "nric": self._nric,
            "attachments": list(map(lambda x: x.payload(verify=False), self._documents)),
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def nric(self):
        return self._nric

    @nric.setter
    def nric(self, nric: str):
        if not isinstance(nric, str):
            raise ValueError("Invalid NRIC number")

        self._nric = nric

    @property
    def documents(self):
        return self._documents

    @documents.setter
    def documents(self, documents: Sequence[DocumentInfo]):
        if not isinstance(documents, Sequence) or not all(map(lambda x: isinstance(x, DocumentInfo), documents)):
            raise ValueError("Documents must be a sequence of DocumentInfo objects!")

        self._documents = documents

    def add_document(self, document: DocumentInfo) -> None:
        if not isinstance(document, DocumentInfo):
            raise ValueError("Document must be a DocumentInfo!")

        self._documents.append(document)


class CancelClaimsInfo(AbstractRequestInfo):
    def __init__(self):
        self._nric: Annotated[str, "Must be a NRIC number"] = None
        self._claimCancelCode: CancelClaimsCode = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, CancelClaimsInfo):
            return False

        return (
            self._nric == other._nric
            and self._claimCancelCode == other._claimCancelCode
        )

    def validate(self) -> tuple[list[str], list[str]]:
        warnings = []
        errors = []

        if self._nric is None or len(self._nric) != 9:
            errors.append("No valid NRIC number is provided!")

        if self._claimCancelCode is None:
            errors.append("No valid Claim Cancel Code is provided!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "nric": self._nric,
            "claimCancelCode": self._claimCancelCode.value[0] if self._claimCancelCode is not None else None
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def nric(self):
        return self._nric

    @nric.setter
    def nric(self, nric: str):
        if not isinstance(nric, str):
            raise ValueError("Invalid NRIC number")

        self._nric = nric

    @property
    def cancel_claims_code(self):
        return self._claimCancelCode

    @cancel_claims_code.setter
    def cancel_claims_code(self, code: CancelClaimsCode):
        if not isinstance(code, CancelClaimsCode):
            raise ValueError("Invalid Claim Cancel Code")

        self._claimCancelCode = code
