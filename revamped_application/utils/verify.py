"""
This file contains verification functions for fields in the Sample Application.
"""

import re


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
