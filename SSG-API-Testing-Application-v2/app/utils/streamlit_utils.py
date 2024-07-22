"""
This file contains utility functions and values to initialise Streamlit session variables.
"""

import streamlit as st

from typing import Union
from app.core.system.logger import Logger
from app.utils.string_utils import StringBuilder


LOGGER = Logger(__name__)


def init() -> None:
    """
    Initialises all the necessary Streamlit variables to record configurations.

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

    if "url" not in st.session_state:
        st.session_state["url"] = None


# this is an experimental feature, should it become part of the mainstream API, make sure to deprecate the use
# of this decorator and replace it with the new syntax
@st.experimental_dialog("Configs", width="large")
def display_config() -> None:
    """Displays all the loaded configuration variables."""

    st.header("API Endpoint")
    try:
        st.code(f"{st.session_state["url"].name if "url" in st.session_state else "Unknown"}: "
                f"{st.session_state["url"].value if "url" in st.session_state else "Unknown URL"}", language="text")
    except AttributeError:
        st.info("Your app has rerun, make sure to navigate back to the **Home** page to reselect the API endpoint!",
                icon="ℹ️")

    st.header("UEN")
    st.code(st.session_state["uen"] if st.session_state["uen"] else "-")

    st.header("Encryption Key:")
    st.code(st.session_state["encryption_key"] if st.session_state["encryption_key"] is not None else "-")

    st.header("Certificate Key:")
    st.code(st.session_state["cert_pem"] if st.session_state["cert_pem"] else "-")

    st.header("Private Key:")
    st.code(st.session_state["key_pem"] if st.session_state["key_pem"] else "-")


def http_code_handler(code: Union[int, str]) -> None:
    """
    Displays the correct informational box depending on the HTTP response code given.

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


def validation_error_handler(errors: list[str], warnings: list[str]) -> bool:
    """
    Handles the errors and warnings returned by the validation function and returns a boolean value
    that indicates if there are any errors or otherwise.

    :param errors: list of errors
    :param warnings: list of warnings
    :return: True if there are no errors, else False
    """

    if len(warnings) > 0:
        LOGGER.warning("Some fields have warnings, request resumed!")
        warning_builder = StringBuilder("Some Warnings are raised with your inputs:").newline()

        for warning in warnings:
            warning_builder = warning_builder.newline().append(f"- {warning}")

        st.warning(warning_builder.get(), icon="⚠️")

    if len(errors) > 0:
        LOGGER.error("Some fields are missing, request aborted!")
        error_builder = StringBuilder("Some Errors are detected with your inputs:").newline().newline()

        for error in errors:
            error_builder = error_builder.newline().append(f"- {error}")

        st.error(error_builder.get(), icon="🚨")

    return len(errors) == 0


def does_not_have_keys() -> bool:
    """Returns true if both private key and cert keys are present."""

    return st.session_state["key_pem"] is None or st.session_state["cert_pem"] is None
