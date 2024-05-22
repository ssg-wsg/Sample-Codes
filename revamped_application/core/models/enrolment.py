import datetime
import json
import streamlit as st

from typing import Optional, Literal, Union

from core.abc.abstract import AbstractRequestInfo
from core.constants import COLLECTION_STATUS, ID_TYPE, SPONSORSHIP_TYPE
from utils.json_utils import remove_null_fields
from utils.verify import verify_uen


class CreateEnrolmentInfo(AbstractRequestInfo):
    """Class to encapsulate all information regarding the creation of an enrolment record for a trainee"""

    def __init__(self):
        self._course_run_id: Optional[str] = None
        self._course_referenceNumber: str = None
        self._trainee_id: str = None
        self._trainee_fees_discountAmount: Union[int, float] = None
        self._trainee_fees_collectionStatus: Literal["Pending Payment", "Partial Payment", "Full Payment"] = None
        self._trainee_idType_type: Literal["NRIC", "FIN", "Others"] = None
        self._trainee_employer_uen: Optional[str] = None
        self._trainee_employer_contact_fullName: Optional[str] = None
        self._trainee_employer_contact_emailAddress: Optional[str] = None
        self._trainee_employer_contact_contactNumber_areaCode: Optional[str] = None
        self._trainee_employer_contact_contactNumber_countryCode: Optional[str] = None
        self._trainee_employer_contact_contactNumber_phoneNumber: Optional[str] = None
        self._trainee_fullName: Optional[str] = None
        self._trainee_dateOfBirth: datetime.date = None
        self._trainee_emailAddress: str = None
        self._trainee_contactNumber_areaCode: Optional[str] = None
        self._trainee_contactNumber_countryCode: Optional[str] = None
        self._trainee_contactNumber_phoneNumber: Optional[str] = None
        self._trainee_enrolmentDate: Optional[datetime.date] = None
        self._trainee_sponsorshipType: Literal["EMPLOYER", "INDIVIDUAL"] = None
        self._trainingPartner_code: str = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._course_referenceNumber is None or len(self._course_referenceNumber) == 0:
            errors.append("No valid course reference number specified!")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No trainee ID specified!")

        if self._trainee_fees_collectionStatus is None or self._trainee_fees_collectionStatus not in COLLECTION_STATUS:
            errors.append("No valid fees collection status specified!")

        if self._trainee_idType is None or self._trainee_idType not in ID_TYPE:
            errors.append("No valid ID type specified!")

        if self._trainee_dateOfBirth is None or len(self._trainee_dateOfBirth) == 0:
            errors.append("No valid date of birth specified!")

        if self._trainee_emailAddress is None or len(self._trainee_emailAddress) == 0:
            errors.append("No valid email address specified!")

        if self._trainee_sponsorshipType is None or self._trainee_sponsorshipType not in SPONSORSHIP_TYPE:
            errors.append("No valid sponsorship type specified!")

        if self._trainingPartner_code is None or len(self._trainingPartner_code) == 0:
            errors.append("No valid training partner code specified!")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "enrolment": {
                "course": {
                    "run": {
                        "id": self._course_run_id
                    },
                    "referenceNumber": self._course_referenceNumber
                },
                "trainee": {
                    "id": self._trainee_id,
                    "fees": {
                        "discountAmount": self._trainee_fees_discountAmount,
                        "collectionStatus": self._trainee_fees_collectionStatus
                    },
                    "idType": {
                        "type": self._trainee_idType_type
                    },
                    "employer": {
                        "uen": self._trainee_employer_uen,
                        "contact": {
                            "fullName": self._trainee_employer_contact_fullName,
                            "emailAddress": self._trainee_employer_contact_emailAddress,
                            "contactNumber": {
                                "areaCode": self._trainee_employer_contact_contactNumber_areaCode,
                                "countryCode": self._trainee_employer_contact_contactNumber_countryCode,
                                "phoneNumber": self._trainee_employer_contact_contactNumber_phoneNumber,
                            }
                        }
                    },
                    "fullName": self._trainee_fullName,
                    "dateOfBirth": (self._trainee_dateOfBirth.strftime("%Y-%m-%d")
                                    if self._trainee_dateOfBirth is not None else None),
                    "emailAddress": self._trainee_emailAddress,
                    "contactNumber": {
                        "areaCode": self._trainee_contactNumber_areaCode,
                        "countryCode": self._trainee_contactNumber_countryCode,
                        "phoneNumber": self._trainee_contactNumber_phoneNumber
                    },
                    "enrolmentDate": self._trainee_enrolmentDate,
                    "sponsorshipType": self._trainee_sponsorshipType
                },
                "trainingPartner": {
                    "uen": st.session_state["uen"],
                    "code": self._trainingPartner_code
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def set_course_run_id(self, run_id: str) -> None:
        if not isinstance(run_id, str):
            raise TypeError("Course Run ID must be a string!")

        self._course_run_id = run_id

    def set_course_referenceNumber(self, course_reference_number: str) -> None:
        if not isinstance(course_reference_number, str):
            raise TypeError("Course Reference Number must be a string!")

        self._course_referenceNumber = course_reference_number

    def set_trainee_id(self, trainee_id: str) -> None:
        if not isinstance(trainee_id, str):
            raise TypeError("Trainee ID must be a string!")

        self._trainee_id = trainee_id

    def set_trainee_fees_discountAmount(self, discountAmount: Union[int, float]) -> None:
        if not isinstance(discountAmount, int) and not isinstance(discountAmount, float) or \
                discountAmount < 0:
            raise ValueError("Discount Amount must be a non-negative number!")

        self._trainee_fees_discountAmount = discountAmount

    def set_trainee_fees_collectionStatus(self, collectionStatus: Literal["Pending Payment", "Partial Payment",
    "Full Payment"]):
        if not isinstance(collectionStatus, str) or collectionStatus not in COLLECTION_STATUS:
            raise ValueError("Collection Status must be a string!")

        self._trainee_fees_collectionStatus = collectionStatus

    def set_trainee_idType(self, idType: Literal["NRIC", "FIN", "OTHERS"]) -> None:
        if not isinstance(idType, str) or idType not in ID_TYPE:
            raise ValueError("ID Type must be a string!")

        self._trainee_id = idType

    def set_employer_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise TypeError("Employer UEN must be a string!")

        if uen is not None and len(uen) > 0 and not verify_uen(uen):
            raise ValueError("Invalid Employer UEN provided!")

        self._trainee_employer_uen = uen

    def set_trainee_employer_contact_fullName(self, fullName: str) -> None:
        if not isinstance(fullName, str):
            raise TypeError("Employer Full Name must be a string!")

        self._trainee_employer_contact_fullName = fullName

    def set_trainee_employer_contact_emailAddress(self, emailAddress: str) -> None:
        if not isinstance(emailAddress, str):
            raise TypeError("Employer Email Address must be a string!")

        self._trainee_employer_contact_emailAddress = emailAddress

    def set_trainee_employer_contactNumber_areaCode(self, areaCode: str) -> None:
        if not isinstance(areaCode, str):
            raise TypeError("Employer Area Code must be a string!")

        self._trainee_employer_contact_contactNumber_areaCode = areaCode

    def set_trainee_employer_contactNumber_countryCode(self, countryCode: str) -> None:
        if not isinstance(countryCode, str):
            raise TypeError("Employer Country Code must be a string!")

        self._trainee_employer_contact_contactNumber_countryCode = countryCode

    def set_trainee_employer_contactNumber_phoneNumber(self, phoneNumber: str) -> None:
        if not isinstance(phoneNumber, str):
            raise TypeError("Employer Phone Number must be a string!")

        self._trainee_employer_contact_contactNumber_phoneNumber = phoneNumber

    def set_trainee_fullName(self, fullName: str) -> None:
        if not isinstance(fullName, str):
            raise TypeError("Trainee Full Name must be a string!")

        self._trainee_fullName = fullName

    def set_trainee_dateOfBirth(self, dateOfBirth: datetime.date) -> None:
        if not isinstance(dateOfBirth, datetime.date):
            raise TypeError("Trainee Date of Birth must be a datetime.date object!")

        self._trainee_dateOfBirth = dateOfBirth

    def set_trainee_emailAddress(self, emailAddress: str) -> None:
        if not isinstance(emailAddress, str):
            raise TypeError("Trainee Email Address must be a string!")

        self._trainee_emailAddress = emailAddress

    def set_trainee_contactNumber_areaCode(self, areaCode: str) -> None:
        if not isinstance(areaCode, str):
            raise TypeError("Trainee Area Code must be a string!")

        self._trainee_contactNumber_areaCode = areaCode

    def set_trainee_contactNumber_countryCode(self, countryCode: str) -> None:
        if not isinstance(countryCode, str):
            raise TypeError("Trainee Country Code must be a string!")

        self._trainee_contactNumber_countryCode = countryCode

    def set_trainee_contactNumber_phoneNumber(self, phoneNumber: str) -> None:
        if not isinstance(phoneNumber, str):
            raise TypeError("Trainee Phone Number must be a string!")

        self._trainee_contactNumber_phoneNumber = phoneNumber

    def set_trainee_enrolmentDate(self, enrolmentDate: datetime.date) -> None:
        if not isinstance(enrolmentDate, datetime.date):
            raise TypeError("Enrolment Date must be a datetime.date object!")

        self._trainee_enrolmentDate = enrolmentDate

    def set_trainee_sponsorshipType(self, sponsorshipType: Literal["EMPLOYER", "INDIVIDUAL"]) -> None:
        if not isinstance(sponsorshipType, str) or sponsorshipType not in ["EMPLOYER", "INDIVIDUAL"]:
            raise ValueError("Sponsorship Type must be a string!")

        self._trainee_sponsorshipType = sponsorshipType

    def set_trainingPartner_code(self, code: str) -> None:
        if not isinstance(code, str):
            raise TypeError("Partner code must be a string!")

        self._trainingPartner_code = code


class UpdateEnrolmentInfo(CreateEnrolmentInfo):
    """Class that encapsulates all information needed to update an enrolment record"""

    def validate(self) -> None:
        # there is nothing to validate since no fields are mandatory
        return

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        # skip verification as there is nothing to verify
        pl = {
            "enrolment": {
                "fees": {
                    "discountAmount": self._trainee_fees_discountAmount,
                    "collectionStatus": self._trainee_fees_collectionStatus
                },
                "action": "Update",
                "course": {
                    "run": {
                        "id": self._course_run_id
                    }
                },
                "trainee": {
                    "email": self._trainee_emailAddress,
                    "contactNumber": {
                        "areaCode": self._trainee_contactNumber_areaCode,
                        "countryCode": self._trainee_contactNumber_countryCode,
                        "phoneNumber": self._trainee_contactNumber_phoneNumber
                    }
                },
                "employer": {
                    "contact": {
                        "email": self._trainee_employer_contact_emailAddress,
                        "fullName": self._trainee_employer_contact_fullName,
                        "contactNumber": {
                            "areaCode": self._trainee_employer_contact_contactNumber_areaCode,
                            "countryCode": self._trainee_employer_contact_contactNumber_countryCode,
                            "phoneNumber": self._trainee_employer_contact_contactNumber_phoneNumber,
                        }
                    }
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl


class CancelEnrolmentInfo(UpdateEnrolmentInfo):
    """Contains information related to the cancelling of an enrolment"""

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        pl = {
            "enrolment": {
                "action": "Cancel"
            }
        }

        if as_json_str:
            return json.dumps(pl)

        return pl


class SearchEnrolmentInfo(AbstractRequestInfo):
    pass


class UpdateEnrolmentFeeCollectionInfo(UpdateEnrolmentInfo):
    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        pl = {
            "enrolment": {
                "fees": {
                    "collectionStatus": self._trainee_fees_collectionStatus
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl
