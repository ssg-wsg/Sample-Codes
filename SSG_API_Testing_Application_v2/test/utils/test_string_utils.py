import io
import unittest

from SSG_API_Testing_Application_v2.utils.string_utils import StringBuilder


class TestStringUtils(unittest.TestCase):
    """
    Tests the classes within the string_utils file.
    """

    def test_empty_builder(self):
        sb = StringBuilder()
        self.assertEqual(sb._buffer.getvalue(), io.StringIO().getvalue())

    def test_set_length(self):
        sb = StringBuilder("12345").set_length(3)
        self.assertEqual(sb._buffer.getvalue(), io.StringIO("123").getvalue())

    def test_clear(self):
        sb = StringBuilder("12345").clear()
        self.assertEqual(sb._buffer.getvalue(), io.StringIO().getvalue())

    def test_append(self):
        sb = StringBuilder().append("123")
        self.assertEqual(sb._buffer.getvalue(), io.StringIO("123").getvalue())

    def test_newline(self):
        sb = StringBuilder("12345").newline()
        self.assertEqual(sb._buffer.getvalue(), io.StringIO("12345\n").getvalue())

    def test_get(self):
        sb = StringBuilder("12345")
        self.assertEqual(sb.get(), "12345")
