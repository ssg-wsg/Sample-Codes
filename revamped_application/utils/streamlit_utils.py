"""
File containing utility functions and values to initialise Streamlit session variables
"""

import streamlit as st

from typing import Union, Optional
from utils.string_utils import StringBuilder


def init() -> None:
    """
    Initialises all the necessary Stremalit variables to record configurations

    :return: None
    """

    if "uen" not in st.session_state:
        st.session_state["uen"] = None

    if "encryption_key" not in st.session_state:
        st.session_state["encryption_key"] = None

    if "cert_pem" not in st.session_state:
        st.session_state["cert_pem"] = None

    if "key_pem" not in st.session_state:
        st.session_state["key_pem"] = None

    if "file_history" not in st.session_state:
        st.session_state["file_history"] = None

    if "url" not in st.session_state:
        st.session_state["url"] = None


def check_status() -> bool:
    """
    A simple callback function that checks if there are any uninitialised variables in the session state

    :return: True if all configuration variables are present, else False
    """

    return all([
        st.session_state["uen"],
        st.session_state["encryption_key"],
        st.session_state["cert_pem"],
        st.session_state["key_pem"]
    ])


def display_status() -> None:
    """
    Conducts a status check and displays an error if there are any missing configuration variables

    :return: None
    """

    if not check_status():
        st.error("There are some configuration variables missing!", icon="🚨")
    else:
        st.success("All configuration variables are present and loaded!")


@st.experimental_dialog("Configs", width="large")
def display_config() -> None:
    """Displays all the loaded configuration variables"""

    st.header("API Endpoint")
    st.code(st.session_state["url"] if st.session_state["url"] else "-", language="text")

    st.header("UEN")
    st.code(st.session_state["uen"] if st.session_state["uen"] else "-")

    st.header("Keys")
    st.subheader("Encryption Key:")
    st.code(st.session_state["encryption_key"] if st.session_state["encryption_key"] else "-")

    st.subheader("Certificate Key:")
    st.code("Loaded at: " + st.session_state["cert_pem"] if st.session_state["cert_pem"] else "-")

    st.subheader("Private Key:")
    st.code("Loaded at: " + st.session_state["key_pem"] if st.session_state["key_pem"] else "-")


def http_code_handler(code: Union[int, str]) -> None:
    """
    Displays the correct informational box depending on the HTTP response code given

    :param code: HTTP response code, String or integer are permitted. If String is provided, it will be coerced
                 into an Integer
    """

    if isinstance(code, str):
        try:
            code = int(code)
        except ValueError | TypeError:
            raise ValueError("Code must be an integer or string")

    base_str = "**Response Code:**"

    if code < 200:
        # info responses
        st.info(f"{base_str} {code}", icon="ℹ️")
        return
    elif code < 300:
        # successful responses
        st.success(f"{base_str} {code}", icon="✅")
        return
    elif code < 400:
        # redirection responses
        st.info(f"{base_str} {code}", icon="ℹ️")
        return
    elif code < 600:
        # client/server error
        st.error(f"{base_str} {code}", icon="🚨")
        return


def validation_error_handler(errors: list[str], warnings: list[str])\
        -> bool:
    """
    Handles the errors and warnings returned by the validation function and returns a boolean value
    that indicates if there are any errors or otherwise

    :param errors: list of errors
    :param warnings: list of warnings
    :return: True if there are no errors, else False
    """

    if len(warnings) > 0:
        warning_builder = StringBuilder("Some Warnings are raised with your inputs:").newline()

        for warning in warnings:
            warning_builder = warning_builder.newline().append(f"- {warning}")

        st.warning(warning_builder.get(), icon="⚠️")

    if len(errors) > 0:
        error_builder = StringBuilder("Some Errors are detected with your inputs:").newline().newline()

        for error in errors:
            error_builder = error_builder.newline().append(f"- {error}")

        st.error(error_builder.get(), icon="🚨")

    return len(errors) == 0

