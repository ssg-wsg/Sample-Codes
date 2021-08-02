from AdditionalFunction import loadFile
import requests
import json
from HttpRequestFunction import *
import re

#-------------------- Description --------------------
#getCourseRun uses getHttpRequest in HttpRequestFunction.py to call Course Run By Run Id API  It is used when retrieving a course Run to view
#Input parameter (runId) : Course Run Id to set the URL for GET Http Request
#Output parameter (resp) : Response Object from request Library
#-----------------------------------------------------
def getCourseRun(runId):
      resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId))
      return resp

#-------------------- Description --------------------
#createCourserun uses postHttpRequest in HttpRequestFunction.py to call Add Course Run API. It is used when creating a new Course Run
#Input parameter (payload) : Course information in text format to send as payload in POST Http Request
#Output parameter (resp) : Response Object from request Library
#-----------------------------------------------------
def createCourserun(payload):
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs" , payload)
      return response

#-------------------- Description --------------------
#updateCourserun uses postHttpRequest in HttpRequestFunction.py to call Update/Delete Course Run API. It is used when updating a existing Course Run
#Input parameter (runId) : Course Run Id to update and set the URL for POST Http Request
#Input parameter (payload) : Updated Course information in text format to send as payload in POST Http Request
#Output parameter (resp) : Response Object from request Library
#Additional Note : This method is similar to delete Course Run. Only different is that payload in delete course run payload is fixed
#-----------------------------------------------------
def updateCourserun(runId, payload):
      print("update")
      response = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), payload)
      return response

#-------------------- Description --------------------
#deleteCourserun uses postHttpRequest in HttpRequestFunction.py to call Update/Delete Course Run API. It is used when deleting a existing Course Run
#Input parameter (runId) : Course Run Id to delete and set the URL for POST Http Request
#Output parameter (resp) : Response Object from request Library
#Additional Note : This method is similar to Update Course Run. Only different is that payload in delete course run payload is fixed thus only require 1 parameter
#----------------------------------------------------- 
def deleteCourserun(runId):
      resp = postHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + str(runId), deleteCourseRunPayLoad)
      return resp


#-------------------- Description --------------------
#getDeleteCourseRunPayLoad is to return the payload for delete course run showing the updated information from config.json file and User's input.
#It shows the correct formatting of the payload which will be used to display on the Application and send as a payload for deleteCourserun method
#Input parameter (CRN) : Course References Number (CRN) 
#Output parameter (deleteCourseRunPayLoad) : Delete Course Run Payload Information according the the CRN and UEN from the User
#----------------------------------------------------- 
def getDeleteCourseRunPayLoad(CRN):
      global deleteCourseRunPayLoad
      
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]

      deleteCourseRunPayLoad = "{\n    \"course\": {\n        \"courseReferenceNumber\": \"" + CRN + "\",\n        \"trainingProvider\": {\n            \"uen\": \""+ uen + "\"\n        },\n        \"run\": {\n            \"action\": \"delete\"\n        }\n    }\n}"
      return deleteCourseRunPayLoad

#-------------------- Description --------------------
#getCourseSession uses getHttpRequest in HttpRequestFunction.py to call Course Session API  It is commonly use to retrieve the Session Id of a Session.
#getCourses uses three parameter to extract all the session within the time frame of a specific course run and Course Refernces Number
#Input parameter (runId) : Course Run Id 
#Input parameter (CRN) : Course References Number (CRN) 
#Input parameter (sessionMonth) : Month and Year to view 
#Output parameter (resp) : Response Object from request Library
#----------------------------------------------------- 
def getCourseSession(runId, CRN, sessionMonth):
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]
      print("getCourseSession")
      if CRN != "":
            CRN = "&courseReferenceNumber=" + str(CRN)
      if (sessionMonth != ""):
            sessionMonth = "&sessionMonth=" + str(sessionMonth)
      resp = getHttpRequest("https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions?uen=" + uen + CRN +sessionMonth)
      return resp

#-------------------- Description --------------------
#curlPostRequest is a formatting method that display the information in the Application in a readable format for POST HTTP Request API 
#Input parameter (runId) : Course Run Id 
#Input parameter (payloadToDisplay) : Request Body information that is going to be send over to the server
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlPostRequest(runId, payloadToDisplay):
      #Remove Whitespacing new line and tabs for accurate content length
      payloadToSend = re.sub(r"[\n\t\s]*", "", payloadToDisplay)
      req = requests.Request('POST',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId,headers={'accept':'application/json'},data=str(payloadToSend)).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n{}\n{}'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            '----------------Payload Information----------------',
            payloadToDisplay,
      )
      return text 
#-------------------- Description --------------------
#curlGetRequestViewCourseRun is a formatting method that display the information in the Application in a readable format for GET HTTP Request API (Course Run By Run Id) 
#Input parameter (runId) : Course Run Id 
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlGetRequestViewCourseRun(runId):
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      )
      return text

#-------------------- Description --------------------
#curlGetCourseSession is a formatting method that display the information in the Application in a readable format for POST HTTP Request API (Course Session) 
#Input parameter (runId) : Course Run Id 
#Input parameter (CRN) : Course References Number (CRN) 
#Input parameter (sessionMonth) : Month and Year to view 
#Output parameter (text) : Formatted Version of the text to be display
#----------------------------------------------------- 
def curlGetCourseSession(runId, CRN, sessionMonth):
      #Set UEN to payload
      config = loadFile(config_path)
      config = json.loads(config)
      uen = config["UEN"]
      if CRN != "":
            CRN = "&courseReferenceNumber=" + str(CRN)
      if (sessionMonth != ""):
            sessionMonth = "&sessionMonth=" + str(sessionMonth)
      req = requests.Request('GET',"https://uat-api.ssg-wsg.sg/courses/runs/" + runId + "/sessions?uen=" + uen + CRN +sessionMonth,headers={'accept':'application/json'}).prepare()
      text =  '{}\n{}\r\n{}\r\n\r\n'.format(
            '----------------Request Information----------------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      )
      return text
      

