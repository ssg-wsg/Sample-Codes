import os
import unittest

from pep8 import StyleGuide


class TestPyCodeStyle(unittest.TestCase):
    @staticmethod
    def _enumerate_all_dirs() -> list[str]:
        paths = []

        for root, dirs, files in os.walk('../../'):
            for file in files:
                if file.endswith('.py'):
                    paths.append(os.path.join(root, file))

        return paths

    def test_pep8_conformance(self):
        """Tests that all Python code files conform to PEP8 style."""

        style = StyleGuide(config_file='.pep8')
        result = style.check_files(TestPyCodeStyle._enumerate_all_dirs())
        self.assertEqual(0, result.total_errors, "Found errors or warnings")
