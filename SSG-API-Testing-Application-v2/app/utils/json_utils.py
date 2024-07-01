"""
This file contains helper functions that handles the manipulation of JSON data.
"""

from typing import Sequence, Sized


def remove_null_fields(d: dict, exclude: Sequence[str] = ()) -> dict:
    """
    Removes any empty fields from a dictionary by iterating through the dictionary deeply.

    This method is destructive and will remove keys and values if:
    1. If the key points to None
    2. If the value is an empty dictionary

    :param d: Dictionary to remove fields from
    :param exclude: Sequence of fields to exclude from the removal action, if they happen to contain None or an empty
                    dictionary.
    :return: Dictionary with fields removed
    """

    keys_to_remove = []

    for k, v in d.items():
        if k in exclude:
            continue

        # recurse deeply if a dict is found
        if isinstance(v, dict):
            d[k] = remove_null_fields(v, exclude)

            # remove any returned dict that is empty
            if len(d[k]) == 0:
                keys_to_remove.append(k)

        # if a list is found, check if its contents are None or empty, and remove accordingly
        if isinstance(v, list):
            # remove any keys with None values or empty values
            d[k] = [item for item in v if item is not None and (not isinstance(item, Sized) or len(item) > 0)]

            if len(v) == 0:
                keys_to_remove.append(k)

        if v is None:
            keys_to_remove.append(k)

    # return only keys with non-None values
    return {k: v for k, v in d.items() if k not in keys_to_remove}
