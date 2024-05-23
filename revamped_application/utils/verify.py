"""
Contains verification functions for fields used in the demo app
"""

import re

_VALID_NRIC_FIN_START_CODE: list[str] = ["S", "T", "F", "G", "M"]
_NRIC_WEIGHTS: list[int] = [2, 7, 6, 5, 4, 3, 2]
_S_T_CHECKSUM: dict[int, str] = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "Z",
    10: "J"
}
_G_F_CHECKSUM: dict[int, str] = {
    0: "K",
    1: "L",
    2: "M",
    3: "N",
    4: "P",
    5: "Q",
    6: "R",
    7: "T",
    8: "U",
    9: "W",
    10: "X",
}
_M_CHECKSUM: dict[int, str] = {
    0: "K",
    1: "L",
    2: "J",
    3: "N",
    4: "P",
    5: "Q",
    6: "R",
    7: "T",
    8: "U",
    9: "W",
    10: "X",
}


def verify_uen(uen: str) -> bool:
    """
    Verifies if the UEN provided is preliminarily valid

    :param uen: UEN number to test
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


def verify_nric_fin(id: str) -> bool:
    """
    Verifies if an ID number is a valid NRIC or FIN number.
    Algorithm taken from: https://userapps.support.sap.com/sap/support/knowledge/en/2572734

    :param id: The ID number to test
    """
    if not isinstance(id, str):
        return False

    if len(id) != 9:
        return False

    first_char = id[0]
    last_char = id[-1]

    if first_char not in _VALID_NRIC_FIN_START_CODE:
        return False

    checksum_sum = 0

    try:
        for i in range(7):
            parsed_num = int(id[1 + i])
            checksum_sum += (parsed_num * _NRIC_WEIGHTS[i])
    except ValueError | TypeError:
        return False

    if first_char == "G" or first_char == "T":
        checksum_sum += 4

    if first_char == "M":
        checksum_sum += 3

    remainder = checksum_sum % 11
    checksum = 11 - (remainder + 1)

    match last_char:
        case "S" | "T":
            return last_char == _S_T_CHECKSUM[checksum]
        case "G" | "F":
            return last_char == _G_F_CHECKSUM[checksum]
        case "M":
            return last_char == _M_CHECKSUM[checksum]
        case _:
            return False
