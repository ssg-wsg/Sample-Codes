from HttpRequestFunction import getHttpRequest, postHttpRequestJson
from AdditionalFunction import pprintJsonFormat, saveJsonFormat, loadFile
import re
from EncryptAndDecryptFunction import *
import requests
import json
#-------------------- Description --------------------
#getSessionAttendance uses getHttpRequest in HttpRequestFunction.py to call Course Session Attendance API.  It is used to retrieve course session attendance information
#Based on the values passed in, the URL will be set dynamically before calling the HTTP Request. Upon completion, the method will return the text decypted using doDecryption method 
#Input parameter (runId) : Course Run Id
#Input parameter (uen) : Training Partner UEN obtained from config.json
#Input parameter (crn) : Course Reference Number
#Input parameter (sessionId) : Session Id of the Course Run
#Output parameter (text) : Response return from the server in Readable Text format
#Additional Note : json.loads follow by json.dumps is used to indent the text into readable format
#-----------------------------------------------------
def getSessionAttendance(runId, uen, crn, sessionId):
    if uen != '':
        uen = "?uen=" + uen
    if crn != '':
        crn = "&courseReferenceNumber=" + crn
    if sessionId != '':
        sessionId = "&sessionId=" + sessionId
    resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions/attendance" + uen + crn + sessionId)
    plainText = doDecryption(resp.text)
    json_load = json.loads(plainText.decode())
    text = json.dumps(json_load, indent = 4)
    return text

#-------------------- Description --------------------
#displayViewSession is a formatting method that display the information in the Application in a readable format for GET HTTP Request API for View Session Attendance Page
#Based on the values passed in, the URL will be displayed dynamically to the User in the Application
#Input parameter (runId) : Course Run Id
#Input parameter (uen) : Training Partner UEN obtained from config.json
#Input parameter (crn) : Course Reference Number
#Input parameter (sessionId) : Session Id of the Course Run
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------  
def displayViewSession(runId, uen, crn, sessionId):
    if uen != '':
        uen = "?uen=" + uen
    if crn != '':
            crn = "&courseReferenceNumber=" + crn
    if sessionId != '':
        sessionId = "&sessionId=" + sessionId
    req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions/attendance" + uen + crn + sessionId,headers={'accept':'application/json'}).prepare()
    text =  '{}\n{}\r\n{}\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            'Decryption: Required'
      )
    return text

#-------------------- Description --------------------
#curlRequestUploadAttendance is a formatting method that display the information in the Application in a readable format for GET HTTP Request API for Upload Session Attendance Page
#Based on the values passed in, the URL will be displayed dynamically to the User in the Application
#Input parameter (runId) : Course Run Id
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#-----------------------------------------------------  
def curlRequestUploadAttendance(runId, payloadToDisplay):
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/courses/runs/" +  str(runId) + "/sessions/attendance" ,headers={'accept':'application/json'},data=str(payloadToDisplay)).prepare()
      text =  '{}\n{}\r\n{}\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
          req.method + ' ' + req.url,
          '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
          'Encryption: Required\n',
          '----------------Payload Information----------------',
          payloadToDisplay,
      )
      return text

#-------------------- Description --------------------
#uploadAttendanceFn uses getHttpRequest in HttpRequestFunction.py to call Upload Course Session Attendance API.  It is used to upload a course session attendance information
#The payload will be encrypted using doEncryption method before calling POST Http Request
#Upon completion, the method will return the text decypted using doDecryption method 
#Input parameter (runId) : Course Run Id
#Input parameter (attendancePayload) : Attendance information in text format to send as payload in POST Http Request
#Output parameter (text) : Response return from the server in Readable Text format
#-----------------------------------------------------
def uploadAttendanceFn(runId, attendancePayload):
    baseAttendanceURL = "https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId) + "/sessions/attendance"
    ciptertext = doEncryption(attendancePayload.encode())
    response = postHttpRequestJson(baseAttendanceURL, ciptertext.decode())
    return response.text
