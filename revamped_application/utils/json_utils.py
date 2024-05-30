from typing import Sequence


def remove_null_fields(d: dict, exclude: Sequence[str] = ()) -> dict:
    """
    Removes any empty fields from a dictionary. This method is destructive and works directly on
    the input dictionary itself

    :param d: Dictionary to remove fields from
    :param exclude: Sequence of fields to exclude
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

        # remove any keys with None values
        if v is None:
            keys_to_remove.append(k)

    # return only keys with non-None values
    return {k: v for k, v in d.items() if k not in keys_to_remove}
