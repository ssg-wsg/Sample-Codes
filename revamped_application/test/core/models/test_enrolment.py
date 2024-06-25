"""
This file contains test cases for the different Enrolment model classes.
"""

import datetime
import unittest

from revamped_application.core.constants import CollectionStatus, IdTypeSummary, SponsorshipType, EnrolmentSortField, \
    SortOrder, EnrolmentCourseStatus, CancellableCollectionStatus
from revamped_application.core.models.enrolment import CreateEnrolmentInfo, UpdateEnrolmentInfo, CancelEnrolmentInfo, \
    SearchEnrolmentInfo, UpdateEnrolmentFeeCollectionInfo


class TestEnrolmentInfo(unittest.TestCase):
    """Class to test classes and methods related to the Enrolment API."""

    COURSE_RUN_ID_ONE = "10026"
    COURSE_RUN_ID_TWO = "10027"
    COURSE_REFERENCE_NUMBER_ONE = "TGS-0026008-ES"
    COURSE_REFERENCE_NUMBER_TWO = "TGS-0026008-ESS"
    TRAINEE_ID_ONE = "S0118316H"
    TRAINEE_ID_TWO = "S4524623Z"
    DISCOUNT_AMOUNT_ONE = 50.25
    DISCOUNT_AMOUNT_TWO = 51.25
    COLLECTION_STATUS_ONE = CollectionStatus.FULL_PAYMENT
    COLLECTION_STATUS_TWO = CollectionStatus.PENDING_PAYMENT
    ID_TYPE_ONE = IdTypeSummary.NRIC
    ID_TYPE_TWO = IdTypeSummary.FIN
    EMPLOYER_UEN_ONE = "12345678X"
    EMPLOYER_UEN_TWO = "123456789X"
    EMPLOYER_FULL_NAME_ONE = "John Doe"
    EMPLOYER_FULL_NAME_TWO = "Jane Doe"
    EMPLOYER_EMAIL_ONE = "john@email.com"
    EMPLOYER_EMAIL_TWO = "jane@email.com"
    EMPLOYER_AREA_CODE_ONE = "123"
    EMPLOYER_AREA_CODE_TWO = "321"
    EMPLOYER_COUNTRY_CODE_ONE = "12"
    EMPLOYER_COUNTRY_CODE_TWO = "21"
    EMPLOYER_PHONE_NUMBER_ONE = "91234567"
    EMPLOYER_PHONE_NUMBER_TWO = "81234567"
    TRAINEE_FULL_NAME_ONE = "Jake Doe"
    TRAINEE_FULL_NAME_TWO = "Jack Doe"
    TRAINEE_DATE_OF_BIRTH_ONE = datetime.date(2000, 1, 1)
    TRAINEE_DATE_OF_BIRTH_TWO = datetime.date(1999, 1, 1)
    TRAINEE_EMAIL_ONE = "jake@email.com"
    TRAINEE_EMAIL_TWO = "jane@email.com"
    TRAINEE_AREA_CODE_ONE = "456"
    TRAINEE_AREA_CODE_TWO = "654"
    TRAINEE_COUNTRY_CODE_ONE = "34"
    TRAINEE_COUNTRY_CODE_TWO = "43"
    TRAINEE_PHONE_NUMBER_ONE = "81234967"
    TRAINEE_PHONE_NUMBER_TWO = "91234867"
    ENROLMENT_DATE_ONE = datetime.date(2023, 12, 2)
    ENROLMENT_DATE_TWO = datetime.date(2024, 12, 2)
    SPONSORSHIP_TYPE_ONE = SponsorshipType.EMPLOYER
    SPONSORSHIP_TYPE_TWO = SponsorshipType.INDIVIDUAL
    TRAINING_PARTNER_UEN_ONE = "T16GB0003C"
    TRAINING_PARTNER_UEN_TWO = "T16GB0003S"
    TRAINING_PARTNER_CODE_ONE = "T16GB0003C-01"
    TRAINING_PARTNER_CODE_TWO = "T16GB0003S-01"

    LAST_UPDATE_DATE_TO_ONE = datetime.date(2023, 12, 2)
    LAST_UPDATE_DATE_TO_TWO = datetime.date(2024, 12, 2)
    LAST_UPDATE_DATE_FROM_ONE = datetime.date(2023, 12, 1)
    LAST_UPDATE_DATE_FROM_TWO = datetime.date(2024, 12, 1)
    SORT_BY_FIELD_ONE = EnrolmentSortField.UPDATED_ON
    SORT_BY_FIELD_TWO = EnrolmentSortField.CREATED_ON
    SORT_ORDER_ONE = SortOrder.ASCENDING
    SORT_ORDER_TWO = SortOrder.DESCENDING
    COURSE_STATUS_ONE = EnrolmentCourseStatus.CONFIRMED
    COURSE_STATUS_TWO = EnrolmentCourseStatus.CANCELLED
    FEE_COLLECTION_STATUS_ONE = CancellableCollectionStatus.CANCELLED
    FEE_COLLECTION_STATUS_TWO = CancellableCollectionStatus.FULL_PAYMENT
    PAGE_ONE = 1
    PAGE_TWO = 2
    PAGE_SIZE_ONE = 10
    PAGE_SIZE_TWO = 20

    CREATE_ENROLMENT_INFO_ONE: CreateEnrolmentInfo = None
    CREATE_ENROLMENT_INFO_TWO: CreateEnrolmentInfo = None
    CREATE_ENROLMENT_INFO_THREE: CreateEnrolmentInfo = None

    UPDATE_ENROLMENT_INFO_ONE: UpdateEnrolmentInfo = None
    UPDATE_ENROLMENT_INFO_TWO: UpdateEnrolmentInfo = None
    UPDATE_ENROLMENT_INFO_THREE: UpdateEnrolmentInfo = None

    CANCEL_ENROLMENT_INFO: CancelEnrolmentInfo = None

    SEARCH_ENROLMENT_INFO_ONE: SearchEnrolmentInfo = None
    SEARCH_ENROLMENT_INFO_TWO: SearchEnrolmentInfo = None
    SEARCH_ENROLMENT_INFO_THREE: SearchEnrolmentInfo = None

    UPDATE_ENROLMENT_FEE_COLLECTION_ONE: UpdateEnrolmentFeeCollectionInfo = None
    UPDATE_ENROLMENT_FEE_COLLECTION_TWO: UpdateEnrolmentFeeCollectionInfo = None

    def __set_up_create_enrolment_info(self):
        # first instance is empty
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE = CreateEnrolmentInfo()

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO = CreateEnrolmentInfo()
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._course_referenceNumber = (
            TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_id = TestEnrolmentInfo.TRAINEE_ID_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._discount_amount = TestEnrolmentInfo.DISCOUNT_AMOUNT_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._collection_status = TestEnrolmentInfo.COLLECTION_STATUS_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_idType_type = TestEnrolmentInfo.ID_TYPE_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_fullName = (
            TestEnrolmentInfo.EMPLOYER_FULL_NAME_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_emailAddress = (
            TestEnrolmentInfo.EMPLOYER_EMAIL_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_areaCode = (
            TestEnrolmentInfo.EMPLOYER_AREA_CODE_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_countryCode = (
            TestEnrolmentInfo.EMPLOYER_COUNTRY_CODE_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_phoneNumber = (
            TestEnrolmentInfo.EMPLOYER_PHONE_NUMBER_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fullName = TestEnrolmentInfo.TRAINEE_FULL_NAME_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_dateOfBirth = TestEnrolmentInfo.TRAINEE_DATE_OF_BIRTH_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_emailAddress = TestEnrolmentInfo.TRAINEE_EMAIL_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_areaCode = (
            TestEnrolmentInfo.TRAINEE_AREA_CODE_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_countryCode = (
            TestEnrolmentInfo.TRAINEE_COUNTRY_CODE_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_phoneNumber = (
            TestEnrolmentInfo.TRAINEE_PHONE_NUMBER_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_sponsorshipType = (
            TestEnrolmentInfo.SPONSORSHIP_TYPE_ONE)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_uen = TestEnrolmentInfo.TRAINING_PARTNER_UEN_ONE
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_code = TestEnrolmentInfo.TRAINING_PARTNER_CODE_ONE

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE = CreateEnrolmentInfo()
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._course_referenceNumber = (
            TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_id = TestEnrolmentInfo.TRAINEE_ID_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._discount_amount = TestEnrolmentInfo.DISCOUNT_AMOUNT_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._collection_status = TestEnrolmentInfo.COLLECTION_STATUS_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_idType_type = TestEnrolmentInfo.ID_TYPE_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_fullName = (
            TestEnrolmentInfo.EMPLOYER_FULL_NAME_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_emailAddress = \
            TestEnrolmentInfo.EMPLOYER_EMAIL_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_areaCode = (
            TestEnrolmentInfo.EMPLOYER_AREA_CODE_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_countryCode = (
            TestEnrolmentInfo.EMPLOYER_COUNTRY_CODE_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_phoneNumber = (
            TestEnrolmentInfo.EMPLOYER_PHONE_NUMBER_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fullName = TestEnrolmentInfo.TRAINEE_FULL_NAME_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_dateOfBirth = TestEnrolmentInfo.TRAINEE_DATE_OF_BIRTH_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_emailAddress = TestEnrolmentInfo.TRAINEE_EMAIL_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_areaCode = (
            TestEnrolmentInfo.TRAINEE_AREA_CODE_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_countryCode = (
            TestEnrolmentInfo.TRAINEE_COUNTRY_CODE_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_phoneNumber = (
            TestEnrolmentInfo.TRAINEE_PHONE_NUMBER_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_sponsorshipType = (
            TestEnrolmentInfo.SPONSORSHIP_TYPE_TWO)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_uen = TestEnrolmentInfo.TRAINING_PARTNER_UEN_TWO
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_code = (
            TestEnrolmentInfo.TRAINING_PARTNER_CODE_TWO)

    def __set_up_update_enrolment_info(self):
        # first instance is empty
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE = UpdateEnrolmentInfo()

        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO = UpdateEnrolmentInfo()
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_fees_discountAmount = TestEnrolmentInfo.DISCOUNT_AMOUNT_ONE
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_fees_collectionStatus = (
            TestEnrolmentInfo.COLLECTION_STATUS_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_ONE
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_emailAddress = TestEnrolmentInfo.TRAINEE_EMAIL_ONE
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_contactNumber_areaCode = (
            TestEnrolmentInfo.TRAINEE_AREA_CODE_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_contactNumber_countryCode = (
            TestEnrolmentInfo.TRAINEE_COUNTRY_CODE_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_contactNumber_phoneNumber = (
            TestEnrolmentInfo.TRAINEE_PHONE_NUMBER_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_employer_contact_emailAddress = (
            TestEnrolmentInfo.EMPLOYER_EMAIL_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_employer_contact_fullName = (
            TestEnrolmentInfo.EMPLOYER_FULL_NAME_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_areaCode = (
            TestEnrolmentInfo.EMPLOYER_AREA_CODE_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_countryCode = (
            TestEnrolmentInfo.EMPLOYER_COUNTRY_CODE_ONE)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_phoneNumber = (
            TestEnrolmentInfo.EMPLOYER_PHONE_NUMBER_ONE)

        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE = UpdateEnrolmentInfo()
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_fees_discountAmount = (
            TestEnrolmentInfo.DISCOUNT_AMOUNT_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_fees_collectionStatus = (
            TestEnrolmentInfo.COLLECTION_STATUS_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_TWO
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_emailAddress = TestEnrolmentInfo.TRAINEE_EMAIL_TWO
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_contactNumber_areaCode = (
            TestEnrolmentInfo.TRAINEE_AREA_CODE_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_contactNumber_countryCode = (
            TestEnrolmentInfo.TRAINEE_COUNTRY_CODE_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_contactNumber_phoneNumber = (
            TestEnrolmentInfo.TRAINEE_PHONE_NUMBER_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_employer_contact_emailAddress = (
            TestEnrolmentInfo.EMPLOYER_EMAIL_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_employer_contact_fullName = (
            TestEnrolmentInfo.EMPLOYER_FULL_NAME_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_areaCode = (
            TestEnrolmentInfo.EMPLOYER_AREA_CODE_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_countryCode = (
            TestEnrolmentInfo.EMPLOYER_COUNTRY_CODE_TWO)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_phoneNumber = (
            TestEnrolmentInfo.EMPLOYER_PHONE_NUMBER_TWO)

    def __set_up_cancel_enrolment_info(self):
        TestEnrolmentInfo.CANCEL_ENROLMENT_INFO = CancelEnrolmentInfo()

    def __set_up_search_enrolment_info(self):
        # first instance is empty
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE = SearchEnrolmentInfo()

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO = SearchEnrolmentInfo()
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateTo = TestEnrolmentInfo.LAST_UPDATE_DATE_TO_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateFrom = TestEnrolmentInfo.LAST_UPDATE_DATE_FROM_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._sortBy_field = TestEnrolmentInfo.SORT_BY_FIELD_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._sortBy_order = TestEnrolmentInfo.SORT_ORDER_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_referenceNumber = (
            TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_ONE)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_status = TestEnrolmentInfo.COURSE_STATUS_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_id = TestEnrolmentInfo.TRAINEE_ID_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_fees_feeCollectionStatus = (
            TestEnrolmentInfo.FEE_COLLECTION_STATUS_ONE)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_idType_type = TestEnrolmentInfo.ID_TYPE_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_sponsorshipType = (
            TestEnrolmentInfo.SPONSORSHIP_TYPE_ONE)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainingPartner_uen = TestEnrolmentInfo.TRAINING_PARTNER_UEN_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainingPartner_code = TestEnrolmentInfo.TRAINING_PARTNER_CODE_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page = TestEnrolmentInfo.PAGE_ONE
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page_size = TestEnrolmentInfo.PAGE_SIZE_ONE

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE = SearchEnrolmentInfo()
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateTo = TestEnrolmentInfo.LAST_UPDATE_DATE_TO_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateFrom = TestEnrolmentInfo.LAST_UPDATE_DATE_FROM_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._sortBy_field = TestEnrolmentInfo.SORT_BY_FIELD_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._sortBy_order = TestEnrolmentInfo.SORT_ORDER_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_referenceNumber = (
            TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_TWO)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_status = TestEnrolmentInfo.COURSE_STATUS_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_id = TestEnrolmentInfo.TRAINEE_ID_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_fees_feeCollectionStatus = (
            TestEnrolmentInfo.FEE_COLLECTION_STATUS_TWO)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_idType_type = TestEnrolmentInfo.ID_TYPE_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_sponsorshipType = (
            TestEnrolmentInfo.SPONSORSHIP_TYPE_TWO)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainingPartner_uen = TestEnrolmentInfo.TRAINING_PARTNER_UEN_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainingPartner_code = (
            TestEnrolmentInfo.TRAINING_PARTNER_CODE_TWO)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page = TestEnrolmentInfo.PAGE_TWO
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page_size = TestEnrolmentInfo.PAGE_SIZE_TWO

    def __set_up_update_enrolment_fee_collection_info(self):
        # first instance is empty
        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE = UpdateEnrolmentFeeCollectionInfo()

        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO = UpdateEnrolmentFeeCollectionInfo()
        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO._trainee_fees_collectionStatus = (
            TestEnrolmentInfo.COLLECTION_STATUS_TWO)

    def setUp(self):
        self.__set_up_create_enrolment_info()
        self.__set_up_update_enrolment_info()
        self.__set_up_cancel_enrolment_info()
        self.__set_up_search_enrolment_info()
        self.__set_up_update_enrolment_fee_collection_info()

    def test_CreateEnrolmentInfo_validate(self):
        e1, _ = TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.validate()
        e2, _ = TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.validate()
        e3, _ = TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_CreateEnrolmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.payload()

        p2 = {
            "enrolment": {
                "course": {
                    "run": {
                        "id": "10026"
                    },
                    "referenceNumber": "TGS-0026008-ES"
                },
                "trainee": {
                    "id": "S0118316H",
                    "idType": {
                        "type": "NRIC"
                    },
                    "employer": {
                        "uen": "12345678X",
                        "contact": {
                            "fullName": "John Doe",
                            "emailAddress": "john@email.com",
                            "contactNumber": {
                                "areaCode": "123",
                                "countryCode": "12",
                                "phoneNumber": "91234567"
                            }
                        }
                    },
                    "fullName": "Jake Doe",
                    "dateOfBirth": "2000-01-01",
                    "emailAddress": "jake@email.com",
                    "contactNumber": {
                        "areaCode": "456",
                        "countryCode": "34",
                        "phoneNumber": "81234967"
                    },
                    "enrolmentDate": "2023-12-02",
                    "sponsorshipType": "EMPLOYER"
                },
                "trainingPartner": {
                    "uen": "T16GB0003C",
                    "code": "T16GB0003C-01"
                }
            }
        }
        p3 = {
            "enrolment": {
                "course": {
                    "run": {
                        "id": "10027"
                    },
                    "referenceNumber": "TGS-0026008-ESS"
                },
                "trainee": {
                    "id": "S4524623Z",
                    "idType": {
                        "type": "FIN"
                    },
                    "employer": {
                        "uen": "123456789X",
                        "contact": {
                            "fullName": "Jane Doe",
                            "emailAddress": "jane@email.com",
                            "contactNumber": {
                                "areaCode": "321",
                                "countryCode": "21",
                                "phoneNumber": "81234567"
                            }
                        }
                    },
                    "fullName": "Jack Doe",
                    "dateOfBirth": "1999-01-01",
                    "emailAddress": "jane@email.com",
                    "contactNumber": {
                        "areaCode": "654",
                        "countryCode": "43",
                        "phoneNumber": "91234867"
                    },
                    "enrolmentDate": "2024-12-02",
                    "sponsorshipType": "INDIVIDUAL"
                },
                "trainingPartner": {
                    "uen": "T16GB0003S",
                    "code": "T16GB0003S-01"
                }
            }
        }

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.payload(), p2)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.payload(), p3)

    def test_CreateEnrolmentInfo_has_overridden_uen(self):
        self.assertFalse(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.has_overridden_uen())
        self.assertTrue(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.has_overridden_uen())
        self.assertTrue(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.has_overridden_uen())

    def test_CreateEnrolmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.course_run_id = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.course_run_id = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.course_run_id = [1234]

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_run_id = "1234"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_run_id = "431"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_run_id = "645435"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_run_id, "1234")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_run_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_run_id, "431")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_run_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_run_id, "645435")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_run_id)

    def test_CreateEnrolmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.course_referenceNumber = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.course_referenceNumber = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.course_referenceNumber = [1234]

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_referenceNumber = "1234"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_referenceNumber = "431"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_referenceNumber = "76545"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_referenceNumber, "1234")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_referenceNumber)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_referenceNumber, "431")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_referenceNumber)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_referenceNumber, "76545")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_referenceNumber)

    def test_CreateEnrolmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_id = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_id = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_id = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_id = "S1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_id = "T1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_id = "T0987654X"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_id, "S1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_id,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_id)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_id, "T1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_id,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_id)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_id, "T0987654X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_id,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_id)

    def test_CreateEnrolmentInfo_set_trainee_fees_discount_amount(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_discountAmount = "abc"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_discountAmount = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_discountAmount = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_discountAmount = 123.45
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_discountAmount = 123.45
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_discountAmount = 123.45

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fees_discountAmount, 123.45)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fees_discountAmount,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_discountAmount)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fees_discountAmount, 123.45)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fees_discountAmount,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_discountAmount)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fees_discountAmount, 123.45)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fees_discountAmount,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_discountAmount)

    def test_CreateEnrolmentInfo_set_trainee_fees_collection_status(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus = CollectionStatus.FULL_PAYMENT
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus = CollectionStatus.PENDING_PAYMENT
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus = CollectionStatus.PARTIAL_PAYMENT

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fees_collectionStatus,
                         CollectionStatus.FULL_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fees_collectionStatus,
                         CollectionStatus.PENDING_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fees_collectionStatus,
                         CollectionStatus.PARTIAL_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus)

    def test_CreateEnrolmentInfo_set_trainee_id_type(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_idType = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_idType = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_idType = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_idType = IdTypeSummary.NRIC
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_idType = IdTypeSummary.FIN
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_idType = IdTypeSummary.OTHERS

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_idType_type, IdTypeSummary.NRIC)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_idType_type,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_idType)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_idType_type, IdTypeSummary.FIN)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_idType_type,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_idType)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_idType_type, IdTypeSummary.OTHERS)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_idType_type,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_idType)

    def test_CreateEnrolmentInfo_set_employer_uen(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_uen = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_uen = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_uen = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_uen = "G1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_uen = "T1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_uen = "T0987654X"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_uen, "G1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_uen)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_uen, "T1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_uen)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_uen, "T0987654X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_uen)

    def test_CreateEnrolmentInfo_set_trainee_employer_contact_full_name(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_fullName = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_fullName = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_fullName = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_fullName = "John Doe"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_fullName = "Jane Doe"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_fullName = "Jack Doe"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_fullName, "John Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_fullName)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_fullName, "Jane Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_fullName)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_fullName, "Jack Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_fullName)

    def test_CreateEnrolmentInfo_set_trainee_employer_contact_email_address(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_emailAddress = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_emailAddress = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_emailAddress = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_emailAddress = "email1@email.com"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_emailAddress = "email2@email.com"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_emailAddress = "email3@email.com"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_emailAddress,
                         "email1@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_emailAddress)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_emailAddress,
                         "email2@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_emailAddress)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_emailAddress,
                         "email3@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_emailAddress)

    def test_CreateEnrolmentInfo_set_trainee_employer_contact_number_area_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_areaCode = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_areaCode = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_areaCode = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_areaCode = "123"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_areaCode = "456"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_areaCode = "789"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_areaCode,
                         "123")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_areaCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_areaCode,
                         "456")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_areaCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_areaCode,
                         "789")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_areaCode)

    def test_CreateEnrolmentInfo_set_trainee_employer_contact_number_country_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_countryCode = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_countryCode = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_countryCode = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_countryCode = "12"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_countryCode = "34"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_countryCode = "56"

        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_countryCode,
            "12")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_countryCode,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_countryCode,
        )
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_countryCode,
            "34")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_countryCode,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_countryCode,
        )
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_countryCode,
            "56")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_countryCode,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_countryCode,
        )

    def test_CreateEnrolmentInfo_set_trainee_employer_contact_number_phone_number(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_phoneNumber = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_phoneNumber = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_phoneNumber = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_phoneNumber = "91234567"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_phoneNumber = "81234567"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_phoneNumber = "71234567"

        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_phoneNumber,
            "91234567")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_employer_contact_contactNumber_phoneNumber,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.employer_phoneNumber
        )
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_phoneNumber,
            "81234567")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_employer_contact_contactNumber_phoneNumber,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.employer_phoneNumber
        )
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_phoneNumber,
            "71234567")
        self.assertEqual(
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_employer_contact_contactNumber_phoneNumber,
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.employer_phoneNumber
        )

    def test_CreateEnrolmentInfo_set_trainee_full_name(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fullName = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fullName = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fullName = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fullName = "John Doe"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fullName = "Jane Doe"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fullName = "Jack Doe"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fullName, "John Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_fullName)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fullName, "Jane Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_fullName)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fullName, "Jack Doe")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_fullName,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_fullName)

    def test_CreateEnrolmentInfo_set_trainee_date_of_birth(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_dateOfBirth = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_dateOfBirth = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_dateOfBirth = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_dateOfBirth = datetime.date(1990, 1, 1)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_dateOfBirth = datetime.date(1991, 1, 1)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_dateOfBirth = datetime.date(1992, 1, 1)

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_dateOfBirth, datetime.date(1990, 1, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_dateOfBirth,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_dateOfBirth)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_dateOfBirth, datetime.date(1991, 1, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_dateOfBirth,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_dateOfBirth)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_dateOfBirth, datetime.date(1992, 1, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_dateOfBirth,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_dateOfBirth)

    def test_CreateEnrolmentInfo_set_trainee_email_address(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_emailAddress = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_emailAddress = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_emailAddress = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_emailAddress = "email1@email.com"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_emailAddress = "email2@email.com"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_emailAddress = "email3@email.com"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_emailAddress, "email1@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_emailAddress)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_emailAddress, "email2@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_emailAddress)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_emailAddress, "email3@email.com")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_emailAddress,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_emailAddress)

    def test_CreateEnrolmentInfo_set_trainee_contact_number_area_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_areaCode = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_areaCode = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_areaCode = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_areaCode = "123"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_areaCode = "456"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_areaCode = "789"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_areaCode, "123")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_areaCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_areaCode, "456")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_areaCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_areaCode, "789")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_areaCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_areaCode)

    def test_CreateEnrolmentInfo_set_trainee_contact_number_country_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_countryCode = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_countryCode = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_countryCode = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_countryCode = "12"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_countryCode = "34"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_countryCode = "56"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_countryCode, "12")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_countryCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_countryCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_countryCode, "34")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_countryCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_countryCode)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_countryCode, "56")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_countryCode,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_countryCode)

    def test_CreateEnrolmentInfo_set_trainee_contact_number_phone_number(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_phoneNumber = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_phoneNumber = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_phoneNumber = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_phoneNumber = "91234567"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_phoneNumber = "81234567"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_phoneNumber = "71234567"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_phoneNumber, "91234567")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_contactNumber_phoneNumber,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_contactNumber_phoneNumber)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_phoneNumber, "81234567")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_contactNumber_phoneNumber,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_contactNumber_phoneNumber)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_phoneNumber, "71234567")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_contactNumber_phoneNumber,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_contactNumber_phoneNumber)

    def test_CreateEnrolmentInfo_set_trainee_enrolment_date(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_enrolmentDate = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_enrolmentDate = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_enrolmentDate = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_enrolmentDate = datetime.date(2019, 1, 1)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_enrolmentDate = datetime.date(2019, 2, 1)
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_enrolmentDate = datetime.date(2019, 3, 1)

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_enrolmentDate, datetime.date(2019, 1, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_enrolmentDate,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_enrolmentDate)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_enrolmentDate, datetime.date(2019, 2, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_enrolmentDate,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_enrolmentDate)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_enrolmentDate,
                         datetime.date(2019, 3, 1))
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainee_enrolmentDate,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_enrolmentDate)

    def test_CreateEnrolmentInfo_set_trainee_sponsorship_type(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_sponsorshipType = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_sponsorshipType = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainee_sponsorshipType = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_sponsorshipType = SponsorshipType.EMPLOYER
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_sponsorshipType = SponsorshipType.INDIVIDUAL

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_sponsorshipType,
                         SponsorshipType.EMPLOYER)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainee_sponsorshipType,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainee_sponsorshipType)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_sponsorshipType,
                         SponsorshipType.INDIVIDUAL)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainee_sponsorshipType,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainee_sponsorshipType)

    def test_CreateEnrolmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_code = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_code = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_code = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_code = "1234"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_code = "431"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_code = "645435"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainingPartner_code, "1234")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainingPartner_code,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_code)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_code, "431")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_code,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_code)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_code, "645435")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_code,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_code)

    def test_CreateEnrolmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_uen = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_uen = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_uen = [1234]

        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_uen = "G1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_uen = "A1234567X"
        TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_uen = "AB123AB123"

        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainingPartner_uen, "G1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE._trainingPartner_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_ONE.trainingPartner_uen)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_uen, "A1234567X")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO._trainingPartner_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_TWO.trainingPartner_uen)
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_uen, "AB123AB123")
        self.assertEqual(TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE._trainingPartner_uen,
                         TestEnrolmentInfo.CREATE_ENROLMENT_INFO_THREE.trainingPartner_uen)

    def test_UpdateEnrolmentInfo_validate(self):
        e1, _ = TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.validate()
        e2, _ = TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.validate()
        e3, _ = TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.validate()

        self.assertTrue(len(e1) == 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_UpdateEnrolmentInfo_payload(self):
        p1 = {
            "enrolment": {
                "action": "Update"
            }
        }

        p2 = {
            "enrolment": {
                "fees": {
                    "discountAmount": 50.25,
                    "collectionStatus": "Full Payment"
                },
                "action": "Update",
                "course": {
                    "run": {
                        "id": "10026"
                    }
                },
                "trainee": {
                    "email": "jake@email.com",
                    "contactNumber": {
                        "areaCode": "456",
                        "countryCode": "34",
                        "phoneNumber": "81234967"
                    }
                },
                "employer": {
                    "contact": {
                        "email": "john@email.com",
                        "fullName": "John Doe",
                        "contactNumber": {
                            "areaCode": "123",
                            "countryCode": "12",
                            "phoneNumber": "91234567"
                        }
                    }
                }
            }
        }

        p3 = {
            "enrolment": {
                "fees": {
                    "discountAmount": 51.25,
                    "collectionStatus": "Pending Payment"
                },
                "action": "Update",
                "course": {
                    "run": {
                        "id": "10027"
                    }
                },
                "trainee": {
                    "email": "jane@email.com",
                    "contactNumber": {
                        "areaCode": "654",
                        "countryCode": "43",
                        "phoneNumber": "91234867"
                    }
                },
                "employer": {
                    "contact": {
                        "email": "jane@email.com",
                        "fullName": "Jane Doe",
                        "contactNumber": {
                            "areaCode": "321",
                            "countryCode": "21",
                            "phoneNumber": "81234567"
                        }
                    }
                }
            }
        }

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.payload(), p1)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.payload(), p2)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.payload(), p3)

    def test_UpdateEnrolmentInfo_set_trainee_fees_collection_status(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus = ["abc"]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus = [1234]

        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.FULL_PAYMENT)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.PENDING_PAYMENT)
        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.PARTIAL_PAYMENT)

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.FULL_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.PENDING_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.PARTIAL_PAYMENT)

        TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.CANCELLED
        )

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.CANCELLED)

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_fees_collectionStatus)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_fees_collectionStatus)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE._trainee_fees_collectionStatus,
                         TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_fees_collectionStatus)

    def test_UpdateEnrolmentInfo_set_course_reference_number(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.course_referenceNumber = (
                TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.course_referenceNumber = (
                TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_TWO)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.course_referenceNumber = (
                TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_ONE)

    def test_UpdateEnrolmentInfo_set_trainee_id(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_id = TestEnrolmentInfo.TRAINEE_ID_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_id = TestEnrolmentInfo.TRAINEE_ID_TWO

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_id = TestEnrolmentInfo.TRAINEE_ID_ONE

    def test_UpdateEnrolmentInfo_set_trainee_id_type(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_idType = TestEnrolmentInfo.ID_TYPE_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_idType = TestEnrolmentInfo.ID_TYPE_TWO

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_idType = TestEnrolmentInfo.ID_TYPE_ONE

    def test_UpdateEnrolmentInfo_set_employer_uen(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_TWO

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_ONE

    def test_UpdateEnrolmentInfo_set_trainee_full_name(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_fullName = TestEnrolmentInfo.TRAINEE_FULL_NAME_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_fullName = TestEnrolmentInfo.TRAINEE_FULL_NAME_TWO

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_fullName = TestEnrolmentInfo.TRAINEE_FULL_NAME_ONE

    def test_UpdateEnrolmentInfo_set_trainee_date_of_birth(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_dateOfBirth = (
                TestEnrolmentInfo.TRAINEE_DATE_OF_BIRTH_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_dateOfBirth = (
                TestEnrolmentInfo.TRAINEE_DATE_OF_BIRTH_TWO)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_dateOfBirth = (
                TestEnrolmentInfo.TRAINEE_DATE_OF_BIRTH_ONE)

    def test_UpdateEnrolmentInfo_set_trainee_enrolment_date(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_TWO

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_enrolmentDate = TestEnrolmentInfo.ENROLMENT_DATE_ONE

    def test_UpdateEnrolmentInfo_set_trainee_sponsorship_type(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainee_sponsorshipType = (
                TestEnrolmentInfo.SPONSORSHIP_TYPE_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainee_sponsorshipType = (
                TestEnrolmentInfo.SPONSORSHIP_TYPE_TWO)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainee_sponsorshipType = (
                TestEnrolmentInfo.SPONSORSHIP_TYPE_ONE)

    def test_UpdateEnrolmentInfo_set_training_partner_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainingPartner_code = (
                TestEnrolmentInfo.TRAINING_PARTNER_CODE_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainingPartner_code = (
                TestEnrolmentInfo.TRAINING_PARTNER_CODE_TWO)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainingPartner_code = (
                TestEnrolmentInfo.TRAINING_PARTNER_CODE_ONE)

    def test_UpdateEnrolmentInfo_set_training_partner_uen(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_ONE.trainingPartner_uen = (
                TestEnrolmentInfo.TRAINING_PARTNER_UEN_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_TWO.trainingPartner_uen = (
                TestEnrolmentInfo.TRAINING_PARTNER_UEN_TWO)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_INFO_THREE.trainingPartner_uen = (
                TestEnrolmentInfo.TRAINING_PARTNER_UEN_ONE)

    def test_CancelEnrolmentInfo_validate(self):
        e, _ = TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.validate()

        self.assertTrue(len(e) == 0)

    def test_CancelEnrolmentInfo_payload(self):
        p = {
            "enrolment": {
                "action": "Cancel"
            }
        }

        self.assertEqual(TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.payload(), p)

    def test_CancelEnrolmentInfo_set_trainee_fees_discount_amount(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_fees_discountAmount = (
                TestEnrolmentInfo.DISCOUNT_AMOUNT_ONE)

    def test_CancelEnrolmentInfo_set_trainee_fees_collection_status(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_fees_collectionStatus = (
                TestEnrolmentInfo.FEE_COLLECTION_STATUS_ONE)

    def test_CancelEnrolmentInfo_set_course_run_id(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_ONE

    def test_CancelEnrolmentInfo_set_trainee_email_address(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_emailAddress = TestEnrolmentInfo.TRAINEE_EMAIL_ONE

    def test_CancelEnrolmentInfo_set_trainee_contact_number_area_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_contactNumber_areaCode = (
                TestEnrolmentInfo.TRAINEE_AREA_CODE_ONE)

    def test_CancelEnrolmentInfo_set_trainee_contact_number_country_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_contactNumber_countryCode = (
                TestEnrolmentInfo.TRAINEE_COUNTRY_CODE_ONE)

    def test_CancelEnrolmentInfo_set_trainee_contact_number_phone_number(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.trainee_contactNumber_phoneNumber = (
                TestEnrolmentInfo.TRAINEE_PHONE_NUMBER_ONE)

    def test_CancelEnrolmentInfo_set_trainee_employer_contact_email_address(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.employer_emailAddress = TestEnrolmentInfo.EMPLOYER_EMAIL_ONE

    def test_CancelEnrolmentInfo_set_trainee_employer_contact_full_name(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.employer_fullName = TestEnrolmentInfo.EMPLOYER_FULL_NAME_ONE

    def test_CancelEnrolmentInfo_set_trainee_employer_contact_number_area_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.employer_areaCode = TestEnrolmentInfo.EMPLOYER_AREA_CODE_ONE

    def test_CancelEnrolmentInfo_set_trainee_employer_contact_number_country_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.employer_countryCode = TestEnrolmentInfo.EMPLOYER_COUNTRY_CODE_ONE

    def test_CancelEnrolmentInfo_set_trainee_employer_contact_number_phone_number(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.CANCEL_ENROLMENT_INFO.employer_phoneNumber = TestEnrolmentInfo.EMPLOYER_PHONE_NUMBER_ONE

    def test_SearchEnrolmentInfo_validate(self):
        e1, _ = TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.validate()
        e2, _ = TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.validate()
        e3, _ = TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.validate()

        self.assertTrue(len(e1) == 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_SearchEnrolmentInfo_payload(self):
        p1 = {}
        p2 = {
            "meta": {
                "lastUpdateDateTo": "2023-12-02",
                "lastUpdateDateFrom": "2023-12-01"
            },
            "sortBy": {
                "field": "updatedOn",
                "order": "asc"
            },
            "enrolment": {
                "course": {
                    "run": {
                        "id": "10026"
                    },
                    "referenceNumber": "TGS-0026008-ES"
                },
                "status": "Confirmed",
                "trainee": {
                    "id": "S0118316H",
                    "fees": {
                        "feeCollectionStatus": "Cancelled"
                    },
                    "idType": {
                        "type": "NRIC"
                    },
                    "employer": {
                        "uen": "12345678X"
                    },
                    "enrolmentDate": "2023-12-02",
                    "sponsorshipType": "EMPLOYER"
                },
                "trainingPartner": {
                    "uen": "T16GB0003C",
                    "code": "T16GB0003C-01"
                }
            },
            "parameters": {
                "page": 1,
                "pageSize": 10
            }
        }

        p3 = {
            "meta": {
                "lastUpdateDateTo": "2024-12-02",
                "lastUpdateDateFrom": "2024-12-01"
            },
            "sortBy": {
                "field": "createdOn",
                "order": "desc"
            },
            "enrolment": {
                "course": {
                    "run": {
                        "id": "10027"
                    },
                    "referenceNumber": "TGS-0026008-ESS"
                },
                "status": "Cancelled",
                "trainee": {
                    "id": "S4524623Z",
                    "fees": {
                        "feeCollectionStatus": "Full Payment"
                    },
                    "idType": {
                        "type": "FIN"
                    },
                    "employer": {
                        "uen": "123456789X"
                    },
                    "enrolmentDate": "2024-12-02",
                    "sponsorshipType": "INDIVIDUAL"
                },
                "trainingPartner": {
                    "uen": "T16GB0003S",
                    "code": "T16GB0003S-01"
                }
            },
            "parameters": {
                "page": 2,
                "pageSize": 20
            }
        }

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.payload(), p1)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.payload(), p2)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.payload(), p3)

    def test_SearchEnrolmentInfo_has_overridden_uen(self):
        self.assertFalse(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.has_overridden_uen())
        self.assertTrue(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.has_overridden_uen())
        self.assertTrue(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.has_overridden_uen())

    def test_SearchEnrolmentInfo_set_last_update_date_to(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateTo = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateTo = "123"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateTo = [datetime.date.today()]

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateTo = datetime.date(2020, 1, 1)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateTo = datetime.date(2020, 1, 2)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateTo = datetime.date(2020, 1, 3)

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._lastUpdateDateTo, datetime.date(2020, 1, 1))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._lastUpdateDateTo,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateTo)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateTo, datetime.date(2020, 1, 2))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateTo,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateTo)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateTo, datetime.date(2020, 1, 3))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateTo,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateTo)

    def test_SearchEnrolmentInfo_set_last_update_date_from(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateFrom = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateFrom = "123"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateFrom = [datetime.date.today()]

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateFrom = datetime.date(2020, 1, 1)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateFrom = datetime.date(2020, 1, 2)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateFrom = datetime.date(2020, 1, 3)

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._lastUpdateDateFrom, datetime.date(2020, 1, 1))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._lastUpdateDateFrom,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.lastUpdateDateFrom)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateFrom, datetime.date(2020, 1, 2))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._lastUpdateDateFrom,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.lastUpdateDateFrom)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateFrom, datetime.date(2020, 1, 3))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._lastUpdateDateFrom,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.lastUpdateDateFrom)

    def test_SearchEnrolmentInfo_set_sort_by_field(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.sortBy_field = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.sortBy_field = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.sortBy_field = "asc"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.sortBy_field = EnrolmentSortField.CREATED_ON
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.sortBy_field = EnrolmentSortField.UPDATED_ON

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._sortBy_field, EnrolmentSortField.CREATED_ON)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._sortBy_field, EnrolmentSortField.UPDATED_ON)

    def test_SearchEnrolmentInfo_set_sort_by_order(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.sortBy_order = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.sortBy_order = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.sortBy_order = "asc"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.sortBy_order = SortOrder.ASCENDING
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.sortBy_order = SortOrder.DESCENDING

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._sortBy_order, SortOrder.ASCENDING)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._sortBy_order, SortOrder.DESCENDING)

    def test_SearchEnrolmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_run_id = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_run_id = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_run_id = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_run_id = "1234"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_run_id = "5678"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_run_id = "91011"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_run_id, "1234")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_run_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_run_id, "5678")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_run_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_run_id, "91011")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_run_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_run_id)

    def test_SearchEnrolmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_referenceNumber = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_referenceNumber = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_referenceNumber = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_referenceNumber = "1234"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_referenceNumber = "5678"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_referenceNumber = "91011"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_referenceNumber, "1234")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_referenceNumber)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_referenceNumber, "5678")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_referenceNumber)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_referenceNumber, "91011")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._course_referenceNumber,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_referenceNumber)

    def test_SearchEnrolmentInfo_set_course_status(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_status = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_status = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.course_status = "active"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_status = EnrolmentCourseStatus.CONFIRMED
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_status = EnrolmentCourseStatus.CANCELLED

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_status, EnrolmentCourseStatus.CONFIRMED)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._course_status,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.course_status)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_status, EnrolmentCourseStatus.CANCELLED)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._course_status,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.course_status)

    def test_SearchEnrolmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_id = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_id = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_id = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_id = "1234"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_id = "5678"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_id = "91011"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_id, "1234")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_id, "5678")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_id)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_id, "91011")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_id,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_id)

    def test_SearchEnrolmentInfo_set_trainee_fee_collection_status(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_fees_feeCollectionStatus = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_fees_feeCollectionStatus = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_fees_feeCollectionStatus = "active"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_fees_feeCollectionStatus = (
            CancellableCollectionStatus.PENDING_PAYMENT)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_fees_feeCollectionStatus = (
            CancellableCollectionStatus.PARTIAL_PAYMENT)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_fees_feeCollectionStatus = (
            CancellableCollectionStatus.FULL_PAYMENT)

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_fees_feeCollectionStatus,
                         CancellableCollectionStatus.PENDING_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_fees_feeCollectionStatus,
                         CancellableCollectionStatus.PARTIAL_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_fees_feeCollectionStatus,
                         CancellableCollectionStatus.FULL_PAYMENT)

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_fees_feeCollectionStatus = (
            CancellableCollectionStatus.CANCELLED)

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_fees_feeCollectionStatus,
                         CancellableCollectionStatus.CANCELLED)

    def test_SearchEnrolmentInfo_set_trainee_id_type(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_idType = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_idType = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_idType = "active"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_idType = IdTypeSummary.NRIC
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_idType = IdTypeSummary.FIN
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_idType = IdTypeSummary.OTHERS

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_idType_type, IdTypeSummary.NRIC)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_idType_type,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_idType)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_idType_type, IdTypeSummary.FIN)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_idType_type,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_idType)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_idType_type, IdTypeSummary.OTHERS)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_idType_type,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_idType)

    def test_SearchEnrolmentInfo_set_employer_uen(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.employer_uen = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.employer_uen = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.employer_uen = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.employer_uen = "G1234567X"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.employer_uen = "G1231231G"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.employer_uen = "A0987542X"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_employer_uen, "G1234567X")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_employer_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.employer_uen)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_employer_uen, "G1231231G")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_employer_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.employer_uen)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_employer_uen, "A0987542X")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_employer_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.employer_uen)

    def test_SearchEnrolmentInfo_set_trainee_enrolment_date(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_enrolmentDate = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_enrolmentDate = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_enrolmentDate = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_enrolmentDate = datetime.date(2020, 1, 1)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_enrolmentDate = datetime.date(2020, 1, 2)
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_enrolmentDate = datetime.date(2020, 1, 3)

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_enrolmentDate, datetime.date(2020, 1, 1))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_enrolmentDate,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_enrolmentDate)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_enrolmentDate, datetime.date(2020, 1, 2))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_enrolmentDate,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_enrolmentDate)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_enrolmentDate,
                         datetime.date(2020, 1, 3))
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainee_enrolmentDate,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_enrolmentDate)

    def test_SearchEnrolmentInfo_set_trainee_sponsorship_type(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_sponsorshipType = "random"

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_sponsorshipType = 123

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainee_sponsorshipType = "active"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_sponsorshipType = SponsorshipType.EMPLOYER
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_sponsorshipType = SponsorshipType.INDIVIDUAL

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_sponsorshipType,
                         SponsorshipType.EMPLOYER)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainee_sponsorshipType,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainee_sponsorshipType)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_sponsorshipType,
                         SponsorshipType.INDIVIDUAL)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainee_sponsorshipType,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainee_sponsorshipType)

    def test_SearchEnrolmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_uen = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainingPartner_uen = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainingPartner_uen = {"ABC123ABC"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_uen = "G1234567X"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainingPartner_uen = "G1231231G"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainingPartner_uen = "A0987542X"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainingPartner_uen, "G1234567X")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainingPartner_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_uen)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainingPartner_uen, "G1231231G")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainingPartner_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainingPartner_uen)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainingPartner_uen, "A0987542X")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainingPartner_uen,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainingPartner_uen)

    def test_SearchEnrolmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_code = 12345

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainingPartner_code = [123]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainingPartner_code = {"1234"}

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_code = "123"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.trainingPartner_code = "321"
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.trainingPartner_code = "111"

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainingPartner_code, "123")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._trainingPartner_code,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.trainingPartner_code)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._trainingPartner_code, "321")
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._trainingPartner_code, "111")

    def test_SearchEnrolmentInfo_set_page(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page = [1]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page = -1

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page = "1"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page = 1
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page = 2
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page = 3

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._parameters_page, 1)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._parameters_page,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page, 2)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page, 3)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page)

    def test_SearchEnrolmentInfo_set_page_size(self):
        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page_size = [1]

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page_size = -1

        with self.assertRaises(ValueError):
            TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page_size = "1"

        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page_size = 1
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page_size = 2
        TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page_size = 3

        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._parameters_page_size, 1)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE._parameters_page_size,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_ONE.page_size)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page_size, 2)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO._parameters_page_size,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_TWO.page_size)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page_size, 3)
        self.assertEqual(TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE._parameters_page_size,
                         TestEnrolmentInfo.SEARCH_ENROLMENT_INFO_THREE.page_size)

    def test_UpdateEnrolmentFeeCollectionInfo_validate(self):
        e1, _ = TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.validate()
        e2, _ = TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.validate()

        self.assertTrue(len(e1) == 0)
        self.assertTrue(len(e2) == 0)

    def test_UpdateEnrolmentFeeCollectionInfo_payload(self):
        p2 = {
            "enrolment": {
                "fees": {
                    "collectionStatus": "Pending Payment"
                }
            }
        }

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.payload(), {})
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.payload(), p2)

    def test_UpdateEnrolmentFeeCollectionInfo_set_last_update_date_to(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.lastUpdateDateTo = (
                TestEnrolmentInfo.LAST_UPDATE_DATE_TO_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.lastUpdateDateTo = (
                TestEnrolmentInfo.LAST_UPDATE_DATE_TO_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_last_update_date_from(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.lastUpdateDateFrom = (
                TestEnrolmentInfo.LAST_UPDATE_DATE_FROM_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.lastUpdateDateFrom = (
                TestEnrolmentInfo.LAST_UPDATE_DATE_FROM_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_sort_by_field(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.sortBy_field = TestEnrolmentInfo.SORT_BY_FIELD_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.sortBy_field = TestEnrolmentInfo.SORT_BY_FIELD_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_sort_by_order(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.sortBy_order = TestEnrolmentInfo.SORT_ORDER_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.sortBy_order = TestEnrolmentInfo.SORT_ORDER_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_course_run_id(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.course_run_id = TestEnrolmentInfo.COURSE_RUN_ID_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_course_reference_number(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.course_referenceNumber = (
                TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.course_referenceNumber = (
                TestEnrolmentInfo.COURSE_REFERENCE_NUMBER_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_course_status(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.course_status = TestEnrolmentInfo.COURSE_STATUS_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.course_status = TestEnrolmentInfo.COURSE_STATUS_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_trainee_id(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_id = TestEnrolmentInfo.TRAINEE_ID_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_id = TestEnrolmentInfo.TRAINEE_ID_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_trainee_fee_collection_status(self):
        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.CANCELLED)
        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.FULL_PAYMENT)

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.CANCELLED)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.FULL_PAYMENT)

        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.PARTIAL_PAYMENT)
        TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_fees_collectionStatus = (
            CancellableCollectionStatus.PENDING_PAYMENT)

        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.PARTIAL_PAYMENT)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO._trainee_fees_collectionStatus,
                         CancellableCollectionStatus.PENDING_PAYMENT)

        # one set of test cases to ensure that setters directly affect the attributes being set
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_fees_collectionStatus,
                         TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_fees_collectionStatus)
        self.assertEqual(TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_fees_collectionStatus,
                         TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_fees_collectionStatus)

    def test_UpdateEnrolmentFeeCollectionInfo_set_trainee_id_type(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_idType = TestEnrolmentInfo.ID_TYPE_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_idType = TestEnrolmentInfo.ID_TYPE_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_employer_uen(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.employer_uen = TestEnrolmentInfo.EMPLOYER_UEN_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_trainee_enrolment_date(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_enrolmentDate = (
                TestEnrolmentInfo.ENROLMENT_DATE_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_enrolmentDate = (
                TestEnrolmentInfo.ENROLMENT_DATE_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_trainee_sponsorship_type(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainee_sponsorshipType = (
                TestEnrolmentInfo.SPONSORSHIP_TYPE_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainee_sponsorshipType = (
                TestEnrolmentInfo.SPONSORSHIP_TYPE_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_training_partner_uen(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainingPartner_uen = (
                TestEnrolmentInfo.TRAINING_PARTNER_UEN_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainingPartner_uen = (
                TestEnrolmentInfo.TRAINING_PARTNER_UEN_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_training_partner_code(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.trainingPartner_code = (
                TestEnrolmentInfo.TRAINING_PARTNER_CODE_ONE)

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.trainingPartner_code = (
                TestEnrolmentInfo.TRAINING_PARTNER_CODE_TWO)

    def test_UpdateEnrolmentFeeCollectionInfo_set_page(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.page = TestEnrolmentInfo.PAGE_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.page = TestEnrolmentInfo.PAGE_TWO

    def test_UpdateEnrolmentFeeCollectionInfo_set_page_size(self):
        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_ONE.page_size = TestEnrolmentInfo.PAGE_SIZE_ONE

        with self.assertRaises(NotImplementedError):
            TestEnrolmentInfo.UPDATE_ENROLMENT_FEE_COLLECTION_TWO.page_size = TestEnrolmentInfo.PAGE_SIZE_TWO
