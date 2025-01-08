"""
This file contains utility functions and values to initialise Streamlit session variables.
"""

import os
from tempfile import NamedTemporaryFile
import streamlit as st

from typing import Union
from app.core.system.logger import Logger
from app.utils.string_utils import StringBuilder

from app.core.constants import Endpoints  # noqa: E402
from app.core.testdata import TestData  # noqa: E402
from app.core.system.secrets import (
    ENV_NAME_CERT, ENV_NAME_ENCRYPT, ENV_NAME_KEY, Refetch_secrets, Set_Default_Secrets, get_cert, get_encryption_key, get_private_key)

LOGGER = Logger(__name__)


def init() -> None:
    """
    Initialises all the necessary Streamlit variables to record configurations.

    :return: None
    """
    # if secrets has not been initialised or fetched, go and fetch it
    if "secret_fetched" not in st.session_state or not st.session_state["secret_fetched"]:
        st.session_state["secret_fetched"] = Set_Default_Secrets(False)
    if "last_fetched" not in st.session_state:
        st.session_state["last_fetched"] = float(0)

    if "uen" not in st.session_state:
        st.session_state["uen"] = TestData.UEN.value

    if "encryption_key" not in st.session_state:
        st.session_state["encryption_key"] = ""

    if "cert_pem" not in st.session_state:
        st.session_state["cert_pem"] = None

    if "key_pem" not in st.session_state:
        st.session_state["key_pem"] = None

    st.session_state["url"] = Endpoints.UAT

    if "default_secrets" not in st.session_state:
        st.session_state["default_secrets"] = True

    if "default_secrets_checkbox" not in st.session_state and "default_secrets" in st.session_state:
        st.session_state["default_secrets_checkbox"] = st.session_state["default_secrets"]


# this is an experimental feature, should it become part of the mainstream API, make sure to deprecate the use
# of this decorator and replace it with the new syntax
@st.experimental_dialog("Configs", width="large")
def display_config() -> None:
    """Displays all the loaded configuration variables."""

    st.header("API Endpoint")
    try:
        st.code(f"{st.session_state['url'].name if 'url' in st.session_state else 'Unknown'}: "
                f"{st.session_state['url'].value if 'url' in st.session_state else 'Unknown URL'}", language="text")
    except AttributeError:
        st.info("Your app has rerun, make sure to navigate back to the **Home** page to reselect the API endpoint!",
                icon="ℹ️")

    st.header("UEN")
    st.code(st.session_state["uen"] if st.session_state["uen"] else "-")

    defaults_col1, defaults_col2 = st.columns(2)

    defaults_col1.header("Are defaults secrets set?")
    defaults_col1.code(st.session_state["secret_fetched"]
                       if st.session_state["secret_fetched"] is not None else "-")
    defaults_col2.write(
        "Please click this button to attempt to refetch default secrets")
    defaults_col2.button(label="Refetch secrets",
                         help="If this button does not work, please try again later",
                         on_click=Refetch_secrets,
                         args=(True, ))

    st.header("Encryption Key (Will not be used):")
    st.code(st.session_state["encryption_key"]
            if st.session_state["encryption_key"] else "-")

    st.header("Certificate Key (Will not be used):")
    st.code(st.session_state["cert_pem"]
            if st.session_state["cert_pem"] else "-")

    st.header("Private Key (Will not be used):")
    st.code(st.session_state["key_pem"]
            if st.session_state["key_pem"] else "-")


def http_code_handler(code: Union[int, str]) -> None:
    """
    Displays the correct informational box depending on the HTTP response code given.

    :param code: HTTP response code, String or integer are permitted. If String is provided, it will be coerced
                 into an Integer
    """

    if isinstance(code, str):
        try:
            code = int(code)
        except (ValueError, TypeError) as e:
            raise ValueError("Code must be an integer or string") from e

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
        warning_builder = StringBuilder(
            "Some Warnings are raised with your inputs:").newline()

        for warning in warnings:
            warning_builder = warning_builder.newline().append(f"- {warning}")

        st.warning(warning_builder.get(), icon="⚠️")

    if len(errors) > 0:
        LOGGER.error("Some fields are missing, request aborted!")
        error_builder = StringBuilder(
            "Some Errors are detected with your inputs:").newline().newline()

        for error in errors:
            error_builder = error_builder.newline().append(f"- {error}")

        st.error(error_builder.get(), icon="🚨")

    return len(errors) == 0


def does_not_have_encryption_key() -> bool:
    """Returns true if user encryption key is missing"""
    return ("encryption_key" not in st.session_state
            or st.session_state["encryption_key"] is None
            or len(st.session_state["encryption_key"]) == 0)


def does_not_have_keys() -> bool:
    """Returns true if either private key or cert keys are missing."""

    return st.session_state["key_pem"] is None or st.session_state["cert_pem"] is None


def does_not_have_url() -> bool:
    """Returns true if url endpoint is missing."""

    return "url" not in st.session_state or st.session_state["url"] is None


def display_debug() -> None:
    """Change the loaded configuration variables."""
    LOGGER.info("Debug is loading")
    st.header("Encryption Key:")
    st.session_state["encryption_key"] = st.text_input("Encryption key",
                                                   value=st.session_state["encryption_key"])
    os.environ[ENV_NAME_ENCRYPT] = st.session_state["encryption_key"]
    st.code(get_encryption_key())
    
    st.header("Certificate Key:")
    cert_pem = st.file_uploader(label="Certificate Key",
                                type=["pem"],
                                accept_multiple_files=False,
                                key="cert_dev")
    if cert_pem is not None:
        st.session_state["cert_pem"] = NamedTemporaryFile(
                        delete=False, delete_on_close=False, suffix=".pem")
        st.session_state["cert_pem"].write(cert_pem.read())
        st.session_state["cert_pem"] = st.session_state["cert_pem"].name
        os.environ[ENV_NAME_CERT] = st.session_state["cert_pem"]
    st.code(get_cert())

    st.header("Private Key:")
    key_pem = st.file_uploader(label="Private Key",
                               type=["pem"],
                               accept_multiple_files=False,
                               key="key_dev")
    if key_pem is not None:
        st.session_state["key_pem"] = NamedTemporaryFile(
                        delete=False, delete_on_close=False, suffix=".pem")
        st.session_state["key_pem"].write(key_pem.read())
        st.session_state["key_pem"] = st.session_state["key_pem"].name
        os.environ[ENV_NAME_KEY] = st.session_state["key_pem"]
    st.code(get_private_key())
