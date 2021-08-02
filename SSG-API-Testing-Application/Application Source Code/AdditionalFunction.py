import json
#-------------------- Description --------------------
#loadFile uses is a open() Function to load a file
#Input parameter (payloadFileName) : File name
#Output parameter (payload) : The text information in the file
#-----------------------------------------------------
def loadFile(payloadFileName):
      global payload
      #This is a template to load the file
      courseRunPayload = open(payloadFileName, "r")
      payload = courseRunPayload.read()
      return payload

#-------------------- Description --------------------
#saveJsonFormat is used in configWindow.py to save the information.
#Input parameter (fileName) : File name to be saved
#Input parameter (content) : text information to be saved
#Output parameter (payload) : The text information in the file
#-----------------------------------------------------
def saveJsonFormat(content, fileName):
      with open(fileName, 'w') as f:
            json.dump(content, f, indent=4)
            
#-------------------- Description --------------------
#printResponse is a debugging tool to print the information received from server in the terminal. It is used after calling the API
#Input parameter (response) : Response object from request library
#-----------------------------------------------------
def printResponse(response):
      print("Status Code: ", response.status_code)
      print(response.text)
      
#-------------------- Description --------------------
#pprintJsonFormat is a debugging tool to print the text in the terminal in a readable format.
#Input parameter (plain) : text to be printed in readable format
#-----------------------------------------------------
def pprintJsonFormat(plain):
    json_load = json.loads(plain.decode())  
    text = json.dumps(json_load, indent = 4)
    print(text)