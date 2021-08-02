from HttpRequestFunction import loadFile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode
import json
from resources import config_path



#-------------------- Description --------------------
#doEncryption encrypt the payload in Bytes format. This method is used when encryption is required based on the API requirement (Request Encrypted)
#doEncryption operate with an external Json file (config.json) where it would load the encryption key ("key") and Initialization Vector ("IV") which will be used to encrypt the payload
#It uses cryptography libraries with a default backend and a preconfigured Initialization Vector - "SSGAPIInitVector"
#Input parameter (payloadByte) : payload to encrypt in Bytes 
#Output parameter (ciphertxt_out) : encrypted payload in Bytes
#Additional Note : "config_path" refers to the location path of the config.json file
#-----------------------------------------------------
def doEncryption(payloadByte):
    #preConfiguration - obtained the required information from config.json file in the folder
    configInfo = loadFile(config_path)
    configInfoJson = json.loads(configInfo) 
    key = b64decode(configInfoJson["key"])
    cipher = Cipher(algorithms.AES(key), modes.CBC((configInfoJson["IV"]).encode()), backend=default_backend())
    padder = padding.PKCS7(128).padder()
    
    encryptor = cipher.encryptor()
    payloadToSend = padder.update(payloadByte) + padder.finalize()
    ciphertxt = encryptor.update(payloadToSend) + encryptor.finalize()
    ciphertxt_out = b64encode(ciphertxt)
    return ciphertxt_out

#-------------------- Description --------------------
#doDecryption encrypt the payload in Bytes format. This method is used when decryption is required based on the API requirement (Response Encrypted)
#doDecryption operate with an external Json file (config.json) where it would load the encryption key ("key") and Initialization Vector ("IV") which will be used to decrypt the payload
#It uses cryptography libraries with a default backend and a preconfigured Initialization Vector - "SSGAPIInitVector"
#Input parameter (response) : response to decrypt in Bytes 
#Output parameter (plain) : decrypted response in Bytes
#Additional Note : "config_path" refers to the location path of the config.json file
#-----------------------------------------------------
def doDecryption(response):
    #preConfiguration - obtained the required information from config.json file in the folder
    configInfo = loadFile(config_path)
    configInfoJson = json.loads(configInfo)
    key = b64decode(configInfoJson["key"])
    cipher = Cipher(algorithms.AES(key), modes.CBC((configInfoJson["IV"]).encode()), backend=default_backend())
    unpadder = padding.PKCS7(128).unpadder()

    result = b64decode(response)
    decryptor = cipher.decryptor()
    plain = decryptor.update(result) + decryptor.finalize()
    plain = unpadder.update(plain) + unpadder.finalize()
    return plain


