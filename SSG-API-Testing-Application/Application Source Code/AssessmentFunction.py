from AdditionalFunction import pprintJsonFormat
import base64
import json
import re

import requests
from EncryptAndDecryptFunction import doDecryption, doEncryption
from HttpRequestFunction import getHttpRequest, postHttpRequestJson

#-------------------- Description --------------------
#getAssessment uses getHttpRequest in HttpRequestFunction.py to call view Assessment API  It is used when retrieving an assessment record to view
#Upon completion, the method will return the text decypted using doDecryption method 
#Input parameter (assessmentRefNum) : Assessment Reference Number to set the URL for GET Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def getAssessment(assessmentRefNum):
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + assessmentRefNum)
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#displayViewAssessment is a formatting method that display the information in the Application in a readable format for GET HTTP Request API for View Assessment API
#Input parameter (assessmentRefNum) : Assessment Reference Number to set the URL for GET Http Request
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------
def displayViewAssessment(assessmentRefNum):
    req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + assessmentRefNum,headers={'accept':'application/json'}).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required',
      )
    return text


#-------------------- Description --------------------
#curlRequestSearchAssessment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API (Search Assessment) 
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlRequestSearchAssessment(payloadToDisplay):
     # Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/assessments/search" ,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
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
#displayUpdateAssessment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API (Update or Void Assessment API) 
#Input parameter (refNum) : Assessment Reference Number
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def displayUpdateAssessment(refNum,payloadToDisplay):
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + refNum ,headers={'accept':'application/json'},data=str(payloadToDisplay)).prepare()
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
#searchAssessment uses postHttpRequestJson in HttpRequestFunction.py to call Search Assessment API. It is used to search existing Assessment record
#The payload will be encrypted using doEncryption method before calling POST Http Request.
#Upon calling the Http Request, the server will response back the information encrypted. The method returns the response decrypted using doDecrypted method
#Input parameter (searchAssessmentPayload) : Assessment information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def searchAssessment(searchAssessmentPayload):
    searchAssessmentURL = ("https://uat-api.ssg-wsg.sg/tpg/assessments/search")

    searchAssessmentEncrypt = doEncryption(searchAssessmentPayload.encode())
    resp = postHttpRequestJson(searchAssessmentURL, searchAssessmentEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#updateAssessment uses postHttpRequestJson in HttpRequestFunction.py to call Update or Void Assessment API. It is used when updating an existing Assessment
#The payload will be encrypted using doEncryption method before calling POST Http Request. Upon completion, the method will return the text decypted using doDecryption method.
#Input parameter (refNum) : Assessment Reference Number to delete and set the URL for POST Http Request
#Input parameter (payload) : Assessment information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format 
#----------------------------------------------------- 
def updateAssessment(refNum, payload):
    updateAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments/details/" + refNum
    updateAssessmenEncrypt = doEncryption(payload.encode())
    resp = postHttpRequestJson(updateAssessmentURL, updateAssessmenEncrypt.decode())
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text
    
#-------------------- Description --------------------
#displayPostRequestAssessment is a formatting method that display the information in the Application in a readable format for POST HTTP Request API (Create Assessment) 
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def displayPostRequestAssessment(payloadToDisplay):
    req = requests.Request('POST', "https://uat-api.ssg-wsg.sg/tpg/assessments",
                           headers={'accept': 'application/json'}, data=str(payloadToDisplay)).prepare()
    text = '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
        '----------------Request Information----------------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        'Encryption: Required\nDecryption: Required',
        '----------------Payload Information----------------',
        payloadToDisplay,
    )
    return text

#-------------------- Description --------------------
#addAssessmentFn uses postHttpRequestJson in HttpRequestFunction.py to call Create Assessment API. It is used when creating a new Assessment Record
#The payload will be encrypted using doEncryption method before calling POST Http Request. Upon completion, the method will return the text decypted using doDecryption method.
#Input parameter (assessmentPayload) : Assessment information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format 
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#----------------------------------------------------- 
def addAssessmentFn(assessmentPayload):
    addAssessmentURL = "https://uat-api.ssg-wsg.sg/tpg/assessments"
    ciptertext = doEncryption(assessmentPayload.encode())
    response = postHttpRequestJson(addAssessmentURL, ciptertext.decode())
    plainText = doDecryption(response.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent=4)
    return text


