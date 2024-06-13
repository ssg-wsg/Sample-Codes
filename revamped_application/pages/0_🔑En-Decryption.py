"""
This page is used to demonstrate, and assist in, the encryption and decryption of messages using a provided
AES256 key.
"""

import streamlit as st

from revamped_application.core.cipher.encrypt_decrypt import Cryptography
from revamped_application.core.system.logger import Logger
from revamped_application.utils.streamlit_utils import (init, display_config,
                                                        validation_error_handler, does_not_have_keys)

# initialise necessary variables
init()
LOGGER = Logger("Encryption/Decryption")

st.set_page_config(page_title="En-Decryption", page_icon="🔑")

with st.sidebar:
    st.header("View Configs")
    if st.button("Configs", key="config_display"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Encryption/Decryption")

st.markdown("Enter in your AES256 key below and key in the message you wish to encrypt/decrypt!")
st.header("AES Key")
key = st.text_input(label="AES Key",
                    value=st.session_state["encryption_key"] if "encryption_key" in st.session_state else "",
                    type="password",
                    key="encryption_key")

st.header("Message Encryption/Decryption")
st.markdown("Select the toggle to switch between encryption and decryption mode!")
encrypt = st.toggle(label="Encrypt Mode")

if encrypt:
    col1, col2 = st.columns(2)
    col1.subheader("Message to Encrypt")
    col2.subheader("Ciphertext")

    encrypt_out = ""
    encrypt_in = col1.text_area(label="Message", key="message")

    if len(encrypt_in) > 0:
        encrypt_out = Cryptography.encrypt(encrypt_in, return_bytes=False, key=key)
    else:
        encrypt_out = ""

    col2.text_area(label="Ciphertext", key="ciphertext", value=encrypt_out, disabled=True)
else:
    col1, col2 = st.columns(2)
    col1.subheader("Message to Decrypt")
    col2.subheader("Plaintext")

    decrypt_out = ""
    decrypt_in = col1.text_area(label="Ciphertext", key="ciphertext")

    if len(decrypt_in) > 0:
        try:
            decrypt_out = Cryptography.decrypt(decrypt_in, return_bytes=False, key=key)
        except:
            col1.error("Ciphertext is invalid or key is incorrect!")
    else:
        decrypt_out = ""

    col2.text_area(label="Plaintext", key="plaintext", value=decrypt_out, disabled=True)
