"""
This file contains verification functions for fields in the Sample Application.
"""

import re

import OpenSSL.crypto


class Validators:
    """
    Contains a series of validators that can conduct verification and validation on credentials.
    """

    # weights for each digit in an NRIC number
    _NRIC_PRODUCT = [2, 7, 6, 5, 4, 3, 2]
    _S_T_CHECKDIGIT = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "Z", "J"]
    _G_F_CHECKDIGIT = ["K", "L", "M", "N", "P", "Q", "R", "T", "U", "W", "X"]
    _M_CHECKDIGIT = ["K", "L", "J", "N", "P", "Q", "R", "T", "U", "W", "X"]

    @staticmethod
    def verify_uen(uen: str) -> bool:
        """
        Verifies if the UEN provided is preliminarily valid. This does not check if a UEN is actually valid, i.e.
        attached to a valid entity in Singapore.

        Algorithms inspired by https://www.uen.gov.sg/ueninternet/faces/pages/admin/aboutUEN.jspx.

        Note:
        [X = character, D = number, E = alpha-numeric, Y = year], T is a literal "T"
        - There are 3 formats for UENs
            1. Businesses registered with ACRA: DDDDDDDDX
            2. Local Companies registered with ACRA: YYYYDDDDDX
            3. Others: TYYXEDDDDX

        The XE combo in Others can only be one of: LP, LL, FC, PF, RF, MQ, MM, NB, CC, CS, MB, FM, GS, DP, CP, NR, CM,
                                                   CD, MD, HS, VH, CH, MH, CL, XL, CX, HC, RP, TU, TC, FB, FN, PA, PB,
                                                   SS, MC, SM, GA, GB

        :param uen: UEN to verify
        :return: True if the UEN is valid, False otherwise
        """

        if not isinstance(uen, str):
            raise ValueError("UEN must be a string!")

        if len(uen) != 9 and len(uen) != 10:
            return False

        if len(uen) == 9:
            return True if re.compile(r"[0-9]{8}[A-Z]{1}").match(uen) else False

        if len(uen) == 10:
            match1 = re.compile(r"[0-9]{9}[A-Z]{1}").match(uen)
            match2 = re.compile(r"T[0-9]{2}(CC|CD|CH|CL|CM|CP|CS|CX|DP|FB|FC|FM|FN|GA|GB|GS|HC|HS|LL|LP|MB|MC|MD|MH|MM|"
                                r"MQ|NB|NR|PA|PB|PF|RF|RP|SM|SS|TC|TU|VH|XL)[0-9]{4}[A-Z]{1}").match(uen)

            # if there are no matches, None is returned
            # check the signature of the match() function to verify
            return (match1 is not None) or (match2 is not None)

        return False

    @staticmethod
    def verify_aes_encryption_key(key: str) -> bool:
        """
        Verifies if the AES-256 key is valid, in a sense that the key is indeed 256 bit / 32 bytes long.

        Taken from: https://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-
                    b64-string-in-python

        :param key: AES-256 key to verify
        :return: True if the AES-256 key is valid length-wise, False otherwise
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string!")

        if len(key) == 0:
            return False

        len_key = len(key)
        count = 0

        if len_key > 1 and key[-2] == "=":
            count -= 1

        if len_key > 0 and key[-1] == "=":
            count -= 1

        count += int((len(key) * 3) / 4)

        return count == 32

    @staticmethod
    def verify_cert_private_key(cert_path: str, private_key_path: str):
        """
        Checks if a given pair of certificate and private key paths are valid.

        Adapted from https://stackoverflow.com/questions/19922790/how-to-check-for-python-the-key-associated-with
        -the-certificate-or-not

        :param cert_path: Path to the certificate file
        :param private_key_path: Path to the private key file
        """

        if not isinstance(cert_path, str) or not isinstance(private_key_path, str):
            raise ValueError("Paths must be strings!")

        try:
            with (open(cert_path, "rb") as cert_file,
                  open(private_key_path, "rb") as private_key_file):
                cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_file.read())
                private_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, private_key_file.read())

            context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
            context.use_certificate(cert)
            context.use_privatekey(private_key)

            return True
        except IOError:
            # cert/key does not exist
            return False
        except OpenSSL.crypto.Error:
            # if cert/key not in the valid format
            return False
        except Exception:
            raise

    @staticmethod
    def verify_nric(nric: str):
        """
        Verifies if a provided NRIC number is valid.

        Algorithm is taken from https://userapps.support.sap.com/sap/support/knowledge/en/2572734

        :param nric: NRIC number to verify
        """

        if not isinstance(nric, str):
            raise ValueError("NRIC must be a string!")

        if len(nric) != 9:
            # NRICs are only 9 digit long
            return False

        first_char = nric[0]
        last_char = nric[-1]
        checksum = 0

        for i in range(1, len(nric) - 1):
            try:
                checksum += int(nric[i]) * Validators._NRIC_PRODUCT[i - 1]
            except Exception:
                # not a number, so cannot be valid
                return False

        if first_char == "G" or first_char == "T":
            checksum += 4
        elif first_char == "M":
            checksum += 3

        remainder = checksum % 11
        checkdigit = 11 - (remainder + 1)

        if first_char == "S" or first_char == "T":
            return Validators._S_T_CHECKDIGIT[checkdigit] == last_char
        elif first_char == "G" or first_char == "F":
            return Validators._G_F_CHECKDIGIT[checkdigit] == last_char
        elif first_char == "M":
            return Validators._M_CHECKDIGIT[checkdigit] == last_char

        return False
