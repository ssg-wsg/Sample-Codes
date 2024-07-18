"""
This page is used to demonstrate, and assist in, the encryption and decryption of messages using a provided
AES256 key.
"""

import streamlit as st

from app.core.cipher.encrypt_decrypt import Cryptography
from app.core.system.logger import Logger
from app.utils.streamlit_utils import init, display_config
from app.utils.verify import Validators

# initialise necessary variables
init()
LOGGER = Logger("Encryption/Decryption")

st.set_page_config(page_title="En-Decryption", page_icon="🔑")

with st.sidebar:
    st.header("View Configs")
    st.markdown("Click the `Configs` button to view your loaded configurations at any time!")

    if st.button("Configs", key="config_display", type="primary"):
        display_config()

st.image("assets/sf.png", width=200)
st.title("Encryption/Decryption")
st.markdown("This page helps you to experiment with the AES-256 encryption algorithm, by allowing you to use "
            "your AES key to encrypt or decrypt messages!")

st.header("AES Key")
st.markdown("Enter in your AES key or reuse the AES key provided in the Home page!")
key = st.text_input(label="AES Key",
                    value=st.session_state["encryption_key"] if "encryption_key" in st.session_state else "",
                    type="password",
                    key="encryption_key")

if key is None or len(key) == 0:
    LOGGER.error("No key provided!")
    st.error("No AES-256 key provided!", icon="🚨")
elif not Validators.verify_aes_encryption_key(key):
    LOGGER.error("No valid AES-256 key provided!")
    st.error("Invalid AES-256 key provided!", icon="🚨")
else:
    LOGGER.info("Valid AES-256 key detected!")
    st.header("Message Encryption/Decryption")
    st.markdown("Select the toggle to switch between encryption and decryption mode!")
    encrypt = st.toggle(label="Encrypt Mode")

    if encrypt:
        LOGGER.info("Encryption mode set...")
        col1, col2 = st.columns(2)
        col1.subheader("Message to Encrypt")
        col2.subheader("Ciphertext")

        encrypt_out = ""
        encrypt_in = col1.text_area(label="Message", label_visibility="hidden", key="message-encrypt", height=200)

        if len(encrypt_in) > 0:
            LOGGER.info("Encrypting message...")

            try:
                encrypt_out = Cryptography.encrypt(encrypt_in, return_bytes=False, key=key)
            except Exception as ex:
                LOGGER.error(f"Encryption failed with: {ex}")
                col1.error("Message is invalid or key is incorrect!", icon="🚨")
        else:
            encrypt_out = ""

        col2.text_area(label="Ciphertext", label_visibility="hidden", key="ciphertext-encrypt",
                       value=encrypt_out, disabled=True, height=200)
    else:
        LOGGER.info("Decryption mode set...")
        col1, col2 = st.columns(2)
        col1.subheader("Message to Decrypt")
        col2.subheader("Plaintext")

        decrypt_out = ""
        decrypt_in = col1.text_area(label="Ciphertext", label_visibility="hidden", key="ciphertext-decrypt", height=200)

        if len(decrypt_in) > 0:
            LOGGER.info("Decrypting message...")

            try:
                decrypt_out = Cryptography.decrypt(decrypt_in, return_bytes=False, key=key)
            except Exception as ex:
                LOGGER.error(f"Decryption failed with: {ex}")
                col1.error("Ciphertext is invalid or key is incorrect!", icon="🚨")
        else:
            decrypt_out = ""

        col2.text_area(label="Plaintext", label_visibility="hidden", key="plaintext",
                       value=decrypt_out, disabled=True, height=200)
