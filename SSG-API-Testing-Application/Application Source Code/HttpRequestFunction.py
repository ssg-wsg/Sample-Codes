import os
from AdditionalFunction import loadFile, printResponse
import requests
import json
from resources import config_path
from tkinter import messagebox

#-------------------- Description --------------------
#httpRequestInit is an automated configuration method that is triggered whenever the following method is called - getHttpRequest, postHttpRequest, postHttpRequestJson.
#httpRequestInit operate with an external Json file (config.json) where it would load the Cert Pem File ("certPath") and Key Pem File ("keyPath") which will be used when calling the API
#It uses loadFile function from Additional Function.py to load the config.json file
#Additional Note : "config_path" refers to the location path of the config.json file
#-----------------------------------------------------
def httpRequestInit():
      global keyPath, certPath
      config = loadFile(config_path)
      config = json.loads(config)
      keyPath = config["keyPath"]
      certPath = config["certPath"]
      isCertPathExist = os.path.exists(certPath)
      isKeyPathExist = os.path.exists(keyPath)
      if isKeyPathExist == False or isCertPathExist == False:
            messagebox.showerror("Error", "Invalid Cert or Key Path")


#-------------------- Description --------------------
#getHttpRequest is a method to send GET Http request.
#getHttpRequest uses requests library to send the GET Http request
#Input parameter (request_url) : URL to send the GET Http request to 
#Output parameter (response) : Response Object
#Additional Note : "cert" is used as a Client Side Certificates.  It can be specific as a single file (containing the private key and the certificate)
#-----------------------------------------------------
def getHttpRequest(request_url):
      httpRequestInit()
      response = requests.get(request_url, cert = (certPath,keyPath))
      return response

      
#-------------------- Description --------------------
#postHttpRequest is a method to send POST Http request.
#postHttpRequest starts by invoking httpRequestInit() method
#postHttpRequest uses requests library to send the POST Http request
#Input parameter (request_url) : URL to send the POST Http request to 
#Input parameter (payload) : payload information set as POST  
#Output parameter (response) : Response Object
#Additional Note 1 : This method is used when encryption is not needed
#Additional Note 2 : "cert" is used as a Client Side Certificates.  It can be specific as a single file (containing the private key and the certificate)
#-----------------------------------------------------
def postHttpRequest(request_url, payload):
      httpRequestInit()
      response = requests.post(request_url, data = payload,cert = (certPath,keyPath))
      printResponse(response)
      return response

#-------------------- Description --------------------
#postHttpRequestJson is a method to send POST Http request.
#postHttpRequestJson starts by invoking httpRequestInit() method
#postHttpRequestJson uses requests library to send the POST Http request
#Input parameter (request_url) : URL to send the POST Http request to 
#Input parameter (payload) : payload information set as POST
#Output parameter (response) : Response Object
#Additional Note 1 : This method is used when encryption is needed. The reason behind is to form-encoded the payload. Using "json = payload", helps to encode it automatically
#Additional Note 2 : "cert" is used as a Client Side Certificates.  It can be specific as a single file (containing the private key and the certificate)
#-----------------------------------------------------
def postHttpRequestJson(request_url, payload):
      httpRequestInit()
      response = requests.post(request_url, json = payload,cert =  (certPath,keyPath))
      return response

