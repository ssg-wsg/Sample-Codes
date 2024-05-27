import streamlit as st

from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


class Cryptography:
    """
    Class used to encrypt and decrypt a message using AES-256, CBC and PKCS7

    Methods are taken from the SSG-WSG Sample Application.
    """

    # Initialisation vector used for encryption and decryption
    INITIAL_VECTOR: bytes = "SSGAPIInitVector".encode()

    @staticmethod
    def encrypt(plaintext: bytes | str, return_bytes: bool = True, key: str = None) -> bytes | str | None:
        """
        Encrypts a message and returns the ciphertext.

        :param plaintext: Plaintext Message to be encrypted. If a string is passed as the argument, it will be
                          encoded into a bytes object.
        :param return_bytes: If True, the ciphertext will be returned as a bytes object.
        :param key: Key to override key stored in session state
        :return:  Ciphertext or None if there are no key files loaded
        """

        if ("encryption_key" not in st.session_state or st.session_state["encryption_key"] is None
                or len(st.session_state["encryption_key"]) == 0) and not key:
            # if there are no keys loaded, do not continue
            return None

        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        enc_key = b64decode(key if key else st.session_state["encryption_key"])
        cipher_algo = Cipher(AES(enc_key), CBC(Cryptography.INITIAL_VECTOR), backend=default_backend())
        padding_algo = PKCS7(128).padder()

        encryptor = cipher_algo.encryptor()
        padded_plaintext = padding_algo.update(plaintext) + padding_algo.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        encoded_ciphertext = b64encode(ciphertext)

        if return_bytes:
            return encoded_ciphertext

        return encoded_ciphertext.decode()

    @staticmethod
    def decrypt(ciphertext: str | bytes, return_bytes: bool = True, key: str = None) -> bytes | str | None:
        """
        Decrypts an encrypted message and returns the plaintext.

        :param ciphertext: Ciphertext Message to be decrypted. It does not matter if a string or bytes are provided,
                           both will be encoded into a bytes object with base64-decode.
        :param key: Key to override key stored in session state
        :param return_bytes: If True, the ciphertext will be returned as a bytes object.
        :return: Plaintext Message
        """

        if ("encryption_key" not in st.session_state or st.session_state["encryption_key"] is None
                or len(st.session_state["encryption_key"]) == 0) and not key:
            # if there are no keys loaded, do not continue
            return None

        # decode the input text into a bytes object
        decoded_ciphertext = b64decode(ciphertext)

        enc_key = b64decode(key if key else st.session_state["encryption_key"])
        cipher_algo = Cipher(AES(enc_key), CBC(Cryptography.INITIAL_VECTOR), backend=default_backend())
        padding_algo = PKCS7(128).unpadder()

        decryptor = cipher_algo.decryptor()
        plaintext = decryptor.update(decoded_ciphertext) + decryptor.finalize()
        unpadded_plaintext = padding_algo.update(plaintext) + padding_algo.finalize()

        if return_bytes:
            return unpadded_plaintext

        return unpadded_plaintext.decode()
