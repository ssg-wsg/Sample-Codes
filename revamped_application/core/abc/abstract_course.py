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


class ABCCourseInfo(ABC):
    """Abstract class to represent a collection of information to be passed into a request as a request body"""

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
        pass

    @abstractmethod
    def payload(self, as_json_str: bool = False) -> dict | str:
        pass
