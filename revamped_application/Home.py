import os
import sys

# append current file path to PATH so that it is discoverable for absolute imports; this must be done
# before the other files from the same project are imported
# taken from https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
FILE_LOC = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(FILE_LOC))

# ignore E402 rule for this part only
import base64  # noqa: E402
import streamlit as st  # noqa: E402
import streamlit_nested_layout  # noqa: E402

from tempfile import NamedTemporaryFile  # noqa: E402

from utils.streamlit_utils import init, display_config  # noqa: E402
from utils.verify import Validators  # noqa: E402
from core.system.cleaner import start_schedule  # noqa: E402
from core.system.logger import Logger  # noqa: E402
from core.constants import Endpoints  # noqa: E402

# initialise all variables and logger
init()
LOGGER = Logger("Home")

# each new connection to the app cleans up the temp folder
start_schedule()

st.set_page_config(page_title="Home", page_icon="🏠")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")
    if st.button("Configs", key="config_display"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("SSG API Sample Application")
st.markdown("Welcome to the SSG API Sample Application!\n\n"
            "Select any one of the pages on the left sidebar to view sample codes for each of the different crucial "
            "components of the SSG API suite!")

st.subheader("Configurations")
st.markdown("Before you continue, make sure to fill up the following configuration details needed for the demo app! "
            "Failure to enter in any one of these variables may **prevent you from fully exploring all features "
            "of the app**!\n\nYou can view your configurations at any time by clicking on the `Configs` button on the "
            "sidebar!")

st.subheader("API Endpoint")
st.markdown("Select the endpoint you wish to connect to!")
st.session_state["url"] = st.selectbox(label="Select an API Endpoint to send your requests to",
                                       options=Endpoints,
                                       format_func=lambda endpoint: endpoint.name)

st.subheader("UEN and Keys")
st.markdown("Key in your UEN number, as well as your encryption keys, certificate key (`.pem`) and private key "
            "(`.pem`) below!")

# UEN to be loaded outside of a form
uen = st.text_input(label="Enter in your UEN",
                    help="UEN stands for **Unique Entity Number**. It is used by the SSG API "
                         "to identify your organisation.",
                    value="" if st.session_state["uen"] is None else st.session_state["uen"])

if len(uen) > 0:
    if not Validators.verify_uen(uen):
        LOGGER.error("Invalid UEN provided!")
        st.error("Invalid **UEN** provided!", icon="🚨")
    else:
        st.session_state["uen"] = uen.upper()  # UENs only have upper case characters
        LOGGER.info("UEN loaded!")
        st.success("**UEN** loaded successfully!", icon="✅")

# AES Encryption Key to be loaded outside of a form
enc_key = st.text_input("Enter in your encryption key", type="password",
                        help="Refer to this [guide](https://developer.ssg-wsg.gov.sg/webapp/guides/"
                             "6gvz7gEnwU2dSIKPrTcXnq#authentication-types) for more info.",
                        value="" if st.session_state["encryption_key"] is None else st.session_state["encryption_key"])

if len(enc_key) > 0:
    if not Validators.verify_aes_encryption_key(enc_key):
        LOGGER.error("Invalid AES-256 encryption key provided!")
        st.error("Invalid **AES-256 Encryption Key** provided!", icon="🚨")
    else:
        st.session_state["encryption_key"] = enc_key
        LOGGER.info("Encryption Key loaded!")
        st.success("**Encryption Key** loaded successfully!", icon="✅")

# Credentials need to be loaded in a form to ensure that the pair submitted is valid
with st.form(key="init_config"):
    cert_pem = st.file_uploader(label="Upload your Certificate Key",
                                type=["pem"],
                                accept_multiple_files=False,
                                key="cert")
    key_pem = st.file_uploader(label="Upload your Private Key",
                               type=["pem"],
                               accept_multiple_files=False,
                               key="key")

    if st.form_submit_button("Load"):
        LOGGER.info("Loading configurations...")

        if cert_pem is None:
            LOGGER.error("No valid Certificate key provided!")
            st.error("**Certificate Key** is not provided!", icon="🚨")
        elif key_pem is None:
            LOGGER.error("No valid Private Key provided!")
            st.error("**Private Key** is not provided!", icon="🚨")
        else:
            try:
                LOGGER.info("Verifying configurations...")
                # save the byte stream into a temp file to give it a path for passing it to requests
                st.session_state["cert_pem"] = NamedTemporaryFile(delete=False, delete_on_close=False, suffix=".pem")
                st.session_state["cert_pem"].write(cert_pem.read())
                st.session_state["cert_pem"] = st.session_state["cert_pem"].name
                LOGGER.info("Certificate loaded!")

                st.session_state["key_pem"] = NamedTemporaryFile(delete=False, delete_on_close=False, suffix=".pem")
                st.session_state["key_pem"].write(key_pem.read())
                st.session_state["key_pem"] = st.session_state["key_pem"].name
                LOGGER.info("Private key loaded!")

                LOGGER.info("Verifying certificate and key...")
                if not Validators.verify_cert_private_key(st.session_state["cert_pem"], st.session_state["key_pem"]):
                    LOGGER.error("Certificate and private key are not valid!")
                    raise AssertionError("Certificate and private key are not valid! Are you sure that you "
                                         "have uploaded your certificates and private keys properly?")
                LOGGER.info("Certificate and key verified!")
                st.success("**Certificate and Key loaded successfully!**\n\n", icon="✅")
            except base64.binascii.Error:
                LOGGER.error("Certificate/Private key is not encoded in Base64, or that the cert/key is invalid!")
                st.error("Certificate or private key is invalid!", icon="🚨")
            except AssertionError as ex:
                LOGGER.error(ex)
                st.error(ex, icon="🚨")
