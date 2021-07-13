# Node.JS Sample Code SSG-WSG
## Introduction
This Sample Code serves as a guide on calling a subscribed API through Certificate Authentication
### The design of the Sample Code
The Sample Code uses a one step process in order to successfully call a subscribed API
1. Call a subscribed API based on the PKCS12 File 
## Prerequisites
The following five prerequisites are required to run the sample code successfully
1. [A SSG-WSG Developer Account](https://developer.ssg-wsg.sg/webapp/guides/13EgI9eYfms1W7Ls4X1hdI)
2. [Ensure the Account is subscribed to an API with Certificate Authentication](https://developer.ssg-wsg.sg/webapp/guides/6gvz7gEnwU2dSIKPrTcXnq)
3. [NodeJS installer](https://nodejs.org/en/download/)
4. [Certificate](https://developer.ssg-wsg.sg/webapp/guides/20TYgEkfmOQWMzngzSQ4Pe)
5. A PKCS12(.p12 Extension) file of the Certificate + Private Key

You can generate a PKCS12 file with the following command
```
openssl pkcs12 -export -inkey "key file" -in "certificate file" -out "Name.p12" -passout pass:"Export password"

//An example of the command:
openssl pkcs12 -export -inkey key.pem -in certificate.pem -out keyStore.p12 -passout pass:password
```
*The Key.pem and Certificate.pem can be obtained from Point 4*

## How to use
1. Download the sample code
2. Modify the path of the file and API endpoint
3. Open CMD and run the following commands
```
//To run the program
node SampleCode.js
```