import json
import logging
import ssl

import requests
import streamlit as st

from utils.streamlit_utils import init, http_code_handler
from typing import Self, Any, Callable
from .string_utils import StringBuilder

BASE_PROD_URL = "https://public-api.ssg-wsg.sg"
ALTERNATIVE_PROD_URL = "https://api.ssg-wsg.sg"

# initialise the session variables here
init()


class HTTPRequestBuilder:
    """
    Class to help in building HTTP requests
    """

    def __init__(self):
        self.endpoint = ""
        # x-api-version is not mentioned here
        self.header = {"accept": "application/json"}
        self.params = {}
        self.body = {}
        self.direct_argument = ""

    def with_endpoint(self, endpoint: str) -> Self:
        """
        Sets the endpoint of the request.

        :param endpoint: Endpoint URL corresponding to the HTTP/S API endpoint. It must be
                         prepended with the HTTP protocol and must not end with '/'. If you
                         need to use '/' at the end of the URL, you must use direct_argument()
                         to specify the character
        :return: This Builder instance
        """

        if not isinstance(endpoint, str):
            raise ValueError("Endpoint must be a string")

        if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
            st.error("Endpoint URL must start with http:// or https://")

        if endpoint.endswith("/"):
            st.warning("Endpoint URL ends with /, it will be removed")
            self.endpoint = endpoint[:-1]
        else:
            self.endpoint = endpoint

        return self

    def with_direct_argument(self, arg: str = "") -> Self:
        """
        Specifies a direct argument to append to the end of the endpoint URL. Note that you
        can only specify one direct argument, subsequent calls of this function will override
        previously declared direct argument.

        Note that any '/' character appended to the end of arg is removed.

        :param arg: Argument to be appended to the end of the endpoint URL
        :return: This builder instance
        """

        if not isinstance(arg, str):
            raise ValueError("Direct argument must be a string")

        if arg.endswith("/"):
            self.direct_argument = arg[:-1]

        self.direct_argument = arg
        return self

    def with_header(self, key: str, value: str) -> Self:
        """
        Adds a key-value pair to the request header.

        :param key: String key
        :param value: String value
        :return: This Builder instance
        """

        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Endpoint must be a string")

        self.header[key] = value
        return self

    def with_param(self, key: str, value: Any) -> Self:
        """
        Adds a key-value query to the request.

        :param key: String key
        :param value: String value
        :return: This Builder instance
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        if not isinstance(value, str):
            raise ValueError("Value must be a string")

        self.params[key] = value
        return self

    def with_body(self, data: dict) -> Self:
        """
        Adds the body of the request to the request.

        :param data: Data to append to the request
        :return: This Builder instance
        """

        if not isinstance(data, dict):
            raise ValueError("Data must be a dict")

        self.body = json.dumps(data)
        return self

    def with_api_version(self, version: str) -> Self:
        """
        Sets the API version of the request.

        :param version: API version
        :return: This Builder instance
        """

        if not isinstance(version, str):
            raise ValueError("API version must be a string")

        return self.with_header("x-api-version", version)

    def get(self) -> requests.Response:
        """
        Sends a GET request to the endpoint using the relevant certs stored in the session state.

        :return: requests.Response object
        """

        return requests.get(self.endpoint + self.direct_argument,
                            params=self.params,
                            headers=self.header,
                            cert=(st.session_state["key_pem"], st.session_state["cert_pem"]))

    def post(self) -> requests.Response:
        """
        Sends a POST request to the endpoint using the relevant certs stored in the sessions state.

        :return: requests.Response object
        """

        return requests.post(self.endpoint + self.direct_argument,
                             params=self.params,
                             headers=self.header,
                             data=self.body,
                             cert=(st.session_state["cert_pem"], st.session_state["key_pem"]))

    def post_encrypted(self) -> requests.Response:
        """
        Sends an encrypted POST request to the endpoint using the relevant certs stored in the session state.

        :return: requests.Response object
        """

        return requests.post(self.endpoint + self.direct_argument,
                             params=self.params,
                             headers=self.header,
                             json=self.body,
                             cert=(st.session_state["cert_pem"], st.session_state["key_pem"]))

    def repr(self, req_type: str) -> str:
        """
        Returns the string representation of the request.

        :param req_type: The String representing the type of request made
        :return: String representation of the request
        """

        builder = (StringBuilder(req_type)
                   .append(" ")
                   .append(self.endpoint)
                   .append(self.direct_argument)
                   .append("?" if len(self.params) > 0 else ""))

        for i, (k, v) in enumerate(self.params.items()):
            if i == len(self.params) - 1:
                builder = (builder.append(k)
                           .append("=")
                           .append(v))
            else:
                builder = (builder.append(k)
                           .append("=")
                           .append(v)
                           .append("&"))

        builder = (builder.newline()
                   .newline()
                   .append("Headers")
                   .newline()
                   .append("-------")
                   .newline())

        for k, v in self.header.items():
            builder = (builder.append(k)
                       .append(": ")
                       .append(v)
                       .newline())

        builder = (builder.newline()
                   .append("Body")
                   .newline()
                   .append("-------")
                   .newline()
                   .append(self.body)
                   .newline())

        return builder.get()


def handle_error(throwable: Callable[[], requests.Response]) -> None:
    """
    Handles the potentially throwing function and uses Streamlit to display or
    handle the error.

    :param throwable: Function to be called.
                      This function accepts no inputs and may potentially raise an error.
                      This function should also return the response object from the request.
    """

    try:
        response = throwable()
        http_code_handler(response.status_code)
        st.json(response.json())
    except json.decoder.JSONDecodeError:
        # likely that the returns are not in JSON format
        st.code(response.text, language="text")
    except ConnectionError:
        # the endpoint url is likely malformed here
        st.error("Check the inputs that you have used for the API request and check that "
                 "they are valid!\n\nIt is likely that you have included a value that "
                 "causes the API request to query from a URL that does not exist or is "
                 "invalid!")
    except requests.exceptions.SSLError:
        # there are some issues with the SSL keys
        st.error("Check your SSL certificate and keys and ensure that they are valid!\n\n"
                 "If your key files are not in `pem` format, ensure that you convert your "
                 "key files into `pem` format!")
    except Exception as ex:
        # float it back to the user to handle
        st.exception(ex)
