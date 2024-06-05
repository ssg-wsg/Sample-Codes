"""
Tests for the Course Runs related model classes.

Code to use vars() inspired by
https://stackoverflow.com/questions/45984018/python-unit-test-to-check-if-objects-are-same-at-different-location
"""

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
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_ONE = RunTrainerEditInfo()

        # set up second instance
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_TWO = RunTrainerEditInfo()
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
        TestCourseRunsModels.RUN_TRAINER_ADD_INFO_THREE = RunTrainerEditInfo()
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
