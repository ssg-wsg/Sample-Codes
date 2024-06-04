"""
This file contains verification functions for fields in the Sample Application.
"""

import re


def verify_uen(uen: str) -> bool:
    """
    Verifies if the UEN provided is preliminarily valid. This does not check if a UEN is actually valid, i.e.
    attached to a valid entity in Singapore.

    :param uen: UEN to verify
    :return: True if the UEN is valid, False otherwise
    """

    if len(uen) != 9 and len(uen) != 10:
        return False

    if len(uen) == 9:
        return True if re.compile(r"[0-9]{8}[A-Z]{1}").match(uen) else False

    if len(uen) == 10:
        match1 = re.compile(r"[0-9]{9}[A-Z]{1}").match(uen)
        match2 = re.compile(r"T[0-9]{2}[A-Z]{2}[0-9]{4}[A-Z]{1}").match(uen)
        found_match = match1 or match2

        return True if found_match else False


def verify_aes_encryption_key(key: str) -> bool:
    """
    Verifies if the AES-256 key is valid, in a sense that the key is indeed 256 bit / 32 bytes long.

    Taken from: https://stackoverflow.com/questions/6793575/estimating-the-size-of-binary-data-encoded-as-a-
                b64-string-in-python

    :param key: AES-256 key to verify
    :return: True if the AES-256 key is valid length-wise, False otherwise
    """

    count = 0

    if key[-2] == "=":
        count -= 1

    if key[-1] == "=":
        count -= 1

    count += int((len(key) * 3) / 4)

    return count == 32
