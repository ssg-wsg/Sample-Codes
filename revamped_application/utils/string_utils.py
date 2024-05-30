"""
Contains classes and functions related to string manipulation
"""

import io

from typing import Self, Any


class StringBuilder:
    """Similar to Java's StringBuilder class, whereby strings are buffered using a StringIO object"""

    def __init__(self, init: str = ""):
        self._buffer = io.StringIO()

        if init or len(init) > 0:
            self._buffer.write(init)

    def setLength(self, length: int) -> Self:
        """
        Sets the length of the buffer to the input value

        :param length: Integer representing length of the buffer to truncate to
        :return: This StringBuilder instance
        """

        if not isinstance(length, int) or length < 0:
            raise ValueError("Length must be of an integer greater than or equal to 0")

        self._buffer.seek(length)
        self._buffer.truncate(length)
        return self

    def clear(self) -> Self:
        """
        Clear the buffer

        It is faster to create a new buffer than to reuse it:
        https://stackoverflow.com/questions/4330812/how-do-i-clear-a-stringio-object

        :return: This StringBuilder instance
        """

        self._buffer = io.StringIO()
        return self

    def append(self, obj: Any) -> Self:
        """
        Appends an object to the end of the buffer. If the object is not a String, then it will be coerced into
        a String object and passed into the StringBuilder.

        :param obj: Object to append
        :return: This StringBuilder instance
        """

        if not isinstance(obj, str):
            try:
                obj = str(obj)
            except TypeError:
                obj = repr(obj)

        self._buffer.write(obj)
        return self

    def newline(self) -> Self:
        """
        Appends a new line character to the end of the buffer

        :return: This StringBuilder instance
        """

        self.append("\n")
        return self

    def get(self) -> str:
        """
        Returns the built string from the buffer

        Note that the buffer is not cleared when this method is called
        :return: Built String
        """

        return self._buffer.getvalue()
