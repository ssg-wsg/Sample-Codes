import unittest

from revamped_application.utils.json_utils import remove_null_fields


class TestJsonUtils(unittest.TestCase):
    """
    Tests all the methods and classes within the json_utils file.
    """

    def test_remove_null_fields(self):
        empty = {}
        test1 = {
            "key": "value",
            "value": 1,
            "item": ["this", "is", "an", "item"],
            "null": None
        }
        result1 = {
            "key": "value",
            "value": 1,
            "item": ["this", "is", "an", "item"],
        }
        test2 = {
            "key": "value",
            "dict1": {
                "dict2": {
                    "dict3": {
                        "dict4": None
                    }
                }
            },
            "item": 100
        }
        result2 = {
            "key": "value",
            "item": 100
        }

        self.assertEqual(remove_null_fields(empty), {})
        self.assertEqual(remove_null_fields(test1), result1)
        self.assertEqual(remove_null_fields(test2), result2)
