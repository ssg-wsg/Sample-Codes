import datetime
import json
import streamlit as st

from typing import Optional, Literal, Union

from core.abc.abstract import AbstractRequestInfo
from core.constants import COLLECTION_STATUS, ID_TYPE, SPONSORSHIP_TYPE, COLLECTION_STATUS_CANCELLED, \
    ENROLMENT_SORT_FIELD, SORT_ORDER, COLLECTION_STATUS_CANCELLED, ENROLMENT_COURSE_STATUS
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

        if self._trainee_idType_type is None or self._trainee_idType_type not in ID_TYPE:
            errors.append("No valid ID type specified!")

        if self._trainee_dateOfBirth is None:
            errors.append("No valid date of birth specified!")

        if self._trainee_emailAddress is None or len(self._trainee_emailAddress) == 0:
            errors.append("No valid email address specified!")

        if self._trainee_sponsorshipType is None or self._trainee_sponsorshipType not in SPONSORSHIP_TYPE:
            errors.append("No valid sponsorship type specified!")

        if self._trainingPartner_code is None or len(self._trainingPartner_code) == 0:
            errors.append("No valid training partner code specified!")

        # validate the pseudo-numerical values
        if self._trainee_employer_uen is not None and len(self._trainee_employer_uen) > 0 and \
                not verify_uen(self._trainee_employer_uen):
            errors.append("Employer UEN is not valid")

        if self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_areaCode)
            except ValueError:
                errors.append("Employer Area Code is not a number!")

        if self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_countryCode)
            except ValueError:
                errors.append("Employer Country Code is not a number!")

        if self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_phoneNumber)
            except ValueError:
                errors.append("Employer Phone Number is not a number!")

        if self._trainee_contactNumber_areaCode is not None and \
                len(self._trainee_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_contactNumber_areaCode)
            except ValueError:
                errors.append("Trainee Area Code is not a number!")

        if self._trainee_contactNumber_countryCode is not None and \
                len(self._trainee_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_contactNumber_countryCode)
            except ValueError:
                errors.append("Trainee Country Code is not a number!")

        if self._trainee_contactNumber_phoneNumber is not None and \
                len(self._trainee_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_contactNumber_phoneNumber)
            except ValueError:
                errors.append("Employer Phone Number is not a number!")

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
                    "enrolmentDate": (self._trainee_enrolmentDate.strftime("%Y-%m-%d")
                                      if self._trainee_enrolmentDate is not None else None),
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
            raise ValueError("Invalid Collection Status provided!")

        self._trainee_fees_collectionStatus = collectionStatus

    def set_trainee_idType(self, idType: Literal["NRIC", "FIN", "OTHERS"]) -> None:
        if not isinstance(idType, str) or idType not in ID_TYPE:
            raise ValueError("Invalid ID Type provided!")

        self._trainee_idType_type = idType

    def set_employer_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise TypeError("Employer UEN must be a String!")

        self._trainee_employer_uen = uen

    def set_trainee_employer_contact_fullName(self, fullName: str) -> None:
        if not isinstance(fullName, str):
            raise TypeError("Invalid Full Name provided!")

        self._trainee_employer_contact_fullName = fullName

    def set_trainee_employer_contact_emailAddress(self, emailAddress: str) -> None:
        if not isinstance(emailAddress, str):
            raise TypeError("Invalid Email Address provided!")

        self._trainee_employer_contact_emailAddress = emailAddress

    def set_trainee_employer_contactNumber_areaCode(self, areaCode: str) -> None:
        if not isinstance(areaCode, str):
            raise TypeError("Invalid Area Code provided!")

        self._trainee_employer_contact_contactNumber_areaCode = areaCode

    def set_trainee_employer_contactNumber_countryCode(self, countryCode: str) -> None:
        if not isinstance(countryCode, str):
            raise TypeError("Invalid Country Code provided!")

        self._trainee_employer_contact_contactNumber_countryCode = countryCode

    def set_trainee_employer_contactNumber_phoneNumber(self, phoneNumber: str) -> None:
        if not isinstance(phoneNumber, str):
            raise TypeError("Invalid Phone Number provided!")

        self._trainee_employer_contact_contactNumber_phoneNumber = phoneNumber

    def set_trainee_fullName(self, fullName: str) -> None:
        if not isinstance(fullName, str):
            raise TypeError("Invalid Trainee Full Name provided!")

        self._trainee_fullName = fullName

    def set_trainee_dateOfBirth(self, dateOfBirth: datetime.date) -> None:
        if not isinstance(dateOfBirth, datetime.date):
            raise TypeError("Invalid Trainee Date of Birth provided!")

        self._trainee_dateOfBirth = dateOfBirth

    def set_trainee_emailAddress(self, emailAddress: str) -> None:
        if not isinstance(emailAddress, str):
            raise TypeError("Invalid Trainee Email Address provided!")

        self._trainee_emailAddress = emailAddress

    def set_trainee_contactNumber_areaCode(self, areaCode: str) -> None:
        if not isinstance(areaCode, str):
            raise TypeError("Invalid Trainee Area Code provided!")

        self._trainee_contactNumber_areaCode = areaCode

    def set_trainee_contactNumber_countryCode(self, countryCode: str) -> None:
        if not isinstance(countryCode, str):
            raise TypeError("Invalid Trainee Country Code provided!")

        self._trainee_contactNumber_countryCode = countryCode

    def set_trainee_contactNumber_phoneNumber(self, phoneNumber: str) -> None:
        if not isinstance(phoneNumber, str):
            raise TypeError("Invalid Trainee Phone Number provided!")

        self._trainee_contactNumber_phoneNumber = phoneNumber

    def set_trainee_enrolmentDate(self, enrolmentDate: datetime.date) -> None:
        if not isinstance(enrolmentDate, datetime.date):
            raise TypeError("Invalid Enrolment Date provided!")

        self._trainee_enrolmentDate = enrolmentDate

    def set_trainee_sponsorshipType(self, sponsorshipType: Literal["EMPLOYER", "INDIVIDUAL"]) -> None:
        if not isinstance(sponsorshipType, str) or sponsorshipType not in SPONSORSHIP_TYPE:
            raise ValueError("Invalid Sponsorship Type provided!")

        self._trainee_sponsorshipType = sponsorshipType

    def set_trainingPartner_code(self, code: str) -> None:
        if not isinstance(code, str):
            raise TypeError("Invalid Partner code provided!")

        self._trainingPartner_code = code


class UpdateEnrolmentInfo(CreateEnrolmentInfo):
    """Class that encapsulates all information needed to update an enrolment record"""

    def validate(self) -> None | list[str]:
        errors = []

        # validate the pseudo-numerical values
        if self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_areaCode)
            except ValueError:
                errors.append("Employer Area Code is not a number!")

        if self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_countryCode)
            except ValueError:
                errors.append("Employer Country Code is not a number!")

        if self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_phoneNumber)
            except ValueError:
                errors.append("Employer Phone Number is not a number!")

        if self._trainee_contactNumber_areaCode is not None and len(self._trainee_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_contactNumber_areaCode)
            except ValueError:
                errors.append("Trainee Area Code is not a number!")

        if self._trainee_contactNumber_countryCode is not None and len(self._trainee_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_contactNumber_countryCode)
            except ValueError:
                errors.append("Trainee Country Code is not a number!")

        if self._trainee_contactNumber_phoneNumber is not None and len(self._trainee_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_contactNumber_phoneNumber)
            except ValueError:
                errors.append("Trainee Phone Number is not a number!")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

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

    def set_trainee_fees_collectionStatus(self, collectionStatus: Literal[
            "Pending Payment", "Partial Payment", "Full Payment", "Cancelled"]):
        if not isinstance(collectionStatus, str) or collectionStatus not in COLLECTION_STATUS_CANCELLED:
            raise ValueError("Invalid Collection Status provided!")

        self._trainee_fees_collectionStatus = collectionStatus


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
    """Contains information related to the query of an enrolment"""

    def __init__(self):
        self._lastUpdateDateTo: Optional[datetime.date] = None
        self._lastUpdateDateFrom: Optional[datetime.date] = None
        self._sortBy_field: Optional[Literal["updatedOn", "createdOn"]] = None
        self._sortBy_order: Optional[Literal["asc", "desc"]] = None
        self._course_run_id: Optional[str] = None
        self._course_referenceNumber: Optional[str] = None
        self._course_status: Optional[Literal["Confirmed", "Cancelled"]] = None
        self._trainee_id: Optional[str] = None
        self._trainee_fees_feeCollectionStatus: Optional[Literal[
            "Pending Payment", "Partial Payment", "Full Payment", "Cancelled"
        ]] = None
        self._trainee_idType_type: Optional[Literal["NRIC", "FIN", "Others"]] = None
        self._trainee_employer_uen: Optional[str] = None
        self._trainee_enrolmentDate: Optional[datetime.date] = None
        self._trainee_sponsorshipType: Optional[Literal["EMPLOYER", "INDIVIDUAL"]] = None
        self._trainingPartner_uen: Optional[str] = st.session_state["uen"]
        self._trainingPartner_code: Optional[str] = None
        self._parameters_page: int = None
        self._parameters_page_size: int = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> None | list[str]:
        errors = []

        if self._trainingPartner_uen is None or len(self._trainingPartner_uen) == 0 or \
                not verify_uen(self._trainingPartner_uen):
            errors.append("No valid Training Partner UEN specified!")

        if self._parameters_page is None:
            errors.append("No valid page specified!")

        if self._parameters_page_size is None:
            errors.append("No valid page size specified!")

        # optionals verification
        if self._trainee_employer_uen is not None and len(self._trainee_employer_uen) > 0 \
                and not verify_uen(self._trainee_employer_uen):
            errors.append("No valid Training Employer UEN specified!")

        if self._lastUpdateDateFrom is not None and self._lastUpdateDateTo is not None and \
                self._lastUpdateDateFrom > self._lastUpdateDateTo:
            errors.append("Last Update Date From should not be after Date To!")

        if len(errors) > 0:
            return errors

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            validation = self.validate()

            if validation is not None and len(validation) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "meta": {
                "lastUpdateDateTo": (self._lastUpdateDateTo.strftime("%Y-%m-%d")
                                     if self._lastUpdateDateTo is not None else self._lastUpdateDateTo),
                "lastUpdateDateFrom": (self._lastUpdateDateFrom.strftime("%Y-%m-%d")
                                       if self._lastUpdateDateFrom is not None else self._lastUpdateDateFrom),
            },
            "sortBy": {
                "field": self._sortBy_field,
                "order": self._sortBy_order,
            },
            "enrolment": {
                "course": {
                    "run": {
                        "id": self._course_run_id
                    },
                    "referenceNumber": self._course_referenceNumber
                },
                "status": self._course_status,
                "trainee": {
                    "id": self._trainee_id,
                    "fees": {
                        "feeCollectionStatus": self._trainee_fees_feeCollectionStatus
                    },
                    "idType": {
                        "type": self._trainee_idType_type
                    },
                    "employer": {
                        "uen": self._trainee_employer_uen
                    },
                    "enrolmentDate": (self._trainee_enrolmentDate.strftime("%Y-%m-%d") if
                                      self._trainee_enrolmentDate is not None else self._lastUpdateDateFrom),
                    "sponsorshipType": self._trainee_sponsorshipType,
                },
                "trainingPartner": {
                    "uen": self._trainingPartner_uen if st.session_state["uen"] is None else st.session_state["uen"],
                    "code": self._trainingPartner_code
                }
            },
            "parameters": {
                "page": self._parameters_page,
                "pageSize": self._parameters_page_size
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def has_training_partner_uen(self) -> bool:
        return self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0

    def set_lastUpdateDateTo(self, lastUpdateDateTo: datetime.date) -> None:
        if not isinstance(lastUpdateDateTo, datetime.date):
            raise ValueError("No valid last update date to specified!")

        self._lastUpdateDateTo = lastUpdateDateTo

    def set_lastUpdateDateFrom(self, lastUpdateDateFrom: datetime.date) -> None:
        if not isinstance(lastUpdateDateFrom, datetime.date):
            raise ValueError("No valid last update date to specified!")

        self._lastUpdateDateFrom = lastUpdateDateFrom

    def set_sortBy_field(self, sort_field: Literal["updatedOn", "createdOn"]) -> None:
        if not isinstance(sort_field, str) or sort_field not in ENROLMENT_SORT_FIELD:
            raise ValueError("No valid sort field specified!")

        self._sortBy_field = sort_field

    def set_sortBy_order(self, sort_order: Literal["asc", "desc"]) -> None:
        if not isinstance(sort_order, str) or sort_order not in SORT_ORDER:
            raise ValueError("No valid sort order specified!")

        self._sortBy_order = sort_order

    def set_course_run_id(self, course_run_id: str) -> None:
        if not isinstance(course_run_id, str):
            raise ValueError("No valid course run ID specified!")

        self._course_run_id = course_run_id

    def set_course_referenceNumber(self, course_reference_number: str) -> None:
        if not isinstance(course_reference_number, str):
            raise ValueError("No valid course reference number specified!")

        self._course_referenceNumber = course_reference_number

    def set_course_status(self, status: Literal["Confirmed", "Cancelled"]):
        if not isinstance(status, str) or status not in ENROLMENT_COURSE_STATUS:
            raise ValueError("No valid course status specified!")

        self._course_status = status

    def set_trainee_id(self, trainee_id: str) -> None:
        if not isinstance(trainee_id, str):
            raise ValueError("No valid trainee ID specified!")

        self._trainee_id = trainee_id

    def set_trainee_fee_collection_status(self, trainee_fee_collection_status: Literal[
        "Pending Payment", "Partial Payment", "Full Payment", "Cancelled"
    ]) -> None:
        if not isinstance(trainee_fee_collection_status, str) or trainee_fee_collection_status not in \
                trainee_fee_collection_status not in COLLECTION_STATUS_CANCELLED:
            raise ValueError("No valid trainee fee collection status specified!")

        self._trainee_fees_feeCollectionStatus = trainee_fee_collection_status

    def set_trainee_idType(self, idType: Literal["NRIC", "FIN", "Others"]):
        if not isinstance(idType, str) or idType not in ID_TYPE:
            raise ValueError("No valid ID type specified!")

        self._trainee_idType_type = idType

    def set_employer_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise ValueError("No valid UEN specified!")

        self._trainee_employer_uen = uen

    def set_trainee_enrolmentDate(self, enrolment_date: datetime.date) -> None:
        if not isinstance(enrolment_date, datetime.date):
            raise ValueError("No valid employment date specified!")

        self._trainee_enrolmentDate = enrolment_date

    def set_trainee_sponsorshipType(self, sponsorship_type: Literal["EMPLOYER", "INDIVIDUAL"]) -> None:
        if not isinstance(sponsorship_type, str) or sponsorship_type not in SPONSORSHIP_TYPE:
            raise ValueError("No valid sponsorship type specified!")

        self._trainee_sponsorshipType = sponsorship_type

    def set_trainingPartner_uen(self, uen: str) -> None:
        if not isinstance(uen, str):
            raise ValueError("No valid UEN specified!")

        self._trainingPartner_uen = uen

    def set_trainingPartner_code(self, code: str) -> None:
        if not isinstance(code, str):
            raise ValueError("No valid code specified!")

        self._trainingPartner_code = code

    def set_page(self, page: int) -> None:
        if not isinstance(page, int) or page < 0:
            raise ValueError("No valid page specified!")

        self._parameters_page = page

    def set_page_size(self, page_size: int) -> None:
        if not isinstance(page_size, int) or page_size < 0:
            raise ValueError("No valid page size specified!")

        self._parameters_page_size = page_size


class UpdateEnrolmentFeeCollectionInfo(UpdateEnrolmentInfo):
    """Contains information about the updating of enrolment fee collection"""

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
