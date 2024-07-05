import os
import unittest

from app.utils.verify import Validators
from app.test.resources.definitions import RESOURCES_PATH


class TestVerify(unittest.TestCase):
    """
    Tests all the methods in the verify.py file.
    """

    VALID_CERT_PATH = os.path.join(RESOURCES_PATH, "utils", "valid_cert.pem")
    VALID_KEY_PATH = os.path.join(RESOURCES_PATH, "utils", "valid_key.pem")
    INVALID_CERT_PATH = os.path.join(RESOURCES_PATH, "utils", "invalid_cert.pem")
    INVALID_KEY_PATH = os.path.join(RESOURCES_PATH, "utils", "invalid_key.pem")
    VALID_NRICS = ["F3875860T", "G3327819K", "S5351748Z", "G5047559Q", "F1455308T", "S4686731I",
                   "F0667074K", "G4961553T", "G8400092U", "T9031775F", "F2082173Q"]
    INVALID_NRICS = ["ABCD", "A1234567X", "T0101010X", "123ABC123"]

    def test_verify_uen(self):
        self.assertFalse(Validators.verify_uen("A1234567A"))
        self.assertFalse(Validators.verify_uen("1234567890"))
        self.assertFalse(Validators.verify_uen("T99SGABCD1"))

        self.assertTrue(Validators.verify_uen("12345678A"))
        self.assertTrue(Validators.verify_uen("123456789A"))
        self.assertTrue(Validators.verify_uen("T99CC1234A"))

    def test_verify_aes_encryption_key(self):
        with self.assertRaises(ValueError):
            Validators.verify_aes_encryption_key(12345)

        self.assertFalse(Validators.verify_aes_encryption_key("AESKEYHERE"))
        self.assertFalse(Validators.verify_aes_encryption_key("lBzq4y040AY0m4I2AUGJcdoaskndlsandlasndsadasdasbg="))

        self.assertTrue(Validators.verify_aes_encryption_key("lBzq4y040AY0m4I2AUGJcxhjcY6Ykl0nHqOMGlN95bg="))

    def test_verify_cert_private_key(self):
        with self.assertRaises(ValueError):
            Validators.verify_cert_private_key(123, TestVerify.VALID_KEY_PATH)

        with self.assertRaises(ValueError):
            Validators.verify_cert_private_key(TestVerify.VALID_CERT_PATH, 123)

        self.assertTrue(Validators.verify_cert_private_key(TestVerify.VALID_CERT_PATH, TestVerify.VALID_KEY_PATH))
        self.assertFalse(Validators.verify_cert_private_key(TestVerify.VALID_KEY_PATH, TestVerify.VALID_CERT_PATH))
        self.assertFalse(Validators.verify_cert_private_key(TestVerify.INVALID_CERT_PATH, TestVerify.INVALID_KEY_PATH))
        self.assertFalse(Validators.verify_cert_private_key(TestVerify.INVALID_KEY_PATH, TestVerify.INVALID_CERT_PATH))

    def test_verify_nric(self):
        # sample NRICs taken from https://www.protecto.ai/blog/personal-dataset-sample-singapore-national-
        # registration-identity-card-number-download-pii-data-examples and refined with
        # https://nric.biz/
        for nric in TestVerify.VALID_NRICS:
            self.assertTrue(Validators.verify_nric(nric))

        for nric in TestVerify.INVALID_NRICS:
            self.assertFalse(Validators.verify_nric(nric))
