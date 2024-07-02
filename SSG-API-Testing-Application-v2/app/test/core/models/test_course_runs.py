"""
Tests for the Course Runs related model classes.

Code to use vars() inspired by
https://stackoverflow.com/questions/45984018/python-unit-test-to-check-if-objects-are-same-at-different-location
"""

import base64
import datetime
import os
import unittest

from streamlit.proto.Common_pb2 import FileURLs as FileURLsProto
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

from app.core.constants import (Vacancy, ModeOfTraining, IdType, Salutations,
                                Role, OptionalSelector)
from app.core.models.course_runs import (RunSessionEditInfo, RunSessionAddInfo,
                                         RunTrainerEditInfo, RunTrainerAddInfo, EditRunInfo,
                                         DeleteRunInfo, AddRunIndividualInfo, AddRunInfo,
                                         LinkedSSECEQA)
from app.test.resources.definitions import RESOURCES_PATH


class TestCourseRunsModels(unittest.TestCase):
    """Tests the different classes in Course Runs models module."""

    # constants to use for testing
    SESSION_ID_ONE = "XX-10000000K-01-TEST 166"
    SESSION_ID_TWO = "XX-10000000K-02-TEST 199"
    SEQUENCE_NUMBER_ONE = 1
    SEQUENCE_NUMBER_TWO = 2
    START_DATE_ONE = datetime.date(year=2024, month=1, day=1)
    START_DATE_TWO = datetime.date(year=2024, month=2, day=1)
    END_DATE_ONE = datetime.date(year=2024, month=2, day=29)
    END_DATE_TWO = datetime.date(year=2024, month=3, day=31)
    START_TIME_ONE = datetime.time(hour=8, minute=30)
    START_TIME_TWO = datetime.time(hour=9, minute=30)
    END_TIME_ONE = datetime.time(hour=18, minute=00)
    END_TIME_TWO = datetime.time(hour=20, minute=00)
    REGISTRATION_DATE_OPENING_ONE = datetime.date(year=2024, month=1, day=1)
    REGISTRATION_DATE_OPENING_TWO = datetime.date(year=2024, month=2, day=1)
    REGISTRATION_DATE_CLOSING_ONE = datetime.date(year=2024, month=1, day=2)
    REGISTRATION_DATE_CLOSING_TWO = datetime.date(year=2024, month=2, day=4)
    COURSE_DATE_START_ONE = datetime.date(year=2024, month=1, day=1)
    COURSE_DATE_START_TWO = datetime.date(year=2024, month=2, day=1)
    COURSE_DATE_END_ONE = datetime.date(year=2024, month=2, day=29)
    COURSE_DATE_END_TWO = datetime.date(year=2024, month=3, day=31)
    SCHEDULE_INFO_TYPE_CODE = "01"
    SCHEDULE_INFO_TYPE_DESCRIPTION = "Description"
    SCHEDULE_INFO = "Sat / 5 Sats / 9am - 6pm"
    MODE_OF_TRAINING_ONE = ModeOfTraining.ASYNCHRONOUS_ELEARNING
    MODE_OF_TRAINING_TWO = ModeOfTraining.ASSESSMENT
    VENUE_BLOCK_ONE = "112A"
    VENUE_BLOCK_TWO = "112B"
    VENUE_STREET_ONE = "Street ABC"
    VENUE_STREET_TWO = "Other Street ABC"
    VENUE_FLOOR_ONE = "15"
    VENUE_FLOOR_TWO = "51"
    VENUE_UNIT_ONE = "001"
    VENUE_UNIT_TWO = "100"
    VENUE_BUILDING_ONE = "Building ABC"
    VENUE_BUILDING_TWO = "Other Building ABC"
    VENUE_POSTAL_CODE_ONE = "123455"
    VENUE_POSTAL_CODE_TWO = "554321"
    VENUE_ROOM_ONE = "24"
    VENUE_ROOM_TWO = "84"
    VENUE_WHEELCHAIR_ACCESS_ONE = OptionalSelector.YES
    VENUE_WHEELCHAIR_ACCESS_TWO = OptionalSelector.NO
    VENUE_PRIMARY_VENUE_ACCESS_ONE = OptionalSelector.YES
    VENUE_PRIMARY_VENUE_ACCESS_TWO = OptionalSelector.NO
    INTAKE_SIZE_ONE = 20
    INTAKE_SIZE_TWO = 50
    THRESHOLD_ONE = 50
    THRESHOLD_TWO = 100
    REGISTERED_USER_COUNT_ONE = 10
    REGISTERED_USER_COUNT_TWO = 20
    COURSE_VACANCY_ONE = Vacancy.AVAILABLE
    COURSE_VACANCY_TWO = Vacancy.FULL
    TRAINER_TYPE_ONE = "1"
    TRAINER_TYPE_TWO = "2"
    TRAINER_TYPE_DESCRIPTION_ONE = "Existing"
    TRAINER_TYPE_DESCRIPTION_TWO = "New"
    INDEX_NUMBER_ONE = 1
    INDEX_NUMBER_TWO = 2
    ID_ONE = "TRAINER_ONE"
    ID_TWO = "TRAINER_TWO"
    NAME_ONE = "JOHN DOE"
    NAME_TWO = "JANE DOE"
    EMAIL_ONE = "john@email.com"
    EMAIL_TWO = "jane@email.com"
    ID_NUMBER_ONE = "S1234567X"
    ID_NUMBER_TWO = "T0123456X"
    ID_TYPE_CODE_ONE = IdType.SINGAPORE_BLUE
    ID_TYPE_CODE_TWO = IdType.FOREIGN_PASSPORT
    ID_TYPE_DESCRIPTION_ONE = "Singapore Blue Identification Card"
    ID_TYPE_DESCRIPTION_TWO = "Foreign Passport"
    ROLES_ONE_ENUM = [Role.TRAINER]
    ROLES_ONE = [
        {
            "id": 1,
            "description": "Trainer"
        }
    ]
    ROLES_TWO_ENUM = [Role.TRAINER, Role.ASSESSOR]
    ROLES_TWO = [
        {
            "id": 1,
            "description": "Trainer"
        },
        {
            "id": 2,
            "description": "Assessor"
        }
    ]
    IN_TRAINING_PROVIDER_PROFILE_ONE = OptionalSelector.YES
    IN_TRAINING_PROVIDER_PROFILE_TWO = OptionalSelector.NO
    DOMAIN_AREA_OF_PRACTICE_ONE = "Testing Management in Computer Application and Diploma in Computer Application"
    DOMAIN_AREA_OF_PRACTICE_TWO = "Change Management in Computer Application and Diploma in Computer Application"
    EXPERIENCE_ONE = "Testing ABC"
    EXPERIENCE_TWO = "Changing ABC"
    LINKEDIN_ONE = "https://sg.linkedin.com/company/linkedin/abc"
    LINKEDIN_TWO = "https://sg.linkedin.com/company/linkedin/def"
    SALUTATION_ID_ONE = Salutations.MR
    SALUTATION_ID_TWO = Salutations.MS
    FILE_NAME_ONE = "abc.jpg"
    FILE_NAME_TWO = "def.jpg"

    with (open(os.path.join(RESOURCES_PATH, "core", "models", FILE_NAME_ONE), "rb") as f1,
          open(os.path.join(RESOURCES_PATH, "core", "models", FILE_NAME_TWO), "rb") as f2):
        FILE_CONTENT_ONE = UploadedFile(
            UploadedFileRec(
                file_id="file_id_1",
                name=FILE_NAME_ONE,
                type="jpg",
                data=f1.read(),
            ),
            FileURLsProto()
        )

        FILE_CONTENT_TWO = UploadedFile(
            UploadedFileRec(
                file_id="file_id_2",
                name=FILE_NAME_TWO,
                type="jpg",
                data=f2.read(),
            ),
            FileURLsProto()
        )

    TEST_SSEC_ONE = LinkedSSECEQA()
    TEST_SSEC_ONE.ssecEQA = "12"
    TEST_SSEC_ONE.description = "EQA test 4"

    TEST_SSEC_TWO = LinkedSSECEQA()
    TEST_SSEC_TWO.ssecEQA = "22"
    TEST_SSEC_TWO.description = "EQA test 7"

    TEST_SSEC_THREE = LinkedSSECEQA()
    TEST_SSEC_THREE.ssecEQA = "65"
    TEST_SSEC_THREE.description = "EQA test 11"

    LINKED_SSEC_EQAS_ONE = [
        TEST_SSEC_ONE
    ]

    LINKED_SSEC_EQAS_TWO = [
        TEST_SSEC_TWO, TEST_SSEC_THREE
    ]

    # model instances
    RUN_SESSION_EDIT_INFO_ONE = RunSessionEditInfo()
    RUN_SESSION_EDIT_INFO_TWO = RunSessionEditInfo()
    RUN_SESSION_EDIT_INFO_THREE = RunSessionEditInfo()

    RUN_SESSION_ADD_INFO_ONE = RunSessionAddInfo()
    RUN_SESSION_ADD_INFO_TWO = RunSessionAddInfo()
    RUN_SESSION_ADD_INFO_THREE = RunSessionAddInfo()

    RUN_TRAINER_EDIT_INFO_ONE = RunTrainerEditInfo()
    RUN_TRAINER_EDIT_INFO_TWO = RunTrainerEditInfo()
    RUN_TRAINER_EDIT_INFO_THREE = RunTrainerAddInfo()

    RUN_TRAINER_ADD_INFO_ONE = RunTrainerAddInfo()
    RUN_TRAINER_ADD_INFO_TWO = RunTrainerAddInfo()
    RUN_TRAINER_ADD_INFO_THREE = RunTrainerAddInfo()

    EDIT_RUN_INFO_ONE = EditRunInfo()
    EDIT_RUN_INFO_TWO = EditRunInfo()
    EDIT_RUN_INFO_THREE = EditRunInfo()

    DELETE_RUN_INFO_ONE = DeleteRunInfo()
    DELETE_RUN_INFO_TWO = DeleteRunInfo()

    ADD_INDIVIDUAL_RUN_INFO_ONE = AddRunIndividualInfo()
    ADD_INDIVIDUAL_RUN_INFO_TWO = AddRunIndividualInfo()
    ADD_INDIVIDUAL_RUN_INFO_THREE = AddRunIndividualInfo()

    ADD_RUN_INFO_ONE = AddRunInfo()
    ADD_RUN_INFO_TWO = AddRunInfo()
    ADD_RUN_INFO_THREE = AddRunInfo()

    def __set_up_run_session_edit(self):
        # set up first instance
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE = RunSessionEditInfo()

        # set up second instance
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO = RunSessionEditInfo()
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.session_id = TestCourseRunsModels.SESSION_ID_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_date = TestCourseRunsModels.START_DATE_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_date = TestCourseRunsModels.END_DATE_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_time = TestCourseRunsModels.START_TIME_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_time = TestCourseRunsModels.END_TIME_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.block = TestCourseRunsModels.VENUE_BLOCK_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.street = TestCourseRunsModels.VENUE_STREET_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.floor = TestCourseRunsModels.VENUE_FLOOR_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.unit = TestCourseRunsModels.VENUE_UNIT_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.building = TestCourseRunsModels.VENUE_BUILDING_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.postal_code = TestCourseRunsModels.VENUE_POSTAL_CODE_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.room = TestCourseRunsModels.VENUE_ROOM_ONE
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.primary_venue = (
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_ONE)

        # set up third instance
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE = RunSessionEditInfo()
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.session_id = TestCourseRunsModels.SESSION_ID_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_date = TestCourseRunsModels.START_DATE_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_date = TestCourseRunsModels.END_DATE_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_time = TestCourseRunsModels.START_TIME_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_time = TestCourseRunsModels.END_TIME_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.block = TestCourseRunsModels.VENUE_BLOCK_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.street = TestCourseRunsModels.VENUE_STREET_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.floor = TestCourseRunsModels.VENUE_FLOOR_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.unit = TestCourseRunsModels.VENUE_UNIT_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.building = TestCourseRunsModels.VENUE_BUILDING_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.postal_code = (
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.room = TestCourseRunsModels.VENUE_ROOM_TWO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.primary_venue = (
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_TWO)

    def __set_up_run_session_add(self):
        # set up first instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE = RunSessionAddInfo()

        # set up second instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO = RunSessionAddInfo()
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.session_id = TestCourseRunsModels.SESSION_ID_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_date = TestCourseRunsModels.START_DATE_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_date = TestCourseRunsModels.END_DATE_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_time = TestCourseRunsModels.START_TIME_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_time = TestCourseRunsModels.END_TIME_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.block = TestCourseRunsModels.VENUE_BLOCK_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.street = TestCourseRunsModels.VENUE_STREET_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.floor = TestCourseRunsModels.VENUE_FLOOR_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.unit = TestCourseRunsModels.VENUE_UNIT_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.building = TestCourseRunsModels.VENUE_BUILDING_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.postal_code = TestCourseRunsModels.VENUE_POSTAL_CODE_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.room = TestCourseRunsModels.VENUE_ROOM_ONE
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.primary_venue = (
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_ONE)

        # set up third instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE = RunSessionAddInfo()
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.session_id = TestCourseRunsModels.SESSION_ID_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_date = TestCourseRunsModels.START_DATE_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_date = TestCourseRunsModels.END_DATE_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_time = TestCourseRunsModels.START_TIME_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_time = TestCourseRunsModels.END_TIME_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.block = TestCourseRunsModels.VENUE_BLOCK_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.street = TestCourseRunsModels.VENUE_STREET_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.floor = TestCourseRunsModels.VENUE_FLOOR_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.unit = TestCourseRunsModels.VENUE_UNIT_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.building = TestCourseRunsModels.VENUE_BUILDING_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.postal_code = (
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.room = TestCourseRunsModels.VENUE_ROOM_TWO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.primary_venue = (
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_TWO)

    def __set_up_run_trainer_edit(self):
        # set up first instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE = RunTrainerEditInfo()

        # set up second instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO = RunTrainerEditInfo()
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_code = TestCourseRunsModels.TRAINER_TYPE_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_description = (
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.index_number = TestCourseRunsModels.INDEX_NUMBER_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_id = TestCourseRunsModels.ID_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_name = TestCourseRunsModels.NAME_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_email = TestCourseRunsModels.EMAIL_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idNumber = TestCourseRunsModels.ID_NUMBER_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType = TestCourseRunsModels.ID_TYPE_CODE_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_roles = TestCourseRunsModels.ROLES_ONE_ENUM
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.inTrainingProviderProfile = (
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.domain_area_of_practice = (
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.experience = TestCourseRunsModels.EXPERIENCE_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.linkedInURL = TestCourseRunsModels.LINKEDIN_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.salutationId = TestCourseRunsModels.SALUTATION_ID_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_name = TestCourseRunsModels.FILE_NAME_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_content = TestCourseRunsModels.FILE_CONTENT_ONE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_ONE[0])

        # set up third instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE = RunTrainerEditInfo()
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_code = TestCourseRunsModels.TRAINER_TYPE_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_description = (
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.index_number = TestCourseRunsModels.INDEX_NUMBER_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_id = TestCourseRunsModels.ID_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_name = TestCourseRunsModels.NAME_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_email = TestCourseRunsModels.EMAIL_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idNumber = TestCourseRunsModels.ID_NUMBER_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idType = TestCourseRunsModels.ID_TYPE_CODE_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.inTrainingProviderProfile = (
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.domain_area_of_practice = (
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.experience = TestCourseRunsModels.EXPERIENCE_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.linkedInURL = TestCourseRunsModels.LINKEDIN_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.salutationId = TestCourseRunsModels.SALUTATION_ID_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_name = TestCourseRunsModels.FILE_NAME_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_content = TestCourseRunsModels.FILE_CONTENT_TWO
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[1])

    def __set_up_run_trainer_add(self):
        # set up first instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE = RunTrainerAddInfo()

        # set up second instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO = RunTrainerAddInfo()
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_code = TestCourseRunsModels.TRAINER_TYPE_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_description = (
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.index_number = TestCourseRunsModels.INDEX_NUMBER_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_id = TestCourseRunsModels.ID_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_name = TestCourseRunsModels.NAME_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_email = TestCourseRunsModels.EMAIL_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idNumber = TestCourseRunsModels.ID_NUMBER_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType = TestCourseRunsModels.ID_TYPE_CODE_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_roles = TestCourseRunsModels.ROLES_ONE_ENUM
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.inTrainingProviderProfile = (
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.domain_area_of_practice = (
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.experience = TestCourseRunsModels.EXPERIENCE_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.linkedInURL = TestCourseRunsModels.LINKEDIN_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.salutationId = TestCourseRunsModels.SALUTATION_ID_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_name = TestCourseRunsModels.FILE_NAME_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_content = TestCourseRunsModels.FILE_CONTENT_ONE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_ONE[0])

        # set up third instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE = RunTrainerAddInfo()
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_code = TestCourseRunsModels.TRAINER_TYPE_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_description = (
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.index_number = TestCourseRunsModels.INDEX_NUMBER_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_id = TestCourseRunsModels.ID_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_name = TestCourseRunsModels.NAME_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_email = TestCourseRunsModels.EMAIL_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idNumber = TestCourseRunsModels.ID_NUMBER_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idType = TestCourseRunsModels.ID_TYPE_CODE_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.inTrainingProviderProfile = (
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.domain_area_of_practice = (
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.experience = TestCourseRunsModels.EXPERIENCE_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.linkedInURL = TestCourseRunsModels.LINKEDIN_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.salutationId = TestCourseRunsModels.SALUTATION_ID_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_name = TestCourseRunsModels.FILE_NAME_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_content = TestCourseRunsModels.FILE_CONTENT_TWO
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[1])

    def __set_up_run_info_edit(self):
        # set up first instance
        TestCourseRunsModels.EDIT_RUN_INFO_ONE = EditRunInfo()

        # set up second instance
        TestCourseRunsModels.EDIT_RUN_INFO_TWO = EditRunInfo()
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.crid = TestCourseRunsModels.SESSION_ID_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.sequence_number = TestCourseRunsModels.SEQUENCE_NUMBER_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.opening_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.closing_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_start_date = TestCourseRunsModels.COURSE_DATE_START_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_end_date = TestCourseRunsModels.COURSE_DATE_END_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_code = TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_description = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info = TestCourseRunsModels.SCHEDULE_INFO
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.block = TestCourseRunsModels.VENUE_BLOCK_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.street = TestCourseRunsModels.VENUE_STREET_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.floor = TestCourseRunsModels.VENUE_FLOOR_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.unit = TestCourseRunsModels.VENUE_UNIT_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.building = TestCourseRunsModels.VENUE_BUILDING_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.postal_code = TestCourseRunsModels.VENUE_POSTAL_CODE_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.room = TestCourseRunsModels.VENUE_ROOM_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.intake_size = TestCourseRunsModels.INTAKE_SIZE_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.threshold = TestCourseRunsModels.THRESHOLD_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.registered_user_count = TestCourseRunsModels.REGISTERED_USER_COUNT_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_admin_email = TestCourseRunsModels.EMAIL_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_vacancy = TestCourseRunsModels.COURSE_VACANCY_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_name = TestCourseRunsModels.FILE_NAME_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_content = TestCourseRunsModels.FILE_CONTENT_ONE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.sessions = [
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ]
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.linked_course_run_trainers = [
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ]

        # set up third instance
        TestCourseRunsModels.EDIT_RUN_INFO_THREE = EditRunInfo()
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.crid = TestCourseRunsModels.SESSION_ID_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.sequence_number = TestCourseRunsModels.SEQUENCE_NUMBER_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.opening_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.closing_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_start_date = TestCourseRunsModels.COURSE_DATE_START_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_end_date = TestCourseRunsModels.COURSE_DATE_END_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_code = TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_description = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info = TestCourseRunsModels.SCHEDULE_INFO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.block = TestCourseRunsModels.VENUE_BLOCK_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.street = TestCourseRunsModels.VENUE_STREET_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.floor = TestCourseRunsModels.VENUE_FLOOR_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.unit = TestCourseRunsModels.VENUE_UNIT_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.building = TestCourseRunsModels.VENUE_BUILDING_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.postal_code = TestCourseRunsModels.VENUE_POSTAL_CODE_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.room = TestCourseRunsModels.VENUE_ROOM_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.intake_size = TestCourseRunsModels.INTAKE_SIZE_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.threshold = TestCourseRunsModels.THRESHOLD_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.registered_user_count = TestCourseRunsModels.REGISTERED_USER_COUNT_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_admin_email = TestCourseRunsModels.EMAIL_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_vacancy = TestCourseRunsModels.COURSE_VACANCY_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_name = TestCourseRunsModels.FILE_NAME_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_content = TestCourseRunsModels.FILE_CONTENT_TWO
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.sessions = [
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ]
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.linked_course_run_trainers = [
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ]

    def __set_up_run_info_delete(self):
        # set up first instance
        TestCourseRunsModels.DELETE_RUN_INFO_ONE = DeleteRunInfo()

        # set up second instance
        TestCourseRunsModels.DELETE_RUN_INFO_TWO = DeleteRunInfo()
        TestCourseRunsModels.DELETE_RUN_INFO_TWO.crid = TestCourseRunsModels.SESSION_ID_ONE

    def __set_up_individual_run_info_add(self):
        # set up first instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE = AddRunIndividualInfo()

        # set up second instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO = AddRunIndividualInfo()
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sequence_number = TestCourseRunsModels.SEQUENCE_NUMBER_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.opening_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.closing_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_start_date = (
            TestCourseRunsModels.COURSE_DATE_START_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_end_date = TestCourseRunsModels.COURSE_DATE_END_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_code = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_description = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info = TestCourseRunsModels.SCHEDULE_INFO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.block = TestCourseRunsModels.VENUE_BLOCK_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.street = TestCourseRunsModels.VENUE_STREET_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.floor = TestCourseRunsModels.VENUE_FLOOR_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.unit = TestCourseRunsModels.VENUE_UNIT_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.building = TestCourseRunsModels.VENUE_BUILDING_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.postal_code = (
            TestCourseRunsModels.VENUE_POSTAL_CODE_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.room = TestCourseRunsModels.VENUE_ROOM_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.intake_size = TestCourseRunsModels.INTAKE_SIZE_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.threshold = TestCourseRunsModels.THRESHOLD_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.registered_user_count = (
            TestCourseRunsModels.REGISTERED_USER_COUNT_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_admin_email = TestCourseRunsModels.EMAIL_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_vacancy = TestCourseRunsModels.COURSE_VACANCY_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_name = TestCourseRunsModels.FILE_NAME_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_content = TestCourseRunsModels.FILE_CONTENT_ONE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sessions = [
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ]
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.linked_course_run_trainers = [
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ]

        # set up third instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE = AddRunIndividualInfo()
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sequence_number = TestCourseRunsModels.SEQUENCE_NUMBER_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.opening_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.closing_registration_date = (
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_start_date = (
            TestCourseRunsModels.COURSE_DATE_START_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_end_date = TestCourseRunsModels.COURSE_DATE_END_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_code = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_description = (
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info = TestCourseRunsModels.SCHEDULE_INFO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.block = TestCourseRunsModels.VENUE_BLOCK_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.street = TestCourseRunsModels.VENUE_STREET_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.floor = TestCourseRunsModels.VENUE_FLOOR_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.unit = TestCourseRunsModels.VENUE_UNIT_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.building = TestCourseRunsModels.VENUE_BUILDING_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.postal_code = (
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.room = TestCourseRunsModels.VENUE_ROOM_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.wheel_chair_access = (
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.intake_size = TestCourseRunsModels.INTAKE_SIZE_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.threshold = TestCourseRunsModels.THRESHOLD_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.registered_user_count = (
            TestCourseRunsModels.REGISTERED_USER_COUNT_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.mode_of_training = TestCourseRunsModels.MODE_OF_TRAINING_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_admin_email = TestCourseRunsModels.EMAIL_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_vacancy = TestCourseRunsModels.COURSE_VACANCY_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_name = TestCourseRunsModels.FILE_NAME_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_content = TestCourseRunsModels.FILE_CONTENT_TWO
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sessions = [
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ]
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.linked_course_run_trainers = [
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ]

    def __set_up_run_info_add(self):
        # set up first instance
        TestCourseRunsModels.ADD_RUN_INFO_ONE = AddRunInfo()

        # set up second instance
        TestCourseRunsModels.ADD_RUN_INFO_TWO = AddRunInfo()
        TestCourseRunsModels.ADD_RUN_INFO_TWO.crid = TestCourseRunsModels.SESSION_ID_ONE
        TestCourseRunsModels.ADD_RUN_INFO_TWO.add_run(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)

        # set up third instance
        TestCourseRunsModels.ADD_RUN_INFO_THREE = AddRunInfo()
        TestCourseRunsModels.ADD_RUN_INFO_THREE.crid = TestCourseRunsModels.SESSION_ID_TWO
        TestCourseRunsModels.ADD_RUN_INFO_THREE.add_run(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
        TestCourseRunsModels.ADD_RUN_INFO_THREE.add_run(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)

    def setUp(self):
        """
        Creates the necessary objects to test before each test method is executed.
        """

        self.__set_up_run_session_edit()
        self.__set_up_run_session_add()
        self.__set_up_run_trainer_edit()
        self.__set_up_run_trainer_add()
        self.__set_up_run_info_edit()
        self.__set_up_run_info_delete()
        self.__set_up_individual_run_info_add()
        self.__set_up_run_info_add()

    # ===== Testing equality ===== #

    def test_RunSessionEditInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE),
                         vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE),
                         msg="RUN_SESSION_EDIT_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO),
                         vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO),
                         msg="RUN_SESSION_EDIT_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE),
                         vars(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE),
                         msg="RUN_SESSION_EDIT_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE == TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE,
            msg="Equality method for RunSessionEditInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO == TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
            msg="Equality method for RunSessionEditInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE == TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE,
            msg="Equality method for RunSessionEditInfo is faulty"
        )

    def test_RunSessionAddInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE),
                         vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE),
                         msg="RUN_SESSION_ADD_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO),
                         vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO),
                         msg="RUN_SESSION_ADD_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE),
                         vars(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE),
                         msg="RUN_SESSION_ADD_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE == TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE,
            msg="Equality method for RunSessionAddInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO == TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO,
            msg="Equality method for RunSessionAddInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE == TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE,
            msg="Equality method for RunSessionAddInfo is faulty"
        )

    def test_RunTrainerEditInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE),
                         vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE),
                         msg="RUN_TRAINER_EDIT_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO),
                         vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO),
                         msg="RUN_TRAINER_EDIT_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE),
                         vars(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE),
                         msg="RUN_TRAINER_EDIT_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE == TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE,
            msg="Equality method for RunTrainerEditInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO == TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
            msg="Equality method for RunTrainerEditInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE == TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE,
            msg="Equality method for RunTrainerEditInfo is faulty"
        )

    def test_RunTrainerAddInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE),
                         vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE),
                         msg="RUN_TRAINER_ADD_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO),
                         vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO),
                         msg="RUN_TRAINER_ADD_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE),
                         vars(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE),
                         msg="RUN_TRAINER_ADD_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE == TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE,
            msg="Equality method for RunTrainerAddInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO == TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO,
            msg="Equality method for RunTrainerAddInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE == TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE,
            msg="Equality method for RunTrainerAddInfo is faulty"
        )

    def test_EditRunInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.EDIT_RUN_INFO_ONE),
                         vars(TestCourseRunsModels.EDIT_RUN_INFO_ONE),
                         msg="EDIT_RUN_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.EDIT_RUN_INFO_TWO),
                         vars(TestCourseRunsModels.EDIT_RUN_INFO_TWO),
                         msg="EDIT_RUN_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.EDIT_RUN_INFO_THREE),
                         vars(TestCourseRunsModels.EDIT_RUN_INFO_THREE),
                         msg="EDIT_RUN_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.EDIT_RUN_INFO_ONE == TestCourseRunsModels.EDIT_RUN_INFO_ONE,
            msg="Equality method for EditRunInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.EDIT_RUN_INFO_TWO == TestCourseRunsModels.EDIT_RUN_INFO_TWO,
            msg="Equality method for EditRunInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.EDIT_RUN_INFO_THREE == TestCourseRunsModels.EDIT_RUN_INFO_THREE,
            msg="Equality method for EditRunInfo is faulty"
        )

    def test_DeleteRunInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.DELETE_RUN_INFO_ONE),
                         vars(TestCourseRunsModels.DELETE_RUN_INFO_ONE),
                         msg="DELETE_RUN_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.DELETE_RUN_INFO_TWO),
                         vars(TestCourseRunsModels.DELETE_RUN_INFO_TWO),
                         msg="DELETE_RUN_INFO_TWO is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.DELETE_RUN_INFO_ONE == TestCourseRunsModels.DELETE_RUN_INFO_ONE,
            msg="Equality method for DeleteRunInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.DELETE_RUN_INFO_ONE == TestCourseRunsModels.DELETE_RUN_INFO_ONE,
            msg="Equality method for DeleteRunInfo is faulty"
        )

    def test_AddRunIndividualInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE),
                         vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE),
                         msg="ADD_INDIVIDUAL_RUN_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO),
                         vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO),
                         msg="ADD_INDIVIDUAL_RUN_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE),
                         vars(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE),
                         msg="ADD_INDIVIDUAL_RUN_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE == TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE,
            msg="Equality method for AddRunIndividualInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO == TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO,
            msg="Equality method for AddRunIndividualInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE == TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE,
            msg="Equality method for AddRunIndividualInfo is faulty"
        )

    def test_AddRunInfo_equality(self):
        # test if the attributes are equal
        self.assertEqual(vars(TestCourseRunsModels.ADD_RUN_INFO_ONE),
                         vars(TestCourseRunsModels.ADD_RUN_INFO_ONE),
                         msg="ADD_RUN_INFO_ONE is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.ADD_RUN_INFO_TWO),
                         vars(TestCourseRunsModels.ADD_RUN_INFO_TWO),
                         msg="ADD_RUN_INFO_TWO is not equal to itself")
        self.assertEqual(vars(TestCourseRunsModels.ADD_RUN_INFO_THREE),
                         vars(TestCourseRunsModels.ADD_RUN_INFO_THREE),
                         msg="ADD_RUN_INFO_THREE is not equal to itself")

        # test if the overridden equality methods works
        self.assertTrue(
            TestCourseRunsModels.ADD_RUN_INFO_ONE == TestCourseRunsModels.ADD_RUN_INFO_ONE,
            msg="Equality method for AddRunInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.ADD_RUN_INFO_TWO == TestCourseRunsModels.ADD_RUN_INFO_TWO,
            msg="Equality method for AddRunInfo is faulty"
        )
        self.assertTrue(
            TestCourseRunsModels.ADD_RUN_INFO_THREE == TestCourseRunsModels.ADD_RUN_INFO_THREE,
            msg="Equality method for AddRunInfo is faulty"
        )

    def test_RunSessionEditInfo_inequality(self):
        for info in [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
                     TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_RunSessionAddInfo_inequality(self):
        for info in [TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO,
                     TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_RunTrainerEditInfo_inequality(self):
        for info in [TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
                     TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_RunTrainerAddInfo_inequality(self):
        for info in [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO,
                     TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_EditRunInfo_inequality(self):
        for info in [TestCourseRunsModels.EDIT_RUN_INFO_ONE, TestCourseRunsModels.EDIT_RUN_INFO_TWO,
                     TestCourseRunsModels.EDIT_RUN_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_DeleteRunInfo_inequality(self):
        for info in [TestCourseRunsModels.DELETE_RUN_INFO_ONE, TestCourseRunsModels.DELETE_RUN_INFO_TWO]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_AddRunIndividualInfo_inequality(self):
        for info in [TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO,
                     TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_RUN_INFO_THREE)

    def test_AddRunInfo_inequality(self):
        for info in [TestCourseRunsModels.ADD_RUN_INFO_ONE, TestCourseRunsModels.ADD_RUN_INFO_TWO,
                     TestCourseRunsModels.ADD_RUN_INFO_THREE]:
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.DELETE_RUN_INFO_TWO)

            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE)

            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_ONE)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_TWO)
            self.assertNotEqual(info, TestCourseRunsModels.EDIT_RUN_INFO_THREE)

    # RunSessionEditInfo tests
    def test_RunSessionEditInfo_validate(self):
        e1, _ = TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.validate()

        self.assertTrue(len(e1) == 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_RunSessionEditInfo_payload(self):
        p1 = {
            "action": "update"
        }

        p2 = {
            "action": "update",
            "sessionId": "XX-10000000K-01-TEST 166",
            "startDate": "20240101",
            "endDate": "20240229",
            "startTime": "08:30",
            "endTime": "18:00",
            "modeOfTraining": "2",
            "venue": {
                "block": "112A",
                "street": "Street ABC",
                "floor": "15",
                "unit": "001",
                "building": "Building ABC",
                "postalCode": "123455",
                "room": "24",
                "wheelChairAccess": True,
                "primaryVenue": True
            }
        }

        p3 = {
            "action": "update",
            "sessionId": "XX-10000000K-02-TEST 199",
            "startDate": "20240201",
            "endDate": "20240331",
            "startTime": "09:30",
            "endTime": "20:00",
            "modeOfTraining": "8",
            "venue": {
                "block": "112B",
                "street": "Other Street ABC",
                "floor": "51",
                "unit": "100",
                "building": "Other Building ABC",
                "postalCode": "554321",
                "room": "84",
                "wheelChairAccess": False,
                "primaryVenue": False
            }
        }

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.payload(), p1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.payload(), p2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.payload(), p3)

    def test_RunSessionEditInfo_get_start_date(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startDate)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate)

    def test_RunSessionEditInfo_get_start_date_year(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_start_date_year(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_start_date_year(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate.year)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_start_date_year(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate.year)

    def test_RunSessionEditInfo_get_end_date_year(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_end_date_year(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_end_date_year(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate.year)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_end_date_year(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate.year)

    def test_RunSessionEditInfo_get_start_date_month(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_start_date_month(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_start_date_month(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate.month)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_start_date_month(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate.month)

    def test_RunSessionEditInfo_get_end_date_month(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_end_date_month(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_end_date_month(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate.month)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_end_date_month(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate.month)

    def test_RunSessionEditInfo_get_start_date_day(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_start_date_day(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_start_date_day(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate.day)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_start_date_day(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate.day)

    def test_RunSessionEditInfo_get_end_date_day(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.get_end_date_day(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.get_end_date_day(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate.day)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.get_end_date_day(),
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate.day)

    def test_RunSessionEditInfo_is_asynchronous_or_on_the_job(self):
        self.assertFalse(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.is_asynchronous_or_on_the_job())
        self.assertTrue(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.is_asynchronous_or_on_the_job())
        self.assertFalse(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.is_asynchronous_or_on_the_job())

    def test_RunSessionEditInfo_set_session_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.session_id = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.session_id = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.session_id = 123.22

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.session_id = "Session 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.session_id = "Session 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.session_id = "Session 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._sessionId, "Session 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._sessionId,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.session_id)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._sessionId, "Session 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._sessionId,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.session_id)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._sessionId, "Session 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._sessionId,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.session_id)

    def test_RunSessionEditInfo_set_start_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_date = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_date = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_date = [datetime.datetime.now()]

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_date = dt1
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_date = dt2
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_date = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_date)

    def test_RunSessionEditInfo_set_end_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_date = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_date = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_date = [datetime.datetime.now()]

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_date = dt1
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_date = dt2
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_date = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_date)

    def test_RunSessionEditInfo_set_start_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_time = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_time = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_time = [datetime.datetime.now()]

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_time = dt1
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_time = dt2
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_time = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.start_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.start_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startTime, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.start_time)

    def test_RunSessionEditInfo_set_end_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_time = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_time = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_time = [datetime.datetime.now()]

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_time = dt1
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_time = dt2
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_time = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.end_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.end_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endTime, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endTime,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.end_time)

    def test_RunSessionEditInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.mode_of_training = "10"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.mode_of_training = 2

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.mode_of_training = [8]

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.mode_of_training = ModeOfTraining.SYNCHRONOUS_LEARNING
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.mode_of_training = ModeOfTraining.PRACTICAL_PRACTICUM
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.mode_of_training = ModeOfTraining.TRAINEESHIP

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._modeOfTraining,
                         ModeOfTraining.SYNCHRONOUS_LEARNING)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.mode_of_training)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._modeOfTraining,
                         ModeOfTraining.PRACTICAL_PRACTICUM)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.mode_of_training)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._modeOfTraining,
                         ModeOfTraining.TRAINEESHIP)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.mode_of_training)

    def test_RunSessionEditInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.block = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.block = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.block = 123.22

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.block = "Block 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.block = "Block 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.block = "Block 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_block,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.block)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_block,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.block)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_block, "Block 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_block,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.block)

    def test_RunSessionEditInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.street = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.street = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.street = {
                "location": {
                    "street": "street"
                }
            }

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.street = "Street 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.street = "Street 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.street = "Street 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_street,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.street)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_street,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.street)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_street, "Street 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_street,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.street)

    def test_RunSessionEditInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.floor = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.floor = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.floor = {"floor"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.floor = "Floor 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.floor = "Floor 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.floor = "Floor 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.floor)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.floor)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_floor, "Floor 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.floor)

    def test_RunSessionEditInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.unit = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.unit = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.unit = {"unit"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.unit = "Unit 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.unit = "Unit 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.unit = "Unit 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.unit)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.unit)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_unit, "Unit 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.unit)

    def test_RunSessionEditInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.building = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.building = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.building = {"building"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.building = "Building 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.building = "Building 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.building = "Building 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_building,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.building)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_building,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.building)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_building, "Building 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_building,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.building)

    def test_RunSessionEditInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.postal_code = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.postal_code = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.postal_code = {"postal_code"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.postal_code = "949494"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.postal_code = "959595"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.postal_code = "969696"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_postalCode, "949494")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.postal_code)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_postalCode, "959595")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.postal_code)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_postalCode, "969696")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.postal_code)

    def test_RunSessionEditInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.room = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.room = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.room = {"room"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.room = "Room 1"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.room = "Room 2"
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.room = "Room 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_room,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.room)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_room,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.room)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_room, "Room 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_room,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.room)

    def test_RunSessionEditInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.wheel_chair_access = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.wheel_chair_access = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.wheel_chair_access = {"wheel_chair_access"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.wheel_chair_access = OptionalSelector.YES
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.wheel_chair_access = OptionalSelector.NO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.wheel_chair_access = OptionalSelector.NIL

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_wheelChairAccess, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_wheelChairAccess, OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_wheelChairAccess, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.wheel_chair_access)

    def test_RunSessionEditInfo_set_venue_primary_venue(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.primary_venue = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.primary_venue = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.primary_venue = {"primary_venue"}

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.primary_venue = OptionalSelector.YES
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.primary_venue = OptionalSelector.NO
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.primary_venue = OptionalSelector.NIL

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_primaryVenue, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_primaryVenue,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.primary_venue)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_primaryVenue, OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_primaryVenue,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.primary_venue)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_primaryVenue, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_primaryVenue,
                         TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.primary_venue)

    # RunSessionAddInfo tests
    def test_RunSessionAddInfo_validate(self):
        e1, _ = TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_RunSessionAddInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.payload()

        p2 = {
            "startDate": "20240101",
            "endDate": "20240229",
            "startTime": "08:30",
            "endTime": "18:00",
            "modeOfTraining": "2",
            "venue": {
                "block": "112A",
                "street": "Street ABC",
                "floor": "15",
                "unit": "001",
                "building": "Building ABC",
                "postalCode": "123455",
                "room": "24",
                "wheelChairAccess": True,
                "primaryVenue": True
            }
        }

        p3 = {
            "startDate": "20240201",
            "endDate": "20240331",
            "startTime": "09:30",
            "endTime": "20:00",
            "modeOfTraining": "8",
            "venue": {
                "block": "112B",
                "street": "Other Street ABC",
                "floor": "51",
                "unit": "100",
                "building": "Other Building ABC",
                "postalCode": "554321",
                "room": "84",
                "wheelChairAccess": False,
                "primaryVenue": False
            }
        }

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.payload(), p2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.payload(), p3)

    def test_RunSessionAddInfo_get_start_date(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startDate)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_start_date(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate)

    def test_RunSessionAddInfo_get_start_date_year(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_start_date_year(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_start_date_year(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate.year)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_start_date_year(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate.year)

    def test_RunSessionAddInfo_get_end_date_year(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_end_date_year(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_end_date_year(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate.year)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_end_date_year(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate.year)

    def test_RunSessionAddInfo_get_start_date_month(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_start_date_month(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_start_date_month(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate.month)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_start_date_month(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate.month)

    def test_RunSessionAddInfo_get_end_date_month(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_end_date_month(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_end_date_month(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate.month)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_end_date_month(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate.month)

    def test_RunSessionAddInfo_get_start_date_day(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_start_date_day(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_start_date_day(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate.day)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_start_date_day(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate.day)

    def test_RunSessionAddInfo_get_end_date_day(self):
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.get_end_date_day(),
                         None)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.get_end_date_day(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate.day)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.get_end_date_day(),
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate.day)

    def test_RunSessionAddInfo_is_asynchronous_or_on_the_job(self):
        self.assertFalse(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.is_asynchronous_or_on_the_job())
        self.assertTrue(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.is_asynchronous_or_on_the_job())
        self.assertFalse(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.is_asynchronous_or_on_the_job())

    def test_RunSessionAddInfo_set_session_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.session_id = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.session_id = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.session_id = 123.22

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.session_id = "Session 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.session_id = "Session 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.session_id = "Session 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._sessionId, "Session 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._sessionId,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.session_id)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._sessionId, "Session 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._sessionId, "Session 3")

    def test_RunSessionAddInfo_set_start_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_date = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_date = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_date = [datetime.datetime.now()]

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_date = dt1
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_date = dt2
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_date = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_date)

    def test_RunSessionAddInfo_set_end_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_date = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_date = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_date = [datetime.datetime.now()]

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_date = dt1
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_date = dt2
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_date = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_date)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_date)

    def test_RunSessionAddInfo_set_start_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_time = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_time = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_time = [datetime.datetime.now()]

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_time = dt1
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_time = dt2
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_time = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.start_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.start_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startTime, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.start_time)

    def test_RunSessionAddInfo_set_end_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_time = 31122024

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_time = 112.2023

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_time = [datetime.datetime.now()]

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_time = dt1
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_time = dt2
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_time = dt3

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.end_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.end_time)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endTime, dt3)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endTime,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.end_time)

    def test_RunSessionAddInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.mode_of_training = "10"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.mode_of_training = 2

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.mode_of_training = [8]

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.mode_of_training = ModeOfTraining.SYNCHRONOUS_LEARNING
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.mode_of_training = ModeOfTraining.PRACTICAL_PRACTICUM
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.mode_of_training = ModeOfTraining.TRAINEESHIP

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._modeOfTraining,
                         ModeOfTraining.SYNCHRONOUS_LEARNING)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.mode_of_training)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._modeOfTraining,
                         ModeOfTraining.PRACTICAL_PRACTICUM)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.mode_of_training)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._modeOfTraining,
                         ModeOfTraining.TRAINEESHIP)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._modeOfTraining,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.mode_of_training)

    def test_RunSessionAddInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.block = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.block = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.block = 123.22

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.block = "Block 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.block = "Block 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.block = "Block 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_block,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.block)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_block,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.block)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_block, "Block 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_block,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.block)

    def test_RunSessionAddInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.street = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.street = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.street = {
                "location": {
                    "street": "street"
                }
            }

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.street = "Street 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.street = "Street 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.street = "Street 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_street,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.street)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_street,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.street)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_street, "Street 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_street,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.street)

    def test_RunSessionAddInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.floor = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.floor = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.floor = {"floor"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.floor = "Floor 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.floor = "Floor 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.floor = "Floor 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.floor)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.floor)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_floor, "Floor 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_floor,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.floor)

    def test_RunSessionAddInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.unit = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.unit = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.unit = {"unit"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.unit = "Unit 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.unit = "Unit 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.unit = "Unit 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.unit)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.unit)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_unit, "Unit 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_unit,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.unit)

    def test_RunSessionAddInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.building = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.building = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.building = {"building"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.building = "Building 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.building = "Building 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.building = "Building 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_building,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.building)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_building,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.building)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_building, "Building 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_building,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.building)

    def test_RunSessionAddInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.postal_code = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.postal_code = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.postal_code = {"postal_code"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.postal_code = "949494"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.postal_code = "959595"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.postal_code = "969696"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_postalCode, "949494")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.postal_code)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_postalCode, "959595")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.postal_code)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_postalCode, "969696")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_postalCode,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.postal_code)

    def test_RunSessionAddInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.room = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.room = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.room = {"room"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.room = "Room 1"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.room = "Room 2"
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.room = "Room 3"

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_room,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.room)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_room,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.room)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_room, "Room 3")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_room,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.room)

    def test_RunSessionAddInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.wheel_chair_access = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.wheel_chair_access = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.wheel_chair_access = {"wheel_chair_access"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.wheel_chair_access = OptionalSelector.YES
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.wheel_chair_access = OptionalSelector.NO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.wheel_chair_access = OptionalSelector.NIL

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_wheelChairAccess, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_wheelChairAccess, OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_wheelChairAccess, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_wheelChairAccess,
                         TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.wheel_chair_access)

    def test_RunSessionAddInfo_set_venue_primary_venue(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.primary_venue = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.primary_venue = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.primary_venue = {"primary_venue"}

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.primary_venue = OptionalSelector.YES
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.primary_venue = OptionalSelector.NO
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.primary_venue = OptionalSelector.NIL

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_primaryVenue, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_primaryVenue, OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_primaryVenue, OptionalSelector.NIL)

    # RunTrainerEditInfo tests
    def test_RunTrainerEditInfo_validate(self):
        e1, _ = TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_RunTrainerEditInfo_payload(self):
        try:
            with (open(os.path.join(RESOURCES_PATH, "core", "models", "abc.jpg"), "rb") as f1,
                  open(os.path.join(RESOURCES_PATH, "core", "models", "def.jpg"), "rb") as f2):
                img1 = base64.b64encode(f1.read()).decode("utf-8")
                img2 = base64.b64encode(f2.read()).decode("utf-8")
        except Exception as ex:
            self.fail(f"Unable to load resources: {ex}")

        # since the photo is large, we need to up the size of the diff to view the differences if any
        self.maxDiff = None

        p2 = {
            "trainer": {
                "trainerType": {
                    "code": "1",
                    "description": "Existing"
                },
                "indexNumber": 1,
                "id": "TRAINER_ONE",
                "name": "JOHN DOE",
                "email": "john@email.com",
                "idNumber": "S1234567X",
                "idType": {
                    "code": "SB",
                    "description": "Singapore Blue Identification Card"
                },
                "roles": [
                    {
                        "role": {
                            "id": 1,
                            "description": "Trainer"
                        }
                    }
                ],
                "inTrainingProviderProfile": True,
                "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in Computer "
                                        "Application",
                "experience": "Testing ABC",
                "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                "salutationId": 1,
                "photo": {
                    "name": "abc.jpg",
                    "content": img1
                },
                "linkedSsecEQAs": [
                    {
                        "description": "EQA test 4",
                        "ssecEQA": {
                            "code": "12"
                        }
                    }
                ]
            }
        }

        p3 = {
            "trainer": {
                "trainerType": {
                    "code": "2",
                    "description": "New"
                },
                "indexNumber": 2,
                "id": "TRAINER_TWO",
                "name": "JANE DOE",
                "email": "jane@email.com",
                "idNumber": "T0123456X",
                "idType": {
                    "code": "FP",
                    "description": "Foreign Passport"
                },
                "roles": [
                    {
                        "role": {
                            "id": 1,
                            "description": "Trainer"
                        }
                    },
                    {
                        "role": {
                            "id": 2,
                            "description": "Assessor"
                        }
                    }
                ],
                "inTrainingProviderProfile": False,
                "domainAreaOfPractice": "Change Management in Computer Application and Diploma in Computer Application",
                "experience": "Changing ABC",
                "linkedInURL": "https://sg.linkedin.com/company/linkedin/def",
                "salutationId": 2,
                "photo": {
                    "name": "def.jpg",
                    "content": img2
                },
                "linkedSsecEQAs": [
                    {
                        "description": "EQA test 7",
                        "ssecEQA": {
                            "code": "22"
                        }
                    },
                    {
                        "description": "EQA test 11",
                        "ssecEQA": {
                            "code": "65"
                        }
                    }
                ]
            }
        }

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.payload()

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.payload(), p2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.payload(), p3)

    def test_RunTrainerEditInfo_is_existing_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.is_existing_trainer()

        self.assertTrue(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.is_existing_trainer())
        self.assertFalse(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.is_existing_trainer())

    def test_RunTrainerEditInfo_is_new_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.is_existing_trainer()

        self.assertFalse(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.is_new_trainer())
        self.assertTrue(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.is_new_trainer())

    def test_RunTrainerEditInfo_set_trainer_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_code = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_code = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_code = 123.22

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_code = "1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_code = "2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_code = "3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_code, "1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_code)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_code, "2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_code)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_code, "3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_code)

    def test_RunTrainerEditInfo_set_trainer_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_description = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_description = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_description = 123.22

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_description = "Trainer Code 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_description = "Trainer Code 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_description = "Trainer Code 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_description, "Trainer Code 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_type_description)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_description, "Trainer Code 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_type_description)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_description, "Trainer Code 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_type_description)

    def test_RunTrainerEditInfo_set_index_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.index_number = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.index_number = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.index_number = {"one"}

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.index_number = 1
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.index_number = 2
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.index_number = 3

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._indexNumber, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.index_number)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._indexNumber, 2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.index_number)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._indexNumber, 3)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.index_number)

    def test_RunTrainerEditInfo_set_trainer_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_id = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_id = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_id = ["three"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_id = "Trainer ID 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_id = "Trainer ID 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_id = "Trainer ID 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._id, "Trainer ID 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._id,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_id)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._id, "Trainer ID 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._id,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_id)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._id, "Trainer ID 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._id,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_id)

    def test_RunTrainerEditInfo_set_trainer_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_name = ["three"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_name = "Trainer Name 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_name = "Trainer Name 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_name = "Trainer Name 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._name, "Trainer Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._name, "Trainer Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._name, "Trainer Name 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_name)

    def test_RunTrainerEditInfo_set_trainer_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_email = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_email = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_email = ["three"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_email = "Trainer Email 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_email = "Trainer Email 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_email = "Trainer Email 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._email, "Trainer Email 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._email,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_email)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._email, "Trainer Email 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._email,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_email)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._email, "Trainer Email 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._email,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_email)

    def test_RunTrainerEditInfo_set_trainer_id_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idNumber = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idNumber = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idNumber = ["three"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idNumber = "Trainer ID Number 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idNumber = "Trainer ID Number 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idNumber = "Trainer ID Number 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idNumber, "Trainer ID Number 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idNumber)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idNumber, "Trainer ID Number 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idNumber)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idNumber, "Trainer ID Number 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idNumber)

    def test_RunTrainerEditInfo_set_trainer_id_type(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idType = "SBBBBBBB"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType = {"OT"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idType = ["FP"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idType = IdType.OTHERS
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType = IdType.SINGAPORE_PINK
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idType = IdType.SINGAPORE_BLUE

        # assert both the code and the description
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_code, "OT")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_code, "SP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idType_code, "SB")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_description, "Others")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_description,
                         "Singapore Pink Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idType_description,
                         "Singapore Blue Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idType,
                         IdType.OTHERS)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType,
                         IdType.SINGAPORE_PINK)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_idType,
                         IdType.SINGAPORE_BLUE)

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idType = IdType.FIN_WORK_PERMIT
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType = IdType.FOREIGN_PASSPORT

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_code, "SO")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_code, "FP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_description, "Fin/Work Permit")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_description, "Foreign Passport")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_idType,
                         IdType.FIN_WORK_PERMIT)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_idType,
                         IdType.FOREIGN_PASSPORT)

    def test_RunTrainerEditInfo_set_trainer_roles(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_roles = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_roles = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_roles = "three"

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_roles = TestCourseRunsModels.ROLES_ONE_ENUM

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._roles,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.trainer_roles)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.trainer_roles)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.trainer_roles)

    def test_RunTrainerEditInfo_set_in_training_provider_profile(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.inTrainingProviderProfile = "Yess"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.inTrainingProviderProfile = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.inTrainingProviderProfile = "n0"

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.inTrainingProviderProfile = OptionalSelector.YES
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.inTrainingProviderProfile = OptionalSelector.NIL
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.inTrainingProviderProfile = OptionalSelector.NO

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._inTrainingProviderProfile,
                         OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.inTrainingProviderProfile)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._inTrainingProviderProfile,
                         OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.inTrainingProviderProfile)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._inTrainingProviderProfile,
                         OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.inTrainingProviderProfile)

    def test_RunTrainerEditInfo_set_domain_area_of_practice(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.domain_area_of_practice = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.domain_area_of_practice = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.domain_area_of_practice = ["domain area 123"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.domain_area_of_practice = "Domain 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.domain_area_of_practice = "Domain 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.domain_area_of_practice = "Domain 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._domainAreaOfPractice,
                         "Domain 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.domain_area_of_practice)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._domainAreaOfPractice,
                         "Domain 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.domain_area_of_practice)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._domainAreaOfPractice,
                         "Domain 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.domain_area_of_practice)

    def test_RunTrainerEditInfo_set_experience(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.experience = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.experience = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.experience = ["experience 123"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.experience = "Experience 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.experience = "Experience 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.experience = "Experience 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._experience, "Experience 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._experience,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.experience)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._experience, "Experience 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._experience,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.experience)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._experience, "Experience 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._experience,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.experience)

    def test_RunTrainerEditInfo_set_linked_in_url(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.linkedInURL = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.linkedInURL = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.linkedInURL = ["linkedin url 123"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.linkedInURL = "LinkedIn URL 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.linkedInURL = "LinkedIn URL 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.linkedInURL = "LinkedIn URL 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._linkedInURL, "LinkedIn URL 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.linkedInURL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedInURL, "LinkedIn URL 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.linkedInURL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedInURL, "LinkedIn URL 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.linkedInURL)

    def test_RunTrainerEditInfo_set_salutation_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.salutationId = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.salutationId = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.salutationId = 3.3333333

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.salutationId = Salutations.MR
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.salutationId = Salutations.MDM
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.salutationId = Salutations.DR

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._salutationId, Salutations.MR)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.salutationId)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._salutationId, Salutations.MDM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.salutationId)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._salutationId, Salutations.DR)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.salutationId)

    def test_RunTrainerEditInfo_set_photo_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_name = ["photo name.jpg"]

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_name = "Photo Name 1"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_name = "Photo Name 2"
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_name = "Photo Name 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_name, "Photo Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_name, "Photo Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_name, "Photo Name 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_name)

    def test_RunTrainerEditInfo_set_photo_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_content = b"image"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_content = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_content = ["photo"]

        with (open(os.path.join(RESOURCES_PATH, "core", "models", "test1.jpg"), "rb") as test1,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test2.jpg"), "rb") as test2,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test3.jpg"), "rb") as test3):
            T1 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_3",
                    name=test1.name,
                    type="jpg",
                    data=test1.read()
                ),
                FileURLsProto()
            )
            T2 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_4",
                    name=test2.name,
                    type="jpg",
                    data=test2.read()
                ),
                FileURLsProto()
            )
            T3 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_5",
                    name=test3.name,
                    type="jpg",
                    data=test3.read()
                ),
                FileURLsProto()
            )

            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_content = T1
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_content = T2
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_content = T3

            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_content, T1)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.photo_content)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_content, T2)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.photo_content)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_content, T3)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.photo_content)

    def test_RunTrainerEditInfo_add_linked_ssec_eqa(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA("three")

        EQA1 = LinkedSSECEQA()
        EQA1.ssecEQA = "1"
        EQA1.description = "EQA 1"

        EQA2 = LinkedSSECEQA()
        EQA2.ssecEQA = "22"
        EQA2.description = "EQA test 21"

        EQA3 = LinkedSSECEQA()
        EQA3.ssecEQA = "23"
        EQA3.description = "EQA test 12"

        # reset the linked SSEC EQAs in RUN_TRAINER_EDIT_INFO_TWO and RUN_TRAINER_EDIT_INFO_THREE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedSsecEQAs = []
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedSsecEQAs = []

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA(EQA1)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_linkedSsecEQA(EQA2)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(EQA3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._linkedSsecEQAs, [EQA1.payload()])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedSsecEQAs, [EQA2.payload()])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedSsecEQAs, [EQA3.payload()])

    # RunTrainerAddInfo tests
    def test_RunTrainerAddInfo_validate(self):
        e1, _ = TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_RunTrainerAddInfo_payload(self):
        try:
            with (open(os.path.join(RESOURCES_PATH, "core", "models", "abc.jpg"), "rb") as f1,
                  open(os.path.join(RESOURCES_PATH, "core", "models", "def.jpg"), "rb") as f2):
                img1 = base64.b64encode(f1.read()).decode("utf-8")
                img2 = base64.b64encode(f2.read()).decode("utf-8")
        except Exception as ex:
            self.fail(f"Unable to load resources: {ex}")

        # since the photo is large, we need to up the size of the diff to view the differences if any
        self.maxDiff = None

        p2 = {
            "trainer": {
                "trainerType": {
                    "code": "1",
                    "description": "Existing"
                },
                "indexNumber": 1,
                "id": "TRAINER_ONE",
                "name": "JOHN DOE",
                "email": "john@email.com",
                "idNumber": "S1234567X",
                "idType": {
                    "code": "SB",
                    "description": "Singapore Blue Identification Card"
                },
                "roles": [
                    {
                        "role": {
                            "id": 1,
                            "description": "Trainer"
                        }
                    }
                ],
                "inTrainingProviderProfile": True,
                "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in Computer "
                                        "Application",
                "experience": "Testing ABC",
                "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                "salutationId": 1,
                "photo": {
                    "name": "abc.jpg",
                    "content": img1
                },
                "linkedSsecEQAs": [
                    {
                        "description": "EQA test 4",
                        "ssecEQA": {
                            "code": "12"
                        }
                    }
                ]
            }
        }

        p3 = {
            "trainer": {
                "trainerType": {
                    "code": "2",
                    "description": "New"
                },
                "indexNumber": 2,
                "id": "TRAINER_TWO",
                "name": "JANE DOE",
                "email": "jane@email.com",
                "idNumber": "T0123456X",
                "idType": {
                    "code": "FP",
                    "description": "Foreign Passport"
                },
                "roles": [
                    {
                        "role": {
                            "id": 1,
                            "description": "Trainer"
                        }
                    },
                    {
                        "role": {
                            "id": 2,
                            "description": "Assessor"
                        }
                    }
                ],
                "inTrainingProviderProfile": False,
                "domainAreaOfPractice": "Change Management in Computer Application and Diploma in Computer Application",
                "experience": "Changing ABC",
                "linkedInURL": "https://sg.linkedin.com/company/linkedin/def",
                "salutationId": 2,
                "photo": {
                    "name": "def.jpg",
                    "content": img2
                },
                "linkedSsecEQAs": [
                    {
                        "description": "EQA test 7",
                        "ssecEQA": {
                            "code": "22"
                        }
                    },
                    {
                        "description": "EQA test 11",
                        "ssecEQA": {
                            "code": "65"
                        }
                    }
                ]
            }
        }

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.payload()

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.payload(), p2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.payload(), p3)

    def test_RunTrainerAddInfo_is_existing_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.is_existing_trainer()

        self.assertTrue(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.is_existing_trainer())
        self.assertFalse(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.is_existing_trainer())

    def test_RunTrainerAddInfo_is_new_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.is_existing_trainer()

        self.assertFalse(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.is_new_trainer())
        self.assertTrue(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.is_new_trainer())

    def test_RunTrainerAddInfo_set_trainer_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_code = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_code = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_code = 123.22

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_code = "1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_code = "2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_code = "3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_code, "1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_code)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_code, "2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_code)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_code, "3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_code,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_code)

    def test_RunTrainerAddInfo_set_trainer_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_description = 123

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_description = [12323]

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_description = 123.22

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_description = "Trainer Code 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_description = "Trainer Code 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_description = "Trainer Code 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_description, "Trainer Code 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_type_description)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_description, "Trainer Code 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_type_description)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_description, "Trainer Code 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_description,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_type_description)

    def test_RunTrainerAddInfo_set_index_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.index_number = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.index_number = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.index_number = {"one"}

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.index_number = 1
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.index_number = 2
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.index_number = 3

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._indexNumber, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.index_number)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._indexNumber, 2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.index_number)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._indexNumber, 3)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._indexNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.index_number)

    def test_RunTrainerAddInfo_set_trainer_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_id = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_id = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_id = ["three"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_id = "Trainer ID 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_id = "Trainer ID 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_id = "Trainer ID 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._id, "Trainer ID 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._id,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_id)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._id, "Trainer ID 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._id,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_id)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._id, "Trainer ID 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._id,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_id)

    def test_RunTrainerAddInfo_set_trainer_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_name = ["three"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_name = "Trainer Name 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_name = "Trainer Name 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_name = "Trainer Name 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._name, "Trainer Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._name, "Trainer Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._name, "Trainer Name 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_name)

    def test_RunTrainerAddInfo_set_trainer_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_email = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_email = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_email = ["three"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_email = "Trainer Email 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_email = "Trainer Email 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_email = "Trainer Email 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._email, "Trainer Email 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._email,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_email)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._email, "Trainer Email 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._email,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_email)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._email, "Trainer Email 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._email,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_email)

    def test_RunTrainerAddInfo_set_trainer_id_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idNumber = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idNumber = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idNumber = ["three"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idNumber = "Trainer ID Number 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idNumber = "Trainer ID Number 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idNumber = "Trainer ID Number 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idNumber, "Trainer ID Number 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idNumber)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idNumber, "Trainer ID Number 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idNumber)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idNumber, "Trainer ID Number 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idNumber,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idNumber)

    def test_RunTrainerAddInfo_set_trainer_id_type(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idType = "SBBBBBBB"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType = {"OT"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idType = ["FP"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idType = IdType.OTHERS
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType = IdType.SINGAPORE_PINK
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idType = IdType.SINGAPORE_BLUE

        # assert both the code and the description
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_code, "OT")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_code, "SP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idType_code, "SB")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_description, "Others")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_description,
                         "Singapore Pink Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idType_description,
                         "Singapore Blue Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idType,
                         IdType.OTHERS)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType,
                         IdType.SINGAPORE_PINK)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_idType,
                         IdType.SINGAPORE_BLUE)

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idType = IdType.FIN_WORK_PERMIT
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType = IdType.FOREIGN_PASSPORT

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_code, "SO")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_code, "FP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_description, "Fin/Work Permit")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_description, "Foreign Passport")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_idType,
                         IdType.FIN_WORK_PERMIT)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_idType,
                         IdType.FOREIGN_PASSPORT)

    def test_RunTrainerAddInfo_set_trainer_roles(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_roles = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_roles = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_roles = "three"

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_roles = TestCourseRunsModels.ROLES_TWO_ENUM
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_roles = TestCourseRunsModels.ROLES_ONE_ENUM

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._roles,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.trainer_roles)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.trainer_roles)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE_ENUM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.trainer_roles)

    def test_RunTrainerAddInfo_set_in_training_provider_profile(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.inTrainingProviderProfile = "Yess"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.inTrainingProviderProfile = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.inTrainingProviderProfile = "n0"

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.inTrainingProviderProfile = OptionalSelector.YES
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.inTrainingProviderProfile = OptionalSelector.NIL
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.inTrainingProviderProfile = OptionalSelector.NO

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._inTrainingProviderProfile, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.inTrainingProviderProfile)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._inTrainingProviderProfile, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.inTrainingProviderProfile)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._inTrainingProviderProfile,
                         OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._inTrainingProviderProfile,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.inTrainingProviderProfile)

    def test_RunTrainerAddInfo_set_domain_area_of_practice(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.domain_area_of_practice = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.domain_area_of_practice = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.domain_area_of_practice = ["domain area 123"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.domain_area_of_practice = "Domain 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.domain_area_of_practice = "Domain 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.domain_area_of_practice = "Domain 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._domainAreaOfPractice,
                         "Domain 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.domain_area_of_practice)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._domainAreaOfPractice,
                         "Domain 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.domain_area_of_practice)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._domainAreaOfPractice,
                         "Domain 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._domainAreaOfPractice,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.domain_area_of_practice)

    def test_RunTrainerAddInfo_set_experience(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.experience = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.experience = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.experience = ["experience 123"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.experience = "Experience 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.experience = "Experience 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.experience = "Experience 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._experience, "Experience 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._experience,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.experience)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._experience, "Experience 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._experience,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.experience)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._experience, "Experience 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._experience,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.experience)

    def test_RunTrainerAddInfo_set_linked_in_url(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.linkedInURL = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.linkedInURL = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.linkedInURL = ["linkedin url 123"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.linkedInURL = "LinkedIn URL 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.linkedInURL = "LinkedIn URL 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.linkedInURL = "LinkedIn URL 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._linkedInURL, "LinkedIn URL 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.linkedInURL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedInURL, "LinkedIn URL 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.linkedInURL)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedInURL, "LinkedIn URL 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedInURL,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.linkedInURL)

    def test_RunTrainerAddInfo_set_salutation_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.salutationId = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.salutationId = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.salutationId = 3.3333333

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.salutationId = Salutations.MR
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.salutationId = Salutations.MDM
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.salutationId = Salutations.PROF

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._salutationId, Salutations.MR)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.salutationId)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._salutationId, Salutations.MDM)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.salutationId)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._salutationId, Salutations.PROF)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._salutationId,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.salutationId)

    def test_RunTrainerAddInfo_set_photo_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_name = ["photo name.jpg"]

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_name = "Photo Name 1"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_name = "Photo Name 2"
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_name = "Photo Name 3"

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_name, "Photo Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_name, "Photo Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_name)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_name, "Photo Name 3")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_name,
                         TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_name)

    def test_RunTrainerAddInfo_set_photo_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_content = b"image"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_content = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_content = ["photo"]

        with (open(os.path.join(RESOURCES_PATH, "core", "models", "test1.jpg"), "rb") as test1,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test2.jpg"), "rb") as test2,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test3.jpg"), "rb") as test3):
            T1 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_3",
                    name=test1.name,
                    type="jpg",
                    data=test1.read()
                ),
                FileURLsProto()
            )
            T2 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_4",
                    name=test2.name,
                    type="jpg",
                    data=test2.read()
                ),
                FileURLsProto()
            )
            T3 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_5",
                    name=test3.name,
                    type="jpg",
                    data=test3.read()
                ),
                FileURLsProto()
            )

            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_content = T1
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_content = T2
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_content = T3

            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_content, T1)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.photo_content)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_content, T2)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.photo_content)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_content, T3)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_content,
                             TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.photo_content)

    def test_RunTrainerAddInfo_add_linked_ssec_eqa(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_linkedSsecEQA(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA("three")

        EQA1 = LinkedSSECEQA()
        EQA1.description = "EQA 1"
        EQA1.ssecEQA = "1"

        EQA2 = LinkedSSECEQA()
        EQA2.description = "EQA test 2"
        EQA2.ssecEQA = "22"

        EQA3 = LinkedSSECEQA()
        EQA3.description = "EQA test 12"
        EQA3.ssecEQA = "23"

        # reset the linked SSEC EQAs in RUN_TRAINER_ADD_INFO_TWO and RUN_TRAINER_ADD_INFO_THREE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedSsecEQAs = []
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedSsecEQAs = []

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_linkedSsecEQA(EQA1)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA(EQA2)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(EQA3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._linkedSsecEQAs, [EQA1.payload()])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedSsecEQAs, [EQA2.payload()])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedSsecEQAs, [EQA3.payload()])

    # EditRunInfo tests
    def test_EditRunInfo_validate(self):
        e1, _ = TestCourseRunsModels.EDIT_RUN_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.EDIT_RUN_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.EDIT_RUN_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) > 0)  # this instance contains some trainers with missing fields
        self.assertTrue(len(e3) == 0)

    def test_EditRunInfo_payload(self):
        try:
            with (open(os.path.join(RESOURCES_PATH, "core", "models", "abc.jpg"), "rb") as f1,
                  open(os.path.join(RESOURCES_PATH, "core", "models", "def.jpg"), "rb") as f2):
                img1 = base64.b64encode(f1.read()).decode("utf-8")
                img2 = base64.b64encode(f2.read()).decode("utf-8")
        except Exception as ex:
            self.fail(f"Unable to load resources: {ex}")

        # since the photo is large, we need to up the size of the diff to view the differences if any
        self.maxDiff = None

        p3 = {
            "course": {
                "courseReferenceNumber": "XX-10000000K-02-TEST 199",  # uen cannot be tested without starting streamlit
                "run": {
                    "action": "update",
                    "sequenceNumber": 2,
                    "registrationDates": {
                        "opening": 20240201,
                        "closing": 20240204
                    },
                    "courseDates": {
                        "start": 20240201,
                        "end": 20240331
                    },
                    "scheduleInfoType": {
                        "code": "01",
                        "description": "Description"
                    },
                    "scheduleInfo": "Sat / 5 Sats / 9am - 6pm",
                    "venue": {
                        "block": "112B",
                        "street": "Other Street ABC",
                        "floor": "51",
                        "unit": "100",
                        "building": "Other Building ABC",
                        "postalCode": "554321",
                        "room": "84",
                        "wheelChairAccess": False
                    },
                    "intakeSize": 50,
                    "threshold": 100,
                    "registeredUserCount": 20,
                    "modeOfTraining": "8",
                    "courseAdminEmail": "jane@email.com",
                    "courseVacancy": {
                        "code": "F",
                        "description": "Full"
                    },
                    "file": {
                        "Name": "def.jpg",
                        "content": img2
                    },
                    "sessions": [
                        {
                            "action": "update",
                            "sessionId": "XX-10000000K-01-TEST 166",
                            "startDate": "20240101",
                            "endDate": "20240229",
                            "startTime": "08:30",
                            "endTime": "18:00",
                            "modeOfTraining": "2",
                            "venue": {
                                "block": "112A",
                                "street": "Street ABC",
                                "floor": "15",
                                "unit": "001",
                                "building": "Building ABC",
                                "postalCode": "123455",
                                "room": "24",
                                "wheelChairAccess": True,
                                "primaryVenue": True
                            }
                        },
                        {
                            "action": "update",
                            "sessionId": "XX-10000000K-01-TEST 166",
                            "startDate": "20240101",
                            "endDate": "20240229",
                            "startTime": "08:30",
                            "endTime": "18:00",
                            "modeOfTraining": "2",
                            "venue": {
                                "block": "112A",
                                "street": "Street ABC",
                                "floor": "15",
                                "unit": "001",
                                "building": "Building ABC",
                                "postalCode": "123455",
                                "room": "24",
                                "wheelChairAccess": True,
                                "primaryVenue": True
                            }
                        }
                    ],
                    "linkCourseRunTrainer": [
                        {
                            "trainer": {
                                "trainerType": {
                                    "code": "1",
                                    "description": "Existing"
                                },
                                "indexNumber": 1,
                                "id": "TRAINER_ONE",
                                "name": "JOHN DOE",
                                "email": "john@email.com",
                                "idNumber": "S1234567X",
                                "idType": {
                                    "code": "SB",
                                    "description": "Singapore Blue Identification Card"
                                },
                                "roles": [
                                    {
                                        "role": {
                                            "id": 1,
                                            "description": "Trainer"
                                        }
                                    }
                                ],
                                "inTrainingProviderProfile": True,
                                "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                        "Computer Application",
                                "experience": "Testing ABC",
                                "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                                "salutationId": 1,
                                "photo": {
                                    "name": "abc.jpg",
                                    "content": img1
                                },
                                "linkedSsecEQAs": [
                                    {
                                        "description": "EQA test 4",
                                        "ssecEQA": {
                                            "code": "12"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "trainer": {
                                "trainerType": {
                                    "code": "1",
                                    "description": "Existing"
                                },
                                "indexNumber": 1,
                                "id": "TRAINER_ONE",
                                "name": "JOHN DOE",
                                "email": "john@email.com",
                                "idNumber": "S1234567X",
                                "idType": {
                                    "code": "SB",
                                    "description": "Singapore Blue Identification Card"
                                },
                                "roles": [
                                    {
                                        "role": {
                                            "id": 1,
                                            "description": "Trainer"
                                        }
                                    }
                                ],
                                "inTrainingProviderProfile": True,
                                "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                        "Computer Application",
                                "experience": "Testing ABC",
                                "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                                "salutationId": 1,
                                "photo": {
                                    "name": "abc.jpg",
                                    "content": img1
                                },
                                "linkedSsecEQAs": [
                                    {
                                        "description": "EQA test 4",
                                        "ssecEQA": {
                                            "code": "12"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
        }

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.payload()

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.payload()

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE.payload(), p3)

    def test_EditRunInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.crid = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.crid = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.crid = ["three"]

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.crid = "CRID 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.crid = "CRID 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.crid = "CRID 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._crid,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.crid)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._crid, "CRID 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._crid,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.crid)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._crid, "CRID 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._crid,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.crid)

    def test_EditRunInfo_set_sequence_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.sequence_number = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.sequence_number = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.sequence_number = {"one"}

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.sequence_number = 1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.sequence_number = 2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.sequence_number = 3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sequenceNumber, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sequenceNumber,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.sequence_number)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sequenceNumber, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sequenceNumber,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.sequence_number)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sequenceNumber, 3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sequenceNumber,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.sequence_number)

    def test_EditRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.opening_registration_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.opening_registration_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.opening_registration_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.opening_registration_date = dt1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.opening_registration_date = dt2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.opening_registration_date = dt3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_opening, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_opening,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.opening_registration_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_opening, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_opening,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.opening_registration_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_opening, dt3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_opening,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.opening_registration_date)

    def test_EditRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.closing_registration_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.closing_registration_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.closing_registration_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.closing_registration_date = dt1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.closing_registration_date = dt2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.closing_registration_date = dt3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_closing, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_closing,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.closing_registration_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_closing, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_closing,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.closing_registration_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_closing, dt3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_closing,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.closing_registration_date)

    def test_EditRunInfo_set_course_dates_start(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_start_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_start_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_start_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_start_date = dt1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_start_date = dt2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_start_date = dt3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_start, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_start,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_start_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_start, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_start,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_start_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_start, dt3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_start,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_start_date)

    def test_EditRunInfo_set_course_dates_end(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_end_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_end_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_end_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_end_date = dt1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_end_date = dt2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_end_date = dt3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_end, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_end,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_end_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_end, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_end,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_end_date)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_end, dt3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_end,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_end_date)

    def test_EditRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_code = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_code = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_code = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_code = "1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_code = "2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_code = "3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_code, "1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_code,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_code)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_code, "2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_code,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_code)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_code, "3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_code,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_code)

    def test_EditRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_description = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_description = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_description = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_description = "Description 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_description = "Description 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_description = "Description 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_description, "Description 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_description,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info_type_description)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_description, "Description 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_description,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info_type_description)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_description,
                         "Description 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_description,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info_type_description)

    def test_EditRunInfo_set_schedule_info(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info = "Schedule Info 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info = "Schedule Info 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info = "Schedule Info 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfo, "Schedule Info 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfo,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.schedule_info)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfo, "Schedule Info 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfo,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.schedule_info)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfo, "Schedule Info 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfo,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.schedule_info)

    def test_EditRunInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.block = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.block = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.block = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.block = "Block 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.block = "Block 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.block = "Block 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_block,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.block)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_block,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.block)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_block, "Block 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_block,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.block)

    def test_EditRunInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.street = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.street = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.street = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.street = "Street 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.street = "Street 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.street = "Street 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_street,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.street)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_street,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.street)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_street, "Street 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_street,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.street)

    def test_EditRunInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.floor = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.floor = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.floor = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.floor = "Floor 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.floor = "Floor 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.floor = "Floor 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_floor,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.floor)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_floor,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.floor)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_floor, "Floor 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_floor,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.floor)

    def test_EditRunInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.unit = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.unit = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.unit = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.unit = "Unit 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.unit = "Unit 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.unit = "Unit 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_unit,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.unit)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_unit,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.unit)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_unit, "Unit 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_unit,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.unit)

    def test_EditRunInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.building = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.building = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.building = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.building = "Building 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.building = "Building 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.building = "Building 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_building,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.building)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_building,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.building)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_building, "Building 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_building,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.building)

    def test_EditRunInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.postal_code = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.postal_code = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.postal_code = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.postal_code = "112233"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.postal_code = "223344"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.postal_code = "334455"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_postalCode, "112233")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.postal_code)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_postalCode, "223344")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_postalCode,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.postal_code)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_postalCode, "334455")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_postalCode,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.postal_code)

    def test_EditRunInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.room = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.room = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.room = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.room = "Room 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.room = "Room 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.room = "Room 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_room,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.room)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_room,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.room)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_room, "Room 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_room,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.room)

    def test_EditRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.wheel_chair_access = "Yess"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.wheel_chair_access = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.wheel_chair_access = "n0"

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.wheel_chair_access = OptionalSelector.YES
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.wheel_chair_access = OptionalSelector.NIL
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.wheel_chair_access = OptionalSelector.NO

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_wheelChairAccess, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_wheelChairAccess,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_wheelChairAccess, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_wheelChairAccess,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_wheelChairAccess, OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_wheelChairAccess,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.wheel_chair_access)

    def test_EditRunInfo_set_intake_size(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.intake_size = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.intake_size = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.intake_size = {"one"}

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.intake_size = 1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.intake_size = 2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.intake_size = 3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._intakeSize, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._intakeSize,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.intake_size)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._intakeSize, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._intakeSize,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.intake_size)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._intakeSize, 3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._intakeSize,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.intake_size)

    def test_EditRunInfo_set_threshold(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.threshold = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.threshold = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.threshold = {"one"}

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.threshold = 1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.threshold = 2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.threshold = 3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._threshold, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._threshold,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.threshold)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._threshold, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._threshold,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.threshold)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._threshold, 3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._threshold,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.threshold)

    def test_EditRunInfo_set_registered_user_count(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.registered_user_count = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.registered_user_count = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.registered_user_count = {"one"}

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.registered_user_count = 1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.registered_user_count = 2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.registered_user_count = 3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registeredUserCount, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registeredUserCount,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.registered_user_count)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registeredUserCount, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registeredUserCount,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.registered_user_count)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registeredUserCount, 3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registeredUserCount,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.registered_user_count)

    def test_EditRunInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.mode_of_training = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.mode_of_training = "One"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.mode_of_training = {"one"}

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.mode_of_training = ModeOfTraining.CLASSROOM
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.mode_of_training = ModeOfTraining.ASYNCHRONOUS_ELEARNING
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.mode_of_training = ModeOfTraining.IN_HOUSE

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._modeOfTraining, ModeOfTraining.CLASSROOM)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._modeOfTraining,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.mode_of_training)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._modeOfTraining, ModeOfTraining.ASYNCHRONOUS_ELEARNING)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._modeOfTraining,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.mode_of_training)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._modeOfTraining, ModeOfTraining.IN_HOUSE)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._modeOfTraining,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.mode_of_training)

    def test_EditRunInfo_set_course_admin_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_admin_email = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_admin_email = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_admin_email = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_admin_email = "Email 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_admin_email = "Email 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_admin_email = "Email 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseAdminEmail, "Email 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseAdminEmail,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_admin_email)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseAdminEmail, "Email 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseAdminEmail,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_admin_email)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseAdminEmail, "Email 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseAdminEmail,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_admin_email)

    def test_EditRunInfo_set_course_vacancy(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_vacancy = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_vacancy = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_vacancy = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_vacancy = Vacancy.FULL
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_vacancy = Vacancy.AVAILABLE
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_vacancy = Vacancy.LIMITED_VACANCY

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseVacancy_code, Vacancy.FULL.value[0])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseVacancy_description, Vacancy.FULL.value[1])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE.course_vacancy, Vacancy.FULL)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseVacancy_code, Vacancy.AVAILABLE.value[0])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseVacancy_description, Vacancy.AVAILABLE.value[1])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO.course_vacancy, Vacancy.AVAILABLE)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseVacancy_code, Vacancy.LIMITED_VACANCY.value[0])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseVacancy_description,
                         Vacancy.LIMITED_VACANCY.value[1])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE.course_vacancy, Vacancy.LIMITED_VACANCY)

    def test_EditRunInfo_set_file_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_name = 3.3333333

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_name = "File Name 1"
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_name = "File Name 2"
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_name = "File Name 3"

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_Name, "File Name 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_Name,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_name)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_Name, "File Name 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_Name,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_name)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_Name, "File Name 3")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_Name,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_name)

    def test_EditRunInfo_set_file_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_content = b"image"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_content = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_content = ["photo"]

        with (open(os.path.join(RESOURCES_PATH, "core", "models", "test1.jpg"), "rb") as test1,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test2.jpg"), "rb") as test2,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test3.jpg"), "rb") as test3):
            T1 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_3",
                    name=test1.name,
                    type="jpg",
                    data=test1.read()
                ),
                FileURLsProto()
            )
            T2 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_4",
                    name=test2.name,
                    type="jpg",
                    data=test2.read()
                ),
                FileURLsProto()
            )
            T3 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_5",
                    name=test3.name,
                    type="jpg",
                    data=test3.read()
                ),
                FileURLsProto()
            )

            TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_content = T1
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_content = T2
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_content = T3

            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_content, T1)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_content,
                             TestCourseRunsModels.EDIT_RUN_INFO_ONE.file_content)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_content, T2)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_content,
                             TestCourseRunsModels.EDIT_RUN_INFO_TWO.file_content)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_content, T3)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_content,
                             TestCourseRunsModels.EDIT_RUN_INFO_THREE.file_content)

    def test_EditRunInfo_set_sessions(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.sessions = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.sessions = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.sessions = 3.3333333

        st1 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO]
        st2 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]
        st3 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.sessions = st1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.sessions = st2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.sessions = st3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sessions, st1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.sessions)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions, st2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.sessions)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions, st3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.sessions)

    def test_EditRunInfo_add_session(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_session({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_session(3.3333333)

        # reset the course sessions in RUN_SESSION_EDIT_INFO_TWO and RUN_SESSION_EDIT_INFO_THREE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions = []
        TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions = []

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.sessions)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.sessions)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.sessions)

    def test_EditRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.linked_course_run_trainers = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.linked_course_run_trainers = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.linked_course_run_trainers = 3.3333333

        cr1 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO]
        cr2 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]
        cr3 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.linked_course_run_trainers = cr1
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.linked_course_run_trainers = cr2
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.linked_course_run_trainers = cr3

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._linkCourseRunTrainer, cr1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._linkCourseRunTrainer,
                         TestCourseRunsModels.EDIT_RUN_INFO_ONE.linked_course_run_trainers)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._linkCourseRunTrainer, cr2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._linkCourseRunTrainer,
                         TestCourseRunsModels.EDIT_RUN_INFO_TWO.linked_course_run_trainers)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._linkCourseRunTrainer, cr3)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._linkCourseRunTrainer,
                         TestCourseRunsModels.EDIT_RUN_INFO_THREE.linked_course_run_trainers)

    def test_EditRunInfo_add_link_course_run_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_linkCourseRunTrainer(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.add_linkCourseRunTrainer({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.add_linkCourseRunTrainer(3.3333333)

        # reset the linked course run trainers in RUN_TRAINER_ADD_INFO_TWO and RUN_TRAINER_ADD_INFO_THREE
        TestCourseRunsModels.EDIT_RUN_INFO_TWO._linkCourseRunTrainer = []
        TestCourseRunsModels.EDIT_RUN_INFO_THREE._linkCourseRunTrainer = []

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.add_linkCourseRunTrainer(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.add_linkCourseRunTrainer(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.add_linkCourseRunTrainer(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE])

    # DeleteRunInfo tests
    def test_DeleteRunInfo_validate(self):
        e1, _ = TestCourseRunsModels.DELETE_RUN_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.DELETE_RUN_INFO_TWO.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)

    def test_DeleteRunInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.payload()

        pl = {
            "course": {
                "courseReferenceNumber": "XX-10000000K-01-TEST 166",
                # courseReferenceNumber is ignored since session state cannot be tested when streamlit is not running
                "run": {
                    "action": "delete"
                }
            }
        }

        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_TWO.payload(), pl)

    def test_DeleteRunInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.crid = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.crid = {"two"}

        TestCourseRunsModels.DELETE_RUN_INFO_ONE.crid = "CRID 1"
        TestCourseRunsModels.DELETE_RUN_INFO_TWO.crid = "CRID 2"

        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_ONE._crid,
                         TestCourseRunsModels.DELETE_RUN_INFO_ONE.crid)
        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_TWO._crid, "CRID 2")
        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_TWO._crid,
                         TestCourseRunsModels.DELETE_RUN_INFO_TWO.crid)

    def test_DeleteRunInfo_set_sequence_number(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.sequence_number = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.sequence_number = "2232131"

    def test_DeleteRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.opening_registration_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.opening_registration_date = "2232131"

    def test_DeleteRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.closing_registration_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.closing_registration_date = "2232131"

    def test_DeleteRunInfo_set_course_dates_start(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.course_start_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.course_start_date = "2232131"

    def test_DeleteRunInfo_set_course_dates_end(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.course_end_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.course_end_date = "2232131"

    def test_DeleteRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.schedule_info_type_code = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.schedule_info_type_code = {"two"}

    def test_DeleteRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.schedule_info_type_description = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.schedule_info_type_description = {"two"}

    def test_DeleteRunInfo_set_schedule_info(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.schedule_info = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.schedule_info = {"two"}

    def test_DeleteRunInfo_set_venue_block(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.block = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.block = {"two"}

    def test_DeleteRunInfo_set_venue_street(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.street = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.street = {"two"}

    def test_DeleteRunInfo_set_venue_floor(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.floor = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.floor = {"two"}

    def test_DeleteRunInfo_set_venue_unit(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.unit = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.unit = {"two"}

    def test_DeleteRunInfo_set_venue_building(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.building = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.building = {"two"}

    def test_DeleteRunInfo_set_venue_postal_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.postal_code = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.postal_code = {"two"}

    def test_DeleteRunInfo_set_venue_room(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.room = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.room = {"two"}

    def test_DeleteRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.wheel_chair_access = "Yess"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.wheel_chair_access = 1

    def test_DeleteRunInfo_set_intake_size(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.intake_size = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.intake_size = "2232131"

    def test_DeleteRunInfo_set_threshold(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.threshold = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.threshold = "2232131"

    def test_DeleteRunInfo_set_registered_user_count(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.registered_user_count = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.registered_user_count = "2232131"

    def test_DeleteRunInfo_set_mode_of_training(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.mode_of_training = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.mode_of_training = "One"

    def test_DeleteRunInfo_set_course_admin_email(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.course_admin_email = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.course_admin_email = {"two"}

    def test_DeleteRunInfo_set_course_vacancy(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.course_vacancy = Vacancy.LIMITED_VACANCY

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.course_vacancy = Vacancy.FULL

    def test_DeleteRunInfo_set_file_name(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.file_name = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.file_name = {"two"}

    def test_DeleteRunInfo_set_file_content(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.file_content = b"image"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.file_content = {"two"}

    def test_DeleteRunInfo_set_sessions(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.sessions = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.sessions = {"two"}

    def test_DeleteRunInfo_add_session(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.add_session({"two"})

    def test_DeleteRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.linked_course_run_trainers = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.linked_course_run_trainers = {"two"}

    def test_DeleteRunInfo_add_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.add_linkCourseRunTrainer(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.add_linkCourseRunTrainer({"two"})

    # AddRunIndividualInfo tests
    def test_AddRunIndividualInfo_validate(self):
        e1, _ = TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) > 0)  # some trainer details are missing and this would fail
        self.assertTrue(len(e3) == 0)

    def test_AddRunIndividualInfo_payload(self):
        try:
            with (open(os.path.join(RESOURCES_PATH, "core", "models", "abc.jpg"), "rb") as f1,
                  open(os.path.join(RESOURCES_PATH, "core", "models", "def.jpg"), "rb") as f2):
                img1 = base64.b64encode(f1.read()).decode("utf-8")
                img2 = base64.b64encode(f2.read()).decode("utf-8")
        except Exception as ex:
            self.fail(f"Failed to load resources: {ex}")

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.payload()

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.payload()

        # since the photo is large, we need to up the size of the diff to view the differences if any
        self.maxDiff = None
        pl = {
            "sequenceNumber": 2,
            "registrationDates": {
                "opening": 20240201,
                "closing": 20240204
            },
            "courseDates": {
                "start": 20240201,
                "end": 20240331
            },
            "scheduleInfoType": {
                "code": "01",
                "description": "Description"
            },
            "scheduleInfo": "Sat / 5 Sats / 9am - 6pm",
            "venue": {
                "block": "112B",
                "street": "Other Street ABC",
                "floor": "51",
                "unit": "100",
                "building": "Other Building ABC",
                "postalCode": "554321",
                "room": "84",
                "wheelChairAccess": False
            },
            "intakeSize": 50,
            "threshold": 100,
            "registeredUserCount": 20,
            "modeOfTraining": "8",
            "courseAdminEmail": "jane@email.com",
            "courseVacancy": {
                "code": "F",
                "description": "Full"
            },
            "file": {
                "Name": "def.jpg",
                "content": img2
            },
            "sessions": [
                {
                    "action": "update",
                    "sessionId": "XX-10000000K-01-TEST 166",
                    "startDate": "20240101",
                    "endDate": "20240229",
                    "startTime": "08:30",
                    "endTime": "18:00",
                    "modeOfTraining": "2",
                    "venue": {
                        "block": "112A",
                        "street": "Street ABC",
                        "floor": "15",
                        "unit": "001",
                        "building": "Building ABC",
                        "postalCode": "123455",
                        "room": "24",
                        "wheelChairAccess": True,
                        "primaryVenue": True
                    }
                },
                {
                    "action": "update",
                    "sessionId": "XX-10000000K-01-TEST 166",
                    "startDate": "20240101",
                    "endDate": "20240229",
                    "startTime": "08:30",
                    "endTime": "18:00",
                    "modeOfTraining": "2",
                    "venue": {
                        "block": "112A",
                        "street": "Street ABC",
                        "floor": "15",
                        "unit": "001",
                        "building": "Building ABC",
                        "postalCode": "123455",
                        "room": "24",
                        "wheelChairAccess": True,
                        "primaryVenue": True
                    }
                }
            ],
            "linkCourseRunTrainer": [
                {
                    "trainer": {
                        "trainerType": {
                            "code": "1",
                            "description": "Existing"
                        },
                        "indexNumber": 1,
                        "id": "TRAINER_ONE",
                        "name": "JOHN DOE",
                        "email": "john@email.com",
                        "idNumber": "S1234567X",
                        "idType": {
                            "code": "SB",
                            "description": "Singapore Blue Identification Card"
                        },
                        "roles": [
                            {
                                "role": {
                                    "id": 1,
                                    "description": "Trainer"
                                }
                            }
                        ],
                        "inTrainingProviderProfile": True,
                        "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                "Computer Application",
                        "experience": "Testing ABC",
                        "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                        "salutationId": 1,
                        "photo": {
                            "name": "abc.jpg",
                            "content": img1
                        },
                        "linkedSsecEQAs": [
                            {
                                "description": "EQA test 4",
                                "ssecEQA": {
                                    "code": "12"
                                }
                            }
                        ]
                    }
                },
                {
                    "trainer": {
                        "trainerType": {
                            "code": "1",
                            "description": "Existing"
                        },
                        "indexNumber": 1,
                        "id": "TRAINER_ONE",
                        "name": "JOHN DOE",
                        "email": "john@email.com",
                        "idNumber": "S1234567X",
                        "idType": {
                            "code": "SB",
                            "description": "Singapore Blue Identification Card"
                        },
                        "roles": [
                            {
                                "role": {
                                    "id": 1,
                                    "description": "Trainer"
                                }
                            }
                        ],
                        "inTrainingProviderProfile": True,
                        "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                "Computer Application",
                        "experience": "Testing ABC",
                        "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                        "salutationId": 1,
                        "photo": {
                            "name": "abc.jpg",
                            "content": img1
                        },
                        "linkedSsecEQAs": [
                            {
                                "description": "EQA test 4",
                                "ssecEQA": {
                                    "code": "12"
                                }
                            }
                        ]
                    }
                }
            ]
        }

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.payload(), pl)

    def test_AddRunIndividualInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.crid = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.crid = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.crid = ["three"]

    def test_AddRunIndividualInfo_set_sequence_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sequence_number = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sequence_number = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sequence_number = {"one"}

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sequence_number = 1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sequence_number = 2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sequence_number = 3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sequenceNumber, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sequenceNumber,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sequence_number)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sequenceNumber, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sequenceNumber,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sequence_number)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sequenceNumber, 3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sequenceNumber,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sequence_number)

    def test_AddRunIndividualInfo_set_registration_dates_opening(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.opening_registration_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.opening_registration_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.opening_registration_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.opening_registration_date = dt1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.opening_registration_date = dt2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.opening_registration_date = dt3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_opening, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_opening,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.opening_registration_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_opening, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_opening,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.opening_registration_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_opening, dt3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_opening,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.opening_registration_date)

    def test_AddRunIndividualInfo_set_registration_dates_closing(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.closing_registration_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.closing_registration_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.closing_registration_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.closing_registration_date = dt1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.closing_registration_date = dt2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.closing_registration_date = dt3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_closing, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_closing,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.closing_registration_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_closing, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_closing,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.closing_registration_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_closing, dt3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_closing,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.closing_registration_date)

    def test_AddRunIndividualInfo_set_course_dates_start(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_start_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_start_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_start_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_start_date = dt1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_start_date = dt2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_start_date = dt3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_start, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_start,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_start_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_start, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_start,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_start_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_start, dt3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_start,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_start_date)

    def test_AddRunIndividualInfo_set_course_dates_end(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_end_date = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_end_date = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_end_date = {"one"}

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_end_date = dt1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_end_date = dt2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_end_date = dt3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_end, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_end,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_end_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_end, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_end,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_end_date)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_end, dt3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_end,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_end_date)

    def test_AddRunIndividualInfo_set_schedule_info_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info_type_code = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_code = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_code = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info_type_code = "1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_code = "2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_code = "3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_code, "1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_code,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_code)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_code, "2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_code,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_code)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_code, "3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_code,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_code)

    def test_AddRunIndividualInfo_set_schedule_info_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info_type_description = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_description = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_description = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info_type_description = "Description 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_description = "Description 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_description = "Description 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_description,
                         "Description 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_description,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info_type_description)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_description,
                         "Description 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_description,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info_type_description)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_description,
                         "Description 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_description,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info_type_description)

    def test_AddRunIndividualInfo_set_schedule_info(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info = "Schedule Info 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info = "Schedule Info 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info = "Schedule Info 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfo, "Schedule Info 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfo,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.schedule_info)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfo, "Schedule Info 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfo,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.schedule_info)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfo, "Schedule Info 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfo,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.schedule_info)

    def test_AddRunIndividualInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.block = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.block = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.block = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.block = "Block 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.block = "Block 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.block = "Block 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_block,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.block)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_block,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.block)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_block, "Block 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_block,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.block)

    def test_AddRunIndividualInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.street = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.street = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.street = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.street = "Street 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.street = "Street 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.street = "Street 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_street,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.street)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_street,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.street)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_street, "Street 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_street,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.street)

    def test_AddRunIndividualInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.floor = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.floor = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.floor = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.floor = "Floor 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.floor = "Floor 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.floor = "Floor 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_floor,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.floor)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_floor,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.floor)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_floor, "Floor 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_floor,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.floor)

    def test_AddRunIndividualInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.unit = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.unit = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.unit = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.unit = "Unit 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.unit = "Unit 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.unit = "Unit 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_unit,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.unit)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_unit,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.unit)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_unit, "Unit 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_unit,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.unit)

    def test_AddRunIndividualInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.building = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.building = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.building = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.building = "Building 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.building = "Building 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.building = "Building 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_building,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.building)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_building,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.building)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_building, "Building 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_building,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.building)

    def test_AddRunIndividualInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.postal_code = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.postal_code = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.postal_code = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.postal_code = "112233"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.postal_code = "223344"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.postal_code = "334455"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_postalCode, "112233")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.postal_code)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_postalCode, "223344")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.postal_code)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_postalCode, "334455")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_postalCode,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.postal_code)

    def test_AddRunIndividualInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.room = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.room = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.room = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.room = "Room 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.room = "Room 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.room = "Room 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_room,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.room)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_room,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.room)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_room, "Room 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_room,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.room)

    def test_AddRunIndividualInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.wheel_chair_access = "Yess"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.wheel_chair_access = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.wheel_chair_access = "n0"

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.wheel_chair_access = OptionalSelector.YES
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.wheel_chair_access = OptionalSelector.NIL
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.wheel_chair_access = OptionalSelector.NO

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_wheelChairAccess, OptionalSelector.YES)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_wheelChairAccess,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_wheelChairAccess, OptionalSelector.NIL)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_wheelChairAccess,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.wheel_chair_access)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_wheelChairAccess,
                         OptionalSelector.NO)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_wheelChairAccess,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.wheel_chair_access)

    def test_AddRunIndividualInfo_set_intake_size(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.intake_size = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.intake_size = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.intake_size = {"one"}

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.intake_size = 1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.intake_size = 2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.intake_size = 3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._intakeSize, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._intakeSize,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.intake_size)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._intakeSize, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._intakeSize,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.intake_size)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._intakeSize, 3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._intakeSize,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.intake_size)

    def test_AddRunIndividualInfo_set_threshold(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.threshold = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.threshold = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.threshold = {"one"}

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.threshold = 1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.threshold = 2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.threshold = 3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._threshold, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._threshold,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.threshold)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._threshold, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._threshold,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.threshold)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._threshold, 3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._threshold,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.threshold)

    def test_AddRunIndividualInfo_set_registered_user_count(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.registered_user_count = "1"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.registered_user_count = "2232131"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.registered_user_count = {"one"}

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.registered_user_count = 1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.registered_user_count = 2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.registered_user_count = 3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registeredUserCount, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registeredUserCount,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.registered_user_count)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registeredUserCount, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registeredUserCount,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.registered_user_count)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registeredUserCount, 3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registeredUserCount,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.registered_user_count)

    def test_AddRunIndividualInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.mode_of_training = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.mode_of_training = "One"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.mode_of_training = {"one"}

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.mode_of_training = ModeOfTraining.CLASSROOM
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.mode_of_training = ModeOfTraining.ASYNCHRONOUS_ELEARNING
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.mode_of_training = ModeOfTraining.IN_HOUSE

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._modeOfTraining, ModeOfTraining.CLASSROOM)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._modeOfTraining,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.mode_of_training)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._modeOfTraining,
                         ModeOfTraining.ASYNCHRONOUS_ELEARNING)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._modeOfTraining,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.mode_of_training)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._modeOfTraining, ModeOfTraining.IN_HOUSE)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._modeOfTraining,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.mode_of_training)

    def test_AddRunIndividualInfo_set_course_admin_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_admin_email = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_admin_email = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_admin_email = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_admin_email = "Email 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_admin_email = "Email 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_admin_email = "Email 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseAdminEmail, "Email 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseAdminEmail,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_admin_email)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseAdminEmail, "Email 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseAdminEmail,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_admin_email)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseAdminEmail, "Email 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseAdminEmail,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_admin_email)

    def test_AddRunIndividualInfo_set_course_vacancy(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_vacancy = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_vacancy = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_vacancy = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_vacancy = Vacancy.LIMITED_VACANCY
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_vacancy = Vacancy.FULL
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_vacancy = Vacancy.AVAILABLE

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseVacancy_code,
                         Vacancy.LIMITED_VACANCY.value[0])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseVacancy_code,
                         Vacancy.FULL.value[0])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseVacancy_code,
                         Vacancy.AVAILABLE.value[0])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseVacancy_description,
                         Vacancy.LIMITED_VACANCY.value[1])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseVacancy_description,
                         Vacancy.FULL.value[1])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseVacancy_description,
                         Vacancy.AVAILABLE.value[1])

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.course_vacancy,
                         Vacancy.LIMITED_VACANCY)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.course_vacancy,
                         Vacancy.FULL)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.course_vacancy,
                         Vacancy.AVAILABLE)

    def test_AddRunIndividualInfo_set_file_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_name = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_name = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_name = 3.3333333

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_name = "File Name 1"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_name = "File Name 2"
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_name = "File Name 3"

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_Name, "File Name 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_Name,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_name)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_Name, "File Name 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_Name,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_name)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_Name, "File Name 3")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_Name,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_name)

    def test_AddRunIndividualInfo_set_file_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_content = b"image"

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_content = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_content = ["photo"]

        with (open(os.path.join(RESOURCES_PATH, "core", "models", "test1.jpg"), "rb") as test1,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test2.jpg"), "rb") as test2,
              open(os.path.join(RESOURCES_PATH, "core", "models", "test3.jpg"), "rb") as test3):
            T1 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_3",
                    name=test1.name,
                    type="jpg",
                    data=test1.read()
                ),
                FileURLsProto()
            )
            T2 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_4",
                    name=test2.name,
                    type="jpg",
                    data=test2.read()
                ),
                FileURLsProto()
            )
            T3 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_5",
                    name=test3.name,
                    type="jpg",
                    data=test3.read()
                ),
                FileURLsProto()
            )

            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_content = T1
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_content = T2
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_content = T3

            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_content, T1)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_content,
                             TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.file_content)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_content, T2)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_content,
                             TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.file_content)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_content, T3)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_content,
                             TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.file_content)

    def test_AddRunIndividualInfo_set_sessions(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sessions = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sessions = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sessions = 3.3333333

        st1 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO]
        st2 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]
        st3 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sessions = st1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sessions = st2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sessions = st3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sessions, st1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sessions,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.sessions)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sessions, st2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sessions,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.sessions)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sessions, st3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sessions,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.sessions)

    def test_AddRunIndividualInfo_add_session(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_session({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_session(3.3333333)

        # reset the course sessions in RUN_SESSION_EDIT_INFO_TWO and RUN_SESSION_EDIT_INFO_THREE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sessions = []
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sessions = []

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.add_session(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE])

    def test_AddRunIndividualInfo_set_link_course_run_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.linked_course_run_trainers = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.linked_course_run_trainers = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.linked_course_run_trainers = 3.3333333

        cr1 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO]
        cr2 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]
        cr3 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.linked_course_run_trainers = cr1
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.linked_course_run_trainers = cr2
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.linked_course_run_trainers = cr3

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._linkCourseRunTrainer, cr1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._linkCourseRunTrainer,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.linked_course_run_trainers)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._linkCourseRunTrainer, cr2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._linkCourseRunTrainer,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.linked_course_run_trainers)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._linkCourseRunTrainer, cr3)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._linkCourseRunTrainer,
                         TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.linked_course_run_trainers)

    def test_AddRunIndividualInfo_add_link_course_run_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_linkCourseRunTrainer(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.add_linkCourseRunTrainer({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.add_linkCourseRunTrainer(3.3333333)

        # reset the linked course run trainers in RUN_TRAINER_ADD_INFO_TWO and RUN_TRAINER_ADD_INFO_THREE
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._linkCourseRunTrainer = []
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._linkCourseRunTrainer = []

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.add_linkCourseRunTrainer(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.add_linkCourseRunTrainer(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.add_linkCourseRunTrainer(
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO])
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._linkCourseRunTrainer,
                         [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE])

    # AddRunInfo test
    def test_AddRunInfo_validate(self):
        # we need to set the trainer status properly for the third run info, which ends up impacting
        # the second run info
        TestCourseRunsModels.ADD_RUN_INFO_THREE._runs = [TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE]

        e1, _ = TestCourseRunsModels.ADD_RUN_INFO_ONE.validate()
        e2, _ = TestCourseRunsModels.ADD_RUN_INFO_TWO.validate()
        e3, _ = TestCourseRunsModels.ADD_RUN_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) > 0)
        self.assertTrue(len(e3) == 0)

    def test_AddRunInfo_payload(self):
        try:
            with (open(os.path.join(RESOURCES_PATH, "core", "models", "abc.jpg"), "rb") as f1,
                  open(os.path.join(RESOURCES_PATH, "core", "models", "def.jpg"), "rb") as f2):
                img1 = base64.b64encode(f1.read()).decode("utf-8")
                img2 = base64.b64encode(f2.read()).decode("utf-8")
        except Exception as ex:
            self.fail(f"Failed to load resource: {ex}")

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.payload()

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.payload()

        # we need to set the trainer status properly for the third run info, which ends up impacting
        # the second run info
        TestCourseRunsModels.ADD_RUN_INFO_THREE._runs = [TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE]

        # since images are tested, we need to increase the size of the diffs
        self.maxDiff = None

        # note that uen is missing here as that is dependent on the application being launched
        # it might be possible to test that in the future once we integrate the Streamlit app testing framework
        # into the unit tests
        p3 = {
            "course": {
                "courseReferenceNumber": "XX-10000000K-02-TEST 199",
                "runs": [
                    {
                        "sequenceNumber": 2,
                        "registrationDates": {
                            "opening": 20240201,
                            "closing": 20240204
                        },
                        "courseDates": {
                            "start": 20240201,
                            "end": 20240331
                        },
                        "scheduleInfoType": {
                            "code": "01",
                            "description": "Description"
                        },
                        "scheduleInfo": "Sat / 5 Sats / 9am - 6pm",
                        "venue": {
                            "block": "112B",
                            "street": "Other Street ABC",
                            "floor": "51", "unit": "100",
                            "building": "Other Building ABC",
                            "postalCode": "554321",
                            "room": "84",
                            "wheelChairAccess": False
                        },
                        "intakeSize": 50,
                        "threshold": 100,
                        "registeredUserCount": 20,
                        "modeOfTraining": "8",
                        "courseAdminEmail": "jane@email.com",
                        "courseVacancy": {
                            "code": "F",
                            "description": "Full"
                        },
                        "file": {
                            "Name": "def.jpg",
                            "content": img2
                        },
                        "sessions": [
                            {
                                "action": "update",
                                "sessionId": "XX-10000000K-01-TEST 166",
                                "startDate": "20240101",
                                "endDate": "20240229",
                                "startTime": "08:30",
                                "endTime": "18:00",
                                "modeOfTraining": "2",
                                "venue": {
                                    "block": "112A",
                                    "street": "Street ABC",
                                    "floor": "15",
                                    "unit": "001",
                                    "building": "Building ABC",
                                    "postalCode": "123455",
                                    "room": "24",
                                    "wheelChairAccess": True,
                                    "primaryVenue": True
                                }
                            },
                            {
                                "action": "update",
                                "sessionId": "XX-10000000K-01-TEST 166",
                                "startDate": "20240101",
                                "endDate": "20240229",
                                "startTime": "08:30",
                                "endTime": "18:00",
                                "modeOfTraining": "2",
                                "venue": {
                                    "block": "112A",
                                    "street": "Street ABC",
                                    "floor": "15",
                                    "unit": "001",
                                    "building": "Building ABC",
                                    "postalCode": "123455",
                                    "room": "24",
                                    "wheelChairAccess": True,
                                    "primaryVenue": True
                                }
                            }
                        ],
                        "linkCourseRunTrainer": [
                            {
                                "trainer": {
                                    "trainerType": {
                                        "code": "1",
                                        "description": "Existing"
                                    },
                                    "indexNumber": 1,
                                    "id": "TRAINER_ONE",
                                    "name": "JOHN DOE",
                                    "email": "john@email.com",
                                    "idNumber": "S1234567X",
                                    "idType": {
                                        "code": "SB",
                                        "description": "Singapore Blue Identification Card"
                                    },
                                    "roles": [
                                        {
                                            "role": {
                                                "id": 1,
                                                "description": "Trainer"
                                            }
                                        }
                                    ],
                                    "inTrainingProviderProfile": True,
                                    "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                            "Computer Application",
                                    "experience": "Testing ABC",
                                    "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                                    "salutationId": 1,
                                    "photo": {
                                        "name": "abc.jpg",
                                        "content": img1
                                    },
                                    "linkedSsecEQAs": [
                                        {
                                            "description": "EQA test 4",
                                            "ssecEQA": {
                                                "code": "12"
                                            }
                                        }
                                    ]
                                },
                            },
                            {
                                "trainer": {
                                    "trainerType":
                                        {
                                            "code": "1",
                                            "description": "Existing"
                                        },
                                    "indexNumber": 1,
                                    "id": "TRAINER_ONE",
                                    "name": "JOHN DOE",
                                    "email": "john@email.com",
                                    "idNumber": "S1234567X",
                                    "idType":
                                        {
                                            "code": "SB",
                                            "description": "Singapore Blue Identification Card"
                                        },
                                    "roles":
                                        [
                                            {
                                                "role": {
                                                    "id": 1,
                                                    "description": "Trainer"
                                                }
                                            }
                                        ],
                                    "inTrainingProviderProfile": True,
                                    "domainAreaOfPractice": "Testing Management in Computer Application and Diploma in "
                                                            "Computer Application",
                                    "experience": "Testing ABC",
                                    "linkedInURL": "https://sg.linkedin.com/company/linkedin/abc",
                                    "salutationId": 1,
                                    "photo":
                                        {
                                            "name": "abc.jpg",
                                            "content": img1
                                        },
                                    "linkedSsecEQAs":
                                        [
                                            {
                                                "description": "EQA test 4",
                                                "ssecEQA": {
                                                    "code": "12"
                                                }
                                            }
                                        ]
                                }
                            }
                        ]
                    }
                ]
            },

        }

        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_THREE.payload(), p3)

    def test_AddRunInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.crid = 1

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.crid = {"two"}

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.crid = ["three"]

        TestCourseRunsModels.ADD_RUN_INFO_ONE.crid = "CRID 1"
        TestCourseRunsModels.ADD_RUN_INFO_TWO.crid = "CRID 2"
        TestCourseRunsModels.ADD_RUN_INFO_THREE.crid = "CRID 3"

        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_ONE._crid,
                         TestCourseRunsModels.ADD_RUN_INFO_ONE.crid)
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_TWO._crid, "CRID 2")
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_TWO._crid,
                         TestCourseRunsModels.ADD_RUN_INFO_TWO.crid)
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_THREE._crid, "CRID 3")
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_THREE._crid,
                         TestCourseRunsModels.ADD_RUN_INFO_THREE.crid)

    def test_AddRunInfo_set_sequence_number(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.sequence_number = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.sequence_number = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.sequence_number = ["seq number"]

    def test_AddRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.opening_registration_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.opening_registration_date = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.opening_registration_date = 123

    def test_AddRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.closing_registration_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.closing_registration_date = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.closing_registration_date = 123

    def test_AddRunInfo_set_course_dates_start(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.course_start_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.course_start_date = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.course_start_date = 123

    def test_AddRunInfo_set_course_dates_end(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.course_end_date = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.course_end_date = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.course_end_date = 123

    def test_AddRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.schedule_info_type_code = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.schedule_info_type_code = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.schedule_info_type_code = "123123"

    def test_AddRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.schedule_info_type_description = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.schedule_info_type_description = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.schedule_info_type_description = "valid but still not implemented"

    def test_AddRunInfo_set_schedule_info(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.schedule_info = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.schedule_info = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.schedule_info = "valid but still not implemented"

    def test_AddRunInfo_set_venue_block(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.block = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.block = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.block = "valid but still not implemented"

    def test_AddRunInfo_set_venue_street(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.street = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.street = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.street = "valid but still not implemented"

    def test_AddRunInfo_set_venue_floor(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.floor = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.floor = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.floor = "valid but still not implemented"

    def test_AddRunInfo_set_venue_unit(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.unit = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.unit = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.unit = "valid but still not implemented"

    def test_AddRunInfo_set_venue_building(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.building = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.building = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.building = "valid but still not implemented"

    def test_AddRunInfo_set_venue_postal_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.postal_code = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.postal_code = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.postal_code = "123456"

    def test_AddRunInfo_set_venue_room(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.room = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.room = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.room = "123456"

    def test_AddRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.wheel_chair_access = "Yess"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.wheel_chair_access = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.wheel_chair_access = "Yes"

    def test_AddRunInfo_set_intake_size(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.intake_size = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.intake_size = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.intake_size = 12

    def test_AddRunInfo_set_threshold(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.threshold = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.threshold = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.threshold = 12

    def test_AddRunInfo_set_registered_user_count(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.registered_user_count = "1"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.registered_user_count = "2232131"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.registered_user_count = 12

    def test_AddRunInfo_set_mode_of_training(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.mode_of_training = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.mode_of_training = "One"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.mode_of_training = "1"

    def test_AddRunInfo_set_course_admin_email(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.course_admin_email = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.course_admin_email = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.course_admin_email = "email@email.com"

    def test_AddRunInfo_set_course_vacancy_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.course_vacancy = Vacancy.LIMITED_VACANCY

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.course_vacancy = Vacancy.FULL

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.course_vacancy = Vacancy.AVAILABLE

    def test_AddRunInfo_set_file_name(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.file_name = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.file_name = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.file_name = "Name"

    def test_AddRunInfo_set_file_content(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.file_content = b"image"

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.file_content = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.file_content = "img"

    def test_AddRunInfo_set_sessions(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.sessions = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.sessions = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.sessions = ["session"]

    def test_AddRunInfo_add_session(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_session({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.add_session("session")

    def test_AddRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.linked_course_run_trainers = 1

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.linked_course_run_trainers = {"two"}

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.linked_course_run_trainers = ["trainer"]

    def test_AddRunInfo_add_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_linkCourseRunTrainer(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.add_linkCourseRunTrainer({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.add_linkCourseRunTrainer("trainer")
