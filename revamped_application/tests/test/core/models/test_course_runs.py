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

from revamped_application.core.models.course_runs import (RunSessionEditInfo, RunSessionAddInfo, RunTrainerEditInfo,
                                                          RunTrainerAddInfo, EditRunInfo, DeleteRunInfo,
                                                          AddRunIndividualInfo, AddRunInfo)
from revamped_application.tests.test.resources.definitions import RESOURCES_PATH


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
    MODE_OF_TRAINING_ONE = "2"
    MODE_OF_TRAINING_TWO = "8"
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
    VENUE_WHEELCHAIR_ACCESS_ONE = "Yes"
    VENUE_WHEELCHAIR_ACCESS_TWO = "No"
    VENUE_PRIMARY_VENUE_ACCESS_ONE = "Yes"
    VENUE_PRIMARY_VENUE_ACCESS_TWO = "No"
    INTAKE_SIZE_ONE = 20
    INTAKE_SIZE_TWO = 50
    THRESHOLD_ONE = 50
    THRESHOLD_TWO = 100
    REGISTERED_USER_COUNT_ONE = 10
    REGISTERED_USER_COUNT_TWO = 20
    COURSE_VACANCY_CODE_ONE = "A"
    COURSE_VACANCY_CODE_TWO = "F"
    COURSE_VACANCY_DESCRIPTION_ONE = "Available"
    COURSE_VACANCY_DESCRIPTION_TWO = "Full"
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
    ID_TYPE_CODE_ONE = "SB"
    ID_TYPE_CODE_TWO = "FP"
    ID_TYPE_DESCRIPTION_ONE = "Singapore Blue Identification Card"
    ID_TYPE_DESCRIPTION_TWO = "Foreign Passport"
    ROLES_ONE = [
        {
            "id": 1,
            "description": "Trainer"
        }
    ]
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
    IN_TRAINING_PROVIDER_PROFILE_ONE = "Yes"
    IN_TRAINING_PROVIDER_PROFILE_TWO = "No"
    DOMAIN_AREA_OF_PRACTICE_ONE = "Testing Management in Computer Application and Diploma in Computer Application"
    DOMAIN_AREA_OF_PRACTICE_TWO = "Change Management in Computer Application and Diploma in Computer Application"
    EXPERIENCE_ONE = "Testing ABC"
    EXPERIENCE_TWO = "Changing ABC"
    LINKEDIN_ONE = "https://sg.linkedin.com/company/linkedin/abc"
    LINKEDIN_TWO = "https://sg.linkedin.com/company/linkedin/def"
    SALUTATION_ID_ONE = 1
    SALUTATION_ID_TWO = 2
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

    LINKED_SSEC_EQAS_ONE = [
        {
            "description": "EQA test 4",
            "ssecEQA": {
                "code": "12"
            }
        }
    ]
    LINKED_SSEC_EQAS_TWO = [
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
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_session_id(TestCourseRunsModels.SESSION_ID_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startDate(TestCourseRunsModels.START_DATE_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endDate(TestCourseRunsModels.END_DATE_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startTime(TestCourseRunsModels.START_TIME_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endTime(TestCourseRunsModels.END_TIME_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_street(TestCourseRunsModels.VENUE_STREET_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_postalCode(TestCourseRunsModels.VENUE_POSTAL_CODE_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_room(TestCourseRunsModels.VENUE_ROOM_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_primaryVenue(
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_ONE)

        # set up third instance
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE = RunSessionEditInfo()
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_session_id(TestCourseRunsModels.SESSION_ID_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startDate(TestCourseRunsModels.START_DATE_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endDate(TestCourseRunsModels.END_DATE_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startTime(TestCourseRunsModels.START_TIME_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endTime(TestCourseRunsModels.END_TIME_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_street(TestCourseRunsModels.VENUE_STREET_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_postalCode(
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_room(TestCourseRunsModels.VENUE_ROOM_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_primaryVenue(
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_TWO)

    def __set_up_run_session_add(self):
        # set up first instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE = RunSessionAddInfo()

        # set up second instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO = RunSessionAddInfo()
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_session_id(TestCourseRunsModels.SESSION_ID_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startDate(TestCourseRunsModels.START_DATE_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endDate(TestCourseRunsModels.END_DATE_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startTime(TestCourseRunsModels.START_TIME_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endTime(TestCourseRunsModels.END_TIME_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_street(TestCourseRunsModels.VENUE_STREET_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_postalCode(TestCourseRunsModels.VENUE_POSTAL_CODE_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_room(TestCourseRunsModels.VENUE_ROOM_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_primaryVenue(
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_ONE)

        # set up third instance
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE = RunSessionAddInfo()
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_session_id(TestCourseRunsModels.SESSION_ID_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startDate(TestCourseRunsModels.START_DATE_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endDate(TestCourseRunsModels.END_DATE_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startTime(TestCourseRunsModels.START_TIME_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endTime(TestCourseRunsModels.END_TIME_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_street(TestCourseRunsModels.VENUE_STREET_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_postalCode(
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_room(TestCourseRunsModels.VENUE_ROOM_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_primaryVenue(
            TestCourseRunsModels.VENUE_PRIMARY_VENUE_ACCESS_TWO)

    def __set_up_run_trainer_edit(self):
        # set up first instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE = RunTrainerEditInfo()

        # set up second instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO = RunTrainerEditInfo()
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_code(TestCourseRunsModels.TRAINER_TYPE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_description(
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_indexNumber(TestCourseRunsModels.INDEX_NUMBER_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_id(TestCourseRunsModels.ID_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_name(TestCourseRunsModels.NAME_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_email(TestCourseRunsModels.EMAIL_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idNumber(TestCourseRunsModels.ID_NUMBER_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idType(TestCourseRunsModels.ID_TYPE_CODE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_roles(TestCourseRunsModels.ROLES_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_inTrainingProviderProfile(
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_domainAreaOfPractice(
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_experience(TestCourseRunsModels.EXPERIENCE_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_linkedInURL(TestCourseRunsModels.LINKEDIN_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_salutationId(TestCourseRunsModels.SALUTATION_ID_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_photo_name(TestCourseRunsModels.FILE_NAME_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_photo_content(TestCourseRunsModels.FILE_CONTENT_ONE)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_ONE[0])

        # set up third instance
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE = RunTrainerEditInfo()
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_code(TestCourseRunsModels.TRAINER_TYPE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_description(
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_indexNumber(TestCourseRunsModels.INDEX_NUMBER_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_id(TestCourseRunsModels.ID_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_name(TestCourseRunsModels.NAME_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_email(TestCourseRunsModels.EMAIL_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idNumber(TestCourseRunsModels.ID_NUMBER_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idType(TestCourseRunsModels.ID_TYPE_CODE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_inTrainingProviderProfile(
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_domainAreaOfPractice(
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_experience(TestCourseRunsModels.EXPERIENCE_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_linkedInURL(TestCourseRunsModels.LINKEDIN_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_salutationId(TestCourseRunsModels.SALUTATION_ID_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_photo_name(TestCourseRunsModels.FILE_NAME_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_photo_content(TestCourseRunsModels.FILE_CONTENT_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[1])

    def __set_up_run_trainer_add(self):
        # set up first instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE = RunTrainerAddInfo()

        # set up second instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO = RunTrainerAddInfo()
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_code(TestCourseRunsModels.TRAINER_TYPE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_description(
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_indexNumber(TestCourseRunsModels.INDEX_NUMBER_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_id(TestCourseRunsModels.ID_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_name(TestCourseRunsModels.NAME_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_email(TestCourseRunsModels.EMAIL_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idNumber(TestCourseRunsModels.ID_NUMBER_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idType(TestCourseRunsModels.ID_TYPE_CODE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_roles(TestCourseRunsModels.ROLES_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_inTrainingProviderProfile(
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_domainAreaOfPractice(
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_experience(TestCourseRunsModels.EXPERIENCE_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_linkedInURL(TestCourseRunsModels.LINKEDIN_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_salutationId(TestCourseRunsModels.SALUTATION_ID_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_name(TestCourseRunsModels.FILE_NAME_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_content(TestCourseRunsModels.FILE_CONTENT_ONE)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_ONE[0])

        # set up third instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE = RunTrainerAddInfo()
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_code(TestCourseRunsModels.TRAINER_TYPE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_description(
            TestCourseRunsModels.TRAINER_TYPE_DESCRIPTION_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_indexNumber(TestCourseRunsModels.INDEX_NUMBER_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_id(TestCourseRunsModels.ID_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_name(TestCourseRunsModels.NAME_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_email(TestCourseRunsModels.EMAIL_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idNumber(TestCourseRunsModels.ID_NUMBER_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idType(TestCourseRunsModels.ID_TYPE_CODE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_inTrainingProviderProfile(
            TestCourseRunsModels.IN_TRAINING_PROVIDER_PROFILE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_domainAreaOfPractice(
            TestCourseRunsModels.DOMAIN_AREA_OF_PRACTICE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_experience(TestCourseRunsModels.EXPERIENCE_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_linkedInURL(TestCourseRunsModels.LINKEDIN_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_salutationId(TestCourseRunsModels.SALUTATION_ID_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_name(TestCourseRunsModels.FILE_NAME_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_content(TestCourseRunsModels.FILE_CONTENT_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(TestCourseRunsModels.LINKED_SSEC_EQAS_TWO[1])

    def __set_up_run_info_edit(self):
        # set up first instance
        TestCourseRunsModels.EDIT_RUN_INFO_ONE = EditRunInfo()

        # set up second instance
        TestCourseRunsModels.EDIT_RUN_INFO_TWO = EditRunInfo()
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_crid(TestCourseRunsModels.SESSION_ID_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sequence_number(TestCourseRunsModels.SEQUENCE_NUMBER_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_opening(
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_closing(
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_start(TestCourseRunsModels.COURSE_DATE_START_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_end(TestCourseRunsModels.COURSE_DATE_END_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_code(TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_description(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfo(TestCourseRunsModels.SCHEDULE_INFO)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_street(TestCourseRunsModels.VENUE_STREET_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_postalCode(TestCourseRunsModels.VENUE_POSTAL_CODE_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_room(TestCourseRunsModels.VENUE_ROOM_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_intakeSize(TestCourseRunsModels.INTAKE_SIZE_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_threshold(TestCourseRunsModels.THRESHOLD_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registeredUserCount(TestCourseRunsModels.REGISTERED_USER_COUNT_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseAdminEmail(TestCourseRunsModels.EMAIL_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_code(TestCourseRunsModels.COURSE_VACANCY_CODE_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_description(
            TestCourseRunsModels.COURSE_VACANCY_DESCRIPTION_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_Name(TestCourseRunsModels.FILE_NAME_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_content(TestCourseRunsModels.FILE_CONTENT_ONE)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sessions([
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ])
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_linkCourseRunTrainer([
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ])

        # set up third instance
        TestCourseRunsModels.EDIT_RUN_INFO_THREE = EditRunInfo()
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_crid(TestCourseRunsModels.SESSION_ID_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sequence_number(TestCourseRunsModels.SEQUENCE_NUMBER_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_opening(
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_closing(
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_start(TestCourseRunsModels.COURSE_DATE_START_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_end(TestCourseRunsModels.COURSE_DATE_END_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_code(TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_description(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfo(TestCourseRunsModels.SCHEDULE_INFO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_street(TestCourseRunsModels.VENUE_STREET_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_postalCode(TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_room(TestCourseRunsModels.VENUE_ROOM_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_intakeSize(TestCourseRunsModels.INTAKE_SIZE_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_threshold(TestCourseRunsModels.THRESHOLD_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registeredUserCount(TestCourseRunsModels.REGISTERED_USER_COUNT_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseAdminEmail(TestCourseRunsModels.EMAIL_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_code(TestCourseRunsModels.COURSE_VACANCY_CODE_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_description(
            TestCourseRunsModels.COURSE_VACANCY_DESCRIPTION_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_Name(TestCourseRunsModels.FILE_NAME_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_content(TestCourseRunsModels.FILE_CONTENT_TWO)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sessions([
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ])
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_linkCourseRunTrainer([
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ])

    def __set_up_run_info_delete(self):
        # set up first instance
        TestCourseRunsModels.DELETE_RUN_INFO_ONE = DeleteRunInfo()

        # set up second instance
        TestCourseRunsModels.DELETE_RUN_INFO_TWO = DeleteRunInfo()
        TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_crid(TestCourseRunsModels.SESSION_ID_ONE)

    def __set_up_individual_run_info_add(self):
        # set up first instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE = AddRunIndividualInfo()

        # set up second instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO = AddRunIndividualInfo()
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sequence_number(TestCourseRunsModels.SEQUENCE_NUMBER_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_opening(
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_closing(
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_start(
            TestCourseRunsModels.COURSE_DATE_START_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_end(TestCourseRunsModels.COURSE_DATE_END_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_code(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_description(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfo(TestCourseRunsModels.SCHEDULE_INFO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_street(TestCourseRunsModels.VENUE_STREET_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_postalCode(
            TestCourseRunsModels.VENUE_POSTAL_CODE_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_room(TestCourseRunsModels.VENUE_ROOM_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_intakeSize(TestCourseRunsModels.INTAKE_SIZE_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_threshold(TestCourseRunsModels.THRESHOLD_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registeredUserCount(
            TestCourseRunsModels.REGISTERED_USER_COUNT_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseAdminEmail(TestCourseRunsModels.EMAIL_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_code(
            TestCourseRunsModels.COURSE_VACANCY_CODE_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_description(
            TestCourseRunsModels.COURSE_VACANCY_DESCRIPTION_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_Name(TestCourseRunsModels.FILE_NAME_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_content(TestCourseRunsModels.FILE_CONTENT_ONE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sessions([
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ])
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_linkCourseRunTrainer([
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ])

        # set up third instance
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE = AddRunIndividualInfo()
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sequence_number(TestCourseRunsModels.SEQUENCE_NUMBER_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_opening(
            TestCourseRunsModels.REGISTRATION_DATE_OPENING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_closing(
            TestCourseRunsModels.REGISTRATION_DATE_CLOSING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_start(
            TestCourseRunsModels.COURSE_DATE_START_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_end(TestCourseRunsModels.COURSE_DATE_END_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_code(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_CODE)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_description(
            TestCourseRunsModels.SCHEDULE_INFO_TYPE_DESCRIPTION)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfo(TestCourseRunsModels.SCHEDULE_INFO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_block(TestCourseRunsModels.VENUE_BLOCK_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_street(TestCourseRunsModels.VENUE_STREET_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_floor(TestCourseRunsModels.VENUE_FLOOR_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_unit(TestCourseRunsModels.VENUE_UNIT_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_building(TestCourseRunsModels.VENUE_BUILDING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_postalCode(
            TestCourseRunsModels.VENUE_POSTAL_CODE_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_room(TestCourseRunsModels.VENUE_ROOM_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_wheelChairAccess(
            TestCourseRunsModels.VENUE_WHEELCHAIR_ACCESS_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_intakeSize(TestCourseRunsModels.INTAKE_SIZE_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_threshold(TestCourseRunsModels.THRESHOLD_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registeredUserCount(
            TestCourseRunsModels.REGISTERED_USER_COUNT_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_modeOfTraining(TestCourseRunsModels.MODE_OF_TRAINING_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseAdminEmail(TestCourseRunsModels.EMAIL_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_code(
            TestCourseRunsModels.COURSE_VACANCY_CODE_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_description(
            TestCourseRunsModels.COURSE_VACANCY_DESCRIPTION_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_Name(TestCourseRunsModels.FILE_NAME_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_content(TestCourseRunsModels.FILE_CONTENT_TWO)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sessions([
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO
        ])
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_linkCourseRunTrainer([
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO,
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO
        ])

    def __set_up_run_info_add(self):
        # set up first instance
        TestCourseRunsModels.ADD_RUN_INFO_ONE = AddRunInfo()

        # set up second instance
        TestCourseRunsModels.ADD_RUN_INFO_TWO = AddRunInfo()
        TestCourseRunsModels.ADD_RUN_INFO_TWO.set_crid(TestCourseRunsModels.SESSION_ID_ONE)
        TestCourseRunsModels.ADD_RUN_INFO_TWO.add_run(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE)

        # set up third instance
        TestCourseRunsModels.ADD_RUN_INFO_THREE = AddRunInfo()
        TestCourseRunsModels.ADD_RUN_INFO_THREE.set_crid(TestCourseRunsModels.SESSION_ID_TWO)
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
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_session_id(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_session_id([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_session_id(123.22)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_session_id("Session 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_session_id("Session 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_session_id("Session 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._sessionId, "Session 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._sessionId, "Session 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._sessionId, "Session 3")

    def test_RunSessionEditInfo_set_start_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_startDate(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startDate(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startDate([datetime.datetime.now()])

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_startDate(dt1)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startDate(dt2)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startDate(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startDate, dt3)

    def test_RunSessionEditInfo_set_end_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_endDate(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endDate(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endDate([datetime.datetime.now()])

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_endDate(dt1)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endDate(dt2)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endDate(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endDate, dt3)

    def test_RunSessionEditInfo_set_start_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_startTime(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startTime(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startTime([datetime.datetime.now()])

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_startTime(dt1)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_startTime(dt2)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_startTime(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._startTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._startTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._startTime, dt3)

    def test_RunSessionEditInfo_set_end_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_endTime(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endTime(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endTime([datetime.datetime.now()])

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_endTime(dt1)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_endTime(dt2)
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_endTime(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._endTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._endTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._endTime, dt3)

    def test_RunSessionEditInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_modeOfTraining("10")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_modeOfTraining(2)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_modeOfTraining([8])

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_modeOfTraining("9")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_modeOfTraining("5")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_modeOfTraining("7")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._modeOfTraining, "9")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._modeOfTraining, "5")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._modeOfTraining, "7")

    def test_RunSessionEditInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_block(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_block([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_block(123.22)

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_block("Block 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_block("Block 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_block("Block 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_block, "Block 3")

    def test_RunSessionEditInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_street(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_street([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_street({
                "location": {
                    "street": "street"
                }
            })

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_street("Street 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_street("Street 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_street("Street 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_street, "Street 3")

    def test_RunSessionEditInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_floor(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_floor([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_floor({"floor"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_floor("Floor 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_floor("Floor 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_floor("Floor 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_floor, "Floor 3")

    def test_RunSessionEditInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_unit(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_unit([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_unit({"unit"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_unit("Unit 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_unit("Unit 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_unit("Unit 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_unit, "Unit 3")

    def test_RunSessionEditInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_building(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_building([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_building({"building"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_building("Building 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_building("Building 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_building("Building 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_building, "Building 3")

    def test_RunSessionEditInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_postalCode(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_postalCode([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_postalCode({"postal_code"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_postalCode("949494")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_postalCode("959595")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_postalCode("969696")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_postalCode, "949494")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_postalCode, "959595")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_postalCode, "969696")

    def test_RunSessionEditInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_room(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_room([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_room({"room"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_room("Room 1")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_room("Room 2")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_room("Room 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_room, "Room 3")

    def test_RunSessionEditInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_wheelChairAccess(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_wheelChairAccess([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_wheelChairAccess({"wheel_chair_access"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_wheelChairAccess("Yes")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_wheelChairAccess("No")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_wheelChairAccess("Select a value")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_wheelChairAccess, True)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_wheelChairAccess, False)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_wheelChairAccess, None)

    def test_RunSessionEditInfo_set_venue_primary_venue(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_primaryVenue(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_primaryVenue([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_primaryVenue({"primary_venue"})

        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE.set_venue_primaryVenue("Yes")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO.set_venue_primaryVenue("No")
        TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE.set_venue_primaryVenue("Select a value")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE._venue_primaryVenue, True)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO._venue_primaryVenue, False)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE._venue_primaryVenue, None)

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
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_session_id(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_session_id([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_session_id(123.22)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_session_id("Session 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_session_id("Session 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_session_id("Session 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._sessionId, "Session 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._sessionId, "Session 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._sessionId, "Session 3")

    def test_RunSessionAddInfo_set_start_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_startDate(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startDate(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startDate([datetime.datetime.now()])

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_startDate(dt1)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startDate(dt2)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startDate(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startDate, dt3)

    def test_RunSessionAddInfo_set_end_date(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_endDate(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endDate(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endDate([datetime.datetime.now()])

        dt1 = datetime.date(2000, 12, 31)
        dt2 = datetime.date(2001, 12, 31)
        dt3 = datetime.date(2002, 12, 31)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_endDate(dt1)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endDate(dt2)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endDate(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endDate, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endDate, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endDate, dt3)

    def test_RunSessionAddInfo_set_start_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_startTime(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startTime(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startTime([datetime.datetime.now()])

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_startTime(dt1)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_startTime(dt2)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_startTime(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._startTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._startTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._startTime, dt3)

    def test_RunSessionAddInfo_set_end_time(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_endTime(31122024)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endTime(112.2023)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endTime([datetime.datetime.now()])

        dt1 = datetime.time(12, 30)
        dt2 = datetime.time(13, 30)
        dt3 = datetime.time(14, 30)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_endTime(dt1)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_endTime(dt2)
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_endTime(dt3)

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._endTime, dt1)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._endTime, dt2)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._endTime, dt3)

    def test_RunSessionAddInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_modeOfTraining("10")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_modeOfTraining(2)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_modeOfTraining([8])

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_modeOfTraining("9")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_modeOfTraining("5")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_modeOfTraining("7")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._modeOfTraining, "9")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._modeOfTraining, "5")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._modeOfTraining, "7")

    def test_RunSessionAddInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_block(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_block([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_block(123.22)

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_block("Block 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_block("Block 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_block("Block 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_block, "Block 3")

    def test_RunSessionAddInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_street(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_street([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_street({
                "location": {
                    "street": "street"
                }
            })

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_street("Street 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_street("Street 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_street("Street 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_street, "Street 3")

    def test_RunSessionAddInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_floor(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_floor([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_floor({"floor"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_floor("Floor 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_floor("Floor 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_floor("Floor 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_floor, "Floor 3")

    def test_RunSessionAddInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_unit(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_unit([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_unit({"unit"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_unit("Unit 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_unit("Unit 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_unit("Unit 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_unit, "Unit 3")

    def test_RunSessionAddInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_building(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_building([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_building({"building"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_building("Building 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_building("Building 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_building("Building 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_building, "Building 3")

    def test_RunSessionAddInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_postalCode(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_postalCode([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_postalCode({"postal_code"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_postalCode("949494")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_postalCode("959595")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_postalCode("969696")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_postalCode, "949494")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_postalCode, "959595")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_postalCode, "969696")

    def test_RunSessionAddInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_room(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_room([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_room({"room"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_room("Room 1")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_room("Room 2")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_room("Room 3")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_room, "Room 3")

    def test_RunSessionAddInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_wheelChairAccess(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_wheelChairAccess([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_wheelChairAccess({"wheel_chair_access"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_wheelChairAccess("Yes")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_wheelChairAccess("No")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_wheelChairAccess("Select a value")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_wheelChairAccess, True)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_wheelChairAccess, False)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_wheelChairAccess, None)

    def test_RunSessionAddInfo_set_venue_primary_venue(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_primaryVenue(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_primaryVenue([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_primaryVenue({"primary_venue"})

        TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE.set_venue_primaryVenue("Yes")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO.set_venue_primaryVenue("No")
        TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE.set_venue_primaryVenue("Select a value")

        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_ONE._venue_primaryVenue, True)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_TWO._venue_primaryVenue, False)
        self.assertEqual(TestCourseRunsModels.RUN_SESSION_ADD_INFO_THREE._venue_primaryVenue, None)

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
        self.maxDiff = 99999999

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
                        "id": 1,
                        "description": "Trainer"
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
                        "id": 1,
                        "description": "Trainer"
                    },
                    {
                        "id": 2,
                        "description": "Assessor"
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
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_type_code(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_code([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_code(123.22)

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_type_code("1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_code("2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_code("3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_code, "1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_code, "2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_code, "3")

    def test_RunTrainerEditInfo_set_trainer_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_type_description(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_description([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_description(123.22)

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_type_description("Trainer Code 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_type_description("Trainer Code 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_type_description("Trainer Code 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._trainerType_description, "Trainer Code 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._trainerType_description, "Trainer Code 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._trainerType_description, "Trainer Code 3")

    def test_RunTrainerEditInfo_set_index_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_indexNumber("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_indexNumber("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_indexNumber({"one"})

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_indexNumber(1)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_indexNumber(2)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_indexNumber(3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._indexNumber, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._indexNumber, 2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._indexNumber, 3)

    def test_RunTrainerEditInfo_set_trainer_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_id(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_id({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_id(["three"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_id("Trainer ID 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_id("Trainer ID 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_id("Trainer ID 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._id, "Trainer ID 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._id, "Trainer ID 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._id, "Trainer ID 3")

    def test_RunTrainerEditInfo_set_trainer_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_name(["three"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_name("Trainer Name 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_name("Trainer Name 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_name("Trainer Name 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._name, "Trainer Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._name, "Trainer Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._name, "Trainer Name 3")

    def test_RunTrainerEditInfo_set_trainer_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_email(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_email({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_email(["three"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_email("Trainer Email 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_email("Trainer Email 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_email("Trainer Email 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._email, "Trainer Email 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._email, "Trainer Email 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._email, "Trainer Email 3")

    def test_RunTrainerEditInfo_set_trainer_id_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_idNumber(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idNumber({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idNumber(["three"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_idNumber("Trainer ID Number 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idNumber("Trainer ID Number 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idNumber("Trainer ID Number 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idNumber, "Trainer ID Number 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idNumber, "Trainer ID Number 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idNumber, "Trainer ID Number 3")

    def test_RunTrainerEditInfo_set_trainer_id_type(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_idType("SBBBBBBB")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idType({"OT"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idType(["FP"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_idType("OT")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idType("SP")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_idType("SB")

        # assert both the code and the description
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_code, "OT")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_code, "SP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idType_code, "SB")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_description, "Others")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_description,
                         "Singapore Pink Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._idType_description,
                         "Singapore Blue Identification Card")

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_idType("SO")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_idType("FP")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_code, "SO")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_code, "FP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._idType_description, "Fin/Work Permit")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._idType_description, "Foreign Passport")

    def test_RunTrainerEditInfo_set_trainer_roles(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_roles(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_roles({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_roles("three")

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_trainer_roles(TestCourseRunsModels.ROLES_ONE)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE)

    def test_RunTrainerEditInfo_add_trainer_role(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_trainer_role(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_trainer_role({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_trainer_role("three")

        # clear out RUN_TRAINER_EDIT_INFO_TWO"s and RUN_TRAINER_EDIT_INFO_THREE"s roles
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles = []
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles = []
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles, [])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles, [])

        # add in the roles
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_trainer_role(TestCourseRunsModels.ROLES_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_trainer_role(TestCourseRunsModels.ROLES_TWO[1])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_trainer_role(TestCourseRunsModels.ROLES_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_trainer_role(TestCourseRunsModels.ROLES_TWO[1])
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_trainer_role(TestCourseRunsModels.ROLES_ONE[0])

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE)

    def test_RunTrainerEditInfo_set_in_training_provider_profile(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_inTrainingProviderProfile("Yess")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_inTrainingProviderProfile(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_inTrainingProviderProfile("n0")

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_inTrainingProviderProfile("Yes")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_inTrainingProviderProfile("Select a value")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_inTrainingProviderProfile("No")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._inTrainingProviderProfile, True)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._inTrainingProviderProfile, None)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._inTrainingProviderProfile, False)

    def test_RunTrainerEditInfo_set_domain_area_of_practice(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_domainAreaOfPractice(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_domainAreaOfPractice({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_domainAreaOfPractice(["domain area 123"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_domainAreaOfPractice("Domain 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_domainAreaOfPractice("Domain 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_domainAreaOfPractice("Domain 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._domainAreaOfPractice,
                         "Domain 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._domainAreaOfPractice,
                         "Domain 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._domainAreaOfPractice,
                         "Domain 3")

    def test_RunTrainerEditInfo_set_experience(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_experience(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_experience({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_experience(["experience 123"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_experience("Experience 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_experience("Experience 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_experience("Experience 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._experience, "Experience 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._experience, "Experience 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._experience, "Experience 3")

    def test_RunTrainerEditInfo_set_linked_in_url(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_linkedInURL(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_linkedInURL({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_linkedInURL(["linkedin url 123"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_linkedInURL("LinkedIn URL 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_linkedInURL("LinkedIn URL 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_linkedInURL("LinkedIn URL 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._linkedInURL, "LinkedIn URL 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedInURL, "LinkedIn URL 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedInURL, "LinkedIn URL 3")

    def test_RunTrainerEditInfo_set_salutation_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_salutationId("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_salutationId({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_salutationId(3.3333333)

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_salutationId(1)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_salutationId(3)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_salutationId(5)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._salutationId, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._salutationId, 3)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._salutationId, 5)

    def test_RunTrainerEditInfo_set_photo_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_name(["photo name.jpg"])

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_name("Photo Name 1")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_photo_name("Photo Name 2")
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_photo_name("Photo Name 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_name, "Photo Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_name, "Photo Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_name, "Photo Name 3")

    def test_RunTrainerEditInfo_set_photo_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_content(b"image")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_content({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_content(["photo"])

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

            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.set_photo_content(T1)
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.set_photo_content(T2)
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.set_photo_content(T3)

            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._photo_content, T1)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._photo_content, T2)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._photo_content, T3)

    def test_RunTrainerEditInfo_add_linked_ssec_eqa(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA("three")

        EQA1 = {
            "description": "EQA 1",
            "ssecEQA": {
                "code": "1"
            }
        }

        EQA2 = {
            "description": "EQA test 21",
            "ssecEQA": {
                "code": "22"
            }
        }

        EQA3 = {
            "description": "EQA test 12",
            "ssecEQA": {
                "code": "23"
            }
        }

        # reset the linked SSEC EQAs in RUN_TRAINER_EDIT_INFO_TWO and RUN_TRAINER_EDIT_INFO_THREE
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedSsecEQAs = []
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedSsecEQAs = []

        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE.add_linkedSsecEQA(EQA1)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO.add_linkedSsecEQA(EQA2)
        TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE.add_linkedSsecEQA(EQA3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_ONE._linkedSsecEQAs, [EQA1])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_TWO._linkedSsecEQAs, [EQA2])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_EDIT_INFO_THREE._linkedSsecEQAs, [EQA3])

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
        self.maxDiff = 99999999

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
                        "id": 1,
                        "description": "Trainer"
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
                        "id": 1,
                        "description": "Trainer"
                    },
                    {
                        "id": 2,
                        "description": "Assessor"
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
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_type_code(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_code([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_code(123.22)

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_type_code("1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_code("2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_code("3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_code, "1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_code, "2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_code, "3")

    def test_RunTrainerAddInfo_set_trainer_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_type_description(123)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_description([12323])

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_description(123.22)

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_type_description("Trainer Code 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_type_description("Trainer Code 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_type_description("Trainer Code 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._trainerType_description, "Trainer Code 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._trainerType_description, "Trainer Code 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._trainerType_description, "Trainer Code 3")

    def test_RunTrainerAddInfo_set_index_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_indexNumber("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_indexNumber("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_indexNumber({"one"})

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_indexNumber(1)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_indexNumber(2)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_indexNumber(3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._indexNumber, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._indexNumber, 2)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._indexNumber, 3)

    def test_RunTrainerAddInfo_set_trainer_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_id(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_id({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_id(["three"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_id("Trainer ID 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_id("Trainer ID 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_id("Trainer ID 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._id, "Trainer ID 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._id, "Trainer ID 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._id, "Trainer ID 3")

    def test_RunTrainerAddInfo_set_trainer_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_name(["three"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_name("Trainer Name 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_name("Trainer Name 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_name("Trainer Name 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._name, "Trainer Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._name, "Trainer Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._name, "Trainer Name 3")

    def test_RunTrainerAddInfo_set_trainer_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_email(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_email({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_email(["three"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_email("Trainer Email 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_email("Trainer Email 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_email("Trainer Email 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._email, "Trainer Email 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._email, "Trainer Email 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._email, "Trainer Email 3")

    def test_RunTrainerAddInfo_set_trainer_id_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_idNumber(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idNumber({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idNumber(["three"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_idNumber("Trainer ID Number 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idNumber("Trainer ID Number 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idNumber("Trainer ID Number 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idNumber, "Trainer ID Number 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idNumber, "Trainer ID Number 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idNumber, "Trainer ID Number 3")

    def test_RunTrainerAddInfo_set_trainer_id_type(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_idType("SBBBBBBB")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idType({"OT"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idType(["FP"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_idType("OT")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idType("SP")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_idType("SB")

        # assert both the code and the description
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_code, "OT")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_code, "SP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idType_code, "SB")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_description, "Others")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_description,
                         "Singapore Pink Identification Card")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._idType_description,
                         "Singapore Blue Identification Card")

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_idType("SO")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_idType("FP")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_code, "SO")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_code, "FP")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._idType_description, "Fin/Work Permit")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._idType_description, "Foreign Passport")

    def test_RunTrainerAddInfo_set_trainer_roles(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_roles(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_roles({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_roles("three")

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_trainer_roles(TestCourseRunsModels.ROLES_TWO)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_trainer_roles(TestCourseRunsModels.ROLES_ONE)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE)

    def test_RunTrainerAddInfo_add_trainer_role(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_trainer_role(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_trainer_role({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_trainer_role("three")

        # clear out RUN_TRAINER_ADD_INFO_TWO"s and RUN_TRAINER_ADD_INFO_THREE"s roles
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles = []
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles = []
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles, [])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles, [])

        # add in the roles
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_trainer_role(TestCourseRunsModels.ROLES_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_trainer_role(TestCourseRunsModels.ROLES_TWO[1])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_trainer_role(TestCourseRunsModels.ROLES_TWO[0])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_trainer_role(TestCourseRunsModels.ROLES_TWO[1])
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_trainer_role(TestCourseRunsModels.ROLES_ONE[0])

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._roles, TestCourseRunsModels.ROLES_TWO)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._roles, TestCourseRunsModels.ROLES_ONE)

    def test_RunTrainerAddInfo_set_in_training_provider_profile(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_inTrainingProviderProfile("Yess")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_inTrainingProviderProfile(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_inTrainingProviderProfile("n0")

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_inTrainingProviderProfile("Yes")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_inTrainingProviderProfile("Select a value")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_inTrainingProviderProfile("No")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._inTrainingProviderProfile, True)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._inTrainingProviderProfile, None)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._inTrainingProviderProfile, False)

    def test_RunTrainerAddInfo_set_domain_area_of_practice(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_domainAreaOfPractice(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_domainAreaOfPractice({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_domainAreaOfPractice(["domain area 123"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_domainAreaOfPractice("Domain 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_domainAreaOfPractice("Domain 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_domainAreaOfPractice("Domain 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._domainAreaOfPractice,
                         "Domain 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._domainAreaOfPractice,
                         "Domain 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._domainAreaOfPractice,
                         "Domain 3")

    def test_RunTrainerAddInfo_set_experience(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_experience(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_experience({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_experience(["experience 123"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_experience("Experience 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_experience("Experience 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_experience("Experience 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._experience, "Experience 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._experience, "Experience 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._experience, "Experience 3")

    def test_RunTrainerAddInfo_set_linked_in_url(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_linkedInURL(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_linkedInURL({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_linkedInURL(["linkedin url 123"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_linkedInURL("LinkedIn URL 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_linkedInURL("LinkedIn URL 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_linkedInURL("LinkedIn URL 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._linkedInURL, "LinkedIn URL 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedInURL, "LinkedIn URL 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedInURL, "LinkedIn URL 3")

    def test_RunTrainerAddInfo_set_salutation_id(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_salutationId("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_salutationId({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_salutationId(3.3333333)

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_salutationId(1)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_salutationId(3)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_salutationId(5)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._salutationId, 1)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._salutationId, 3)
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._salutationId, 5)

    def test_RunTrainerAddInfo_set_photo_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_photo_name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_name(["photo name.jpg"])

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_photo_name("Photo Name 1")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_name("Photo Name 2")
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_name("Photo Name 3")

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_name, "Photo Name 1")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_name, "Photo Name 2")
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_name, "Photo Name 3")

    def test_RunTrainerAddInfo_set_photo_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_photo_content(b"image")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_content({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_content(["photo"])

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

            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.set_photo_content(T1)
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.set_photo_content(T2)
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.set_photo_content(T3)

            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._photo_content, T1)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._photo_content, T2)
            self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._photo_content, T3)

    def test_RunTrainerAddInfo_add_linked_ssec_eqa(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_linkedSsecEQA(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA("three")

        EQA1 = {
            "description": "EQA 1",
            "ssecEQA": {
                "code": "1"
            }
        }

        EQA2 = {
            "description": "EQA test 21",
            "ssecEQA": {
                "code": "22"
            }
        }

        EQA3 = {
            "description": "EQA test 12",
            "ssecEQA": {
                "code": "23"
            }
        }

        # reset the linked SSEC EQAs in RUN_TRAINER_ADD_INFO_TWO and RUN_TRAINER_ADD_INFO_THREE
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedSsecEQAs = []
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedSsecEQAs = []

        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE.add_linkedSsecEQA(EQA1)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO.add_linkedSsecEQA(EQA2)
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE.add_linkedSsecEQA(EQA3)

        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE._linkedSsecEQAs, [EQA1])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO._linkedSsecEQAs, [EQA2])
        self.assertEqual(TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE._linkedSsecEQAs, [EQA3])

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
        self.maxDiff = 99999999

        p3 = {
            "course": {
                "courseReferenceNumber": "XX-10000000K-02-TEST 199"  # uen cannot be tested without starting streamlit
            },
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
                                    "id": 1,
                                    "description": "Trainer"
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
                                    "id": 1,
                                    "description": "Trainer"
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
        }

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.payload()

        with self.assertRaises(AttributeError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.payload()

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE.payload(), p3)

    def test_EditRunInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_crid(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_crid({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_crid(["three"])

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_crid("CRID 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_crid("CRID 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_crid("CRID 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._crid, "CRID 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._crid, "CRID 3")

    def test_EditRunInfo_set_sequence_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_sequence_number("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sequence_number("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sequence_number({"one"})

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_sequence_number(1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sequence_number(2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sequence_number(3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sequenceNumber, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sequenceNumber, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sequenceNumber, 3)

    def test_EditRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registrationDates_opening("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_opening("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_opening({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registrationDates_opening(dt1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_opening(dt2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_opening(dt3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_opening, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_opening, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_opening, dt3)

    def test_EditRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registrationDates_closing("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_closing("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_closing({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registrationDates_closing(dt1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registrationDates_closing(dt2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registrationDates_closing(dt3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registrationDates_closing, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registrationDates_closing, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registrationDates_closing, dt3)

    def test_EditRunInfo_set_course_dates_start(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseDates_start("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_start("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_start({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseDates_start(dt1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_start(dt2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_start(dt3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_start, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_start, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_start, dt3)

    def test_EditRunInfo_set_course_dates_end(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseDates_end("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_end("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_end({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseDates_end(dt1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseDates_end(dt2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseDates_end(dt3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseDates_end, dt1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseDates_end, dt2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseDates_end, dt3)

    def test_EditRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfoType_code(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_code({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_code(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfoType_code("1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_code("2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_code("3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_code, "1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_code, "2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_code, "3")

    def test_EditRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfoType_description(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_description({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_description(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfoType_description("Description 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfoType_description("Description 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfoType_description("Description 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfoType_description, "Description 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfoType_description, "Description 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfoType_description,
                         "Description 3")

    def test_EditRunInfo_set_schedule_info(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfo(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfo({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfo(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_scheduleInfo("Schedule Info 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_scheduleInfo("Schedule Info 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_scheduleInfo("Schedule Info 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._scheduleInfo, "Schedule Info 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._scheduleInfo, "Schedule Info 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._scheduleInfo, "Schedule Info 3")

    def test_EditRunInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_block(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_block({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_block(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_block("Block 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_block("Block 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_block("Block 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_block, "Block 3")

    def test_EditRunInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_street(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_street({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_street(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_street("Street 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_street("Street 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_street("Street 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_street, "Street 3")

    def test_EditRunInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_floor(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_floor({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_floor(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_floor("Floor 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_floor("Floor 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_floor("Floor 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_floor, "Floor 3")

    def test_EditRunInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_unit(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_unit({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_unit(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_unit("Unit 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_unit("Unit 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_unit("Unit 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_unit, "Unit 3")

    def test_EditRunInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_building(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_building({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_building(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_building("Building 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_building("Building 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_building("Building 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_building, "Building 3")

    def test_EditRunInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_postalCode(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_postalCode({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_postalCode(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_postalCode("112233")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_postalCode("223344")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_postalCode("334455")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_postalCode, "112233")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_postalCode, "223344")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_postalCode, "334455")

    def test_EditRunInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_room(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_room({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_room(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_room("Room 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_room("Room 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_room("Room 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_room, "Room 3")

    def test_EditRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_wheelChairAccess("Yess")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_wheelChairAccess(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_wheelChairAccess("n0")

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_venue_wheelChairAccess("Yes")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_venue_wheelChairAccess("Select a value")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_venue_wheelChairAccess("No")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._venue_wheelChairAccess, True)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._venue_wheelChairAccess, None)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._venue_wheelChairAccess, False)

    def test_EditRunInfo_set_intake_size(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_intakeSize("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_intakeSize("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_intakeSize({"one"})

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_intakeSize(1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_intakeSize(2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_intakeSize(3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._intakeSize, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._intakeSize, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._intakeSize, 3)

    def test_EditRunInfo_set_threshold(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_threshold("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_threshold("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_threshold({"one"})

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_threshold(1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_threshold(2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_threshold(3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._threshold, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._threshold, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._threshold, 3)

    def test_EditRunInfo_set_registered_user_count(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registeredUserCount("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registeredUserCount("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registeredUserCount({"one"})

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_registeredUserCount(1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_registeredUserCount(2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_registeredUserCount(3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._registeredUserCount, 1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._registeredUserCount, 2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._registeredUserCount, 3)

    def test_EditRunInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_modeOfTraining(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_modeOfTraining("One")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_modeOfTraining({"one"})

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_modeOfTraining("1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_modeOfTraining("2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_modeOfTraining("3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._modeOfTraining, "1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._modeOfTraining, "2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._modeOfTraining, "3")

    def test_EditRunInfo_set_course_admin_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseAdminEmail(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseAdminEmail({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseAdminEmail(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseAdminEmail("Email 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseAdminEmail("Email 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseAdminEmail("Email 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseAdminEmail, "Email 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseAdminEmail, "Email 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseAdminEmail, "Email 3")

    def test_EditRunInfo_set_course_vacancy_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseVacancy_code(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_code({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_code(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseVacancy_code("1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_code("2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_code("3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseVacancy_code, "1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseVacancy_code, "2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseVacancy_code, "3")

    def test_EditRunInfo_set_course_vacancy_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseVacancy_description(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_description({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_description(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_courseVacancy_description("Description 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_courseVacancy_description("Description 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_courseVacancy_description("Description 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._courseVacancy_description, "Description 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._courseVacancy_description, "Description 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._courseVacancy_description, "Description 3")

    def test_EditRunInfo_set_file_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_file_Name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_Name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_Name(3.3333333)

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_file_Name("File Name 1")
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_Name("File Name 2")
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_Name("File Name 3")

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_Name, "File Name 1")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_Name, "File Name 2")
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_Name, "File Name 3")

    def test_EditRunInfo_set_file_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_file_content(b"image")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_content({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_content(["photo"])

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

            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_file_content(T1)
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_file_content(T2)
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_file_content(T3)

            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._file_content, T1)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._file_content, T2)
            self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._file_content, T3)

    def test_EditRunInfo_set_sessions(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_sessions(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sessions({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sessions(3.3333333)

        st1 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO]
        st2 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]
        st3 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_sessions(st1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_sessions(st2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_sessions(st3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._sessions, st1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions, st2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions, st3)

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
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO])
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._sessions,
                         [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE])

    def test_EditRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_linkCourseRunTrainer(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_linkCourseRunTrainer({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_linkCourseRunTrainer(3.3333333)

        cr1 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO]
        cr2 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]
        cr3 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]

        TestCourseRunsModels.EDIT_RUN_INFO_ONE.set_linkCourseRunTrainer(cr1)
        TestCourseRunsModels.EDIT_RUN_INFO_TWO.set_linkCourseRunTrainer(cr2)
        TestCourseRunsModels.EDIT_RUN_INFO_THREE.set_linkCourseRunTrainer(cr3)

        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_ONE._linkCourseRunTrainer, cr1)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_TWO._linkCourseRunTrainer, cr2)
        self.assertEqual(TestCourseRunsModels.EDIT_RUN_INFO_THREE._linkCourseRunTrainer, cr3)

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
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_crid(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_crid({"two"})

        TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_crid("CRID 1")
        TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_crid("CRID 2")

        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.DELETE_RUN_INFO_TWO._crid, "CRID 2")

    def test_DeleteRunInfo_set_sequence_number(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_sequence_number("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_sequence_number("2232131")

    def test_DeleteRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_registrationDates_opening("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_registrationDates_opening("2232131")

    def test_DeleteRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_registrationDates_closing("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_registrationDates_closing("2232131")

    def test_DeleteRunInfo_set_course_dates_start(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_courseDates_start("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_courseDates_start("2232131")

    def test_DeleteRunInfo_set_course_dates_end(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_courseDates_end("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_courseDates_end("2232131")

    def test_DeleteRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_scheduleInfoType_code(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_scheduleInfoType_code({"two"})

    def test_DeleteRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_scheduleInfoType_description(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_scheduleInfoType_description({"two"})

    def test_DeleteRunInfo_set_schedule_info(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_scheduleInfo(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_scheduleInfo({"two"})

    def test_DeleteRunInfo_set_venue_block(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_block(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_block({"two"})

    def test_DeleteRunInfo_set_venue_street(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_street(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_street({"two"})

    def test_DeleteRunInfo_set_venue_floor(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_floor(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_floor({"two"})

    def test_DeleteRunInfo_set_venue_unit(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_unit(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_unit({"two"})

    def test_DeleteRunInfo_set_venue_building(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_building(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_building({"two"})

    def test_DeleteRunInfo_set_venue_postal_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_postalCode(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_postalCode({"two"})

    def test_DeleteRunInfo_set_venue_room(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_room(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_room({"two"})

    def test_DeleteRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_venue_wheelChairAccess("Yess")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_venue_wheelChairAccess(1)

    def test_DeleteRunInfo_set_intake_size(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_intakeSize("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_intakeSize("2232131")

    def test_DeleteRunInfo_set_threshold(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_threshold("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_threshold("2232131")

    def test_DeleteRunInfo_set_registered_user_count(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_registeredUserCount("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_registeredUserCount("2232131")

    def test_DeleteRunInfo_set_mode_of_training(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_modeOfTraining(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_modeOfTraining("One")

    def test_DeleteRunInfo_set_course_admin_email(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_courseAdminEmail(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_courseAdminEmail({"two"})

    def test_DeleteRunInfo_set_course_vacancy_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_courseVacancy_code(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_courseVacancy_code({"two"})

    def test_DeleteRunInfo_set_course_vacancy_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_courseVacancy_description(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_courseVacancy_description({"two"})

    def test_DeleteRunInfo_set_file_name(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_file_Name(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_file_Name({"two"})

    def test_DeleteRunInfo_set_file_content(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_file_content(b"image")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_file_content({"two"})

    def test_DeleteRunInfo_set_sessions(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_sessions(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_sessions({"two"})

    def test_DeleteRunInfo_add_session(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.add_session({"two"})

    def test_DeleteRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_ONE.set_linkCourseRunTrainer(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.DELETE_RUN_INFO_TWO.set_linkCourseRunTrainer({"two"})

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
        self.maxDiff = 99999999

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
                                "id": 1,
                                "description": "Trainer"
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
                                "id": 1,
                                "description": "Trainer"
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
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_crid(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_crid({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_crid(["three"])

    def test_AddRunIndividualInfo_set_sequence_number(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_sequence_number("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sequence_number("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sequence_number({"one"})

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_sequence_number(1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sequence_number(2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sequence_number(3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sequenceNumber, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sequenceNumber, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sequenceNumber, 3)

    def test_AddRunIndividualInfo_set_registration_dates_opening(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registrationDates_opening("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_opening("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_opening({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registrationDates_opening(dt1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_opening(dt2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_opening(dt3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_opening, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_opening, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_opening, dt3)

    def test_AddRunIndividualInfo_set_registration_dates_closing(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registrationDates_closing("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_closing("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_closing({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registrationDates_closing(dt1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registrationDates_closing(dt2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registrationDates_closing(dt3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registrationDates_closing, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registrationDates_closing, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registrationDates_closing, dt3)

    def test_AddRunIndividualInfo_set_course_dates_start(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseDates_start("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_start("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_start({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseDates_start(dt1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_start(dt2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_start(dt3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_start, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_start, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_start, dt3)

    def test_AddRunIndividualInfo_set_course_dates_end(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseDates_end("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_end("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_end({"one"})

        dt1 = datetime.date(2021, 1, 1)
        dt2 = datetime.date(2022, 1, 1)
        dt3 = datetime.date(2023, 1, 1)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseDates_end(dt1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseDates_end(dt2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseDates_end(dt3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseDates_end, dt1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseDates_end, dt2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseDates_end, dt3)

    def test_AddRunIndividualInfo_set_schedule_info_type_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfoType_code(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_code({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_code(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfoType_code("1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_code("2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_code("3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_code, "1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_code, "2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_code, "3")

    def test_AddRunIndividualInfo_set_schedule_info_type_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfoType_description(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_description({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_description(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfoType_description("Description 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfoType_description("Description 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfoType_description("Description 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfoType_description,
                         "Description 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfoType_description,
                         "Description 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfoType_description,
                         "Description 3")

    def test_AddRunIndividualInfo_set_schedule_info(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfo(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfo({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfo(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_scheduleInfo("Schedule Info 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_scheduleInfo("Schedule Info 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_scheduleInfo("Schedule Info 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._scheduleInfo, "Schedule Info 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._scheduleInfo, "Schedule Info 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._scheduleInfo, "Schedule Info 3")

    def test_AddRunIndividualInfo_set_venue_block(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_block(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_block({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_block(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_block("Block 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_block("Block 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_block("Block 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_block, "Block 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_block, "Block 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_block, "Block 3")

    def test_AddRunIndividualInfo_set_venue_street(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_street(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_street({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_street(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_street("Street 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_street("Street 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_street("Street 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_street, "Street 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_street, "Street 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_street, "Street 3")

    def test_AddRunIndividualInfo_set_venue_floor(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_floor(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_floor({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_floor(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_floor("Floor 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_floor("Floor 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_floor("Floor 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_floor, "Floor 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_floor, "Floor 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_floor, "Floor 3")

    def test_AddRunIndividualInfo_set_venue_unit(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_unit(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_unit({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_unit(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_unit("Unit 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_unit("Unit 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_unit("Unit 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_unit, "Unit 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_unit, "Unit 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_unit, "Unit 3")

    def test_AddRunIndividualInfo_set_venue_building(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_building(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_building({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_building(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_building("Building 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_building("Building 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_building("Building 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_building, "Building 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_building, "Building 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_building, "Building 3")

    def test_AddRunIndividualInfo_set_venue_postal_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_postalCode(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_postalCode({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_postalCode(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_postalCode("112233")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_postalCode("223344")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_postalCode("334455")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_postalCode, "112233")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_postalCode, "223344")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_postalCode, "334455")

    def test_AddRunIndividualInfo_set_venue_room(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_room(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_room({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_room(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_room("Room 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_room("Room 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_room("Room 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_room, "Room 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_room, "Room 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_room, "Room 3")

    def test_AddRunIndividualInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_wheelChairAccess("Yess")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_wheelChairAccess(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_wheelChairAccess("n0")

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_venue_wheelChairAccess("Yes")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_venue_wheelChairAccess("Select a value")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_venue_wheelChairAccess("No")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._venue_wheelChairAccess, True)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._venue_wheelChairAccess, None)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._venue_wheelChairAccess, False)

    def test_AddRunIndividualInfo_set_intake_size(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_intakeSize("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_intakeSize("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_intakeSize({"one"})

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_intakeSize(1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_intakeSize(2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_intakeSize(3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._intakeSize, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._intakeSize, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._intakeSize, 3)

    def test_AddRunIndividualInfo_set_threshold(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_threshold("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_threshold("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_threshold({"one"})

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_threshold(1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_threshold(2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_threshold(3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._threshold, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._threshold, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._threshold, 3)

    def test_AddRunIndividualInfo_set_registered_user_count(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registeredUserCount("1")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registeredUserCount("2232131")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registeredUserCount({"one"})

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_registeredUserCount(1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_registeredUserCount(2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_registeredUserCount(3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._registeredUserCount, 1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._registeredUserCount, 2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._registeredUserCount, 3)

    def test_AddRunIndividualInfo_set_mode_of_training(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_modeOfTraining(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_modeOfTraining("One")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_modeOfTraining({"one"})

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_modeOfTraining("1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_modeOfTraining("2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_modeOfTraining("3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._modeOfTraining, "1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._modeOfTraining, "2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._modeOfTraining, "3")

    def test_AddRunIndividualInfo_set_course_admin_email(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseAdminEmail(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseAdminEmail({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseAdminEmail(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseAdminEmail("Email 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseAdminEmail("Email 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseAdminEmail("Email 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseAdminEmail, "Email 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseAdminEmail, "Email 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseAdminEmail, "Email 3")

    def test_AddRunIndividualInfo_set_course_vacancy_code(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseVacancy_code(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_code({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_code(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseVacancy_code("1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_code("2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_code("3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseVacancy_code, "1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseVacancy_code, "2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseVacancy_code, "3")

    def test_AddRunIndividualInfo_set_course_vacancy_description(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseVacancy_description(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_description({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_description(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_courseVacancy_description("Description 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_courseVacancy_description("Description 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_courseVacancy_description("Description 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._courseVacancy_description, "Description 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._courseVacancy_description, "Description 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._courseVacancy_description, "Description 3")

    def test_AddRunIndividualInfo_set_file_name(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_file_Name(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_Name({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_Name(3.3333333)

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_file_Name("File Name 1")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_Name("File Name 2")
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_Name("File Name 3")

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_Name, "File Name 1")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_Name, "File Name 2")
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_Name, "File Name 3")

    def test_AddRunIndividualInfo_set_file_content(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_file_content(b"image")

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_content({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_content(["photo"])

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

            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_file_content(T1)
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_file_content(T2)
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_file_content(T3)

            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._file_content, T1)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._file_content, T2)
            self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._file_content, T3)

    def test_AddRunIndividualInfo_set_sessions(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_sessions(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sessions({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sessions(3.3333333)

        st1 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_ONE, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO]
        st2 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_TWO, TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]
        st3 = [TestCourseRunsModels.RUN_SESSION_EDIT_INFO_THREE]

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_sessions(st1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_sessions(st2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_sessions(st3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._sessions, st1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._sessions, st2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._sessions, st3)

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
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_linkCourseRunTrainer(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_linkCourseRunTrainer({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_linkCourseRunTrainer(3.3333333)

        cr1 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO]
        cr2 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO, TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]
        cr3 = [TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE]

        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE.set_linkCourseRunTrainer(cr1)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO.set_linkCourseRunTrainer(cr2)
        TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE.set_linkCourseRunTrainer(cr3)

        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_ONE._linkCourseRunTrainer, cr1)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_TWO._linkCourseRunTrainer, cr2)
        self.assertEqual(TestCourseRunsModels.ADD_INDIVIDUAL_RUN_INFO_THREE._linkCourseRunTrainer, cr3)

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
        self.maxDiff = 99999999

        p3 = {
            "course": {
                "courseReferenceNumber": "XX-10000000K-02-TEST 199"
            },
            "runs": [
                {
                    'sequenceNumber': 2,
                    'registrationDates': {
                        'opening': 20240201,
                        'closing': 20240204
                    },
                    'courseDates': {
                        'start': 20240201,
                        'end': 20240331
                    },
                    'scheduleInfoType': {
                        'code': '01',
                        'description': 'Description'
                    },
                    'scheduleInfo': 'Sat / 5 Sats / 9am - 6pm',
                    'venue': {
                        'block': '112B',
                        'street': 'Other Street ABC',
                        'floor': '51', 'unit': '100',
                        'building': 'Other Building ABC',
                        'postalCode': '554321',
                        'room': '84',
                        'wheelChairAccess': False
                    },
                    'intakeSize': 50,
                    'threshold': 100,
                    'registeredUserCount': 20,
                    'modeOfTraining': '8',
                    'courseAdminEmail': 'jane@email.com',
                    'courseVacancy': {
                        'code': 'F',
                        'description': 'Full'
                    },
                    "file": {
                        "Name": "def.jpg",
                        "content": img2
                    },
                    "sessions": [
                        {
                            'action': 'update',
                            'sessionId': 'XX-10000000K-01-TEST 166',
                            'startDate': '20240101',
                            'endDate': '20240229',
                            'startTime': '08:30',
                            'endTime': '18:00',
                            'modeOfTraining': '2',
                            'venue': {
                                'block': '112A',
                                'street': 'Street ABC',
                                'floor': '15',
                                'unit': '001',
                                'building': 'Building ABC',
                                'postalCode': '123455',
                                'room': '24',
                                'wheelChairAccess': True,
                                'primaryVenue': True
                            }
                        },
                        {
                            'action': 'update',
                            'sessionId': 'XX-10000000K-01-TEST 166',
                            'startDate': '20240101',
                            'endDate': '20240229',
                            'startTime': '08:30',
                            'endTime': '18:00',
                            'modeOfTraining': '2',
                            'venue': {
                                'block': '112A',
                                'street': 'Street ABC',
                                'floor': '15',
                                'unit': '001',
                                'building': 'Building ABC',
                                'postalCode': '123455',
                                'room': '24',
                                'wheelChairAccess': True,
                                'primaryVenue': True
                            }
                        }
                    ],
                    "linkCourseRunTrainer": [
                        {
                            "trainer": {
                                'trainerType': {
                                    'code': '1',
                                    'description': 'Existing'
                                },
                                'indexNumber': 1,
                                'id': 'TRAINER_ONE',
                                'name': 'JOHN DOE',
                                'email': 'john@email.com',
                                'idNumber': 'S1234567X',
                                'idType': {
                                    'code': 'SB',
                                    'description': 'Singapore Blue Identification Card'
                                },
                                'roles': [
                                    {
                                        'id': 1,
                                        'description': 'Trainer'
                                    }
                                ],
                                'inTrainingProviderProfile': True,
                                'domainAreaOfPractice': 'Testing Management in Computer Application and Diploma in '
                                                        'Computer Application',
                                'experience': 'Testing ABC',
                                'linkedInURL': 'https://sg.linkedin.com/company/linkedin/abc',
                                'salutationId': 1,
                                "photo": {
                                    "name": "abc.jpg",
                                    "content": img1
                                },
                                'linkedSsecEQAs': [
                                    {
                                        'description': 'EQA test 4',
                                        'ssecEQA': {
                                            'code': '12'
                                        }
                                    }
                                ]
                            },
                        },
                        {
                            "trainer": {
                                'trainerType':
                                    {
                                        'code': '1',
                                        'description': 'Existing'
                                    },
                                'indexNumber': 1,
                                'id': 'TRAINER_ONE',
                                'name': 'JOHN DOE',
                                'email': 'john@email.com',
                                'idNumber': 'S1234567X',
                                'idType':
                                    {
                                        'code': 'SB',
                                        'description': 'Singapore Blue Identification Card'
                                    },
                                'roles':
                                    [
                                        {
                                            'id': 1,
                                            'description': 'Trainer'
                                        }
                                    ],
                                'inTrainingProviderProfile': True,
                                'domainAreaOfPractice': 'Testing Management in Computer Application and Diploma in '
                                                        'Computer Application',
                                'experience': 'Testing ABC',
                                'linkedInURL': 'https://sg.linkedin.com/company/linkedin/abc',
                                'salutationId': 1,
                                "photo":
                                    {
                                        "name": "abc.jpg",
                                        "content": img1
                                    },
                                'linkedSsecEQAs':
                                    [
                                        {
                                            'description': 'EQA test 4',
                                            'ssecEQA': {
                                                'code': '12'
                                            }
                                        }
                                    ]
                            }
                        }
                    ]
                }
            ]
        }

        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_THREE.payload(), p3)

    def test_AddRunInfo_set_crid(self):
        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_crid(1)

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_crid({"two"})

        with self.assertRaises(ValueError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_crid(["three"])

        TestCourseRunsModels.ADD_RUN_INFO_ONE.set_crid("CRID 1")
        TestCourseRunsModels.ADD_RUN_INFO_TWO.set_crid("CRID 2")
        TestCourseRunsModels.ADD_RUN_INFO_THREE.set_crid("CRID 3")

        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_ONE._crid, "CRID 1")
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_TWO._crid, "CRID 2")
        self.assertEqual(TestCourseRunsModels.ADD_RUN_INFO_THREE._crid, "CRID 3")

    def test_AddRunInfo_set_sequence_number(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_sequence_number("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_sequence_number("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_sequence_number(["seq number"])

    def test_AddRunInfo_set_registration_dates_opening(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_registrationDates_opening("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_registrationDates_opening("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_registrationDates_opening(123)

    def test_AddRunInfo_set_registration_dates_closing(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_registrationDates_closing("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_registrationDates_closing("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_registrationDates_closing(123)

    def test_AddRunInfo_set_course_dates_start(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_courseDates_start("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_courseDates_start("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_courseDates_start(123)

    def test_AddRunInfo_set_course_dates_end(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_courseDates_end("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_courseDates_end("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_courseDates_end(123)

    def test_AddRunInfo_set_schedule_info_type_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_scheduleInfoType_code(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_scheduleInfoType_code({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_scheduleInfoType_code("123123")

    def test_AddRunInfo_set_schedule_info_type_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_scheduleInfoType_description(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_scheduleInfoType_description({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_scheduleInfoType_description("valid but still not implemented")

    def test_AddRunInfo_set_schedule_info(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_scheduleInfo(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_scheduleInfo({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_scheduleInfo("valid but still not implemented")

    def test_AddRunInfo_set_venue_block(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_block(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_block({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_block("valid but still not implemented")

    def test_AddRunInfo_set_venue_street(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_street(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_street({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_street("valid but still not implemented")

    def test_AddRunInfo_set_venue_floor(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_floor(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_floor({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_floor("valid but still not implemented")

    def test_AddRunInfo_set_venue_unit(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_unit(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_unit({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_unit("valid but still not implemented")

    def test_AddRunInfo_set_venue_building(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_building(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_building({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_building("valid but still not implemented")

    def test_AddRunInfo_set_venue_postal_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_postalCode(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_postalCode({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_postalCode("123456")

    def test_AddRunInfo_set_venue_room(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_room(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_room({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_room("123456")

    def test_AddRunInfo_set_venue_wheel_chair_access(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_venue_wheelChairAccess("Yess")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_venue_wheelChairAccess(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_venue_wheelChairAccess("Yes")

    def test_AddRunInfo_set_intake_size(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_intakeSize("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_intakeSize("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_intakeSize(12)

    def test_AddRunInfo_set_threshold(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_threshold("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_threshold("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_threshold(12)

    def test_AddRunInfo_set_registered_user_count(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_registeredUserCount("1")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_registeredUserCount("2232131")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_registeredUserCount(12)

    def test_AddRunInfo_set_mode_of_training(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_modeOfTraining(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_modeOfTraining("One")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_modeOfTraining("1")

    def test_AddRunInfo_set_course_admin_email(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_courseAdminEmail(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_courseAdminEmail({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_courseAdminEmail("email@email.com")

    def test_AddRunInfo_set_course_vacancy_code(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_courseVacancy_code(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_courseVacancy_code({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_courseVacancy_code("A")

    def test_AddRunInfo_set_course_vacancy_description(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_courseVacancy_description(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_courseVacancy_description({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_courseVacancy_description("Available")

    def test_AddRunInfo_set_file_name(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_file_Name(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_file_Name({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_file_Name("Name")

    def test_AddRunInfo_set_file_content(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_file_content(b"image")

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_file_content({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_file_content("img")

    def test_AddRunInfo_set_sessions(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_sessions(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_sessions({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_sessions(["session"])

    def test_AddRunInfo_add_session(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_session(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_session({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.add_session("session")

    def test_AddRunInfo_set_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.set_linkCourseRunTrainer(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.set_linkCourseRunTrainer({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.set_linkCourseRunTrainer(["trainer"])

    def test_AddRunInfo_add_link_course_run_trainer(self):
        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_ONE.add_linkCourseRunTrainer(1)

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_TWO.add_linkCourseRunTrainer({"two"})

        with self.assertRaises(NotImplementedError):
            TestCourseRunsModels.ADD_RUN_INFO_THREE.add_linkCourseRunTrainer("trainer")
