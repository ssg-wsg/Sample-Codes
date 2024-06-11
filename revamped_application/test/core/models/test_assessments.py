"""
Contains test cases for CreateAssAssessmentInfo, UpdateVoidAssessmentInfo, and SearchAssessmentInfo.
"""

import unittest
from datetime import date

from revamped_application.core.constants import IdTypeSummary, SortOrder, SortField
from revamped_application.core.models.assessments import (CreateAssessmentInfo, SearchAssessmentInfo,
                                                          UpdateVoidAssessmentInfo)


class TestCreateAssessmentInfo(unittest.TestCase):
    """
    Test cases for CreateAssessmentInfo, UpdateVoidAssessmentInfo, and SearchAssessmentInfo.
    """

    GRADE_ONE = "A"
    GRADE_TWO = "E"
    GRADE_SCORE_ONE = 100
    GRADE_SCORE_TWO = 50
    COURSE_RUN_ID_ONE = "course_run_id_1"
    COURSE_RUN_ID_TWO = "course_run_id_2"
    COURSE_REFERENCE_NUMBER_ONE = "course_reference_number_1"
    COURSE_REFERENCE_NUMBER_TWO = "course_reference_number_2"
    RESULT_ONE = "Pass"
    RESULT_TWO = "Fail"
    TRAINEE_ID_ONE = "T0123456X"
    TRAINEE_ID_TWO = "S0123456Y"
    TRAINEE_ID_TYPE_ONE = "NRIC"
    TRAINEE_ID_TYPE_TWO = "OTHERS"
    TRAINEE_FULL_NAME_ONE = "John Doe"
    TRAINEE_FULL_NAME_TWO = "Jane Doe"
    SKILL_CODE_ONE = "CODE1"
    SKILL_CODE_TWO = "CODE2"
    ASSESSMENT_DATE_ONE = date(2020, 1, 1)
    ASSESSMENT_DATE_TWO = date(2020, 2, 2)
    TRAINING_PARTNER_CODE_ONE = "TP1"
    TRAINING_PARTNER_CODE_TWO = "TP2"
    TRAINING_PARTNER_UEN_ONE = "12345678G"
    TRAINING_PARTNER_UEN_TWO = "87654321G"
    CONFERRING_INSTITUTE_CODE_ONE = "CI1"
    CONFERRING_INSTITUTE_CODE_TWO = "CI2"
    LAST_UPDATE_TO_ONE = date(2023, 1, 12)
    LAST_UPDATE_TO_TWO = date(2023, 2, 12)
    LAST_UPDATE_FROM_ONE = date(2023, 1, 1)
    LAST_UPDATE_FROM_TWO = date(2023, 2, 1)
    SORT_BY_ONE = SortField.UPDATED_ON
    SORT_BY_TWO = SortField.ASSESSMENT_DATE
    SORT_ORDER_ONE = SortOrder.ASCENDING
    SORT_ORDER_TWO = SortOrder.DESCENDING
    PAGE_ONE = 1
    PAGE_TWO = 2
    PAGE_SIZE_ONE = 10
    PAGE_SIZE_TWO = 20
    ASSESSMENT_REFERENCE_NUMBER_ONE = "assessment_reference_number_1"
    ASSESSMENT_REFERENCE_NUMBER_TWO = "assessment_reference_number_2"
    ENROLMENT_REFERENCE_NUMBER_ONE = "enrolment_reference_number_1"
    ENROLMENT_REFERENCE_NUMBER_TWO = "enrolment_reference_number_2"

    CREATE_ASSESSMENT_ONE = None
    CREATE_ASSESSMENT_TWO = None
    CREATE_ASSESSMENT_THREE = None

    UPDATE_VOID_ASSESSMENT_ONE = None
    UPDATE_VOID_ASSESSMENT_TWO = None
    UPDATE_VOID_ASSESSMENT_THREE = None

    SEARCH_ASSESSMENT_ONE = None
    SEARCH_ASSESSMENT_TWO = None
    SEARCH_ASSESSMENT_THREE = None

    def __set_up_create_assessment_info(self):
        """
        Set up the CreateAssessmentInfo instances.

        Do not use setters here as they are not tested yet.
        """

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE = CreateAssessmentInfo()

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO = CreateAssessmentInfo()
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._grade = TestCreateAssessmentInfo.GRADE_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._grade_score = TestCreateAssessmentInfo.GRADE_SCORE_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._course_runId = TestCreateAssessmentInfo.COURSE_RUN_ID_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._course_referenceNumber = (
            TestCreateAssessmentInfo.COURSE_REFERENCE_NUMBER_ONE)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._result = (
            TestCreateAssessmentInfo.RESULT_ONE)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_id = TestCreateAssessmentInfo.TRAINEE_ID_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_idType = TestCreateAssessmentInfo.TRAINEE_ID_TYPE_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_fullName = (
            TestCreateAssessmentInfo.TRAINEE_FULL_NAME_ONE)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._skillCode = TestCreateAssessmentInfo.SKILL_CODE_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._assessmentDate = TestCreateAssessmentInfo.ASSESSMENT_DATE_ONE
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_code = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_CODE_ONE)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_uen = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_UEN_ONE)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._conferringInstitute_code = (
            TestCreateAssessmentInfo.CONFERRING_INSTITUTE_CODE_ONE)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE = CreateAssessmentInfo()
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._grade = TestCreateAssessmentInfo.GRADE_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._grade_score = TestCreateAssessmentInfo.GRADE_SCORE_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._course_runId = TestCreateAssessmentInfo.COURSE_RUN_ID_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._course_referenceNumber = (
            TestCreateAssessmentInfo.COURSE_REFERENCE_NUMBER_TWO)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._result = TestCreateAssessmentInfo.RESULT_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_id = TestCreateAssessmentInfo.TRAINEE_ID_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_idType = TestCreateAssessmentInfo.TRAINEE_ID_TYPE_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_fullName = (
            TestCreateAssessmentInfo.TRAINEE_FULL_NAME_TWO)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._skillCode = TestCreateAssessmentInfo.SKILL_CODE_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._assessmentDate = TestCreateAssessmentInfo.ASSESSMENT_DATE_TWO
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_code = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_CODE_TWO)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_uen = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_UEN_TWO)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._conferringInstitute_code = (
            TestCreateAssessmentInfo.CONFERRING_INSTITUTE_CODE_TWO)

    def __set_up_update_void_assessment_info(self):
        """Set up the UpdateVoidAssessmentInfo instances."""

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE = UpdateVoidAssessmentInfo()

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO = UpdateVoidAssessmentInfo()
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade = TestCreateAssessmentInfo.GRADE_ONE
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade_score = TestCreateAssessmentInfo.GRADE_SCORE_ONE
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._action = "update"
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._result = TestCreateAssessmentInfo.RESULT_ONE
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._trainee_fullName = (
            TestCreateAssessmentInfo.TRAINEE_FULL_NAME_ONE)
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._skillCode = TestCreateAssessmentInfo.SKILL_CODE_ONE
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._assessmentDate = (
            TestCreateAssessmentInfo.ASSESSMENT_DATE_ONE)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE = UpdateVoidAssessmentInfo()
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade = TestCreateAssessmentInfo.GRADE_TWO
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade_score = TestCreateAssessmentInfo.GRADE_SCORE_TWO
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._action = "void"
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._result = TestCreateAssessmentInfo.RESULT_TWO
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._trainee_fullName = (
            TestCreateAssessmentInfo.TRAINEE_FULL_NAME_TWO)
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._skillCode = TestCreateAssessmentInfo.SKILL_CODE_TWO
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._assessmentDate = (
            TestCreateAssessmentInfo.ASSESSMENT_DATE_TWO)

    def __set_up_search_assessment_info(self):
        """Set up the SearchAssessmentInfo instances."""

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE = SearchAssessmentInfo()

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO = SearchAssessmentInfo()
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateTo = TestCreateAssessmentInfo.LAST_UPDATE_TO_ONE
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateFrom = (
            TestCreateAssessmentInfo.LAST_UPDATE_FROM_ONE)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_field = TestCreateAssessmentInfo.SORT_BY_ONE.value
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_order = TestCreateAssessmentInfo.SORT_ORDER_ONE.value[0]
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_page = TestCreateAssessmentInfo.PAGE_ONE
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_pageSize = TestCreateAssessmentInfo.PAGE_SIZE_ONE
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_courseRunId = (
            TestCreateAssessmentInfo.COURSE_RUN_ID_ONE)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_referenceNumber = (
            TestCreateAssessmentInfo.ASSESSMENT_REFERENCE_NUMBER_ONE)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_traineeId = TestCreateAssessmentInfo.TRAINEE_ID_ONE
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_enrolement_referenceNumber = (
            TestCreateAssessmentInfo.ENROLMENT_REFERENCE_NUMBER_ONE
        )
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_skillCode = TestCreateAssessmentInfo.SKILL_CODE_ONE
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_uen = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_UEN_ONE)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_code = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_CODE_ONE)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE = SearchAssessmentInfo()
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateTo = TestCreateAssessmentInfo.LAST_UPDATE_TO_TWO
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateFrom = (
            TestCreateAssessmentInfo.LAST_UPDATE_FROM_TWO)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_field = TestCreateAssessmentInfo.SORT_BY_TWO.value
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_order = TestCreateAssessmentInfo.SORT_ORDER_TWO.value[0]
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_page = TestCreateAssessmentInfo.PAGE_TWO
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_pageSize = TestCreateAssessmentInfo.PAGE_SIZE_TWO
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_courseRunId = (
            TestCreateAssessmentInfo.COURSE_RUN_ID_TWO)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_referenceNumber = (
            TestCreateAssessmentInfo.ASSESSMENT_REFERENCE_NUMBER_TWO)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId = TestCreateAssessmentInfo.TRAINEE_ID_TWO
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber = (
            TestCreateAssessmentInfo.ENROLMENT_REFERENCE_NUMBER_TWO
        )
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_skillCode = TestCreateAssessmentInfo.SKILL_CODE_TWO
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_uen = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_UEN_TWO)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_code = (
            TestCreateAssessmentInfo.TRAINING_PARTNER_CODE_TWO)

    def setUp(self):
        """Create the objects to test"""

        self.__set_up_create_assessment_info()
        self.__set_up_update_void_assessment_info()
        self.__set_up_search_assessment_info()

    def test_CreateAssessmentInfo_equality(self):
        """
        Test the equality of the CreateAssessmentInfo instances.
        """

        self.assertEqual(vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE),
                         vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE))
        self.assertEqual(vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO),
                         vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO))
        self.assertEqual(vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE),
                         vars(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE))

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE, TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE)
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO, TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO)
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE,
                         TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE)

    def test_UpdateVoidAssessmentInfo_equality(self):
        """
        Test the equality of the UpdateVoidAssessmentInfo instances.
        """

        self.assertEqual(vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE),
                         vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE))
        self.assertEqual(vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO),
                         vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO))
        self.assertEqual(vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE),
                         vars(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE))

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                         TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE)
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
                         TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO)
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE,
                         TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)

    def test_SearchAssessmentInfo_equality(self):
        """
        Test the equality of the SearchAssessmentInfo instances.
        """

        self.assertEqual(vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE),
                         vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE))
        self.assertEqual(vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO),
                         vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO))
        self.assertEqual(vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE),
                         vars(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE))

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                         TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO,
                         TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE,
                         TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE)

    def test_CreateAssessmentInfo_inequality(self):
        self.assertNotEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO)
        self.assertNotEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE)
        self.assertNotEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO,
                            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE)

    def test_UpdateVoidAssessmentInfo_inequality(self):
        self.assertNotEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO)
        self.assertNotEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)
        self.assertNotEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
                            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)

    def test_SearchAssessmentInfo_inequality(self):
        self.assertNotEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO)
        self.assertNotEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE)
        self.assertNotEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO,
                            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE)

    def test_all_inequality(self):
        test_array = [
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE,
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO,
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE,
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE,
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE,
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO,
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE
        ]

        for i in range(len(test_array)):
            for j in range(len(test_array)):
                if i == j:
                    continue

                self.assertNotEqual(test_array[i], test_array[j])

    def test_CreateAssessmentInfo_validate(self):
        e1, _ = TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.validate()
        e2, _ = TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.validate()
        e3, _ = TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_CreateAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.payload()

        p2 = {
            "assessment": {
                "grade": "A",
                "course": {
                    "run": {
                        "id": "course_run_id_1"
                    },
                    "referenceNumber": "course_reference_number_1"
                },
                "result": "Pass",
                "trainee": {
                    "id": "T0123456X",
                    "idType": "NRIC",
                    "fullName": "John Doe"
                },
                "skillCode": "CODE1",
                "assessmentDate": "2020-01-01",
                "trainingPartner": {
                    "uen": "12345678G",
                    "code": "TP1"
                },
                "conferringInstitute": {
                    "code": "CI1"
                }
            }
        }

        p3 = {
            'assessment': {
                'grade': 'E',
                'course': {
                    'run': {
                        'id': 'course_run_id_2'
                    },
                    'referenceNumber': 'course_reference_number_2'
                },
                'result': 'Fail',
                'trainee': {
                    'id': 'S0123456Y',
                    'idType': 'OTHERS',
                    'fullName': 'Jane Doe'
                },
                'skillCode': 'CODE2',
                'assessmentDate': '2020-02-02',
                'trainingPartner': {
                    'uen': '87654321G',
                    'code': 'TP2'
                },
                'conferringInstitute': {
                    'code': 'CI2'
                }
            }
        }

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.payload(), p3)

    def test_CreateAssessmentInfo_get_referenceNumber(self):
        self.assertEqual(
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.get_referenceNumber(),
            None
        )

        self.assertEqual(
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.get_referenceNumber(),
            TestCreateAssessmentInfo.COURSE_REFERENCE_NUMBER_ONE
        )

        self.assertEqual(
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.get_referenceNumber(),
            TestCreateAssessmentInfo.COURSE_REFERENCE_NUMBER_TWO
        )

    def test_CreateAssessmentInfo_set_grade(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_grade(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_grade({"E"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_grade(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_grade("E")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_grade("B")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_grade("C")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._grade, "E")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._grade, "B")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._grade, "C")

    def test_CreateAssessmentInfo_set_score(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_score("100")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_score(100.0)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_score("50")

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_score(100)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_score(50)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_score(75)

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._score, 100)
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._score, 50)
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._score, 75)

    def test_CreateAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_course_runId(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_course_runId({"course_run_id"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_course_runId(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_course_runId("course_run_id1")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_course_runId("course_run_id2")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_course_runId("course_run_id3")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._course_runId, "course_run_id1")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._course_runId, "course_run_id2")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._course_runId, "course_run_id3")

    def test_CreateAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_course_referenceNumber(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_course_referenceNumber({"course_reference_number"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_course_referenceNumber(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_course_referenceNumber("course_reference_number1")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_course_referenceNumber("course_reference_number2")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_course_referenceNumber("course_reference_number3")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._course_referenceNumber,
                         "course_reference_number1")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._course_referenceNumber,
                         "course_reference_number2")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._course_referenceNumber,
                         "course_reference_number3")

    def test_CreateAssessmentInfo_set_result(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_result(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_result({"result"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_result(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_result("Fail")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_result("Pass")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_result("Exempt")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._result, "Fail")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._result, "Pass")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._result, "Exempt")

    def test_CreateAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_traineeId(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_traineeId({"trainee_id"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_traineeId(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_traineeId("T0123456X")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_traineeId("S0123456Y")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_traineeId("T0123456Z")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_id, "T0123456X")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_id, "S0123456Y")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_id, "T0123456Z")

    def test_CreateAssessmentInfo_set_trainee_id_type(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainee_id_type(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainee_id_type({"NRIC"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainee_id_type(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainee_id_type(IdTypeSummary.FIN)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainee_id_type(IdTypeSummary.OTHERS)
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainee_id_type(IdTypeSummary.NRIC)

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_idType, "FIN")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_idType, "OTHERS")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_idType, "NRIC")

    def test_CreateAssessmentInfo_set_trainee_full_name(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainee_fullName(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainee_fullName({"trainee_full_name"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainee_fullName(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainee_fullName("John Doe")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainee_fullName("Jane Doe")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainee_fullName("Jack Doe")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_fullName, "John Doe")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_fullName, "Jane Doe")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_fullName, "Jack Doe")

    def test_CreateAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_skillCode(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_skillCode({"skill_code"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_skillCode(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_skillCode("CODE1")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_skillCode("CODE2")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_skillCode("CODE3")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._skillCode, "CODE1")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._skillCode, "CODE2")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._skillCode, "CODE3")

    def test_CreateAssessmentInfo_set_assessment_date(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_assessmentDate("2020-01-01")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_assessmentDate(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_assessmentDate(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_assessmentDate(date(2020, 1, 1))
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_assessmentDate(date(2020, 2, 2))
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_assessmentDate(date(2020, 3, 3))

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._assessmentDate, date(2020, 1, 1))
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._assessmentDate, date(2020, 2, 2))
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._assessmentDate, date(2020, 3, 3))

    def test_CreateAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainingPartner_uen(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainingPartner_uen({"12345678G"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainingPartner_uen(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainingPartner_uen("12345678G")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainingPartner_uen("87654321G")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainingPartner_uen("12348765G")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_uen, "12345678G")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_uen, "87654321G")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_uen, "12348765G")

    def test_CreateAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainingPartner_code(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainingPartner_code({"TP1"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainingPartner_code(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_trainingPartner_code("TP1")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_trainingPartner_code("TP2")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_trainingPartner_code("TP3")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_code, "TP1")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_code, "TP2")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_code, "TP3")

    def test_CreateAssessmentInfo_set_conferring_institute_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_conferringInstitute_code(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_conferringInstitute_code({"CI1"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_conferringInstitute_code(1.0)

        TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE.set_conferringInstitute_code("CI1")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO.set_conferringInstitute_code("CI2")
        TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE.set_conferringInstitute_code("CI3")

        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_ONE._conferringInstitute_code, "CI1")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_TWO._conferringInstitute_code, "CI2")
        self.assertEqual(TestCreateAssessmentInfo.CREATE_ASSESSMENT_THREE._conferringInstitute_code, "CI3")

    def test_UpdateVoidAssessmentInfo_validate(self):
        e1, _ = TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.validate()
        e2, _ = TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.validate()
        e3, _ = TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)  # blank instance have no action
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_UpdateVoidAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.payload()

        p2 = {
            'assessment': {
                'grade': 'A',
                'action': 'update',
                'result': 'Pass',
                'trainee': {
                    'fullName': 'John Doe'
                },
                'skillCode': 'CODE1',
                'assessmentDate': '2020-01-01'
            }
        }

        p3 = {
            'assessment': {
                'grade': 'E',
                'action': 'void',
                'result': 'Fail',
                'trainee': {
                    'fullName': 'Jane Doe'
                },
                'skillCode': 'CODE2',
                'assessmentDate': '2020-02-02'
            }
        }

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.payload(), p3)

    def test_UpdateVoidAssessmentInfo_get_referenceNumber(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.get_referenceNumber()

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.get_referenceNumber()

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.get_referenceNumber()

    def test_UpdateVoidAssessmentInfo_set_grade(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_grade(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_grade({"E"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_grade(1.0)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_grade("E")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_grade("B")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_grade("C")

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._grade, "E")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade, "B")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade, "C")

    def test_UpdateVoidAssessmentInfo_set_score(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_score("100")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_score(100.0)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_score("50")

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_score(100)
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_score(50)
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_score(75)

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._score, 100)
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._score, 50)
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._score, 75)

    def test_UpdateVoidAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_course_runId("course run 1")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_course_runId("course run 2")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_course_runId("course run 3")

    def test_UpdateVoidAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_course_referenceNumber("crn1")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_course_referenceNumber("crn2")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_course_referenceNumber("crn3")

    def test_UpdateVoidAssessmentInfo_set_result(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_result(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_result({"result"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_result(1.0)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_result("Fail")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_result("Pass")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_result("Exempt")

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._result, "Fail")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._result, "Pass")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._result, "Exempt")

    def test_UpdateVoidAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_traineeId("T0123456X")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_traineeId("S0123456X")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_traineeId("T0123456G")

    def test_UpdateVoidAssessmentInfo_set_trainee_id_type(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_trainee_id_type("FIN")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_trainee_id_type("OTHERS")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_trainee_id_type("NRIC")

    def test_UpdateVoidAssessmentInfo_set_trainee_full_name(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_trainee_fullName(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_trainee_fullName({"trainee_full_name"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_trainee_fullName(1.0)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_trainee_fullName("John Doe")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_trainee_fullName("Jane Doe")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_trainee_fullName("Jack Doe")

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._trainee_fullName, "John Doe")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._trainee_fullName, "Jane Doe")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._trainee_fullName, "Jack Doe")

    def test_UpdateVoidAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_skillCode(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_skillCode({"skill_code"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_skillCode(1.0)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_skillCode("CODE1")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_skillCode("CODE2")
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_skillCode("CODE3")

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._skillCode, "CODE1")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._skillCode, "CODE2")
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._skillCode, "CODE3")

    def test_UpdateVoidAssessmentInfo_set_assessment_date(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_assessmentDate("2020-01-01")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_assessmentDate(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_assessmentDate(1.0)

        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_assessmentDate(date(2020, 1, 1))
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_assessmentDate(date(2020, 2, 2))
        TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_assessmentDate(date(2020, 3, 3))

        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._assessmentDate, date(2020, 1, 1))
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._assessmentDate, date(2020, 2, 2))
        self.assertEqual(TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._assessmentDate, date(2020, 3, 3))

    def test_UpdateVoidAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_trainingPartner_uen("12345678G")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_trainingPartner_uen("87654321G")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_trainingPartner_uen("12348765G")

    def test_UpdateVoidAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_trainingPartner_code("TP1")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_trainingPartner_code("TP2")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_trainingPartner_code("TP3")

    def test_UpdateVoidAssessmentInfo_set_conferring_institute_code(self):
        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.set_conferringInstitute_code("CI1")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.set_conferringInstitute_code("CI2")

        with self.assertRaises(NotImplementedError):
            TestCreateAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.set_conferringInstitute_code("CI3")

    def test_SearchAssessmentInfo_validate(self):
        e1, _ = TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.validate()
        e2, _ = TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.validate()
        e3, _ = TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_SearchAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.payload()

        p2 = {
            'meta': {
                'lastUpdateDateTo': '2023-01-12',
                'lastUpdateDateFrom': '2023-01-01'
            },
            'sortBy': {
                'field': 'updatedOn',
                'order': 'asc'
            },
            'parameters': {
                'page': 1,
                'pageSize': 10
            },
            'assessment': {
                'course': {
                    'run': {
                        'id': 'course_run_id_1'
                    },
                    'referenceNumber': 'assessment_reference_number_1'
                }
            },
            'trainee': {
                'id': 'T0123456X'
            },
            'enrolment': {
                'referenceNumber': 'enrolment_reference_number_1'
            },
            'skillCode': 'CODE1',
            'trainingPartner': {
                'uen': '12345678G',
                'code': 'TP1'
            }
        }

        p3 = {
            'meta': {
                'lastUpdateDateTo': '2023-02-12',
                'lastUpdateDateFrom': '2023-02-01'
            },
            'sortBy': {
                'field': 'assessmentDate',
                'order': 'desc'
            },
            'parameters': {
                'page': 2,
                'pageSize': 20
            },
            'assessment': {
                'course': {
                    'run': {
                        'id': 'course_run_id_2'
                    },
                    'referenceNumber': 'assessment_reference_number_2'
                }
            },
            'trainee': {
                'id': 'S0123456Y'
            },
            'enrolment': {
                'referenceNumber': 'enrolment_reference_number_2'
            },
            'skillCode': 'CODE2',
            'trainingPartner': {
                'uen': '87654321G',
                'code': 'TP2'
            }
        }

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.payload(), p3)

    def test_SearchAssessmentInfo_set_last_update_date_to(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_lastUpdateDateTo("2020-01-01")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_lastUpdateDateTo(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_lastUpdateDateTo(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_lastUpdateDateTo(date(2020, 1, 1))
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_lastUpdateDateTo(date(2020, 2, 2))
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_lastUpdateDateTo(date(2020, 3, 3))

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateTo, date(2020, 1, 1))
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateTo, date(2020, 2, 2))
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateTo, date(2020, 3, 3))

    def test_SearchAssessmentInfo_set_last_update_date_from(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_lastUpdateDateFrom("2020-01-01")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_lastUpdateDateFrom(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_lastUpdateDateFrom(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_lastUpdateDateFrom(date(2020, 1, 1))
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_lastUpdateDateFrom(date(2020, 2, 2))
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_lastUpdateDateFrom(date(2020, 3, 3))

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateFrom, date(2020, 1, 1))
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateFrom, date(2020, 2, 2))
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateFrom, date(2020, 3, 3))

    def test_SearchAssessmentInfo_set_sort_by_field(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_sortBy_field(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_sortBy_field({"updatedOn"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_sortBy_field(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_sortBy_field(SortField.UPDATED_ON)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_sortBy_field(SortField.CREATED_ON)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_sortBy_field(SortField.ASSESSMENT_DATE)

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_field, "updatedOn")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_field, "createdOn")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_field, "assessmentDate")

    def test_SearchAssessmentInfo_set_sort_by_order(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_sortBy_order(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_sortBy_order({"asc"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_sortBy_order(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_sortBy_order(SortOrder.ASCENDING)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_sortBy_order(SortOrder.DESCENDING)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_sortBy_order(SortOrder.ASCENDING)

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_order, "asc")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_order, "desc")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_order, "asc")

    def test_SearchAssessmentInfo_set_page(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_page(1.0)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_page("1")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_page({"1"})

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_page(1)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_page(2)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_page(3)

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_page, 1)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_page, 2)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_page, 3)

    def test_SearchAssessmentInfo_set_page_size(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_pageSize(1.0)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_pageSize("1")

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_pageSize({"1"})

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_pageSize(1)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_pageSize(2)
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_pageSize(3)

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_pageSize, 1)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_pageSize, 2)
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_pageSize, 3)

    def test_SearchAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_courseRunId(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_courseRunId({"course_run_id"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_courseRunId(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_courseRunId("course_run_id1")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_courseRunId("course_run_id2")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_courseRunId("course_run_id3")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_courseRunId, "course_run_id1")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_courseRunId, "course_run_id2")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_courseRunId, "course_run_id3")

    def test_SearchAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_courseReferenceNumber(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_courseReferenceNumber({"course_reference_number"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_courseReferenceNumber(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_courseReferenceNumber("course_reference_number1")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_courseReferenceNumber("course_reference_number2")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_courseReferenceNumber("course_reference_number3")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_referenceNumber,
                         "course_reference_number1")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_referenceNumber,
                         "course_reference_number2")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_referenceNumber,
                         "course_reference_number3")

    def test_SearchAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_traineeId(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_traineeId({"trainee_id"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_traineeId(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_traineeId("T0123456X")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_traineeId("S0123456Y")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_traineeId("T0123456Z")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_traineeId, "T0123456X")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_traineeId, "S0123456Y")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId, "T0123456Z")

    def test_SearchAssessmentInfo_set_enrolment_reference_number(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_enrolment_referenceNumber(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_enrolment_referenceNumber({"enrolment_reference_number"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_enrolment_referenceNumber(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_enrolment_referenceNumber("enrolment_reference_number1")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_enrolment_referenceNumber("enrolment_reference_number2")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_enrolment_referenceNumber("enrolment_reference_number3")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number1")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number2")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number3")

    def test_SearchAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_skillCode(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_skillCode({"skill_code"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_skillCode(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_skillCode("CODE1")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_skillCode("CODE2")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_skillCode("CODE3")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_skillCode, "CODE1")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_skillCode, "CODE2")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_skillCode, "CODE3")

    def test_SearchAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_trainingPartner_code(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_trainingPartner_code({"TP1"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_trainingPartner_code(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_trainingPartner_code("TP1")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_trainingPartner_code("TP2")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_trainingPartner_code("TP3")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_code, "TP1")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_code, "TP2")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_code, "TP3")

    def test_SearchAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_trainingPartner_uen(1)

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_trainingPartner_uen({"12345678G"})

        with self.assertRaises(ValueError):
            TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_trainingPartner_uen(1.0)

        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE.set_trainingPartner_uen("12345678G")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO.set_trainingPartner_uen("87654321G")
        TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE.set_trainingPartner_uen("12348765G")

        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_uen, "12345678G")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_uen, "87654321G")
        self.assertEqual(TestCreateAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_uen, "12348765G")
