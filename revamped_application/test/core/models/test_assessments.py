"""
Contains test cases for CreateAssAssessmentInfo, UpdateVoidAssessmentInfo, and SearchAssessmentInfo.
"""

import unittest
from datetime import date

from revamped_application.core.constants import IdTypeSummary, SortOrder, SortField, Results, Grade, \
    AssessmentUpdateVoidActions
from revamped_application.core.models.assessments import (CreateAssessmentInfo, SearchAssessmentInfo,
                                                          UpdateVoidAssessmentInfo)


class TestAssessmentInfo(unittest.TestCase):
    """
    Test cases for CreateAssessmentInfo, UpdateVoidAssessmentInfo, and SearchAssessmentInfo.
    """

    GRADE_ONE = Grade.A
    GRADE_TWO = Grade.E
    GRADE_SCORE_ONE = 100
    GRADE_SCORE_TWO = 50
    COURSE_RUN_ID_ONE = "course_run_id_1"
    COURSE_RUN_ID_TWO = "course_run_id_2"
    COURSE_REFERENCE_NUMBER_ONE = "course_reference_number_1"
    COURSE_REFERENCE_NUMBER_TWO = "course_reference_number_2"
    RESULT_ONE = Results.PASS
    RESULT_TWO = Results.FAIL
    TRAINEE_ID_ONE = "T0123456X"
    TRAINEE_ID_TWO = "S0123456Y"
    TRAINEE_ID_TYPE_ONE = IdTypeSummary.NRIC
    TRAINEE_ID_TYPE_TWO = IdTypeSummary.OTHERS
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

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE = CreateAssessmentInfo()

        TestAssessmentInfo.CREATE_ASSESSMENT_TWO = CreateAssessmentInfo()
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._grade = TestAssessmentInfo.GRADE_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._score = TestAssessmentInfo.GRADE_SCORE_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_runId = TestAssessmentInfo.COURSE_RUN_ID_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_referenceNumber = (
            TestAssessmentInfo.COURSE_REFERENCE_NUMBER_ONE)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._result = (
            TestAssessmentInfo.RESULT_ONE)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_id = TestAssessmentInfo.TRAINEE_ID_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_idType = TestAssessmentInfo.TRAINEE_ID_TYPE_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_fullName = (
            TestAssessmentInfo.TRAINEE_FULL_NAME_ONE)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._skillCode = TestAssessmentInfo.SKILL_CODE_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._assessmentDate = TestAssessmentInfo.ASSESSMENT_DATE_ONE
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_code = (
            TestAssessmentInfo.TRAINING_PARTNER_CODE_ONE)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_uen = (
            TestAssessmentInfo.TRAINING_PARTNER_UEN_ONE)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO._conferringInstitute_code = (
            TestAssessmentInfo.CONFERRING_INSTITUTE_CODE_ONE)

        TestAssessmentInfo.CREATE_ASSESSMENT_THREE = CreateAssessmentInfo()
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._grade = TestAssessmentInfo.GRADE_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._score = TestAssessmentInfo.GRADE_SCORE_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_runId = TestAssessmentInfo.COURSE_RUN_ID_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_referenceNumber = (
            TestAssessmentInfo.COURSE_REFERENCE_NUMBER_TWO)
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._result = TestAssessmentInfo.RESULT_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_id = TestAssessmentInfo.TRAINEE_ID_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_idType = TestAssessmentInfo.TRAINEE_ID_TYPE_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_fullName = (
            TestAssessmentInfo.TRAINEE_FULL_NAME_TWO)
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._skillCode = TestAssessmentInfo.SKILL_CODE_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._assessmentDate = TestAssessmentInfo.ASSESSMENT_DATE_TWO
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_code = (
            TestAssessmentInfo.TRAINING_PARTNER_CODE_TWO)
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_uen = (
            TestAssessmentInfo.TRAINING_PARTNER_UEN_TWO)
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE._conferringInstitute_code = (
            TestAssessmentInfo.CONFERRING_INSTITUTE_CODE_TWO)

    def __set_up_update_void_assessment_info(self):
        """Set up the UpdateVoidAssessmentInfo instances."""

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE = UpdateVoidAssessmentInfo()

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO = UpdateVoidAssessmentInfo()
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade = TestAssessmentInfo.GRADE_ONE
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._score = TestAssessmentInfo.GRADE_SCORE_ONE
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._action = AssessmentUpdateVoidActions.UPDATE
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._result = TestAssessmentInfo.RESULT_ONE
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._trainee_fullName = (
            TestAssessmentInfo.TRAINEE_FULL_NAME_ONE)
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._skillCode = TestAssessmentInfo.SKILL_CODE_ONE
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._assessmentDate = (
            TestAssessmentInfo.ASSESSMENT_DATE_ONE)

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE = UpdateVoidAssessmentInfo()
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade = TestAssessmentInfo.GRADE_TWO
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._score = TestAssessmentInfo.GRADE_SCORE_TWO
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._action = AssessmentUpdateVoidActions.VOID
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._result = TestAssessmentInfo.RESULT_TWO
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._trainee_fullName = (
            TestAssessmentInfo.TRAINEE_FULL_NAME_TWO)
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._skillCode = TestAssessmentInfo.SKILL_CODE_TWO
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._assessmentDate = (
            TestAssessmentInfo.ASSESSMENT_DATE_TWO)

    def __set_up_search_assessment_info(self):
        """Set up the SearchAssessmentInfo instances."""

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE = SearchAssessmentInfo()

        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO = SearchAssessmentInfo()
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateTo = TestAssessmentInfo.LAST_UPDATE_TO_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateFrom = (
            TestAssessmentInfo.LAST_UPDATE_FROM_ONE)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_field = TestAssessmentInfo.SORT_BY_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_order = TestAssessmentInfo.SORT_ORDER_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_page = TestAssessmentInfo.PAGE_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_pageSize = TestAssessmentInfo.PAGE_SIZE_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_courseRunId = (
            TestAssessmentInfo.COURSE_RUN_ID_ONE)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_referenceNumber = (
            TestAssessmentInfo.ASSESSMENT_REFERENCE_NUMBER_ONE)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_traineeId = TestAssessmentInfo.TRAINEE_ID_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_enrolement_referenceNumber = (
            TestAssessmentInfo.ENROLMENT_REFERENCE_NUMBER_ONE
        )
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_skillCode = TestAssessmentInfo.SKILL_CODE_ONE
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_uen = (
            TestAssessmentInfo.TRAINING_PARTNER_UEN_ONE)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_code = (
            TestAssessmentInfo.TRAINING_PARTNER_CODE_ONE)

        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE = SearchAssessmentInfo()
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateTo = TestAssessmentInfo.LAST_UPDATE_TO_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateFrom = (
            TestAssessmentInfo.LAST_UPDATE_FROM_TWO)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_field = TestAssessmentInfo.SORT_BY_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_order = (
            TestAssessmentInfo.SORT_ORDER_TWO)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_page = TestAssessmentInfo.PAGE_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_pageSize = TestAssessmentInfo.PAGE_SIZE_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_courseRunId = (
            TestAssessmentInfo.COURSE_RUN_ID_TWO)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_referenceNumber = (
            TestAssessmentInfo.ASSESSMENT_REFERENCE_NUMBER_TWO)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId = TestAssessmentInfo.TRAINEE_ID_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber = (
            TestAssessmentInfo.ENROLMENT_REFERENCE_NUMBER_TWO
        )
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_skillCode = TestAssessmentInfo.SKILL_CODE_TWO
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_uen = (
            TestAssessmentInfo.TRAINING_PARTNER_UEN_TWO)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_code = (
            TestAssessmentInfo.TRAINING_PARTNER_CODE_TWO)

    def setUp(self):
        """Create the objects to test"""

        self.__set_up_create_assessment_info()
        self.__set_up_update_void_assessment_info()
        self.__set_up_search_assessment_info()

    def test_CreateAssessmentInfo_equality(self):
        """
        Test the equality of the CreateAssessmentInfo instances.
        """

        self.assertEqual(vars(TestAssessmentInfo.CREATE_ASSESSMENT_ONE),
                         vars(TestAssessmentInfo.CREATE_ASSESSMENT_ONE))
        self.assertEqual(vars(TestAssessmentInfo.CREATE_ASSESSMENT_TWO),
                         vars(TestAssessmentInfo.CREATE_ASSESSMENT_TWO))
        self.assertEqual(vars(TestAssessmentInfo.CREATE_ASSESSMENT_THREE),
                         vars(TestAssessmentInfo.CREATE_ASSESSMENT_THREE))

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE, TestAssessmentInfo.CREATE_ASSESSMENT_ONE)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO, TestAssessmentInfo.CREATE_ASSESSMENT_TWO)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE)

    def test_UpdateVoidAssessmentInfo_equality(self):
        """
        Test the equality of the UpdateVoidAssessmentInfo instances.
        """

        self.assertEqual(vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE),
                         vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE))
        self.assertEqual(vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO),
                         vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO))
        self.assertEqual(vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE),
                         vars(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE))

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)

    def test_SearchAssessmentInfo_equality(self):
        """
        Test the equality of the SearchAssessmentInfo instances.
        """

        self.assertEqual(vars(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE),
                         vars(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE))
        self.assertEqual(vars(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO),
                         vars(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO))
        self.assertEqual(vars(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE),
                         vars(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE))

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE)

    def test_CreateAssessmentInfo_inequality(self):
        self.assertNotEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE,
                            TestAssessmentInfo.CREATE_ASSESSMENT_TWO)
        self.assertNotEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE,
                            TestAssessmentInfo.CREATE_ASSESSMENT_THREE)
        self.assertNotEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO,
                            TestAssessmentInfo.CREATE_ASSESSMENT_THREE)

    def test_UpdateVoidAssessmentInfo_inequality(self):
        self.assertNotEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO)
        self.assertNotEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
                            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)
        self.assertNotEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
                            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE)

    def test_SearchAssessmentInfo_inequality(self):
        self.assertNotEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO)
        self.assertNotEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE,
                            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE)
        self.assertNotEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO,
                            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE)

    def test_all_inequality(self):
        test_array = [
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE,
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO,
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE,
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE,
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO,
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE,
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE,
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO,
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE
        ]

        for i in range(len(test_array)):
            for j in range(len(test_array)):
                if i == j:
                    continue

                self.assertNotEqual(test_array[i], test_array[j])

    def test_CreateAssessmentInfo_validate(self):
        e1, _ = TestAssessmentInfo.CREATE_ASSESSMENT_ONE.validate()
        e2, _ = TestAssessmentInfo.CREATE_ASSESSMENT_TWO.validate()
        e3, _ = TestAssessmentInfo.CREATE_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_CreateAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.payload()

        p2 = {
            "assessment": {
                "grade": "A",
                "score": 100,
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
                'score': 50,
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

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE.payload(), p3)

    def test_CreateAssessmentInfo_get_referenceNumber(self):
        self.assertEqual(
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_referenceNumber,
            None
        )

        self.assertEqual(
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_referenceNumber,
            TestAssessmentInfo.COURSE_REFERENCE_NUMBER_ONE
        )

        self.assertEqual(
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_referenceNumber,
            TestAssessmentInfo.COURSE_REFERENCE_NUMBER_TWO
        )

    def test_CreateAssessmentInfo_set_grade(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.grade = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.grade = {"E"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.grade = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.grade = Grade.E
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.grade = Grade.B
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.grade = Grade.C

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._grade, Grade.E)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._grade,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.grade)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._grade, Grade.B)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._grade,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.grade)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._grade, Grade.C)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._grade,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.grade)

    def test_CreateAssessmentInfo_set_score(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.score = "100"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.score = 100.0

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.score = "50"

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.score = 100
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.score = 50
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.score = 75

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._score, 100)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._score,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.score)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._score, 50)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._score,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.score)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._score, 75)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._score,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.score)

    def test_CreateAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_runId = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_runId = {"course_run_id"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_runId = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_runId = "course_run_id1"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_runId = "course_run_id2"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_runId = "course_run_id3"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._course_runId, "course_run_id1")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._course_runId,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_runId)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_runId, "course_run_id2")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_runId,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_runId)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_runId, "course_run_id3")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_runId,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_runId)

    def test_CreateAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_referenceNumber = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_referenceNumber = {"course_reference_number"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_referenceNumber = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_referenceNumber = "course_reference_number1"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_referenceNumber = "course_reference_number2"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_referenceNumber = "course_reference_number3"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._course_referenceNumber,
                         "course_reference_number1")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._course_referenceNumber,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.course_referenceNumber)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_referenceNumber,
                         "course_reference_number2")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._course_referenceNumber,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.course_referenceNumber)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_referenceNumber,
                         "course_reference_number3")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._course_referenceNumber,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.course_referenceNumber)

    def test_CreateAssessmentInfo_set_result(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.result = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.result = {"result"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.result = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.result = Results.FAIL
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.result = Results.PASS
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.result = Results.EXEMPT

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._result, Results.FAIL)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._result,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.result)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._result, Results.PASS)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._result,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.result)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._result, Results.EXEMPT)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._result,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.result)

    def test_CreateAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_id = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_id = {"trainee_id"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_id = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_id = "T0123456X"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_id = "S0123456Y"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_id = "T0123456Z"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_id, "T0123456X")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_id,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_id)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_id, "S0123456Y")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_id,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_id)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_id, "T0123456Z")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_id,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_id)

    def test_CreateAssessmentInfo_set_trainee_id_type(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_idType = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_idType = {"NRIC"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_idType = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_idType = IdTypeSummary.FIN
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_idType = IdTypeSummary.OTHERS
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_idType = IdTypeSummary.NRIC

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_idType, IdTypeSummary.FIN)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_idType,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_idType)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_idType, IdTypeSummary.OTHERS)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_idType,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_idType)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_idType, IdTypeSummary.NRIC)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_idType,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_idType)

    def test_CreateAssessmentInfo_set_trainee_full_name(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_fullName = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_fullName = {"trainee_full_name"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_fullName = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_fullName = "John Doe"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_fullName = "Jane Doe"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_fullName = "Jack Doe"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_fullName, "John Doe")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainee_fullName,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainee_fullName)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_fullName, "Jane Doe")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainee_fullName,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainee_fullName)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_fullName, "Jack Doe")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainee_fullName,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainee_fullName)

    def test_CreateAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.skillCode = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.skillCode = {"skill_code"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.skillCode = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.skillCode = "CODE1"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.skillCode = "CODE2"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.skillCode = "CODE3"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._skillCode, "CODE1")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._skillCode,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.skillCode)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._skillCode, "CODE2")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._skillCode,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.skillCode)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._skillCode, "CODE3")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._skillCode,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.skillCode)

    def test_CreateAssessmentInfo_set_assessment_date(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.assessmentDate = "2020-01-01"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.assessmentDate = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.assessmentDate = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.assessmentDate = date(2020, 1, 1)
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.assessmentDate = date(2020, 2, 2)
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.assessmentDate = date(2020, 3, 3)

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._assessmentDate, date(2020, 1, 1))
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._assessmentDate,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.assessmentDate)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._assessmentDate, date(2020, 2, 2))
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._assessmentDate,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.assessmentDate)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._assessmentDate, date(2020, 3, 3))
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._assessmentDate,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.assessmentDate)

    def test_CreateAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_uen = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_uen = {"12345678G"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_uen = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_uen = "12345678G"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_uen = "87654321G"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_uen = "12348765G"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_uen, "12345678G")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_uen,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_uen)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_uen, "87654321G")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_uen,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_uen)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_uen, "12348765G")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_uen,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_uen)

    def test_CreateAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_code = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_code = {"TP1"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_code = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_code = "TP1"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_code = "TP2"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_code = "TP3"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_code, "TP1")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._trainingPartner_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.trainingPartner_code)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_code, "TP2")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._trainingPartner_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.trainingPartner_code)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_code, "TP3")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._trainingPartner_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.trainingPartner_code)

    def test_CreateAssessmentInfo_set_conferring_institute_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_ONE.conferringInstitute_code = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_TWO.conferringInstitute_code = {"CI1"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.CREATE_ASSESSMENT_THREE.conferringInstitute_code = 1.0

        TestAssessmentInfo.CREATE_ASSESSMENT_ONE.conferringInstitute_code = "CI1"
        TestAssessmentInfo.CREATE_ASSESSMENT_TWO.conferringInstitute_code = "CI2"
        TestAssessmentInfo.CREATE_ASSESSMENT_THREE.conferringInstitute_code = "CI3"

        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._conferringInstitute_code, "CI1")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_ONE._conferringInstitute_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_ONE.conferringInstitute_code)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._conferringInstitute_code, "CI2")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_TWO._conferringInstitute_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_TWO.conferringInstitute_code)
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._conferringInstitute_code, "CI3")
        self.assertEqual(TestAssessmentInfo.CREATE_ASSESSMENT_THREE._conferringInstitute_code,
                         TestAssessmentInfo.CREATE_ASSESSMENT_THREE.conferringInstitute_code)

    def test_UpdateVoidAssessmentInfo_validate(self):
        e1, _ = TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.validate()
        e2, _ = TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.validate()
        e3, _ = TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)  # blank instance have no action
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_UpdateVoidAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.payload()

        p2 = {
            'assessment': {
                'grade': 'A',
                'score': 100,
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
                'score': 50,
                'action': 'void',
                'result': 'Fail',
                'trainee': {
                    'fullName': 'Jane Doe'
                },
                'skillCode': 'CODE2',
                'assessmentDate': '2020-02-02'
            }
        }

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.payload(), p3)

    def test_UpdateVoidAssessmentInfo_get_referenceNumber(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.course_referenceNumber()

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.course_referenceNumber()

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.course_referenceNumber()

    def test_UpdateVoidAssessmentInfo_set_grade(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.grade = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.grade = {"E"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.grade = 1.0

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.grade = Grade.E
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.grade = Grade.B
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.grade = Grade.C

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._grade, Grade.E)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._grade,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.grade)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade, Grade.B)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._grade,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.grade)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade, Grade.C)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._grade,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.grade)

    def test_UpdateVoidAssessmentInfo_setscore_(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.score = "100"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.score = 100.0

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.score = "50"

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.score = 100
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.score = 50
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.score = 75

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._score, 100)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._score,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.score)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._score, 50)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._score,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.score)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._score, 75)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._score,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.score)

    def test_UpdateVoidAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.course_runId = "course run 1"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.course_runId = "course run 2"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.course_runId = "course run 3"

    def test_UpdateVoidAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.course_referenceNumber = "crn1"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.course_referenceNumber = "crn2"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.course_referenceNumber = "crn3"

    def test_UpdateVoidAssessmentInfo_set_result(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.result = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.result = {"result"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.result = 1.0

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.result = Results.FAIL
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.result = Results.PASS
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.result = Results.EXEMPT

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._result, Results.FAIL)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._result,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.result)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._result, Results.PASS)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._result,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.result)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._result, Results.EXEMPT)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._result,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.result)

    def test_UpdateVoidAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainee_id = "T0123456X"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainee_id = "S0123456X"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainee_id = "T0123456G"

    def test_UpdateVoidAssessmentInfo_set_trainee_id_type(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainee_idType = "FIN"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainee_idType = "OTHERS"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainee_idType = "NRIC"

    def test_UpdateVoidAssessmentInfo_set_trainee_full_name(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainee_fullName = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainee_fullName = {"trainee_full_name"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainee_fullName = 1.0

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainee_fullName = "John Doe"
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainee_fullName = "Jane Doe"
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainee_fullName = "Jack Doe"

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._trainee_fullName, "John Doe")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._trainee_fullName,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainee_fullName)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._trainee_fullName, "Jane Doe")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._trainee_fullName,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainee_fullName)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._trainee_fullName, "Jack Doe")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._trainee_fullName,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainee_fullName)

    def test_UpdateVoidAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.skillCode = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.skillCode = {"skill_code"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.skillCode = 1.0

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.skillCode = "CODE1"
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.skillCode = "CODE2"
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.skillCode = "CODE3"

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._skillCode, "CODE1")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._skillCode,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.skillCode)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._skillCode, "CODE2")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._skillCode,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.skillCode)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._skillCode, "CODE3")
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._skillCode,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.skillCode)

    def test_UpdateVoidAssessmentInfo_set_assessment_date(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.assessmentDate = "2020-01-01"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.assessmentDate = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.assessmentDate = 1.0

        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.assessmentDate = date(2020, 1, 1)
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.assessmentDate = date(2020, 2, 2)
        TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.assessmentDate = date(2020, 3, 3)

        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._assessmentDate, date(2020, 1, 1))
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE._assessmentDate,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.assessmentDate)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._assessmentDate, date(2020, 2, 2))
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO._assessmentDate,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.assessmentDate)
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._assessmentDate, date(2020, 3, 3))
        self.assertEqual(TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE._assessmentDate,
                         TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.assessmentDate)

    def test_UpdateVoidAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainingPartner_uen = "12345678G"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainingPartner_uen = "87654321G"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainingPartner_uen = "12348765G"

    def test_UpdateVoidAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.trainingPartner_code = "TP1"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.trainingPartner_code = "TP2"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.trainingPartner_code = "TP3"

    def test_UpdateVoidAssessmentInfo_set_conferring_institute_code(self):
        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_ONE.conferringInstitute_code = "CI1"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_TWO.conferringInstitute_code = "CI2"

        with self.assertRaises(NotImplementedError):
            TestAssessmentInfo.UPDATE_VOID_ASSESSMENT_THREE.conferringInstitute_code = "CI3"

    def test_SearchAssessmentInfo_validate(self):
        e1, _ = TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.validate()
        e2, _ = TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.validate()
        e3, _ = TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_SearchAssessmentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.payload()

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

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.payload(), p2)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.payload(), p3)

    def test_SearchAssessmentInfo_set_last_update_date_to(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateTo = "2020-01-01"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateTo = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateTo = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateTo = date(2020, 1, 1)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateTo = date(2020, 2, 2)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateTo = date(2020, 3, 3)

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateTo, date(2020, 1, 1))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateTo,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateTo)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateTo, date(2020, 2, 2))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateTo,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateTo)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateTo, date(2020, 3, 3))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateTo,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateTo)

    def test_SearchAssessmentInfo_set_last_update_date_from(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateFrom = "2020-01-01"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateFrom = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateFrom = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateFrom = date(2020, 1, 1)
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateFrom = date(2020, 2, 2)
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateFrom = date(2020, 3, 3)

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateFrom, date(2020, 1, 1))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._lastUpdateDateFrom,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.lastUpdateDateFrom)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateFrom, date(2020, 2, 2))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._lastUpdateDateFrom,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.lastUpdateDateFrom)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateFrom, date(2020, 3, 3))
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._lastUpdateDateFrom,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.lastUpdateDateFrom)

    def test_SearchAssessmentInfo_set_sort_by_field(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_field = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_field = {"updatedOn"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_field = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_field = SortField.UPDATED_ON
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_field = SortField.CREATED_ON
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_field = SortField.ASSESSMENT_DATE

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_field, SortField.UPDATED_ON)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_field,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_field)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_field, SortField.CREATED_ON)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_field,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_field)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_field, SortField.ASSESSMENT_DATE)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_field,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_field)

    def test_SearchAssessmentInfo_set_sort_by_order(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_order = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_order = {"asc"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_order = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_order = SortOrder.ASCENDING
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_order = SortOrder.DESCENDING
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_order = SortOrder.ASCENDING

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_order, SortOrder.ASCENDING)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._sortBy_order,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.sortBy_order)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_order, SortOrder.DESCENDING)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._sortBy_order,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.sortBy_order)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_order, SortOrder.ASCENDING)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._sortBy_order,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.sortBy_order)

    def test_SearchAssessmentInfo_set_page(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.page = 1.0

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.page = "1"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.page = {"1"}

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.page = 1
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.page = 2
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.page = 3

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_page, 1)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_page,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.page)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_page, 2)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_page,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.page)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_page, 3)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_page,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.page)

    def test_SearchAssessmentInfo_set_page_size(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.pageSize = 1.0

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.pageSize = "1"

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.pageSize = {"1"}

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.pageSize = 1
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.pageSize = 2
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.pageSize = 3

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_pageSize, 1)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._parameters_pageSize,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.pageSize)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_pageSize, 2)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._parameters_pageSize,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.pageSize)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_pageSize, 3)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._parameters_pageSize,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.pageSize)

    def test_SearchAssessmentInfo_set_course_run_id(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseRunId = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseRunId = {"course_run_id"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseRunId = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseRunId = "course_run_id1"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseRunId = "course_run_id2"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseRunId = "course_run_id3"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_courseRunId, "course_run_id1")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_courseRunId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseRunId)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_courseRunId, "course_run_id2")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_courseRunId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseRunId)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_courseRunId, "course_run_id3")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_courseRunId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseRunId)

    def test_SearchAssessmentInfo_set_course_reference_number(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseReferenceNumber = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseReferenceNumber = {"course_reference_number"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseReferenceNumber = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseReferenceNumber = "course_reference_number1"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseReferenceNumber = "course_reference_number2"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseReferenceNumber = "course_reference_number3"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_referenceNumber,
                         "course_reference_number1")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.courseReferenceNumber)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_referenceNumber,
                         "course_reference_number2")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.courseReferenceNumber)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_referenceNumber,
                         "course_reference_number3")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.courseReferenceNumber)

    def test_SearchAssessmentInfo_set_trainee_id(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainee_id = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainee_id = {"trainee_id"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainee_id = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainee_id = "T0123456X"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainee_id = "S0123456Y"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainee_id = "T0123456Z"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_traineeId, "T0123456X")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_traineeId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainee_id)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_traineeId, "S0123456Y")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_traineeId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainee_id)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId, "T0123456Z")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_traineeId)

    def test_SearchAssessmentInfo_set_enrolment_reference_number(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.enrolment_referenceNumber = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.enrolment_referenceNumber = {"enrolment_reference_number"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.enrolment_referenceNumber = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.enrolment_referenceNumber = "enrolment_reference_number1"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.enrolment_referenceNumber = "enrolment_reference_number2"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.enrolment_referenceNumber = "enrolment_reference_number3"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number1")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_enrolement_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.enrolment_referenceNumber)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number2")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_enrolement_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.enrolment_referenceNumber)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber,
                         "enrolment_reference_number3")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_enrolement_referenceNumber)

    def test_SearchAssessmentInfo_set_skill_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.skillCode = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.skillCode = {"skill_code"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.skillCode = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.skillCode = "CODE1"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.skillCode = "CODE2"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.skillCode = "CODE3"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_skillCode, "CODE1")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._assessment_skillCode,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.skillCode)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_skillCode, "CODE2")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._assessment_skillCode,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.skillCode)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_skillCode, "CODE3")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._assessment_skillCode,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.skillCode)

    def test_SearchAssessmentInfo_set_training_partner_code(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_code = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_code = {"TP1"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_code = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_code = "TP1"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_code = "TP2"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_code = "TP3"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_code, "TP1")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_code,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_code)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_code, "TP2")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_code,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_code)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_code, "TP3")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_code,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_code)

    def test_SearchAssessmentInfo_set_training_partner_uen(self):
        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_uen = 1

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_uen = {"12345678G"}

        with self.assertRaises(ValueError):
            TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_uen = 1.0

        TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_uen = "12345678G"
        TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_uen = "87654321G"
        TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_uen = "12348765G"

        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_uen, "12345678G")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_ONE._trainingPartner_uen,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_ONE.trainingPartner_uen)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_uen, "87654321G")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_TWO._trainingPartner_uen,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_TWO.trainingPartner_uen)
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_uen, "12348765G")
        self.assertEqual(TestAssessmentInfo.SEARCH_ASSESSMENT_THREE._trainingPartner_uen,
                         TestAssessmentInfo.SEARCH_ASSESSMENT_THREE.trainingPartner_uen)
