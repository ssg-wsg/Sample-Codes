import unittest

from revamped_application.utils.verify import verify_uen, verify_aes_encryption_key


class TestVerify(unittest.TestCase):
    """
    Tests all the methods in the verify.py file.
    """

    def test_verify_uen(self):
        self.assertFalse(verify_uen("A1234567A"))
        self.assertFalse(verify_uen("1234567890"))
        self.assertFalse(verify_uen("T99SGABCD1"))

        self.assertTrue(verify_uen("12345678A"))
        self.assertTrue(verify_uen("123456789A"))
        self.assertTrue(verify_uen("T99CC1234A"))

    def test_verify_aes_encryption_key(self):
        with self.assertRaises(ValueError):
            verify_aes_encryption_key(12345)

        self.assertFalse(verify_aes_encryption_key("AESKEYHERE"))
        self.assertFalse(verify_aes_encryption_key("lBzq4y040AY0m4I2AUGJcdoaskndlsandlasndsadasdasbg="))

        self.assertTrue(verify_aes_encryption_key("lBzq4y040AY0m4I2AUGJcxhjcY6Ykl0nHqOMGlN95bg="))
