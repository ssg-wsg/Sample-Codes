"""
Tests for the Attendance related model classes.

Code to use vars() inspired by
https://stackoverflow.com/questions/45984018/python-unit-test-to-check-if-objects-are-same-at-different-location
"""

import unittest

from revamped_application.core.constants import IdType, Attendance, SurveyLanguage
from revamped_application.core.models.attendance import UploadAttendanceInfo


class TestAttendanceInfo(unittest.TestCase):
    """Tests the UploadAttendanceInfo class in Attendance models module."""

    SESSION_ID_ONE = "123456"
    SESSION_ID_TWO = "654321"
    STATUS_CODE_ONE = Attendance.CONFIRMED
    STATUS_CODE_TWO = Attendance.UNCONFIRMED
    TRAINEE_ID_ONE = "T1234567A"
    TRAINEE_ID_TWO = "T7654321B"
    TRAINEE_NAME_ONE = "John Doe"
    TRAINEE_NAME_TWO = "Jane Doe"
    TRAINEE_EMAIL_ONE = "john@email.com"
    TRAINEE_EMAIL_TWO = "jane@email.com"
    TRAINEE_ID_TYPE_ONE = IdType.SINGAPORE_BLUE
    TRAINEE_ID_TYPE_TWO = IdType.SINGAPORE_PINK
    TRAINEE_CONTACT_NUMBER_MOBILE_ONE = "91234567"
    TRAINEE_CONTACT_NUMBER_MOBILE_TWO = "98765432"
    TRAINEE_CONTACT_NUMBER_AREACODE_ONE = 65
    TRAINEE_CONTACT_NUMBER_AREACODE_TWO = 130
    TRAINEE_CONTACT_NUMBER_COUNTRYCODE_ONE = 65
    TRAINEE_CONTACT_NUMBER_COUNTRYCODE_TWO = 66
    NUMBER_OF_HOURS_ONE = 1.5
    NUMBER_OF_HOURS_TWO = 2.5
    SURVEY_LANGUAGE_CODE_ONE = SurveyLanguage.ENGLISH
    SURVEY_LANGUAGE_CODE_TWO = SurveyLanguage.MALAY
    REFERENCE_NUMBER_ONE = "123456"
    REFERENCE_NUMBER_TWO = "654321"
    CORPPASS_ID_ONE = "C1234567A"
    CORPPASS_ID_TWO = "C7654321B"

    UPLOAD_ATTENDANCE_ONE = UploadAttendanceInfo()
    UPLOAD_ATTENDANCE_TWO = UploadAttendanceInfo()
    UPLOAD_ATTENDANCE_THREE = UploadAttendanceInfo()

    def __set_up_instances(self):
        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE = UploadAttendanceInfo()
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO = UploadAttendanceInfo()
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE = UploadAttendanceInfo()

        # set up second instance
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId = TestAttendanceInfo.SESSION_ID_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code = TestAttendanceInfo.STATUS_CODE_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id = TestAttendanceInfo.TRAINEE_ID_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name = TestAttendanceInfo.TRAINEE_NAME_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email = TestAttendanceInfo.TRAINEE_EMAIL_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type = TestAttendanceInfo.TRAINEE_ID_TYPE_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_MOBILE_ONE)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_AREACODE_ONE)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_COUNTRYCODE_ONE)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours = TestAttendanceInfo.NUMBER_OF_HOURS_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code = TestAttendanceInfo.SURVEY_LANGUAGE_CODE_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber = TestAttendanceInfo.REFERENCE_NUMBER_ONE
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId = TestAttendanceInfo.CORPPASS_ID_ONE

        # set up third instance
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId = TestAttendanceInfo.SESSION_ID_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code = TestAttendanceInfo.STATUS_CODE_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id = TestAttendanceInfo.TRAINEE_ID_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name = TestAttendanceInfo.TRAINEE_NAME_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email = TestAttendanceInfo.TRAINEE_EMAIL_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type = TestAttendanceInfo.TRAINEE_ID_TYPE_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_MOBILE_TWO)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_AREACODE_TWO)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode = (
            TestAttendanceInfo.TRAINEE_CONTACT_NUMBER_COUNTRYCODE_TWO)
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours = TestAttendanceInfo.NUMBER_OF_HOURS_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code = TestAttendanceInfo.SURVEY_LANGUAGE_CODE_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber = TestAttendanceInfo.REFERENCE_NUMBER_TWO
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId = TestAttendanceInfo.CORPPASS_ID_TWO

    def setUp(self):
        self.__set_up_instances()

    def test_UploadAttendanceInfo_equality(self):
        self.assertEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE), vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE))
        self.assertEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO), vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO))
        self.assertEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE),
                         vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE))

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE, TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO, TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE, TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE)

    def test_UploadAttendanceInfo_inequality(self):
        self.assertNotEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE),
                            vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO))
        self.assertNotEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE),
                            vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE))
        self.assertNotEqual(vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO),
                            vars(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE))

        self.assertNotEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE, TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO)
        self.assertNotEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE, TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE)
        self.assertNotEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO, TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE)

    def test_UploadAttendanceInfo_validate(self):
        e1, _ = TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.validate()
        e2, _ = TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.validate()
        e3, _ = TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_UploadAttendanceInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.payload()

        p2 = {
            'course': {
                'sessionID': '123456',
                'attendance': {
                    'status': {
                        'code': '1'
                    },
                    'trainee': {
                        'id': 'T1234567A',
                        'name': 'John Doe',
                        'email': 'john@email.com',
                        'idType': {
                            'code': 'SB'
                        },
                        'contactNumber': {
                            'mobile': '91234567',
                            'areaCode': 65,
                            'countryCode': 65
                        },
                        'numberOfHours': 1.5,
                        'surveyLanguage': {
                            'code': 'EL'
                        }
                    }
                },
                'referenceNumber': '123456'
            },
            'corppassId': 'C1234567A'
        }

        p3 = {
            'course': {
                'sessionID': '654321',
                'attendance': {
                    'status': {
                        'code': '2'
                    },
                    'trainee': {
                        'id': 'T7654321B',
                        'name': 'Jane Doe',
                        'email': 'jane@email.com',
                        'idType': {
                            'code': 'SP'
                        },
                        'contactNumber': {
                            'mobile': '98765432',
                            'areaCode': 130,
                            'countryCode': 66
                        },
                        'numberOfHours': 2.5,
                        'surveyLanguage': {
                            'code': 'MY'
                        }
                    }
                },
                'referenceNumber': '654321'
            },
            'corppassId': 'C7654321B'
        }

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.payload(), p2)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.payload(), p3)

    def test_UploadAttendanceInfo_set_session_id(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.sessionId = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId = {"Session ID"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.sessionId = "Session ID 1"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId = "Session ID 2"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId = "Session ID 3"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.sessionId_, "Session ID 1")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.sessionId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.sessionId)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId_, "Session ID 2")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.sessionId)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId_, "Session ID 3")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.sessionId)

    def test_UploadAttendanceInfo_set_status_code(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.status_code = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code = {"3"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.status_code = Attendance.TP_VOIDED
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code = Attendance.REJECTED
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code = Attendance.CONFIRMED

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.status_code_, Attendance.TP_VOIDED)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.status_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.status_code)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code_, Attendance.REJECTED)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.status_code)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code_, Attendance.CONFIRMED)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.status_code)

    def test_UploadAttendanceInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id = {"S7654321B"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id = "T1234567A"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id = "S7654321B"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id = "S1234567A"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_, "T1234567A")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_, "S7654321B")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_, "S1234567A")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id)

    def test_UploadAttendanceInfo_set_trainee_name(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_name = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name = {"Eric Doe"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_name = "Eric Doe"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name = "Henry Doe"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name = "Emily Doe"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_name_, "Eric Doe")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_name_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_name)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name_, "Henry Doe")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_name)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name_, "Emily Doe")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_name)

    def test_UploadAttendanceInfo_set_trainee_email(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_email = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email = {"henry@email.com"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_email = "eric@email.com"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email = "henry@email.com"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email = "emily@email.com"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_email_, "eric@email.com")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_email_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_email)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email_, "henry@email.com")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_email)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email_, "emily@email.com")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_email)

    def test_UploadAttendanceInfo_set_trainee_id_type(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_type = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type = {"SO"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_type = IdType.FIN_WORK_PERMIT
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type = IdType.FOREIGN_PASSPORT
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type = IdType.OTHERS

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_type_, IdType.FIN_WORK_PERMIT)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_type_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.trainee_id_type)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type_, IdType.FOREIGN_PASSPORT)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.trainee_id_type)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type_, IdType.OTHERS)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.trainee_id_type)

    def test_UploadAttendanceInfo_set_contact_number_mobile(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_mobile = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile = {"95425555"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile = 1234567890

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_mobile = "95425555"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile = "81234567"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile = "98989898"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_mobile_, "95425555")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_mobile_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_mobile)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile_, "81234567")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_mobile)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile_, "98989898")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_mobile)

    def test_UploadAttendanceInfo_set_contact_number_areacode(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_areacode = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode = {"64"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode = "64"

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_areacode = 128
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode = 64
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode = 32

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_areacode_, 128)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_areacode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_areacode)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode_, 64)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_areacode)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode_, 32)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_areacode)

    def test_UploadAttendanceInfo_set_contact_number_country_code(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_countryCode = 123.44

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode = {"64"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode = "64"

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_countryCode = 128
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode = 64
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode = 32

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_countryCode_, 128)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_countryCode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.contactNumber_countryCode)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode_, 64)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.contactNumber_countryCode)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode_, 32)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.contactNumber_countryCode)

    def test_UploadAttendanceInfo_set_number_of_hours(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.numberOfHours = "1.0"

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours = {"2.5"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours = "64"

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.numberOfHours = 2.5
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours = 4.5
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours = 6.5

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.numberOfHours_, 2.5)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.numberOfHours_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.numberOfHours)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours_, 4.5)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.numberOfHours)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours_, 6.5)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.numberOfHours)

    def test_UploadAttendanceInfo_set_survey_language_code(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.surveyLanguage_code = 1.0

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code = {"TM"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code = 64

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.surveyLanguage_code = SurveyLanguage.MANDARIN
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code = SurveyLanguage.TAMIL
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code = SurveyLanguage.MALAY

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.surveyLanguage_code_, SurveyLanguage.MANDARIN)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.surveyLanguage_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.surveyLanguage_code)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code_, SurveyLanguage.TAMIL)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.surveyLanguage_code)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code_, SurveyLanguage.MALAY)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.surveyLanguage_code)

    def test_UploadAttendanceInfo_set_reference_number(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.referenceNumber = 1.0

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber = {"Reference Number 3"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber = 64

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.referenceNumber = "Reference Number 1"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber = "Reference Number 2"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber = "Reference Number 3"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.referenceNumber_, "Reference Number 1")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.referenceNumber_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.referenceNumber)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber_, "Reference Number 2")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.referenceNumber)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber_, "Reference Number 3")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.referenceNumber)

    def test_UploadAttendanceInfo_set_corppass_id(self):
        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.corppassId = 1.0

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId = {"Reference Number 3"}

        with self.assertRaises(ValueError):
            TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId = 64

        TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.corppassId = "T1234567X"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId = "T7654321Y"
        TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId = "S1234567Z"

        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.corppassId_, "T1234567X")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.corppassId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_ONE.corppassId)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId_, "T7654321Y")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_TWO.corppassId)
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId_, "S1234567Z")
        self.assertEqual(TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId_,
                         TestAttendanceInfo.UPLOAD_ATTENDANCE_THREE.corppassId)
