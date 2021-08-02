import re
import json

from cryptography.hazmat.primitives.ciphers.base import CipherContext
import requests
from requests.models import Response
from EncryptAndDecryptFunction import doDecryption, doEncryption
from HttpRequestFunction import getHttpRequest, postHttpRequestJson

#-------------------- Description --------------------
#addEnrolment uses postHttpRequestJson in HttpRequestFunction.py to call Add Enrolment API. It is used when creating a new Enrolement
#The payload will be encrypted using doEncryption method before calling POST Http Request
#Input parameter (enrolmentPayload) : Enrolment information in text format to send as payload in POST Http Request
#Output parameter (response.text) : Response in Text format return from the server
#-----------------------------------------------------
def addEnrolment(enrolmentPayload):
    createEnrollmenturl = "https://uat-api.ssg-wsg.sg/tpg/enrolments"
    ciptertext = doEncryption(enrolmentPayload.encode())
    response = postHttpRequestJson(createEnrollmenturl, ciptertext.decode())
    return response.text

#-------------------- Description --------------------
#cancelEnrolment uses postHttpRequestJson in HttpRequestFunction.py to call Update or Cancel Enrolment API. It is used when deleting a existing Course Run
#The payload will be preset then encrypted using doEncryption method before calling POST Http Request
#Upon calling the Http Request, the server will response back the information encrypted. The method returns the response decrypted using doDecrypted method
#Input parameter (referenceNumber) : Enrolment Id to delete and set the URL for POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#----------------------------------------------------- 
def cancelEnrolment(referenceNumber):
    print("Cancel Enrolment")
    cancelPayloadurl = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(referenceNumber)
    cancelPayload = "{\"enrolment\":{\"action\":\"Cancel\"}}"
    
    cancelPayloadEncrypt = doEncryption(cancelPayload.encode())
    resp = postHttpRequestJson(cancelPayloadurl, cancelPayloadEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent=4)
    return text
#-------------------- Description --------------------
#updateEnrolment uses postHttpRequestJson in HttpRequestFunction.py to call Update or Cancel Enrolment API. It is used when updating a existing Enrolment
#The payload will be encrypted using doEncryption method before calling POST Http Request
#Input parameter (referenceNumber) : Enrolment Reference Number to delete and set the URL for POST Http Request
#Input parameter (payload) : Enrolment information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format 
#Additional Note : This method update all possible fields for Enrolment
#----------------------------------------------------- 
def updateEnrolment(referenceNumber, payload):
    url = "https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(referenceNumber)
    payloadEncrypted = doEncryption(payload.encode())
    resp = postHttpRequestJson(url, payloadEncrypted.decode())
    return resp.text 

#-------------------- Description --------------------
#getEnrolment uses getHttpRequest in HttpRequestFunction.py to call view Enrolment API.  It is used when retrieving an Enrolment to view
#Upon completion, the method will return the text decypted using doDecryption method 
#Input parameter (enrolmentRefNo) : Enrolment Reference Number to set the URL for GET Http Request
#Output parameter (resp) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def getEnrolment(enrolmentRefNo):
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + str(enrolmentRefNo))
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#updateEnrolmentFee uses postHttpRequestJson in HttpRequestFunction.py to call Update Enrolment Fee Collection API. It is used when updating an existing Enrolment's CollectionStatus
#This method uses the payload information from another method (getUpdateEnrolmentFeePayLoad) that is obtained from the Application based on the User's Input
#Upon completion, the method will return the text decypted using doDecryption method 
#Input parameter (enrolmentRefNo) : Enrolment Reference Number to update and set the URL for POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : This method only update the collectionStatus of the enrolment
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def updateEnrolmentFee(enrolmentRefNo):
    updateEnrolmentFeeURL = ("https://uat-api.ssg-wsg.sg/tpg/enrolments/feeCollections/" + str(enrolmentRefNo))

    UpdateEnrolmentFeeEncrypt = doEncryption(updateEnrolmentFeePayLoad.encode())
    resp = postHttpRequestJson(updateEnrolmentFeeURL, UpdateEnrolmentFeeEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#searchEnrolment uses postHttpRequestJson in HttpRequestFunction.py to call Search Enrolment API. It is used to search existing Enrolment record
#The payload will be encrypted using doEncryption method before calling POST Http Request.
#Upon calling the Http Request, the server will response back the information encrypted. The method returns the response decrypted using doDecrypted method
#Input parameter (searchEnrolmentPayload) : Enrolment information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def searchEnrolment(searchEnrolmentPayload):
    searchEnrolmentURL = ("https://uat-api.ssg-wsg.sg/tpg/enrolments/search")

    searchEnrolmentEncrypt = doEncryption(searchEnrolmentPayload.encode())
    resp = postHttpRequestJson(searchEnrolmentURL, searchEnrolmentEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#curlRequestSearchEnrolment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API (Search Enrolment) 
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlRequestSearchEnrolment(payloadToDisplay):
     # Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/search/" ,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
          req.method + ' ' + req.url,
          '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
          'Encryption: Required\nDecryption: Required',
          '----------------Payload Information----------------',
          payloadToDisplay,
      )
      return text

#-------------------- Description --------------------
#curlPostRequest is a formatting method that display the information in the Application in a readable format for POST HTTP Request API for delete Enrolment Page
#Input parameter (EnrolmentRefNum) : Enrolment References Number
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlPostRequest(EnrolmentRefNum, payloadToDisplay):
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + EnrolmentRefNum,headers={'accept':'application/json'},data=str(payloadToDisplay)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Encryption: Required\nDecryption: Required',
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text

#-------------------- Description --------------------
#getDeleteEnrolmentPayLoad is fixed method to return the preset payload for delete Enrolment
#It shows the correct formatting of the payload which will be used to display on the Application and send as a payload for cancelEnrolment method
#Output parameter (deleteEnrolmentPayLoad) : Delete Enrolment Payload
#----------------------------------------------------- 
def getDeleteEnrolmentPayLoad():
    global deleteEnrolmentPayLoad
    deleteEnrolmentPayLoad = "{\n    \"enrolment\": {\n        \"action\": \"" + "Cancel" + "\"\n    }   \n}"
    return deleteEnrolmentPayLoad

#-------------------- Description --------------------
#displayPostRequestEnrolment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API for Create Enrolment Page
#Input parameter (refnumber) : Enrolment References Number
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------  
def displayPostRequestEnrolment(refnumber, payloadToDisplay):

    req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/" + refnumber,headers={'accept':'application/json'},data=str(payloadToDisplay)).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
        '----------------Request Information----------------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        'Encryption: Required\nDecryption: Required',
        '----------------Payload Information----------------',
        payloadToDisplay,
    )
    return text

#-------------------- Description --------------------
#getUpdateEnrolmentFeePayLoad is fixed method to return the payload for updateEnrolmentFee showing the updated information according to the User's input.
#It shows the correct formatting of the payload which will be used to display on the Application and send as a payload for cancelEnrolment method
#Input parameter (status) : Collection Status that is going to be updated
#Output parameter (updateEnrolmentFeePayLoad) : Delete Enrolment Payload
#----------------------------------------------------- 
def getUpdateEnrolmentFeePayLoad(status):
    global updateEnrolmentFeePayLoad

    updateEnrolmentFeePayLoad = "{\n    \"enrolment\": {\n        \"fees\": " + "{" + "\n          \"collectionStatus\": \"" + status + "\" \n        } \n     }   \n }"
    return updateEnrolmentFeePayLoad


#-------------------- Description --------------------
#curlPostRequestUpdateEnrolmentFee is a formatting method that display the information in the Application in a readable format for POST HTTP Request API for Update enrolment fee Page
#Input parameter (EnrolmentRefNum) : Enrolment References Number
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------  
def curlPostRequestUpdateEnrolmentFee(EnrolmentRefNum, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/enrolments/feeCollections/" + EnrolmentRefNum,headers={'accept':'application/json'},data=str(payloadToDisplay)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Encryption: Required\nDecryption: Required',
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text




#-------------------- Description --------------------
#curlGetRequestViewEnrolment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API for View Enrolment Page
#Input parameter (EnrolmentRefNum) : Enrolment References Number
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------  
def curlGetRequestViewEnrolment(EnrolmentRefNum):
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/enrolments/details/" + EnrolmentRefNum,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required'
      )
      return text
