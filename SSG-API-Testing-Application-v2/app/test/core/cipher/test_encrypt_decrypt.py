import unittest

from app.core.cipher.encrypt_decrypt import Cryptography


class TestEncryptDecrypt(unittest.TestCase):
    """
    Test the encryption and decryption methods of the Cryptography class.
    """

    KEY = "u/fzxu+5FBlE7Wq7OWRMVbGB4snxf8xNyFZdTQ3tHBU="

    def test_encrypt(self):
        plaintext = "Hello, World!"
        ciphertext = b'FqhnvlhHlHszFIi0AVhqzQ=='

        encrypted = Cryptography.encrypt(self.KEY, plaintext)
        self.assertNotEqual(plaintext, encrypted)
        self.assertEqual(ciphertext, encrypted)

    def test_decrypt(self):
        plaintext = b"Hello, World!"
        ciphertext = b'FqhnvlhHlHszFIi0AVhqzQ=='

        decrypted = Cryptography.decrypt(self.KEY, ciphertext)
        self.assertEqual(plaintext, decrypted)

    def test_symmetry(self):
        plaintext = b"Hello, World!"
        encrypted = Cryptography.encrypt(self.KEY, plaintext)
        decrypted = Cryptography.decrypt(self.KEY, encrypted)

        self.assertEqual(plaintext, decrypted)
