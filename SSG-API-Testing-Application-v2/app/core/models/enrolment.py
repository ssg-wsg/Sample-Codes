import datetime
import json
import streamlit as st

from typing import Optional, Union, Annotated

from app.core.abc.abstract import AbstractRequestInfo
from app.core.constants import (CollectionStatus, CancellableCollectionStatus, IdTypeSummary,
                                SponsorshipType, EnrolmentSortField, SortOrder,
                                EnrolmentCourseStatus)
from app.utils.json_utils import remove_null_fields
from app.utils.verify import Validators


class CreateEnrolmentInfo(AbstractRequestInfo):
    """Class to encapsulate all information regarding the creation of an enrolment record for a trainee"""

    def __init__(self):
        self._course_run_id: Annotated[Optional[str], "Max length of 20"] = None
        self._course_referenceNumber: Annotated[str, "Max length of 100"] = None
        self._trainee_id: Annotated[str, "Max length of 20"] = None
        self._trainee_fees_discountAmount: Union[int, float] = None
        self._trainee_fees_collectionStatus: Annotated[CollectionStatus.value, "Max length of 50"] = None
        self._trainee_idType_type: IdTypeSummary.value = None
        self._trainee_employer_uen: Annotated[Optional[str], "Max length of 50"] = None
        self._trainee_employer_contact_fullName: Annotated[Optional[str], "Max length of 50"] = None
        self._trainee_employer_contact_emailAddress: Annotated[Optional[str], "Max length of 100"] = None
        self._trainee_employer_contact_contactNumber_areaCode: Annotated[Optional[str], "Max length of 10"] = None
        self._trainee_employer_contact_contactNumber_countryCode: Annotated[Optional[str], "Max length of 5"] = None
        self._trainee_employer_contact_contactNumber_phoneNumber: Annotated[Optional[str], "Max length of 20"] = None
        self._trainee_fullName: Annotated[Optional[str], "Max length of 200"] = None
        self._trainee_dateOfBirth: Annotated[datetime.date, "Formatted as YYYY-MM-DD, max length of 10"] = None
        self._trainee_emailAddress: Annotated[str, "Max length of 100"] = None
        self._trainee_contactNumber_areaCode: Annotated[Optional[str], "Max length of 10"] = None
        self._trainee_contactNumber_countryCode: Annotated[Optional[str], "Max length of 5"] = None
        self._trainee_contactNumber_phoneNumber: Annotated[Optional[str], "Max length of 20"] = None
        self._trainee_enrolmentDate: Annotated[Optional[datetime.date], "Formatted as YYYY-MM-DD"] = None
        self._trainee_sponsorshipType: Annotated[SponsorshipType.value, "Max length of 50"] = None
        self._trainingPartner_code: Annotated[str, "Max length of 12"] = None
        self._trainingPartner_uen: Annotated[Optional[str], "Max length of 15"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    @property
    def course_run_id(self):
        return self._course_run_id

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        if not isinstance(course_run_id, str):
            raise ValueError("Course Run ID must be a string!")

        self._course_run_id = course_run_id

    @property
    def course_referenceNumber(self):
        return self._course_referenceNumber

    @course_referenceNumber.setter
    def course_referenceNumber(self, course_referenceNumber: str):
        if not isinstance(course_referenceNumber, str):
            raise ValueError("Course Reference Number must be a string!")

        self._course_referenceNumber = course_referenceNumber

    @property
    def trainee_id(self):
        return self._trainee_id

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        if not isinstance(trainee_id, str):
            raise ValueError("Trainee ID must be a string!")

        self._trainee_id = trainee_id

    @property
    def trainee_fees_discountAmount(self):
        return self._trainee_fees_discountAmount

    @trainee_fees_discountAmount.setter
    def trainee_fees_discountAmount(self, discountAmount: Union[int, float]):
        if not isinstance(discountAmount, int) and not isinstance(discountAmount, float):
            raise ValueError("Discount Amount must be a number")
        elif discountAmount < 0:
            raise ValueError("Discount Amount must be a non-negative number!")

        self._trainee_fees_discountAmount = discountAmount

    @property
    def trainee_fees_collectionStatus(self):
        return self._trainee_fees_collectionStatus

    @trainee_fees_collectionStatus.setter
    def trainee_fees_collectionStatus(self, collectionStatus: CollectionStatus):
        if not isinstance(collectionStatus, CollectionStatus):
            try:
                collectionStatus = CollectionStatus(collectionStatus)
            except Exception:
                raise ValueError("Invalid Collection Status provided!")

        self._trainee_fees_collectionStatus = collectionStatus

    @property
    def trainee_idType(self):
        return self._trainee_idType_type

    @trainee_idType.setter
    def trainee_idType(self, idType: IdTypeSummary):
        if not isinstance(idType, IdTypeSummary):
            try:
                idType = IdTypeSummary(idType)
            except Exception:
                raise ValueError("Invalid ID Type provided!")

        self._trainee_idType_type = idType

    @property
    def employer_uen(self):
        return self._trainee_employer_uen

    @employer_uen.setter
    def employer_uen(self, uen: str):
        if not isinstance(uen, str):
            raise ValueError("Employer UEN must be a String!")

        self._trainee_employer_uen = uen

    @property
    def employer_fullName(self):
        return self._trainee_employer_contact_fullName

    @employer_fullName.setter
    def employer_fullName(self, fullName: str):
        if not isinstance(fullName, str):
            raise ValueError("Invalid Full Name provided!")

        self._trainee_employer_contact_fullName = fullName

    @property
    def employer_emailAddress(self):
        return self._trainee_employer_contact_emailAddress

    @employer_emailAddress.setter
    def employer_emailAddress(self, emailAddress: str):
        if not isinstance(emailAddress, str):
            raise ValueError("Invalid Email Address provided!")

        self._trainee_employer_contact_emailAddress = emailAddress

    @property
    def employer_areaCode(self):
        return self._trainee_employer_contact_contactNumber_areaCode

    @employer_areaCode.setter
    def employer_areaCode(self, areaCode: str):
        if not isinstance(areaCode, str):
            raise ValueError("Invalid Area Code provided!")

        self._trainee_employer_contact_contactNumber_areaCode = areaCode

    @property
    def employer_countryCode(self):
        return self._trainee_employer_contact_contactNumber_countryCode

    @employer_countryCode.setter
    def employer_countryCode(self, countryCode: str):
        if not isinstance(countryCode, str):
            raise ValueError("Invalid Country Code provided!")

        self._trainee_employer_contact_contactNumber_countryCode = countryCode

    @property
    def employer_phoneNumber(self):
        return self._trainee_employer_contact_contactNumber_phoneNumber

    @employer_phoneNumber.setter
    def employer_phoneNumber(self, phoneNumber: str):
        if not isinstance(phoneNumber, str):
            raise ValueError("Invalid Phone Number provided!")

        self._trainee_employer_contact_contactNumber_phoneNumber = phoneNumber

    @property
    def trainee_fullName(self):
        return self._trainee_fullName

    @trainee_fullName.setter
    def trainee_fullName(self, fullName: str):
        if not isinstance(fullName, str):
            raise ValueError("Invalid Trainee Full Name provided!")

        self._trainee_fullName = fullName

    @property
    def trainee_dateOfBirth(self):
        return self._trainee_dateOfBirth

    @trainee_dateOfBirth.setter
    def trainee_dateOfBirth(self, dateOfBirth: datetime.date):
        if not isinstance(dateOfBirth, datetime.date):
            raise ValueError("Invalid Trainee Date of Birth provided!")

        self._trainee_dateOfBirth = dateOfBirth

    @property
    def trainee_emailAddress(self):
        return self._trainee_emailAddress

    @trainee_emailAddress.setter
    def trainee_emailAddress(self, emailAddress: str):
        if not isinstance(emailAddress, str):
            raise ValueError("Invalid Trainee Email Address provided!")

        self._trainee_emailAddress = emailAddress

    @property
    def trainee_contactNumber_areaCode(self):
        return self._trainee_contactNumber_areaCode

    @trainee_contactNumber_areaCode.setter
    def trainee_contactNumber_areaCode(self, areaCode: str):
        if not isinstance(areaCode, str):
            raise ValueError("Invalid Trainee Area Code provided!")

        self._trainee_contactNumber_areaCode = areaCode

    @property
    def trainee_contactNumber_countryCode(self):
        return self._trainee_contactNumber_countryCode

    @trainee_contactNumber_countryCode.setter
    def trainee_contactNumber_countryCode(self, countryCode: str):
        if not isinstance(countryCode, str):
            raise ValueError("Invalid Trainee Country Code provided!")

        self._trainee_contactNumber_countryCode = countryCode

    @property
    def trainee_contactNumber_phoneNumber(self):
        return self._trainee_contactNumber_phoneNumber

    @trainee_contactNumber_phoneNumber.setter
    def trainee_contactNumber_phoneNumber(self, phoneNumber: str):
        if not isinstance(phoneNumber, str):
            raise ValueError("Invalid Trainee Phone Number provided!")

        self._trainee_contactNumber_phoneNumber = phoneNumber

    @property
    def trainee_enrolmentDate(self):
        return self._trainee_enrolmentDate

    @trainee_enrolmentDate.setter
    def trainee_enrolmentDate(self, enrolmentDate: datetime.date):
        if not isinstance(enrolmentDate, datetime.date):
            raise ValueError("Invalid Enrolment Date provided!")

        self._trainee_enrolmentDate = enrolmentDate

    @property
    def trainee_sponsorshipType(self):
        return self._trainee_sponsorshipType

    @trainee_sponsorshipType.setter
    def trainee_sponsorshipType(self, sponsorshipType: SponsorshipType):
        if not isinstance(sponsorshipType, SponsorshipType):
            try:
                sponsorshipType = SponsorshipType(sponsorshipType)
            except Exception:
                raise ValueError("Invalid Sponsorship Type provided!")

        self._trainee_sponsorshipType = sponsorshipType

    @property
    def trainingPartner_code(self):
        return self._trainingPartner_code

    @trainingPartner_code.setter
    def trainingPartner_code(self, code: str):
        if not isinstance(code, str):
            raise ValueError("Invalid Partner code provided!")

        self._trainingPartner_code = code

    @property
    def trainingPartner_uen(self):
        return self._trainingPartner_uen

    @trainingPartner_uen.setter
    def trainingPartner_uen(self, uen: str):
        if not isinstance(uen, str):
            raise ValueError("Invalid Partner UEN must be a String!")

        self._trainingPartner_uen = uen

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._course_run_id is not None and len(self._course_run_id) == 0:
            errors.append("Course Run ID is empty even though it is marked as specified!")

        if (self._trainee_employer_uen is None or len(self._trainee_employer_uen) == 0) and \
                self.trainee_sponsorshipType == SponsorshipType.EMPLOYER:
            errors.append("No valid Employer UEN specified!")

        if (self._trainee_employer_contact_fullName is None or len(self._trainee_employer_contact_fullName) == 0) \
                and self.trainee_sponsorshipType == SponsorshipType.EMPLOYER:
            errors.append("No valid Trainee Full Name specified!")

        if (self._trainee_employer_contact_emailAddress is None
            or len(self._trainee_employer_contact_emailAddress) == 0) \
                and self.trainee_sponsorshipType == SponsorshipType.EMPLOYER:
            errors.append("No valid Employer Email Address specified!")

        if (self._trainee_employer_contact_contactNumber_countryCode is None
            or len(self._trainee_employer_contact_contactNumber_countryCode) == 0) \
                and self.trainee_sponsorshipType == SponsorshipType.EMPLOYER:
            errors.append("No valid Employer Contact Number Country Code specified!")

        if (self._trainee_employer_contact_contactNumber_phoneNumber is None
            or len(self._trainee_employer_contact_contactNumber_phoneNumber) == 0) \
                and self.trainee_sponsorshipType == SponsorshipType.EMPLOYER:
            errors.append("No valid Employer Contact Number Phone Number specified!")

        if self._course_referenceNumber is None or len(self._course_referenceNumber) == 0:
            errors.append("No valid Course Reference Number specified!")

        if self._trainee_id is None or len(self._trainee_id) == 0:
            errors.append("No Trainee ID specified!")

        if self._trainee_fees_discountAmount is not None and self._trainee_fees_collectionStatus is None:
            errors.append("No valid Fees Collection Status specified!")

        if self._trainee_dateOfBirth is None:
            errors.append("No valid Trainee Date Of Birth specified!")

        if self._trainee_emailAddress is None or len(self._trainee_emailAddress) == 0:
            errors.append("No valid Trainee Email Address specified!")

        if self._trainee_emailAddress is not None and len(self._trainee_emailAddress) > 0:
            if not Validators.verify_email(self._trainee_emailAddress):
                errors.append("Trainee Email specified is not of the correct format!")

        if self._trainingPartner_code is None or len(self._trainingPartner_code) == 0:
            errors.append("No valid Training Partner Code specified!")

        if self._trainingPartner_uen is not None and not Validators.verify_uen(self._trainingPartner_uen):
            errors.append("Overridden Training Partner UEN provided is invalid!")

        if self._trainee_employer_uen is not None and len(self._trainee_employer_uen) > 0 and \
                not Validators.verify_uen(self._trainee_employer_uen):
            errors.append("Employer UEN is not valid!")

        if self._trainee_contactNumber_countryCode is not None and \
                len(self._trainee_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_contactNumber_countryCode)
            except ValueError:
                errors.append("Trainee Country Code is not a number!")
        elif self._trainee_contactNumber_countryCode is not None and len(self._trainee_contactNumber_countryCode) == 0:
            errors.append("No valid Trainee Country Code specified!")

        if self._trainee_contactNumber_phoneNumber is not None and len(self._trainee_contactNumber_phoneNumber) == 0:
            errors.append("No valid Trainee Phone Number specified!")

        # optional parameter validation
        # validate the pseudo-numerical values
        if self._trainee_employer_uen is not None and len(self._trainee_employer_uen) == 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            warnings.append("Employer UEN is empty even though it is marked as specified!")

        if self._trainee_employer_contact_fullName is not None and len(self._trainee_employer_contact_fullName) == 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            warnings.append("Employer Full Name is empty even though it is marked as specified!")

        if self._trainee_employer_contact_emailAddress is not None \
                and len(self._trainee_employer_contact_emailAddress) == 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            warnings.append("Employer Email Address is empty even though it is marked as specified!")

        if self._trainee_employer_contact_emailAddress is not None and \
                len(self._trainee_employer_contact_emailAddress) > 0:
            if not Validators.verify_email(self._trainee_employer_contact_emailAddress):
                errors.append("Employer Email Address specified is not of the correct format!")

        if self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_areaCode)
            except ValueError:
                warnings.append("Employer Area Code is not a number!")
        elif self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) == 0:
            warnings.append("Employer Contact Number Area Code is empty even though it is marked as specified!")

        if self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) != 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            try:
                int(self._trainee_employer_contact_contactNumber_countryCode)
            except ValueError:
                warnings.append("Employer Country Code is not a number!")
        elif self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) == 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            warnings.append("Employer Country Code is empty even though it is marked as specified!")

        if self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) != 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            try:
                int(self._trainee_employer_contact_contactNumber_phoneNumber)
            except ValueError:
                warnings.append("Employer Phone Number is not a number!")
        elif self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) == 0 \
                and self.trainee_sponsorshipType != SponsorshipType.EMPLOYER:
            warnings.append("Employer Phone Number is empty even though it is marked as specified!")

        if self._trainee_contactNumber_areaCode is not None and \
                len(self._trainee_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_contactNumber_areaCode)
            except ValueError:
                warnings.append("Trainee Area Code is not a number!")
        elif self._trainee_contactNumber_areaCode is not None and len(self._trainee_contactNumber_areaCode) == 0:
            warnings.append("Trainee Area Code is empty though it is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
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
                        "collectionStatus": (self._trainee_fees_collectionStatus.value if
                                             self._trainee_fees_collectionStatus is not None else None)
                    },
                    "idType": {
                        "type": self._trainee_idType_type.value if self._trainee_idType_type is not None else None
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
                    "sponsorshipType": (self._trainee_sponsorshipType.value if
                                        self._trainee_sponsorshipType is not None else None),
                },
                "trainingPartner": {
                    "uen": (self._trainingPartner_uen
                            if ("uen" not in st.session_state or st.session_state["uen"] is None)
                            else self._trainingPartner_uen),
                    "code": self._trainingPartner_code
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    def has_overridden_uen(self) -> bool:
        return self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0


class UpdateEnrolmentInfo(CreateEnrolmentInfo):
    """Class that encapsulates all information needed to update an enrolment record"""

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    @property
    def course_run_id(self):
        return self._course_run_id

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        if not isinstance(course_run_id, str):
            raise ValueError("Course Run ID must be a string!")

        self._course_run_id = course_run_id

    @property
    def course_referenceNumber(self):
        raise NotImplementedError("This method is not supported!")

    @course_referenceNumber.setter
    def course_referenceNumber(self, course_referenceNumber: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_id(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_fees_discountAmount(self):
        return self._trainee_fees_discountAmount

    @trainee_fees_discountAmount.setter
    def trainee_fees_discountAmount(self, discountAmount: Union[int, float]):
        if not isinstance(discountAmount, int) and not isinstance(discountAmount, float):
            raise ValueError("Discount Amount must be a number")
        elif discountAmount < 0:
            raise ValueError("Discount Amount must be a non-negative number!")

        self._trainee_fees_discountAmount = discountAmount

    @property
    def trainee_fees_collectionStatus(self):
        return self._trainee_fees_collectionStatus

    @trainee_fees_collectionStatus.setter
    def trainee_fees_collectionStatus(self, collectionStatus: CancellableCollectionStatus):
        if not isinstance(collectionStatus, CancellableCollectionStatus):
            try:
                collectionStatus = CancellableCollectionStatus(collectionStatus)
            except Exception:
                raise ValueError("Invalid Cancellable Collection Status provided!")

        self._trainee_fees_collectionStatus = collectionStatus

    @property
    def trainee_idType(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_idType.setter
    def trainee_idType(self, idType: IdTypeSummary):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_uen(self):
        raise NotImplementedError("This method is not supported!")

    @employer_uen.setter
    def employer_uen(self, uen: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_fullName(self):
        return self._trainee_employer_contact_fullName

    @employer_fullName.setter
    def employer_fullName(self, fullName: str):
        if not isinstance(fullName, str):
            raise ValueError("Invalid Full Name provided!")

        self._trainee_employer_contact_fullName = fullName

    @property
    def employer_emailAddress(self):
        return self._trainee_employer_contact_emailAddress

    @employer_emailAddress.setter
    def employer_emailAddress(self, emailAddress: str):
        if not isinstance(emailAddress, str):
            raise ValueError("Invalid Email Address provided!")

        self._trainee_employer_contact_emailAddress = emailAddress

    @property
    def employer_areaCode(self):
        return self._trainee_employer_contact_contactNumber_areaCode

    @employer_areaCode.setter
    def employer_areaCode(self, areaCode: str):
        if not isinstance(areaCode, str):
            raise ValueError("Invalid Area Code provided!")

        self._trainee_employer_contact_contactNumber_areaCode = areaCode

    @property
    def employer_countryCode(self):
        return self._trainee_employer_contact_contactNumber_countryCode

    @employer_countryCode.setter
    def employer_countryCode(self, countryCode: str):
        if not isinstance(countryCode, str):
            raise ValueError("Invalid Country Code provided!")

        self._trainee_employer_contact_contactNumber_countryCode = countryCode

    @property
    def employer_phoneNumber(self):
        return self._trainee_employer_contact_contactNumber_phoneNumber

    @employer_phoneNumber.setter
    def employer_phoneNumber(self, phoneNumber: str):
        if not isinstance(phoneNumber, str):
            raise ValueError("Invalid Phone Number provided!")

        self._trainee_employer_contact_contactNumber_phoneNumber = phoneNumber

    @property
    def trainee_fullName(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_fullName.setter
    def trainee_fullName(self, fullName: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_dateOfBirth(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_dateOfBirth.setter
    def trainee_dateOfBirth(self, dateOfBirth: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_emailAddress(self):
        return self._trainee_emailAddress

    @trainee_emailAddress.setter
    def trainee_emailAddress(self, emailAddress: str):
        if not isinstance(emailAddress, str):
            raise ValueError("Invalid Trainee Email Address provided!")

        self._trainee_emailAddress = emailAddress

    @property
    def trainee_contactNumber_areaCode(self):
        return self._trainee_contactNumber_areaCode

    @trainee_contactNumber_areaCode.setter
    def trainee_contactNumber_areaCode(self, areaCode: str):
        if not isinstance(areaCode, str):
            raise ValueError("Invalid Trainee Area Code provided!")

        self._trainee_contactNumber_areaCode = areaCode

    @property
    def trainee_contactNumber_countryCode(self):
        return self._trainee_contactNumber_countryCode

    @trainee_contactNumber_countryCode.setter
    def trainee_contactNumber_countryCode(self, countryCode: str):
        if not isinstance(countryCode, str):
            raise ValueError("Invalid Trainee Country Code provided!")

        self._trainee_contactNumber_countryCode = countryCode

    @property
    def trainee_contactNumber_phoneNumber(self):
        return self._trainee_contactNumber_phoneNumber

    @trainee_contactNumber_phoneNumber.setter
    def trainee_contactNumber_phoneNumber(self, phoneNumber: str):
        if not isinstance(phoneNumber, str):
            raise ValueError("Invalid Trainee Phone Number provided!")

        self._trainee_contactNumber_phoneNumber = phoneNumber

    @property
    def trainee_enrolmentDate(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_enrolmentDate.setter
    def trainee_enrolmentDate(self, enrolmentDate: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_sponsorshipType(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_sponsorshipType.setter
    def trainee_sponsorshipType(self, sponsorshipType: SponsorshipType):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainingPartner_code(self):
        raise NotImplementedError("This method is not supported!")

    @trainingPartner_code.setter
    def trainingPartner_code(self, code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainingPartner_uen(self):
        raise NotImplementedError("This method is not supported!")

    @trainingPartner_uen.setter
    def trainingPartner_uen(self, uen: str):
        raise NotImplementedError("This method is not supported!")

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._course_run_id is not None and len(self._course_run_id) == 0:
            errors.append("Course Run ID is empty even though it was marked as specified!")

        if self._trainee_employer_contact_emailAddress is not None and \
                len(self._trainee_employer_contact_emailAddress) > 0:
            if not Validators.verify_email(self._trainee_employer_contact_emailAddress):
                errors.append("Employer Email Address specified is not of the correct format!")

        if self._trainee_emailAddress is not None and \
                len(self._trainee_emailAddress) > 0:
            if not Validators.verify_email(self._trainee_emailAddress):
                errors.append("Trainee Email Address specified is not of the correct format!")

        # optional parameter validation
        if self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0 and not \
                Validators.verify_uen(self._trainingPartner_uen):
            errors.append("Invalid Training Partner UEN provided!")

        if self._trainee_employer_contact_fullName is not None and len(self._trainee_employer_contact_fullName) == 0:
            warnings.append("Employer Full Name is empty even though it was marked as specified!")

        if self._trainee_employer_contact_emailAddress is not None and \
                len(self._trainee_employer_contact_emailAddress) == 0:
            warnings.append("Employer Email Address is empty even though it was marked as specified!")

        if self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_areaCode)
            except ValueError:
                warnings.append("Employer Area Code is not a number!")
        elif self._trainee_employer_contact_contactNumber_areaCode is not None and \
                len(self._trainee_employer_contact_contactNumber_areaCode) == 0:
            warnings.append("Employer Area Code is empty even though it was marked as specified!")

        if self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_countryCode)
            except ValueError:
                warnings.append("Employer Country Code is not a number!")
        elif self._trainee_employer_contact_contactNumber_countryCode is not None and \
                len(self._trainee_employer_contact_contactNumber_countryCode) == 0:
            warnings.append("Employer Country Code is empty even though it was marked as specified!")

        if self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_employer_contact_contactNumber_phoneNumber)
            except ValueError:
                warnings.append("Employer Phone Number is not a number!")
        elif self._trainee_employer_contact_contactNumber_phoneNumber is not None and \
                len(self._trainee_employer_contact_contactNumber_phoneNumber) == 0:
            warnings.append("Employer Phone Number is empty even though it was marked as specified!")

        if self._trainee_emailAddress is not None and len(self._trainee_emailAddress) == 0:
            warnings.append("Trainee Email Address is empty even though it was marked as specified!")

        if self._trainee_contactNumber_areaCode is not None and len(self._trainee_contactNumber_areaCode) != 0:
            try:
                int(self._trainee_contactNumber_areaCode)
            except ValueError:
                warnings.append("Trainee Area Code is not a number!")
        elif self._trainee_contactNumber_areaCode is not None and len(self._trainee_contactNumber_areaCode) == 0:
            warnings.append("Trainee Area Code is empty even though it was marked as specified!")

        if self._trainee_contactNumber_countryCode is not None and len(self._trainee_contactNumber_countryCode) != 0:
            try:
                int(self._trainee_contactNumber_countryCode)
            except ValueError:
                warnings.append("Trainee Country Code is not a number!")
        elif self._trainee_contactNumber_countryCode is not None and len(self._trainee_contactNumber_countryCode) == 0:
            warnings.append("Trainee Country Code is empty though it was marked as specified!")

        if self._trainee_contactNumber_phoneNumber is not None and len(self._trainee_contactNumber_phoneNumber) != 0:
            try:
                int(self._trainee_contactNumber_phoneNumber)
            except ValueError:
                warnings.append("Trainee Phone Number is not a number!")
        elif self._trainee_contactNumber_phoneNumber is not None and len(self._trainee_contactNumber_phoneNumber) == 0:
            warnings.append("Trainee Phone Number is empty though it was marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        # skip verification as there is nothing to verify
        pl = {
            "enrolment": {
                "fees": {
                    "discountAmount": self._trainee_fees_discountAmount,
                    "collectionStatus": (self._trainee_fees_collectionStatus.value if
                                         self._trainee_fees_collectionStatus is not None else None)
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

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    def validate(self) -> tuple[list[str], list[str]]:
        errors, warnings = [], []

        if self._course_run_id is not None and len(self._course_run_id) == 0:
            errors.append("No valid Course Run ID specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        pl = {
            "enrolment": {
                "action": "Cancel",
                "course": {
                    "run": {
                        "id": self._course_run_id
                    }
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def course_run_id(self):
        return self._course_run_id

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        if not isinstance(course_run_id, str):
            raise ValueError("Invalid Course Run ID")

        self._course_run_id = course_run_id

    @property
    def trainee_fees_discountAmount(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_fees_discountAmount.setter
    def trainee_fees_discountAmount(self, discountAmount: Union[int, float]):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_fees_collectionStatus(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_fees_collectionStatus.setter
    def trainee_fees_collectionStatus(self, collectionStatus: CollectionStatus):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_fullName(self):
        raise NotImplementedError("This method is not supported!")

    @employer_fullName.setter
    def employer_fullName(self, fullName: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_emailAddress(self):
        raise NotImplementedError("This method is not supported!")

    @employer_emailAddress.setter
    def employer_emailAddress(self, emailAddress: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_areaCode(self):
        raise NotImplementedError("This method is not supported!")

    @employer_areaCode.setter
    def employer_areaCode(self, areaCode: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_countryCode(self):
        raise NotImplementedError("This method is not supported!")

    @employer_countryCode.setter
    def employer_countryCode(self, countryCode: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_phoneNumber(self):
        raise NotImplementedError("This method is not supported!")

    @employer_phoneNumber.setter
    def employer_phoneNumber(self, phoneNumber: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_emailAddress(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_emailAddress.setter
    def trainee_emailAddress(self, emailAddress: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_contactNumber_areaCode(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_contactNumber_areaCode.setter
    def trainee_contactNumber_areaCode(self, areaCode: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_contactNumber_countryCode(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_contactNumber_countryCode.setter
    def trainee_contactNumber_countryCode(self, countryCode: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_contactNumber_phoneNumber(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_contactNumber_phoneNumber.setter
    def trainee_contactNumber_phoneNumber(self, phoneNumber: str):
        raise NotImplementedError("This method is not supported!")


class SearchEnrolmentInfo(AbstractRequestInfo):
    """Contains information related to the query of an enrolment"""

    def __init__(self):
        self._lastUpdateDateTo: Annotated[Optional[datetime.date], "Formatted as YYYY-MM-DD"] = None
        self._lastUpdateDateFrom: Annotated[Optional[datetime.date], "Formatted as YYYY-MM-DD"] = None
        self._sortBy_field: Optional[EnrolmentSortField] = None
        self._sortBy_order: Optional[SortOrder] = None
        self._course_run_id: Annotated[Optional[str], "Max length of 20"] = None
        self._course_referenceNumber: Annotated[Optional[str], "Max length of 100"] = None
        self._course_status: Optional[EnrolmentCourseStatus] = None
        self._trainee_id: Annotated[Optional[str], "Max length of 20"] = None
        self._trainee_fees_feeCollectionStatus: Optional[CancellableCollectionStatus] = None
        self._trainee_idType_type: Optional[IdTypeSummary] = None
        self._trainee_employer_uen: Annotated[Optional[str], "Max length of 50"] = None
        self._trainee_enrolmentDate: Optional[datetime.date] = None
        self._trainee_sponsorshipType: Optional[SponsorshipType] = None
        self._trainingPartner_uen: Annotated[Optional[str], "Max length of 12"] = None
        self._trainingPartner_code: Annotated[Optional[str], "Max length of 15"] = None
        self._parameters_page: Annotated[int, "Minimum is 0"] = None
        self._parameters_page_size: Annotated[int, "Minimum is 1, Maximum is 100"] = None

    def __repr__(self):
        return self.payload(verify=False, as_json_str=True)

    def __str__(self):
        return self.__repr__()

    @property
    def lastUpdateDateTo(self):
        return self._lastUpdateDateTo

    @lastUpdateDateTo.setter
    def lastUpdateDateTo(self, lastUpdateDateTo: datetime.date):
        if not isinstance(lastUpdateDateTo, datetime.date):
            raise ValueError("No valid last update date to specified!")

        self._lastUpdateDateTo = lastUpdateDateTo

    @property
    def lastUpdateDateFrom(self):
        return self._lastUpdateDateFrom

    @lastUpdateDateFrom.setter
    def lastUpdateDateFrom(self, lastUpdateDateFrom: datetime.date):
        if not isinstance(lastUpdateDateFrom, datetime.date):
            raise ValueError("No valid last update date to specified!")

        self._lastUpdateDateFrom = lastUpdateDateFrom

    @property
    def sortBy_field(self):
        return self._sortBy_field

    @sortBy_field.setter
    def sortBy_field(self, sort_field: EnrolmentSortField):
        if not isinstance(sort_field, EnrolmentSortField):
            try:
                sort_field = EnrolmentSortField(sort_field)
            except Exception:
                raise ValueError("No valid sort field specified!")

        self._sortBy_field = sort_field

    @property
    def sortBy_order(self):
        return self._sortBy_order

    @sortBy_order.setter
    def sortBy_order(self, sort_order: SortOrder):
        if not isinstance(sort_order, SortOrder):
            try:
                sort_order = SortOrder(sort_order)
            except Exception:
                raise ValueError("No valid sort order specified!")

        self._sortBy_order = sort_order

    @property
    def course_run_id(self):
        return self._course_run_id

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        if not isinstance(course_run_id, str):
            raise ValueError("No valid course run ID specified!")

        self._course_run_id = course_run_id

    @property
    def course_referenceNumber(self):
        return self._course_referenceNumber

    @course_referenceNumber.setter
    def course_referenceNumber(self, course_referenceNumber: str):
        if not isinstance(course_referenceNumber, str):
            raise ValueError("No valid course reference number specified!")

        self._course_referenceNumber = course_referenceNumber

    @property
    def course_status(self):
        return self._course_status

    @course_status.setter
    def course_status(self, status: EnrolmentCourseStatus):
        if not isinstance(status, EnrolmentCourseStatus):
            try:
                status = EnrolmentCourseStatus(status)
            except Exception:
                raise ValueError("No valid course status specified!")

        self._course_status = status

    @property
    def trainee_id(self):
        return self._trainee_id

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        if not isinstance(trainee_id, str):
            raise ValueError("No valid trainee ID specified!")

        self._trainee_id = trainee_id

    @property
    def trainee_fees_feeCollectionStatus(self):
        return self._trainee_fees_feeCollectionStatus

    @trainee_fees_feeCollectionStatus.setter
    def trainee_fees_feeCollectionStatus(self, feeCollectionStatus: CancellableCollectionStatus):
        if not isinstance(feeCollectionStatus, CancellableCollectionStatus):
            try:
                feeCollectionStatus = CancellableCollectionStatus(feeCollectionStatus)
            except Exception:
                raise ValueError("No valid trainee fee collection status specified!")

        self._trainee_fees_feeCollectionStatus = feeCollectionStatus

    @property
    def trainee_idType(self):
        return self._trainee_idType_type

    @trainee_idType.setter
    def trainee_idType(self, idType: IdTypeSummary):
        if not isinstance(idType, IdTypeSummary):
            try:
                idType = IdTypeSummary(idType)
            except Exception:
                raise ValueError("No valid ID type specified!")

        self._trainee_idType_type = idType

    @property
    def employer_uen(self):
        return self._trainee_employer_uen

    @employer_uen.setter
    def employer_uen(self, uen: str):
        if not isinstance(uen, str):
            raise ValueError("No valid UEN specified!")

        self._trainee_employer_uen = uen

    @property
    def trainee_enrolmentDate(self):
        return self._trainee_enrolmentDate

    @trainee_enrolmentDate.setter
    def trainee_enrolmentDate(self, enrolmentDate: datetime.date):
        if not isinstance(enrolmentDate, datetime.date):
            raise ValueError("No valid employment date specified!")

        self._trainee_enrolmentDate = enrolmentDate

    @property
    def trainee_sponsorshipType(self):
        return self._trainee_sponsorshipType

    @trainee_sponsorshipType.setter
    def trainee_sponsorshipType(self, sponsorshipType: SponsorshipType):
        if not isinstance(sponsorshipType, SponsorshipType):
            try:
                sponsorshipType = SponsorshipType(sponsorshipType)
            except Exception:
                raise ValueError("No valid sponsorship type specified!")

        self._trainee_sponsorshipType = sponsorshipType

    @property
    def trainingPartner_uen(self):
        return self._trainingPartner_uen

    @trainingPartner_uen.setter
    def trainingPartner_uen(self, uen: str):
        if not isinstance(uen, str):
            raise ValueError("No valid UEN specified!")

        self._trainingPartner_uen = uen

    @property
    def trainingPartner_code(self):
        return self._trainingPartner_code

    @trainingPartner_code.setter
    def trainingPartner_code(self, code: str):
        if not isinstance(code, str):
            raise ValueError("No valid code specified!")

        self._trainingPartner_code = code

    @property
    def page(self):
        return self._parameters_page

    @page.setter
    def page(self, page: int):
        if not isinstance(page, int) or page < 0:
            raise ValueError("No valid page specified!")

        self._parameters_page = page

    @property
    def page_size(self):
        return self._parameters_page_size

    @page_size.setter
    def page_size(self, page_size: int):
        if not isinstance(page_size, int) or page_size < 0:
            raise ValueError("No valid page size specified!")

        self._parameters_page_size = page_size

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0 and not \
                Validators.verify_uen(self._trainingPartner_uen):
            errors.append("Invalid Training Partner UEN provided!")

        if self._trainingPartner_code is None or len(self._trainingPartner_code) == 0:
            errors.append("Invalid Training Partner Code provided!")

        if self._lastUpdateDateFrom is not None and self._lastUpdateDateTo is not None and \
                self._lastUpdateDateFrom > self._lastUpdateDateTo:
            warnings.append("Last Update Date From should not be after Date To!")

        if self._course_run_id is not None and len(self._course_run_id) == 0:
            warnings.append("Course Run ID is empty even though it is marked as specified!")

        if self._course_referenceNumber is not None and len(self._course_referenceNumber) == 0:
            warnings.append("Course Reference Number is empty even though it is marked as specified!")

        if self._trainee_id is not None and len(self._trainee_id) == 0:
            warnings.append("Trainee ID is empty even though it is marked as specified!")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
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
                "field": self._sortBy_field.value if self._sortBy_field is not None else None,
                "order": self._sortBy_order.value[0] if self._sortBy_order is not None else None
            },
            "enrolment": {
                "course": {
                    "run": {
                        "id": self._course_run_id
                    },
                    "referenceNumber": self._course_referenceNumber
                },
                "status": self._course_status.value if self._course_status is not None else None,
                "trainee": {
                    "id": self._trainee_id,
                    "fees": {
                        "feeCollectionStatus": (self._trainee_fees_feeCollectionStatus.value
                                                if self._trainee_fees_feeCollectionStatus is not None else None)
                    },
                    "idType": {
                        "type": self._trainee_idType_type.value if self._trainee_idType_type is not None else None
                    },
                    "employer": {
                        "uen": self._trainee_employer_uen
                    },
                    "enrolmentDate": (self._trainee_enrolmentDate.strftime("%Y-%m-%d") if
                                      self._trainee_enrolmentDate is not None else None),
                    "sponsorshipType": (self._trainee_sponsorshipType.value if
                                        self._trainee_sponsorshipType is not None else None),
                },
                "trainingPartner": {
                    "uen": (self._trainingPartner_uen
                            if ("uen" not in st.session_state or st.session_state["uen"] is None)
                            else st.session_state["uen"]),
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

    def has_overridden_uen(self) -> bool:
        return self._trainingPartner_uen is not None and len(self._trainingPartner_uen) > 0


class UpdateEnrolmentFeeCollectionInfo(UpdateEnrolmentInfo):
    """Contains information about the updating of enrolment fee collection"""

    def validate(self) -> tuple[list[str], list[str]]:
        errors = []
        warnings = []

        if self._trainee_fees_collectionStatus is None:
            errors.append("No Fee Collection Status provided")

        return errors, warnings

    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        if verify:
            err, _ = self.validate()

            if len(err) > 0:
                raise AttributeError("There are some required fields that are missing! Use payload() to find the "
                                     "missing fields!")

        pl = {
            "enrolment": {
                "fees": {
                    "collectionStatus": (self._trainee_fees_collectionStatus.value if
                                         self._trainee_fees_collectionStatus is not None else None)
                }
            }
        }

        pl = remove_null_fields(pl)

        if as_json_str:
            return json.dumps(pl)

        return pl

    @property
    def lastUpdateDateTo(self):
        raise NotImplementedError("This method is not supported!")

    @lastUpdateDateTo.setter
    def lastUpdateDateTo(self, lastUpdateDateTo: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def lastUpdateDateFrom(self):
        raise NotImplementedError("This method is not supported!")

    @lastUpdateDateFrom.setter
    def lastUpdateDateFrom(self, lastUpdateDateFrom: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def sortBy_field(self):
        raise NotImplementedError("This method is not supported!")

    @sortBy_field.setter
    def sortBy_field(self, sort_field: EnrolmentSortField):
        raise NotImplementedError("This method is not supported!")

    @property
    def sortBy_order(self):
        raise NotImplementedError("This method is not supported!")

    @sortBy_order.setter
    def sortBy_order(self, sort_order: SortOrder):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_run_id(self):
        raise NotImplementedError("This method is not supported!")

    @course_run_id.setter
    def course_run_id(self, course_run_id: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_referenceNumber(self):
        raise NotImplementedError("This method is not supported!")

    @course_referenceNumber.setter
    def course_referenceNumber(self, course_referenceNumber: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def course_status(self):
        raise NotImplementedError("This method is not supported!")

    @course_status.setter
    def course_status(self, status: EnrolmentCourseStatus):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_id(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_id.setter
    def trainee_id(self, trainee_id: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_fees_feeCollectionStatus(self):
        return self._trainee_fees_feeCollectionStatus

    @trainee_fees_feeCollectionStatus.setter
    def trainee_fees_feeCollectionStatus(self, feeCollectionStatus: CancellableCollectionStatus):
        if not isinstance(feeCollectionStatus, CancellableCollectionStatus):
            try:
                feeCollectionStatus = CancellableCollectionStatus(feeCollectionStatus)
            except Exception:
                raise ValueError("No valid trainee fee collection status specified!")

        self._trainee_fees_feeCollectionStatus = feeCollectionStatus

    @property
    def trainee_idType(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_idType.setter
    def trainee_idType(self, idType: IdTypeSummary):
        raise NotImplementedError("This method is not supported!")

    @property
    def employer_uen(self):
        raise NotImplementedError("This method is not supported!")

    @employer_uen.setter
    def employer_uen(self, uen: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_enrolmentDate(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_enrolmentDate.setter
    def trainee_enrolmentDate(self, enrolmentDate: datetime.date):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainee_sponsorshipType(self):
        raise NotImplementedError("This method is not supported!")

    @trainee_sponsorshipType.setter
    def trainee_sponsorshipType(self, sponsorshipType: SponsorshipType):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainingPartner_uen(self):
        raise NotImplementedError("This method is not supported!")

    @trainingPartner_uen.setter
    def trainingPartner_uen(self, uen: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def trainingPartner_code(self):
        raise NotImplementedError("This method is not supported!")

    @trainingPartner_code.setter
    def trainingPartner_code(self, code: str):
        raise NotImplementedError("This method is not supported!")

    @property
    def page(self):
        raise NotImplementedError("This method is not supported!")

    @page.setter
    def page(self, page: int):
        raise NotImplementedError("This method is not supported!")

    @property
    def page_size(self):
        raise NotImplementedError("This method is not supported!")

    @page_size.setter
    def page_size(self, page_size: int):
        raise NotImplementedError("This method is not supported!")
