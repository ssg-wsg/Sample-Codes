import unittest
import requests

from SSG_API_Testing_Application_v2.core.abc.abstract import AbstractRequest, AbstractRequestInfo


class TestAbstract(unittest.TestCase):
    """Tests the different classes in the abstract module."""

    def test_init_abstract_request(self):
        """Tests to ensure that AbstractRequest cannot be initialised if its abstract methods are not implemented."""

        with self.assertRaises(TypeError):
            AbstractRequest()

    def test_init_abstract_request_info(self):
        """
        Tests to ensure that AbstractRequestInfo cannot be initialised if its abstract methods are not
        implemented.
        """

        with self.assertRaises(TypeError):
            AbstractRequestInfo()

    def test_concrete_abstract_request(self):
        """Tests to ensure that concrete instances of AbstractRequest can be initialised."""

        class ConcreteRequest(AbstractRequest):
            def __init__(self, *args, **kwargs):
                pass

            def __repr__(self):
                pass

            def __str__(self):
                pass

            def _prepare(self, *args, **kwargs):
                pass

            def execute(self) -> requests.Response:
                pass

        try:
            ConcreteRequest()
        except Exception as ex:
            self.fail(ex)

    def test_concrete_abstract_request_info(self):
        """Tests to ensure that concrete instances of AbstractRequestInfo can be initialised."""

        class ConcreteRequestInfo(AbstractRequestInfo):
            def __init__(self, *args, **kwargs):
                pass

            def __repr__(self):
                pass

            def __str__(self):
                pass

            def validate(self) -> None | list[str]:
                pass

            def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
                pass

        try:
            ConcreteRequestInfo()
        except Exception as ex:
            self.fail(ex)
