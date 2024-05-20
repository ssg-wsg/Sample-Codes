import base64
import logging
import os
import tempfile

import streamlit as st

from utils.streamlit_utils import init, display_config
from utils.verify import verify_uen
from core.system.cleaner import clean_temp
from tempfile import NamedTemporaryFile

# initialise all variables
init()

# initialise cron process
clean_temp()

st.set_page_config(page_title="Home", page_icon="🏠")

with st.sidebar:
    if st.button("Configs", key="config_display"):
        display_config()


st.title("SSG API Demo")
st.markdown("Welcome to the SSG API Demo App!\n\n"
            "Select any one of the pages on the left sidebar to view sample codes for each of the different crucial "
            "components of the SSG API suite!")

st.subheader("Configurations")
st.markdown("Before you continue, make sure to fill up the following configuration details needed for the demo app! "
            "Failure to enter in any one of these variables may prevent you from fully exploring all features "
            "of the app!\n\nYou can view your configurations at any time by clicking on the `Configs` button on the "
            "sidebar!")

with st.form(key="init_config"):
    uen = st.text_input("Enter in your UEN", help="UEN stands for **Unique Entity Number**. It is used by the SSG API "
                                                  "to identify your organisation.")
    enc_key = st.text_area("Enter in your encryption key", help="Refer to this [guide](https://developer.ssg-wsg.gov"
                                                                ".sg/webapp/guides/6gvz7gEnwU2dSIKPrTcXnq#authenticat"
                                                                "ion-types) for more info.")
    cert_pem = st.file_uploader("Upload your Certificate Key", type=["pem"], accept_multiple_files=False)
    key_pem = st.file_uploader("Upload your Private Key", type=["pem"], accept_multiple_files=False)

    if st.form_submit_button():
        if len(uen) > 0 and not verify_uen(uen):
            st.error("Invalid UEN provided!")
        elif all([uen, enc_key, cert_pem, key_pem]) and len(uen) > 0 and len(enc_key) > 0:
            try:
                # save the byte stream into a temp file to give it a path for passing it to requests
                st.session_state["cert_pem"] = NamedTemporaryFile(delete=False, delete_on_close=False, suffix=".pem")
                st.session_state["cert_pem"].write(cert_pem.read())
                st.session_state["cert_pem"] = st.session_state["cert_pem"].name

                st.session_state["key_pem"] = NamedTemporaryFile(delete=False, delete_on_close=False, suffix=".pem")
                st.session_state["key_pem"].write(cert_pem.read())
                st.session_state["key_pem"] = st.session_state["key_pem"].name

                st.session_state["uen"] = uen.upper()  # UENs only have upper case characters
                st.session_state["encryption_key"] = enc_key
                st.success("Configurations loaded!")
            except base64.binascii.Error:
                st.error("Certificate or private key is invalid!")
        else:
            st.error("Please fill up the above configuration details needed for the demo app!")
