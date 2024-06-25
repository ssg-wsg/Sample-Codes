"""
This file contains useful classes and methods used for creating and handling HTTP requests.
"""

import binascii
import json
import textwrap

import certifi
import requests
import streamlit as st

from requests.exceptions import ConnectionError, HTTPError, SSLError, InvalidURL, InvalidHeader

from core.system.logger import Logger
from utils.streamlit_utils import init, http_code_handler
from core.abc.abstract import AbstractRequest
from core.constants import HttpMethod
from core.cipher.encrypt_decrypt import Cryptography
from typing import Self, Any, Callable
from utils.string_utils import StringBuilder


# initiaise the session variables here
init()
LOGGER = Logger("HTTP Request")


class HTTPRequestBuilder:
    """
    Class to help in building HTTP requests
    """

    # specifies the max length to truncate text to and cause a text wrap
    WRAP_LEVEL: int = 72

    # specifies the level of indent for any json.dumps() function calls below
    _INDENT_LEVEL: int = 4

    def __init__(self):
        """
        Initialises the request builder object.
        """

        self.endpoint = None
        self.header = {"accept": "application/json"}
        self.params = {}
        self.body = {}

    def __str__(self):
        """
        String representation of the HTTPRequestBuilder returns the JSON string representing the payload/body
        of the request.
        """

        return json.dumps(self.body, indent=HTTPRequestBuilder._INDENT_LEVEL)

    def with_endpoint(self, endpoint: str, direct_argument: str = "") -> Self:
        """
        Specifies the API endpoint to send requests to.

        :param endpoint: Endpoint URL corresponding to the HTTP/S API endpoint. It must be
                         prepended with the HTTP protocol and must not end with '/'. If you
                         need to use '/' at the end of the URL, specify it with the "direct_argument"
                         parameter below
        :param direct_argument: String to append to the end of the URL string. This is provided for convenience
                                in the event that you need to specify any other strings at the back of the provided
                                endpoint URL for the correct API endpoint to connect to. This should also not end
                                with '/'.
        :return: This Builder instance
        """

        if not isinstance(endpoint, str):
            raise ValueError("Endpoint must be a string!")

        if endpoint is not None and len(endpoint) == 0:
            raise ValueError("Endpoint cannot be empty!")

        if not isinstance(direct_argument, str):
            raise ValueError("Direct argument must be a string!")

        if not endpoint.startswith("http://") and not endpoint.startswith("https://"):
            raise ValueError("Endpoint URL must start with http:// or https://!")

        self.endpoint = endpoint

        if direct_argument is not None and len(direct_argument) > 0:
            # remove the "/" at the start of the direct argument if it exists
            while direct_argument.startswith("/"):
                direct_argument = direct_argument[1:]

            # appends the direct argument to the endpoint if it is not empty and strips the end of the url
            # endpoint if it has a trailing '/'
            self.endpoint = (f"{self.endpoint}{direct_argument}"
                             if self.endpoint.endswith("/")
                             else f"{self.endpoint}/{direct_argument}")

        while self.endpoint.endswith("/"):
            self.endpoint = self.endpoint[:-1]

        return self

    def with_header(self, key: str, value: str) -> Self:
        """
        Adds a key-value pair to the request header.

        :param key: String key
        :param value: String value
        :return: This Builder instance
        """

        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Header values must be strings!")

        if len(key) == 0:
            raise ValueError("Header key cannot be empty!")

        self.header[key] = value
        return self

    def with_param(self, key: str, value: Any) -> Self:
        """
        Adds a key-value query to the request.

        :param key: String key
        :param value: String value. This value should be JSON-serializable.
        :return: This Builder instance
        """

        if not isinstance(key, str):
            raise ValueError("Parameter Key values must be strings")

        if len(key) == 0:
            raise ValueError("Parameter Key cannot be empty!")

        try:
            json.dumps(value)
        except Exception:
            raise ValueError("Parameter Value must be JSON-serializable!")

        self.params[key] = value
        return self

    def with_body(self, data: dict) -> Self:
        """
        Adds the dictionary data representing the request body to the request.

        :param data: Data to append to the request
        :return: This Builder instance
        """

        if not isinstance(data, dict):
            raise ValueError("Data must be a dict!")

        self.body = json.dumps(data)
        return self

    def with_api_version(self, version: str) -> Self:
        """
        Sets the API version of the request.

        WARNING: You are highly discouraged to use this function to specify the API version within the request.
        Doing so may open you up to errors if the API version you indicated has been deprecated/decommissioned, and
        you failed to update this parameter regularly. Leaving the API version field blank will ensure that you will
        always be using the most updated version of the API!

        :param version: API version
        :return: This Builder instance
        """

        if not isinstance(version, str) or len(version) == 0:
            raise ValueError("API version must be a string")

        return self.with_header("x-api-version", version)

    def get(self) -> requests.Response:
        """
        Sends a GET request to the endpoint using the relevant certs stored in the session state.

        :return: requests.Response object
        """

        if "key_pem" not in st.session_state or "cert_pem" not in st.session_state:
            raise ValueError("No Key or Certificate files specified!")

        return requests.get(self.endpoint,
                            params=self.params,
                            headers=self.header,
                            verify=certifi.where(),
                            cert=(st.session_state["cert_pem"], st.session_state["key_pem"]))

    def post(self) -> requests.Response:
        """
        Sends a POST request to the endpoint using the relevant certs stored in the sessions state.

        :return: requests.Response object
        """

        if "key_pem" not in st.session_state or "cert_pem" not in st.session_state:
            raise ValueError("No Key or Certificate files specified!")

        return requests.post(self.endpoint,
                             params=self.params,
                             headers=self.header,
                             data=self.body,
                             verify=certifi.where(),
                             cert=(st.session_state["cert_pem"], st.session_state["key_pem"]))

    def post_encrypted(self) -> requests.Response:
        """
        Sends an encrypted POST request to the endpoint using the relevant certs stored in the session state.
        Note that we use json=... here to ensure the encrypted payload is automatically form-encoded.

        Make sure that you set return_bytes=False for Cryptography.encrypt() to decode the payload into a String;
        the json field does not allow you to pass in bytes objects.

        cert can either be a single value representing the file path to a file that contains the private key and
        certificate, or a 2-tuple (cert, key) representing the file path to a certificate and private key file
        respectively.

        :return: requests.Response object
        """

        if "key_pem" not in st.session_state or "cert_pem" not in st.session_state:
            raise ValueError("No Key or Certificate files specified!")

        return requests.post(self.endpoint,
                             params=self.params,
                             headers=self.header,
                             json=Cryptography.encrypt(json.dumps(self.body), return_bytes=False),
                             verify=certifi.where(),
                             cert=(st.session_state["cert_pem"], st.session_state["key_pem"]))

    def repr(self, req_type: HttpMethod) -> str:
        """
        Returns the string representation of the request. This method will return a pretty-printed summary of
        the request that this HTTPRequestBuilder has built.

        :param req_type: HttpMethod representing the type of request made
        :return: String representation of the request this HTTPRequestBuilder has built
        """

        builder = (StringBuilder(req_type.value)
                   .append(" ")
                   .append(self.endpoint)
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

        # wrap the url as it might become too long
        # code idea taken from https://discuss.streamlit.io/t/st-code-on-multiple-lines/50511/8
        curr_str = "\n".join(textwrap.wrap(builder.get(), width=HTTPRequestBuilder.WRAP_LEVEL))
        builder = builder.clear() \
                         .append(curr_str)

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

        # the dictionary needs to be loaded up as a JSON object first before we can dump it out as a pretty
        # JSON string, hence the convoluted operation below to load and then dump the JSON string
        builder = (builder.newline()
                   .append("Body")
                   .newline()
                   .append("-------")
                   .newline()
                   .append(json.dumps(json.loads(str(self.body)), indent=HTTPRequestBuilder._INDENT_LEVEL))
                   .newline())

        return builder.get()


def handle_request(rec_obj: AbstractRequest, require_encryption: bool = False) -> None:
    """
    Handles the request to be sent to the endpoint and shows the encrypted payload if required.

    :param rec_obj: Request object to be sent to the endpoint
    :param require_encryption: Boolean to indicate if the request should be encrypted or not. If the request should
                               be encrypted, then a section to display the encrypted text is displayed.
    """

    if require_encryption:
        st.subheader("Plaintext Request")
        st.code(repr(rec_obj), language="text")

        st.subheader("Encrypted Request Payload")
        try:
            LOGGER.info("Encrypting Request Payload...")
            # decode the object and wrap it to display it properly
            ciphertext = Cryptography.encrypt(str(rec_obj)).decode()
            st.code("\n".join(textwrap.wrap(ciphertext, width=HTTPRequestBuilder.WRAP_LEVEL)), language="text")
        except binascii.Error:
            LOGGER.error("Encryption failed! Aborting request...")
            st.error("Unable to perform Encryption! Check your AES key to make sure that it is valid!", icon="🚨")
    else:
        st.subheader("Request")
        st.code(repr(rec_obj), language="text")


def handle_response(throwable: Callable[[], requests.Response], require_decryption: bool = False) -> None:
    """
    Handles the potentially throwing request function and uses Streamlit to display or handle the error.

    :param throwable: Function to be called.
                      This function accepts no inputs and may potentially raise an error.
                      This function should also return the response object from the request.
    :param require_decryption: Boolean indicating whether decryption is required for the returned payload. If the
                               response should be decrypted, then a section will display the decrypted response.
    """

    try:
        LOGGER.info("Executing request...")
        response = throwable()
        if not isinstance(throwable(), requests.Response):
            LOGGER.error("Function does not return the expected requests.Response object! Aborting request...")
            raise AssertionError("The request function does not return a valid HTTP response!")

        http_code_handler(response.status_code)

        if response.status_code >= 400:
            # is an error, no need to decrypt
            LOGGER.error(f"Request failed with HTTP request code {response.status_code}! Aborting request...")
            st.header("Error Message")
            st.code(response.text)
            return

        LOGGER.info("Decrypting response...")
        if require_decryption:
            st.subheader("Encrypted Response")
            st.code(response.text)

            st.subheader("Decrypted Response")
            try:
                data = Cryptography.decrypt(response.text).decode()
                json_data = json.loads(data)
                st.json(json_data)
            except Exception:
                st.error("Unable to decrypt the response! It might be possible that the outputs are already "
                         "decrypted (as with the Mock API endpoint)!", icon="🚨")

        else:
            st.subheader("Response")
            try:
                st.json(response.json())
            except json.decoder.JSONDecodeError:
                LOGGER.warning("Message is not JSON-serializable! Defaulting to plain text instead...")
                st.code(response.text, language="text")
    except HTTPError as ex:
        LOGGER.error(f"Request failed with HTTP exception! Error: {ex}. Aborting request...")
        st.error("Unable to make a HTTP request to the API endpoint! "
                 "Check your inputs and make sure that there are no mistakes in your inputs!")
    except InvalidURL as ex:
        LOGGER.error(f"Request failed due to URL error. Error: {ex}. Aborting request...")
        st.error("Check that the URL you provided is a valid URL!")
    except InvalidHeader as ex:
        LOGGER.error(f"Request failed due to HTTP header error. Error: {ex}. Aborting request...")
        st.error("Check that the headers you provided is valid!")
    except SSLError as ex:
        # there are some issues with the SSL keys
        LOGGER.error(f"Unable to establish SSL connection with the server! Error: {ex}. Aborting request...")
        st.error("Check your SSL certificate and keys and ensure that they are valid!\n\n", icon="🚨")
    except ConnectionError as ex:
        # the endpoint url is likely malformed here
        LOGGER.error(f"There is an issue with the connection with the API endpoint! Error: {ex}. Aborting request...")
        st.error("Check the inputs that you have used for the API request and check that "
                 "they are valid!\n\nIt is likely that you have included a value that "
                 "causes the API request to query from a URL that does not exist or is "
                 "invalid!", icon="🚨")
    except Exception as ex:
        # float it back to the user to handle
        st.exception(ex)
