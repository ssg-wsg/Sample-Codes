import datetime
import json
import base64

from typing import Optional, Literal

from core.abc.abstract import AbstractRequestInfo
from core.constants import CANCEL_CLAIMS_CODE
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils.json_utils import remove_null_fields


class EncryptPayloadInfo(AbstractRequestInfo):
    def __init__(self):
        self._course_id: str = None
        self._course_fee: float = None
        self._course_run_id: Optional[str] = None
        self._startDate: datetime.date = None
        self._nric: str = None
        self._email: str = None
        self._homeNumber: str = None
        self._mobileNumber: str = None
        self._additionalInformation: Optional[str] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        warnings = []
        errors = []

        if self._nric is None or len(self._nric) != 9:
            errors.append("No valid NRIC number is provided!")

        if self._email is None or len(self._email) == 0:
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

    def set_course_id(self, course_id: str) -> None:
        if not isinstance(course_id, str):
            raise TypeError("Course ID must be a string!")

        self._course_id = course_id

    def set_course_fee(self, course_fee: float) -> None:
        if not isinstance(course_fee, float):
            raise TypeError("Course fee must be a floating point number!")

        self._course_fee = course_fee

    def set_course_run_id(self, course_run_id: str) -> None:
        if not isinstance(course_run_id, str):
            raise TypeError("Course run ID must be a string!")

        self._course_run_id = course_run_id

    def set_start_date(self, startDate: datetime.date) -> None:
        if not isinstance(startDate, datetime.date):
            raise TypeError("Start date must be a date!")

        self._startDate = startDate

    def set_nric(self, nric: str) -> None:
        if not isinstance(nric, str):
            raise TypeError("NRIC must be a string!")

        self._nric = nric

    def set_email(self, email: str) -> None:
        if not isinstance(email, str):
            raise TypeError("Email must be a string!")

        self._email = email

    def set_home_number(self, homeNumber: str) -> None:
        if not isinstance(homeNumber, str):
            raise TypeError("Home Number must be a string!")

        self._homeNumber = homeNumber

    def set_mobile_number(self, mobileNumber: str) -> None:
        if not isinstance(mobileNumber, str):
            raise TypeError("Mobile Number must be a string!")

        self._mobileNumber = mobileNumber

    def set_additional_information(self, additionalInformation: str) -> None:
        if not isinstance(additionalInformation, str):
            raise TypeError("Additional information must be a string!")

        self._additionalInformation = additionalInformation


class DecryptPayloadInfo(AbstractRequestInfo):
    def __init__(self):
        self._encrypted_request: str = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

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

    def set_request(self, request: str) -> None:
        if not isinstance(request, str):
            raise TypeError("Encrypted Request must be a string!")

        self._encrypted_request = request


class DocumentInfo(AbstractRequestInfo):
    def __init__(self):
        self._fileName: str = None
        self._fileSize: str = None
        self._fileType: Literal["pdf", "doc", "docx", "tif", "jpg", "jpeg", "png", "xls", "xlsm", "xlsx"] = None
        self._attachmentId: Optional[str] = None
        self._attachmentBytes: UploadedFile = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._fileName is not None and len(self._fileName) == 0:
            errors.append("File name cannot be empty!")

        if self._fileSize is not None and len(self._fileSize) == 0:
            errors.append("File size cannot be empty!")

        if self._fileType is not None and len(self._fileType) == 0:
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
            "fileType": self._fileType,
            "attachmentId": self._attachmentId,
            "attachmentBytes": (base64.b64encode(self._attachmentBytes.getvalue() if self._attachmentBytes else b"")
                                .decode("utf-8")),
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_file_name(self, file_name: str) -> None:
        if not isinstance(file_name, str):
            raise TypeError("File name must be a string!")

        self._fileName = file_name

    def set_file_size(self, file_size: str) -> None:
        if not isinstance(file_size, str):
            raise TypeError("File size must be a string!")

        self._fileSize = file_size

    def set_file_type(self, file_type: str) -> None:
        if not isinstance(file_type, str):
            raise TypeError("File type must be a string!")

        self._fileType = file_type

    def set_attachment_id(self, attachment_id: str) -> None:
        if not isinstance(attachment_id, str):
            raise TypeError("Attachment ID must be a string!")

        self._attachmentId = attachment_id

    def set_file(self, file: UploadedFile) -> None:
        if file is not None and not isinstance(file, UploadedFile):
            print(file)
            raise TypeError("File should of a Streamlit UploadedFile type!")

        self._attachmentBytes = file

    def get_file_name(self) -> str:
        if self._attachmentBytes is not None:
            return self._attachmentBytes.name

        return ""

    def get_file_type(self) -> str:
        return self._fileType

    def get_attachment_id(self) -> str:
        if self._attachmentId is not None:
            return self._attachmentId

        return ""

    def get_file_size(self) -> int:
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
        self._nric: str = None
        self._documents: list[DocumentInfo] = []

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._nric is not None and len(self._nric) != 9:
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

    def set_nric(self, nric: str) -> None:
        if not isinstance(nric, str):
            raise TypeError("NRIC must be a string!")

        self._nric = nric

    def add_document(self, document: DocumentInfo) -> None:
        if not isinstance(document, DocumentInfo):
            raise TypeError("Document must be a DocumentInfo!")

        self._documents.append(document)


class CancelClaimsInfo(AbstractRequestInfo):
    def __init__(self):
        self._nric: str = None
        self._claimCancelCode: Literal["51", "52", "53", "54", "55"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        warnings = []
        errors = []

        if self._nric is None or len(self._nric) != 9:
            errors.append("No valid NRIC number is provided!")

        if self._claimCancelCode is None or len(self._claimCancelCode) == 10:
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
            "claimCancelCode": self._claimCancelCode
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_nric(self, nric: str) -> None:
        if not isinstance(nric, str):
            raise TypeError("NRIC must be a string")

        self._nric = nric

    def set_cancel_claims_code(self, cancel_claims_code: Literal["51", "52", "53", "54", "55"]) -> None:
        if not isinstance(cancel_claims_code, str) or cancel_claims_code not in CANCEL_CLAIMS_CODE:
            raise TypeError(f"Claim Cancel Code must be of values: {CANCEL_CLAIMS_CODE.keys()}")

        self._claimCancelCode = cancel_claims_code
