import requests

from abc import ABC, abstractmethod


class ABCCourse(ABC):
    """Abstract class to represent a course related action"""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def _prepare(self, *args, **kwargs):
        """Scaffolds the request and prepares it for execution"""

        pass

    @abstractmethod
    def execute(self) -> requests.Response:
        """Executes the request and returns the response"""

        pass
