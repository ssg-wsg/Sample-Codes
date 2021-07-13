------------
INTRODUCTION
------------

This is a sample guide when creating a Certificate (MTLS) Application in Developer Portal (https://developer.ssg-wsg.sg) by providing the Client Certificate and adding an Encryption Key to the Application.

------------


To use API with “Authentication” = “Certificate”
------------------------------------------------
1. After clicking “Create New App” in Developer Portal, choose “Certificate” as Authentication type. This create an app that uses Mutual TLS authentication.

2. Subscribe to APIs required.
                                
3. Generate Self-Signed Certificate:
* Download and install OpenSSL for Windows.
* Run in command prompt:  **_openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes_**
* Enter info required for certificate request in command prompt
* Note the location of the generated key.pem and cert.pem files

4. In Developer Portal, go to Credentials, browse to find and upload the generated Self-Signed Certificate (cert.pem) 

5. Calling API using Postman, Curl or SampleCode.js (In sampleCode folder):
* Need to provide the certificate that was uploaded to the Developer Portal.

    **[Postman]** Refer to https://learning.getpostman.com/docs/postman/sending-api-requests/certificates/ 

      Under File -> Settings -> Certificates, Add Certificate for the Client Certificates

      Host : domain of the Request URL
      CRT file : cert.pem that was generated then uploaded to Dev Portal
      KEY file : key.pem that was generated along with the cert.pem
      Passphrase : Can leave blank if there's no passphrase from generated certificate

    **[Curl]** From generated certificate's location, run the following command: 
    
    `curl --cert cert.pem --key key.pem {RequestURL}`



To use API with “Encryption” = “AES256” (API Request and/or Response Payload Encryption)
------------------------------------------------
1. Subscribe to APIs required

2. Generate Encryption Key
- Download and install OpenSSL for Windows.
- Run in command prompt: openssl rand -base64 32
- Copy Generated Encryption Key in command prompt

3. In Developer Portal, go to Credentials, paste the Generated Encryption Key and save it.

4. To test API that requires Encryption of Request payload, use Encryption Key to encrypt the request payload
- From https://github.com/ssg-wsg/sampleUtil/tree/master/encryptdecrypt, use the encryptdecrypt.html
- Key in the following fields:

         Key in (Base64) : <Generated Encryption Key>
         Original String :  <Payload (Request) to encrypt> -> Trigger Encrypt 
         
- Use Postman, Curl or SampleCode.js (In sampleCode folder) to call the API
- Copy the **Encrypted String** and use in **Body** of API request                                                
                      
5. To test Decryption of Response (if encrypted)
- From https://github.com/ssg-wsg/sampleUtil/tree/master/encryptdecrypt, use the encryptdecrypt.html
- Key in the following fields:

         Key in (Base64) : <Generated Encryption Key>
         Original String :  <Payload (Request) to encrypt> -> Trigger Encrypt 
         
- **Decrypted String** in clear text
