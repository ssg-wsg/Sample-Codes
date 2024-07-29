"""
Tests for the classes related to SF Credit Pay API.
"""
import base64
import datetime
import os
import unittest

from streamlit.proto.Common_pb2 import FileURLs as FileURLsProto
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

from app.core.constants import PermittedFileUploadType, CancelClaimsCode
from app.core.models.credit import EncryptPayloadInfo, DecryptPayloadInfo, DocumentInfo, \
    CancelClaimsInfo, UploadDocumentInfo
from app.test.utils.test_verify import TestVerify
from app.test.resources.definitions import RESOURCES_PATH


class TestSFCreditInfo(unittest.TestCase):
    COURSE_ID_ONE = "course_id_one"
    COURSE_ID_TWO = "course_id_two"
    COURSE_FEE_ONE = 12.34
    COURSE_FEE_TWO = 56.78
    COURSE_RUN_ID_ONE = "course_run_id_one"
    COURSE_RUN_ID_TWO = "course_run_id_two"
    COURSE_START_DATE_ONE = datetime.date(2020, 1, 1)
    COURSE_START_DATE_TWO = datetime.date(2020, 2, 1)
    NRIC_ONE = TestVerify.VALID_NRICS[0]
    NRIC_TWO = TestVerify.VALID_NRICS[1]
    EMAIL_ONE = "john@email.com"
    EMAIL_TWO = "emily@email.com"
    HOME_PHONE_ONE = "81234567"
    HOME_PHONE_TWO = "87654321"
    MOBILE_PHONE_ONE = "91234567"
    MOBILE_PHONE_TWO = "98765432"
    ADDITIONAL_INFO_ONE = "additional_info_one"
    ADDITIONAL_INFO_TWO = "additional_info_two"
    ENCRYPTED_PAYLOAD = "encrypted_payload"
    FILE_NAME_ONE = "file.pdf"
    FILE_NAME_TWO = "file.docx"
    FILE_NAME_THREE = "abc.jpg"
    FILE_SIZE_ONE = "1 MB"
    FILE_SIZE_TWO = "2 MB"
    FILE_TYPE_ONE = PermittedFileUploadType.PDF
    FILE_TYPE_TWO = PermittedFileUploadType.DOCX
    ATTACHMENT_ID_ONE = "attachment_one"
    ATTACHMENT_ID_TWO = "attachment_two"
    CANCEL_CLAIMS_CODE_ONE = CancelClaimsCode.COURSE_CANCELLED
    CANCEL_CLAIMS_CODE_TWO = CancelClaimsCode.NOT_ENROLLED

    with (open(os.path.join(RESOURCES_PATH, "core", "models", FILE_NAME_ONE), "rb") as file1,
          open(os.path.join(RESOURCES_PATH, "core", "models", FILE_NAME_TWO), "rb") as file2):
        ATTACHMENT_BYTES_ONE = UploadedFile(
            UploadedFileRec(
                file_id="file_id_1",
                name=FILE_NAME_ONE,
                type="jpg",
                data=file1.read(),
            ),
            FileURLsProto()
        )

        ATTACHMENT_BYTES_TWO = UploadedFile(
            UploadedFileRec(
                file_id="file_id_2",
                name=FILE_NAME_TWO,
                type="jpg",
                data=file2.read(),
            ),
            FileURLsProto()
        )

    ENCRYPT_PAYLOAD_ONE: EncryptPayloadInfo = None
    ENCRYPT_PAYLOAD_TWO: EncryptPayloadInfo = None
    ENCRYPT_PAYLOAD_THREE: EncryptPayloadInfo = None

    DECRYPT_PAYLOAD_ONE: DecryptPayloadInfo = None
    DECRYPT_PAYLOAD_TWO: DecryptPayloadInfo = None

    DOCUMENT_INFO_ONE: DocumentInfo = None
    DOCUMENT_INFO_TWO: DocumentInfo = None
    DOCUMENT_INFO_THREE: DocumentInfo = None

    UPLOAD_DOCUMENT_INFO_ONE: UploadDocumentInfo = None
    UPLOAD_DOCUMENT_INFO_TWO: UploadDocumentInfo = None
    UPLOAD_DOCUMENT_INFO_THREE: UploadDocumentInfo = None

    CANCEL_CLAIMS_INFO_ONE: CancelClaimsInfo = None
    CANCEL_CLAIMS_INFO_TWO: CancelClaimsInfo = None
    CANCEL_CLAIMS_INFO_THREE: CancelClaimsInfo = None

    DOCUMENT_LIST_ONE: list[DocumentInfo] = None
    DOCUMENT_LIST_TWO: list[DocumentInfo] = None

    @staticmethod
    def __set_up_encrypt_payload():
        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE = EncryptPayloadInfo()

        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO = EncryptPayloadInfo()
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_id = TestSFCreditInfo.COURSE_ID_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_fee = TestSFCreditInfo.COURSE_FEE_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_run_id = TestSFCreditInfo.COURSE_RUN_ID_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_start_date = TestSFCreditInfo.COURSE_START_DATE_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.nric = TestSFCreditInfo.NRIC_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.email = TestSFCreditInfo.EMAIL_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.home_phone = TestSFCreditInfo.HOME_PHONE_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.mobile_phone = TestSFCreditInfo.MOBILE_PHONE_ONE
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.additional_info = TestSFCreditInfo.ADDITIONAL_INFO_ONE

        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE = EncryptPayloadInfo()
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_id = TestSFCreditInfo.COURSE_ID_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_fee = TestSFCreditInfo.COURSE_FEE_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_run_id = TestSFCreditInfo.COURSE_RUN_ID_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_start_date = TestSFCreditInfo.COURSE_START_DATE_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.nric = TestSFCreditInfo.NRIC_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.email = TestSFCreditInfo.EMAIL_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.home_phone = TestSFCreditInfo.HOME_PHONE_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.mobile_phone = TestSFCreditInfo.MOBILE_PHONE_TWO
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.additional_info = TestSFCreditInfo.ADDITIONAL_INFO_TWO

    @staticmethod
    def __set_up_decrypt_payload():
        TestSFCreditInfo.DECRYPT_PAYLOAD_ONE = DecryptPayloadInfo()

        TestSFCreditInfo.DECRYPT_PAYLOAD_TWO = DecryptPayloadInfo()
        TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.encrypted_request = TestSFCreditInfo.ENCRYPTED_PAYLOAD

    @staticmethod
    def __set_up_document_info():
        TestSFCreditInfo.DOCUMENT_INFO_ONE = DocumentInfo()

        TestSFCreditInfo.DOCUMENT_INFO_TWO = DocumentInfo()
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_name = TestSFCreditInfo.FILE_NAME_ONE
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_size = TestSFCreditInfo.FILE_SIZE_ONE
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_type = TestSFCreditInfo.FILE_TYPE_ONE
        TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_id = TestSFCreditInfo.ATTACHMENT_ID_ONE
        TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_bytes = TestSFCreditInfo.ATTACHMENT_BYTES_ONE

        TestSFCreditInfo.DOCUMENT_INFO_THREE = DocumentInfo()
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_name = TestSFCreditInfo.FILE_NAME_TWO
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_size = TestSFCreditInfo.FILE_SIZE_TWO
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_type = TestSFCreditInfo.FILE_TYPE_TWO
        TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_id = TestSFCreditInfo.ATTACHMENT_ID_TWO
        TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_bytes = TestSFCreditInfo.ATTACHMENT_BYTES_TWO

        TestSFCreditInfo.DOCUMENT_LIST_ONE = [TestSFCreditInfo.DOCUMENT_INFO_TWO]
        TestSFCreditInfo.DOCUMENT_LIST_TWO = [TestSFCreditInfo.DOCUMENT_INFO_TWO, TestSFCreditInfo.DOCUMENT_INFO_THREE]

    @staticmethod
    def __set_up_upload_document_info():
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE = UploadDocumentInfo()

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO = UploadDocumentInfo()
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.nric = TestSFCreditInfo.NRIC_ONE
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.documents = TestSFCreditInfo.DOCUMENT_LIST_ONE

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE = UploadDocumentInfo()
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.nric = TestSFCreditInfo.NRIC_TWO
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.documents = TestSFCreditInfo.DOCUMENT_LIST_TWO

    @staticmethod
    def __set_up_cancel_claims_info():
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE = CancelClaimsInfo()

        TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO = CancelClaimsInfo()
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.nric = TestSFCreditInfo.NRIC_ONE
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.cancel_claims_code = TestSFCreditInfo.CANCEL_CLAIMS_CODE_ONE

        TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE = CancelClaimsInfo()
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.nric = TestSFCreditInfo.NRIC_TWO
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.cancel_claims_code = TestSFCreditInfo.CANCEL_CLAIMS_CODE_TWO

    def setUp(self):
        self.__set_up_encrypt_payload()
        self.__set_up_decrypt_payload()
        self.__set_up_document_info()
        self.__set_up_upload_document_info()
        self.__set_up_cancel_claims_info()

    def test_encrypt_payload_info_equality(self):
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE, TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE, TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE)

    def test_decrypt_payload_info_equality(self):
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_ONE, TestSFCreditInfo.DECRYPT_PAYLOAD_ONE)
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_TWO, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO)

    def test_document_info_equality(self):
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE, TestSFCreditInfo.DOCUMENT_INFO_ONE)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO, TestSFCreditInfo.DOCUMENT_INFO_TWO)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE, TestSFCreditInfo.DOCUMENT_INFO_THREE)

    def test_upload_document_info_equality(self):
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE)

    def test_cancel_claims_info_equality(self):
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE, TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE)

    def test_encrypt_payload_info_inequality(self):
        for info in [TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO,
                     TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE]:
            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO)

            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE)

    def test_decrypt_payload_info_inequality(self):
        for info in [TestSFCreditInfo.DECRYPT_PAYLOAD_ONE, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO]:
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE)

    def test_document_info_info_inequality(self):
        for info in [TestSFCreditInfo.DOCUMENT_INFO_ONE, TestSFCreditInfo.DOCUMENT_INFO_TWO,
                     TestSFCreditInfo.DOCUMENT_INFO_THREE]:
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO)

            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE)

    def test_upload_document_info_inequality(self):
        for info in [TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO,
                     TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE]:
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO)

            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE)

    def test_cancel_claims_info_inequality(self):
        for info in [TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO,
                     TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE]:
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DECRYPT_PAYLOAD_TWO)

            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.DOCUMENT_INFO_THREE)

            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO)
            self.assertNotEqual(info, TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE)

    def test_EncryptPayloadInfo_validate(self):
        e1, _ = TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.validate()
        e2, _ = TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.validate()
        e3, _ = TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_EncryptPayloadInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.payload()

        p1 = {
            'claimRequest': {
                'course': {
                    'id': 'course_id_one',
                    'fee': '12.34',
                    'runId': 'course_run_id_one'
                },
                'individual': {
                    'nric': 'F3875860T',
                    'email': 'john@email.com'
                }
            }
        }

        p2 = {
            'claimRequest': {
                'course': {
                    'id': 'course_id_two',
                    'fee': '56.78',
                    'runId': 'course_run_id_two'
                },
                'individual': {
                    'nric': 'G3327819K',
                    'email': 'emily@email.com'
                }
            }
        }

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.payload(), p1)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.payload(), p2)

    def test_EncryptPayloadInfo_course_id(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_id = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_id = ["hello"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_id = {"abc"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_id = "course_id_1"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_id = "course_id_2"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_id = "course_id_3"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_id, "course_id_1")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_id)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_id, "course_id_2")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_id)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_id, "course_id_3")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_id)

    def test_EncryptPayloadInfo_course_fee(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_fee = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_fee = ["hello"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_fee = {"abc"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_fee = 123.22
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_fee = 1000.00
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_fee = 321.12

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_fee, 123.22)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_fee,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_fee)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_fee, 1000.00)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_fee,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_fee)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_fee, 321.12)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_fee,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_fee)

    def test_EncryptPayloadInfo_course_run_id(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_run_id = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_run_id = ["hello"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_run_id = {"abc"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_run_id = "course_run_id_1"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_run_id = "course_run_id_2"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_run_id = "course_run_id_3"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_run_id, "course_run_id_1")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._course_run_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.course_run_id)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_run_id, "course_run_id_2")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._course_run_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.course_run_id)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_run_id, "course_run_id_3")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._course_run_id,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.course_run_id)

    def test_EncryptPayloadInfo_start_date(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.start_date = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.start_date = [datetime.date(2024, 1, 2)]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.start_date = {datetime.date(2024, 1, 2)}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.start_date = datetime.date(2023, 1, 2)
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.start_date = datetime.date(2024, 1, 2)
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.start_date = datetime.date(2025, 1, 2)

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._startDate, datetime.date(2023, 1, 2))
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._startDate,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.start_date)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._startDate, datetime.date(2024, 1, 2))
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._startDate,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.start_date)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._startDate, datetime.date(2025, 1, 2))
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._startDate,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.start_date)

    def test_EncryptPayloadInfo_nric(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.nric = 123456789

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.nric = ["T0123456X"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.nric = {"T0123456X"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.nric = "T0123456X"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.nric = "S0123456X"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.nric = "T0123444X"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._nric, "T0123456X")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._nric,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.nric)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._nric, "S0123456X")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._nric,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.nric)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._nric, "T0123444X")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._nric,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.nric)

    def test_EncryptPayloadInfo_email(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.email = 123456789

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.email = ["john@email.com"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.email = {"john@email.com"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.email = "john@email.com"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.email = "emily@email.com"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.email = "jake@email.com"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._email, "john@email.com")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._email,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.email)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._email, "emily@email.com")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._email,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.email)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._email, "jake@email.com")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._email,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.email)

    def test_EncryptPayloadInfo_home_number(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.home_number = 91234567

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.home_number = ["91234567"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.home_number = {"91234567"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.home_number = "91234567"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.home_number = "81234567"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.home_number = "91234563"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._homeNumber, "91234567")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._homeNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.home_number)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._homeNumber, "81234567")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._homeNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.home_number)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._homeNumber, "91234563")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._homeNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.home_number)

    def test_EncryptPayloadInfo_mobile_number(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.mobile_number = 91234567

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.mobile_number = ["91234567"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.mobile_number = {"91234567"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.mobile_number = "91234567"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.mobile_number = "81234567"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.mobile_number = "91234563"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._mobileNumber, "91234567")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._mobileNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.mobile_number)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._mobileNumber, "81234567")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._mobileNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.mobile_number)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._mobileNumber, "91234563")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._mobileNumber,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.mobile_number)

    def test_EncryptPayloadInfo_additional_information(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.additional_information = 91234567

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.additional_information = ["additional info"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.additional_information = {"additional info"}

        TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.additional_information = "additional info 1"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.additional_information = "additional info 2"
        TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.additional_information = "additional info 3"

        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._additionalInformation, "additional info 1")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE._additionalInformation,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_ONE.additional_information)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._additionalInformation, "additional info 2")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO._additionalInformation,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_TWO.additional_information)
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._additionalInformation, "additional info 3")
        self.assertEqual(TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE._additionalInformation,
                         TestSFCreditInfo.ENCRYPT_PAYLOAD_THREE.additional_information)

    def test_DecryptPayloadInfo_validate(self):
        e1, _ = TestSFCreditInfo.DECRYPT_PAYLOAD_ONE.validate()
        e2, _ = TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.validate()

        self.assertTrue(len(e1) == 0)
        self.assertTrue(len(e2) == 0)

    def test_DecryptPayloadInfo_payload(self):
        p1 = {}
        p2 = {
            "claimRequestStatus": "encrypted_payload"
        }

        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_ONE.payload(), p1)
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.payload(), p2)

    def test_DecryptPayloadInfo_encrypted_request(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DECRYPT_PAYLOAD_ONE.encrypted_request = 91234567

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.encrypted_request = ["encrypted 1"]

        TestSFCreditInfo.DECRYPT_PAYLOAD_ONE.encrypted_request = "encrypted 1"
        TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.encrypted_request = "encrypted 2"

        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_ONE._encrypted_request, "encrypted 1")
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_ONE._encrypted_request,
                         TestSFCreditInfo.DECRYPT_PAYLOAD_ONE.encrypted_request)
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_TWO._encrypted_request, "encrypted 2")
        self.assertEqual(TestSFCreditInfo.DECRYPT_PAYLOAD_TWO._encrypted_request,
                         TestSFCreditInfo.DECRYPT_PAYLOAD_TWO.encrypted_request)

    def test_TestDocumentInfo_validate(self):
        e1, _ = TestSFCreditInfo.DOCUMENT_INFO_ONE.validate()
        e2, _ = TestSFCreditInfo.DOCUMENT_INFO_TWO.validate()
        e3, _ = TestSFCreditInfo.DOCUMENT_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_TestDocumentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.payload()

        with (open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_ONE), "rb") as file1,
              open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_TWO), "rb") as file2,
              open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_THREE), "rb") as file3):
            attachment_1 = file1.read()
            attachment_2 = file2.read()

            self.assertEqual(
                TestSFCreditInfo.DOCUMENT_INFO_TWO.payload(),
                {
                    'fileName': 'file.pdf',
                    'fileSize': '1 MB',
                    'fileType': 'pdf',
                    'attachmentId': 'attachment_one',
                    'attachmentByte': base64.b64encode(attachment_1).decode("utf-8")
                }
            )

            self.assertEqual(
                TestSFCreditInfo.DOCUMENT_INFO_THREE.payload(),
                {
                    'fileName': 'file.docx',
                    'fileSize': '2 MB',
                    'fileType': 'docx',
                    'attachmentId': 'attachment_two',
                    'attachmentByte': base64.b64encode(attachment_2).decode("utf-8")
                }
            )

    def test_TestDocumentInfo_file_name(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.file_name = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_TWO.file_name = ["file.pdf"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_THREE.file_name = {"file.pdf"}

        TestSFCreditInfo.DOCUMENT_INFO_ONE.file_name = "file.png"
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_name = "file.pdf"
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_name = "file.docx"

        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileName, "file.png")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileName, TestSFCreditInfo.DOCUMENT_INFO_ONE.file_name)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileName, "file.pdf")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileName, TestSFCreditInfo.DOCUMENT_INFO_TWO.file_name)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileName, "file.docx")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileName, TestSFCreditInfo.DOCUMENT_INFO_THREE.file_name)

    def test_TestDocumentInfo_file_size(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.file_size = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_TWO.file_size = ["1 MB"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_THREE.file_size = {"1 MB"}

        TestSFCreditInfo.DOCUMENT_INFO_ONE.file_size = "1 MB"
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_size = "2 MB"
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_size = "3 MB"

        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileSize, "1 MB")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileSize, TestSFCreditInfo.DOCUMENT_INFO_ONE.file_size)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileSize, "2 MB")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileSize, TestSFCreditInfo.DOCUMENT_INFO_TWO.file_size)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileSize, "3 MB")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileSize, TestSFCreditInfo.DOCUMENT_INFO_THREE.file_size)

    def test_TestDocumentInfo_file_type(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.file_type = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_TWO.file_type = [PermittedFileUploadType.DOCX]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_THREE.file_type = {PermittedFileUploadType.DOCX}

        TestSFCreditInfo.DOCUMENT_INFO_ONE.file_type = PermittedFileUploadType.PDF
        TestSFCreditInfo.DOCUMENT_INFO_TWO.file_type = PermittedFileUploadType.DOCX
        TestSFCreditInfo.DOCUMENT_INFO_THREE.file_type = PermittedFileUploadType.TIF

        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileType, PermittedFileUploadType.PDF)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._fileType, TestSFCreditInfo.DOCUMENT_INFO_ONE.file_type)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileType, PermittedFileUploadType.DOCX)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._fileType, TestSFCreditInfo.DOCUMENT_INFO_TWO.file_type)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileType, PermittedFileUploadType.TIF)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._fileType, TestSFCreditInfo.DOCUMENT_INFO_THREE.file_type)

    def test_TestDocumentInfo_attachment_id(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_id = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_id = ["attachment_one"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_id = {"attachment_one"}

        TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_id = "attachment_one"
        TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_id = "attachment_two"
        TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_id = "attachment_three"

        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._attachmentId, "attachment_one")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._attachmentId,
                         TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_id)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._attachmentId, "attachment_two")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._attachmentId,
                         TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_id)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._attachmentId, "attachment_three")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._attachmentId,
                         TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_id)

    def test_TestDocumentInfo_attachment_bytes(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_bytes = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_bytes = ["attachment_one"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_bytes = {"attachment_one"}

        with (open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_ONE), "rb") as file1,
              open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_TWO), "rb") as file2,
              open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_THREE), "rb") as file3):
            attachment_1 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_1",
                    name=TestSFCreditInfo.FILE_NAME_ONE,
                    type="jpg",
                    data=file1.read(),
                ),
                FileURLsProto()
            )

            attachment_2 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_2",
                    name=TestSFCreditInfo.FILE_NAME_TWO,
                    type="jpg",
                    data=file2.read(),
                ),
                FileURLsProto()
            )

            attachment_3 = UploadedFile(
                UploadedFileRec(
                    file_id="file_id_3",
                    name=TestSFCreditInfo.FILE_NAME_THREE,
                    type="jpg",
                    data=file3.read(),
                ),
                FileURLsProto()
            )

            TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_bytes = attachment_1
            TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_bytes = attachment_2
            TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_bytes = attachment_3

            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._attachmentByte, attachment_1)
            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE._attachmentByte,
                             TestSFCreditInfo.DOCUMENT_INFO_ONE.attachment_bytes)
            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._attachmentByte, attachment_2)
            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO._attachmentByte,
                             TestSFCreditInfo.DOCUMENT_INFO_TWO.attachment_bytes)
            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._attachmentByte, attachment_3)
            self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE._attachmentByte,
                             TestSFCreditInfo.DOCUMENT_INFO_THREE.attachment_bytes)

    def test_TestDocumentInfo_get_file_size(self):
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE.get_file_size(), 0)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO.get_file_size(), 0.009)
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE.get_file_size(), 0.013)

    def test_TestDocumentInfo_get_formatted_size(self):
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_ONE.get_formatted_size(), "")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_TWO.get_formatted_size(), "0.009 MB")
        self.assertEqual(TestSFCreditInfo.DOCUMENT_INFO_THREE.get_formatted_size(), "0.013 MB")

    def test_TestDocumentInfo_has_file(self):
        self.assertFalse(TestSFCreditInfo.DOCUMENT_INFO_ONE.has_file())
        self.assertTrue(TestSFCreditInfo.DOCUMENT_INFO_TWO.has_file())
        self.assertTrue(TestSFCreditInfo.DOCUMENT_INFO_THREE.has_file())

    def test_UploadDocumentInfo_validate(self):
        e1, _ = TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.validate()
        e2, _ = TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.validate()
        e3, _ = TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_UploadDocumentInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.payload()

        with (open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_ONE), "rb") as file1,
              open(os.path.join(RESOURCES_PATH, "core", "models", TestSFCreditInfo.FILE_NAME_TWO), "rb") as file2):
            attachment_1 = file1.read()
            attachment_2 = file2.read()

            p1 = {
                "nric": "F3875860T",
                "attachments": [
                    {
                        'fileName': 'file.pdf',
                        'fileSize': '1 MB',
                        'fileType': 'pdf',
                        'attachmentId': 'attachment_one',
                        'attachmentByte': base64.b64encode(attachment_1).decode("utf-8")
                    }
                ]
            }

            p2 = {
                'nric': 'G3327819K',
                'attachments': [
                    {
                        'fileName': 'file.pdf',
                        'fileSize': '1 MB', 'fileType': 'pdf',
                        'attachmentId': 'attachment_one',
                        'attachmentByte': base64.b64encode(attachment_1).decode("utf-8")
                    },
                    {
                        'fileName': 'file.docx',
                        'fileSize': '2 MB', 'fileType': 'docx',
                        'attachmentId': 'attachment_two',
                        'attachmentByte': base64.b64encode(attachment_2).decode("utf-8")
                    }
                ]
            }

            self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.payload(), p1)
            self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.payload(), p2)

    def test_UploadDocumentInfo_nric(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.nric = 123456789

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.nric = ["T0123456X"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.nric = {"T0123456X"}

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.nric = "T0123456X"
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.nric = "S0123456X"
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.nric = "T0123444X"

        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._nric, "T0123456X")
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._nric,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.nric)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._nric, "S0123456X")
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._nric,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.nric)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._nric, "T0123444X")
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._nric,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.nric)

    def test_UploadDocumentInfo_documents(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.documents = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.documents = "document"

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.documents = ["document"]

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.documents = [TestSFCreditInfo.DOCUMENT_INFO_ONE]
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.documents = [TestSFCreditInfo.DOCUMENT_INFO_TWO]
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.documents = [TestSFCreditInfo.DOCUMENT_INFO_THREE]

        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_ONE])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.documents)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_TWO])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.documents)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_THREE])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.documents)

    def test_UploadDocumentInfo_add_document(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.add_document(123)

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.add_document("document")

        with self.assertRaises(ValueError):
            TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.add_document(["document"])

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._documents = []
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._documents = []
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._documents = []

        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.add_document(TestSFCreditInfo.DOCUMENT_INFO_ONE)
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.add_document(TestSFCreditInfo.DOCUMENT_INFO_TWO)
        TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.add_document(TestSFCreditInfo.DOCUMENT_INFO_THREE)

        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_ONE])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_ONE.documents)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_TWO])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_TWO.documents)
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._documents,
                         [TestSFCreditInfo.DOCUMENT_INFO_THREE])
        self.assertEqual(TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE._documents,
                         TestSFCreditInfo.UPLOAD_DOCUMENT_INFO_THREE.documents)

    def test_CancelClaimsInfo_validate(self):
        e1, _ = TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.validate()
        e2, _ = TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.validate()
        e3, _ = TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.validate()

        self.assertTrue(len(e1) > 0)
        self.assertTrue(len(e2) == 0)
        self.assertTrue(len(e3) == 0)

    def test_CancelClaimsInfo_payload(self):
        with self.assertRaises(AttributeError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.payload()

        p1 = {
            'nric': 'F3875860T',
            'claimCancelCode': '53'
        }

        p2 = {
            'nric': 'G3327819K',
            'claimCancelCode': '55'
        }

        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.payload(), p1)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.payload(), p2)

    def test_CancelClaimsInfo_nric(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.nric = 123456789

        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.nric = ["T0123456X"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.nric = {"T0123456X"}

        TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.nric = "T0123456X"
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.nric = "S0123456X"
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.nric = "T0123444X"

        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE._nric, "T0123456X")
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE._nric, TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.nric)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO._nric, "S0123456X")
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO._nric, TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.nric)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE._nric, "T0123444X")
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE._nric,
                         TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.nric)

    def test_CancelClaimsInfo_cancel_claims_code(self):
        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.cancel_claims_code = 123

        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.cancel_claims_code = ["cancel_claims_code"]

        with self.assertRaises(ValueError):
            TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.cancel_claims_code = {"cancel_claims_code"}

        TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.cancel_claims_code = CancelClaimsCode.NO_CREDIT_CLAIM
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.cancel_claims_code = CancelClaimsCode.COURSE_CANCELLED
        TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.cancel_claims_code = CancelClaimsCode.COURSE_POSTPONED

        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE._claimCancelCode, CancelClaimsCode.NO_CREDIT_CLAIM)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE._claimCancelCode,
                         TestSFCreditInfo.CANCEL_CLAIMS_INFO_ONE.cancel_claims_code)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO._claimCancelCode, CancelClaimsCode.COURSE_CANCELLED)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO._claimCancelCode,
                         TestSFCreditInfo.CANCEL_CLAIMS_INFO_TWO.cancel_claims_code)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE._claimCancelCode, CancelClaimsCode.COURSE_POSTPONED)
        self.assertEqual(TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE._claimCancelCode,
                         TestSFCreditInfo.CANCEL_CLAIMS_INFO_THREE.cancel_claims_code)
