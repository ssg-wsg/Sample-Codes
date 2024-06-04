"""
This file contains different abstract base classes that form the basis for other request-related classes.
"""

import requests

from abc import ABC, abstractmethod


class AbstractRequest(ABC):
    """Abstract class to represent the interface that all request-related classes should implement"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def _prepare(self, *args, **kwargs):
        """Scaffolds the request and prepares it for execution"""

        pass

    @abstractmethod
    def execute(self) -> requests.Response:
        """Executes the request and returns the response"""

        pass


class AbstractRequestInfo(ABC):
    """
    Abstract class used to represent the collection of information to pass into the
    different APIs
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def validate(self) -> None | list[str]:
        """Validates the inputs passed to the APIs"""

        pass

    @abstractmethod
    def payload(self, verify: bool = True, as_json_str: bool = False) -> dict | str:
        """Returns the payload to attach to the request for the Attendance API"""

        pass
