import tempfile

import streamlit as st
import requests

from utils.streamlit_utils import display_config
from core.system.logger import Logger

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

st.set_page_config(page_title="Demo Code", page_icon="🔐")

LOGGER = Logger("Demo Code")

CERT_AUTH_PYTHON = """
import requests

try:
    request_url = input("Enter the Open Authentication endpoint URL: ")
    response = requests.get(request_url, cert=("path/to/cert.pem", "path/to/key.pem"))
    print("Response code: ", response.status_code)
    print("Response body: ", response.json())
except:
    print("Please check to make sure that the endpoint URL or the path to certificates is valid!")
"""

CERT_AUTH_JAVA = """
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.KeyStore;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;

/*
 * This Sample Code utilizes HttpURLConnection, KeyStore, KeyManagerFactory, SSLContext Class to call the subscribed API
 */
public class SSGWSGSampleCodeCertJava {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("################################################################");
        System.out.println("Simple Program in Java to Get API with Certificate");
        System.out.println("################################################################");

        System.out.println("1) Please get ready the GET API URL");

        System.out.print("Enter URL to continue: ");
        String url = sc.nextLine();
        sc.close();

        httpRequestGetMethod(url);

    }

    /*
     * This function sends a "GET" HTTP Request in order to obtain the specified
     * content
     */
    private static void httpRequestGetMethod(String url) {

        try {
            URL getUrl = new URL(url);

            // Initialize Keystore, the default type is "PKCS12"
            KeyStore ks = KeyStore.getInstance("PKCS12");

            // ***** Adjust Path parameter for PKCS12 file accordingly *****
            FileInputStream fis = new FileInputStream("C:/Users/Username/ExampleFolder/SampleCode/example.p12");

            // Load the keystore file
            // ***** The 2nd parameter is the password to unlock the PKCS12 file. Adjust
            // accordingly *****
            ks.load(fis, "password".toCharArray());

            // Initialize KeyManagerFactory , the default type is "SunX509"
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");

            // Initializes the factory
            // ***** The 2nd parameter is the password to unlock the PKCS12 file. Adjust
            // accordingly *****
            kmf.init(ks, "password".toCharArray());

            SSLContext sc = SSLContext.getInstance("TLS");
        //Allocating a null value for 2nd & 3rd Parameter will use the default implementation
            sc.init(kmf.getKeyManagers(), null, null);

            // Initialises a open connection
            HttpURLConnection connection = (HttpURLConnection) getUrl.openConnection();
            if (connection instanceof HttpsURLConnection) {
                ((HttpsURLConnection) connection).setSSLSocketFactory(sc.getSocketFactory());
            }
            connection.setRequestMethod("GET");

            printResponseContent(connection);

        } catch (Exception e) {
            System.out.println("Error Message: " + e);
            System.out.println("Please check if you have subscribed to the API or enter the correct Input Value");

        }
    }

    // Read and display the content return from the server
    private static void printResponseContent(HttpURLConnection connection) throws Exception {
        // Request Header Information (Response)
        System.out.println();
        Map<String, List<String>> hdrs = connection.getHeaderFields();
        Set<String> hdrKeys = hdrs.keySet();

        for (String k : hdrKeys)
            System.out.println("Key: " + k + "  Value: " + hdrs.get(k));
        System.out.println();

        InputStream _is;
        if (connection.getResponseCode() < HttpURLConnection.HTTP_BAD_REQUEST) {
            _is = connection.getInputStream();
        } else {
            /* error from server */
            _is = connection.getErrorStream();
        }
        InputStreamReader inputstreamreader = new InputStreamReader(_is);
        BufferedReader bufferedreader = new BufferedReader(inputstreamreader);
        String string = null;
        while ((string = bufferedreader.readLine()) != null) {
            System.out.println(string);
        }
    }

}
"""

CERT_AUTH_NODE = """
var https = require('https'),                  // Module for https
    fs =    require('fs');                     // Required to read certs and keys

    var options = {
       hostname: 'api.ssg-wsg.sg',			// Production Base URL
       path: '/skillsFramework/sectors',		// This API is to retrieve all Sectors
       method: 'GET',					// Method : Get or POST
       key: fs.readFileSync('C://exampleDirectory/MTLS-Sample/key.pem'),		//Input the directory for key.pem
       cert: fs.readFileSync('C://exampleDirectory/MTLS-Sample/cert.pem') 		//Input the directory for cert.pem
       //passphrase: 'InputPassWord' 						                    //Input the passphrase, please
                                                                                //remember to put ',' End of Line for
                                                                                //cert
    };

    makeAPICall = function(response) {
       var str = '';
       response.on('data', function (chunk) {
          str += chunk;
       });

       response.on('end', function () {
          console.log(str);
       });
    }

https.request(options, makeAPICall).end();
"""

OPEN_AUTH_PYTHON = """
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

try:
    request_url = input("Enter URL to continue: ")
    client_id = input("Enter Client Id: ")
    client_secret = input("Input Secret Key: ")

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url='https://public-api.ssg-wsg.sg/dp-oauth/oauth/token',
        client_id=client_id,
        client_secret=client_secret
    )

    response = oauth.get(request_url)
    print("Status Code= ", response.status_code)
    print(response.json())
except:
    print("An error has occurred. Please check data input")
"""

OPEN_AUTH_JAVA = """
import java.util.Scanner;
import java.util.Set;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Base64;
import java.net.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/*
 * This Sample Code utilizes HttpURLConnection Class to retrieve the token and API query
 */
public class SSGWSGSampleCodeJava {

    private static String tokenType;
    private static String tokenValue;

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("################################################################");
        System.out.println("Simple Program in Java to call OAuth 2 Token for Get API");
        System.out.println("################################################################");

        System.out.println("1) Please get ready the GET API URL");
        System.out.println("2) Please get ready the Client ID from developer portal");
        System.out.println("3) Please get ready the Secret from developer portal\n");
        System.out.println("Client Id and Secret can be obtain under App Setting - \"Client Id and Secret\"");

        System.out.print("Enter URL to continue: ");
        String query = sc.nextLine();

        System.out.print("\nEnter Client Id: ");
        String client = sc.nextLine();

        System.out.print("\nEnter Secret Key: ");
        String password = sc.nextLine();
        System.out.println();

        getToken(client, password);
        httpRequestGetMethod(query);
        sc.close();

    }

    /*
     * This function sends a "POST" HTTP Request in order to obtain a token
     */

    private static void getToken(String clientId, String secret) {

        String auth = clientId + ":" + secret;

        // getBytes() method uses platform's default charset if the parameter is empty
        byte[] encodedBytes = Base64.getEncoder().encode(auth.getBytes(StandardCharsets.UTF_8));

        String tokenData = "grant_type=client_credentials";
        byte[] postData = tokenData.getBytes(StandardCharsets.UTF_8);

        try {

            URL url = new URL("https://public-api.ssg-wsg.sg/dp-oauth/oauth/token");

            // Initialises a open connection
            HttpURLConnection con = (HttpURLConnection) url.openConnection();

            // setDoOutput() method is required to be 'true' (default 'false') in order to
            // send a request body (mainly for 'POST' and 'PUT' Request)
            con.setDoOutput(true);

            // Setting of HTTP header parameter as required
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            con.setRequestProperty("Authorization", "Basic " + new String(encodedBytes));

            // getOutputStream() and write() method is used to write the request body
            // DataOutputStream is not required. It is serve to let an application to write
            // primitive Java data types to an output stream in a portable way
            // Alternative would be "con.getOutputStream().write(postData)"
            try (DataOutputStream wr = new DataOutputStream(con.getOutputStream())) {
                wr.write(postData);
            }

            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer content = new StringBuffer();
            while ((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();

            // This method breaks the String into an Array in order to retrieve and store
            // the token value and token type
            String strArray[] = content.toString().split(",");
            for (String s : strArray) {
                List<String> placeholder = Arrays.asList(s.split("\""));
                for (String placeholderS : placeholder) {
                    if (placeholderS.contains("access_token")) {
                        int i = placeholder.indexOf(placeholderS);
                        tokenValue = placeholder.get(i + 2);
                    } else if (placeholderS.contains("token_type")) {
                        int k = placeholder.indexOf(placeholderS);
                        tokenType = placeholder.get(k + 2);
                    }
                }
            }

        } catch (Exception ex) {
            System.out.println("Error Message: " + ex);
        }
    }

    /*
     * This function sends a "GET" HTTP Request in order to obtain the specified
     * content
     */
    private static void httpRequestGetMethod(String url) {
        try {
            URL getUrl = new URL(url);
            // Initialises a open connection
            HttpURLConnection con = (HttpURLConnection) getUrl.openConnection();

            // Setting of HTTP header parameter as required
            con.setRequestMethod("GET");
            con.setRequestProperty("Authorization", tokenType + " " + tokenValue);

            printResponseContent(con);

        } catch (Exception ex) {
            System.out.println("Error Message: " + ex);
            System.out.println("Please check if you have subscribed to the API or enter the correct Input Value");
        }

    }

    // Read and display the content return from the server
    private static void printResponseContent(HttpURLConnection connection) throws Exception {
        // Display Request Header Information (Response)
        System.out.println();
        Map<String, List<String>> hdrs = connection.getHeaderFields();
        Set<String> hdrKeys = hdrs.keySet();

        for (String k : hdrKeys)
            System.out.println("Key: " + k + "  Value: " + hdrs.get(k));
        System.out.println();
        InputStream _is;
        if (connection.getResponseCode() < HttpURLConnection.HTTP_BAD_REQUEST) {
            _is = connection.getInputStream();
        } else {
            /* error from server */
            _is = connection.getErrorStream();
        }
        InputStreamReader inputstreamreader = new InputStreamReader(_is);
        BufferedReader bufferedreader = new BufferedReader(inputstreamreader);
        String string = null;
        while ((string = bufferedreader.readLine()) != null) {
            System.out.println(string);
        }
    }

}
"""

OPEN_AUTH_NODE = """
console.log('################################################################');
console.log('Simple Program in JavaScript to call OAuth 2 Token for Get API');
console.log('################################################################');

console.log('1) Please get ready the GET API URL');
console.log('2) Please get ready the Client ID from developer portal');
console.log('3) Please get ready the Secret from developer portal');
console.log('4) Save File into csv format');
console.log('  ');

// Include prompt module.
var prompt = require('prompt');

// This json object is used to configure what data will be retrieved from command line.
var prompt_attributes = [
    {
        name: 'api_name',
    },
    {
        name: 'clientID',
    },
    {
        name: 'secret',
    },
    {
        name: 'file_name',
    }
];

// Start the prompt to read user input.
prompt.start();

// Prompt and get user input then display those data in console.
prompt.get(prompt_attributes, function (err, result) {
if (err) {
    console.log(err);
    return 1;
} else {
    // Get user input from result object.
    var api_name = result.api_name;
    var file_name = result.file_name;

    //Buffer() requires a number, array or string as the first parameter, and an optional encoding type as the second
    // parameter.
    // Default is utf8, possible encoding types are ascii, utf8, ucs2, base64, binary, and hex
    var login = Buffer.from(result.clientID + ":" + result.secret);
    // If we don't use toString(), JavaScript assumes we want to convert the object to utf8.
    // We can make it convert to other formats by passing the encoding type to toString().
    var loginDetails = login.toString('base64');

    var data = "grant_type=client_credentials";

    // The require() method is used to load and cache JavaScript modules.
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
    var reqtoken = new XMLHttpRequest();
    var urltoken = "https://public-api.ssg-wsg.sg/dp-oauth/oauth/token"


    // .withCredentials indicates whether or not cross - site Access - Control requests should be made using credentials
    reqtoken.withCredentials = true;

    // Initializes a newly-created request.
    reqtoken.open("POST", urltoken);

    // Send the proper header information along with the request
    // setRequestHeader() sets the value of an HTTP request header.

    // "application/x-www-form-urlencoded" represents an URL encoded form. This is the default value if enctype
    // attribute is not set to anything.
    reqtoken.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    // The "Basic" authentication scheme is used, the credentials are constructed like - The resulting string is
    //(base64 encoded).
    reqtoken.setRequestHeader("Authorization", "Basic " + loginDetails);

    reqtoken.send(data);

    reqtoken.onload = function () {
        //--------- GET Json File from Url ---------

        var response = reqtoken.responseText;
        var jsondata = JSON.parse(response);
        token = jsondata["access_token"];
        // The console. log() is a function in JavaScript which is used to print any kind of variables
        console.log(token)
        var reqget = new XMLHttpRequest();
        var urlgetjson = api_name;
        reqget.open("GET", urlgetjson, true)
        reqget.setRequestHeader("Authorization", "Bearer " + token);
        reqget.send();
        reqget.onload = function () {
        console.log(reqget.responseText);
            //--------- JSON converts to CSV ---------
            var response1 = reqget.responseText;
            var csvjson = require('csvjson');
            var csvdata = csvjson.toCSV(response1, {
                headers: 'key'
            });
            var fs = require('fs');

            // The fs.writeFile() method create new file, containing the specified content.
            fs.writeFile(file_name, csvdata, function (err) {
                if (err) {
                    console.log(err);
                }
                console.log('Success!');
            });
        }
    }
}
});
"""

st.image("assets/sf.png", width=200)
st.title("Demo Code")

with st.sidebar:
    st.header("View Configs")
    if st.button("Configs", key="config_display"):
        display_config()

open_auth, cert_auth = st.tabs(["Open Authentication", "Certificate Authentication"])

with cert_auth:
    st.subheader("Certificate Authentication")
    st.markdown("Certificate Authentication employs a BYOK (bring-your-own-keys) approach to ensuring that your "
                "API Requests are secure, by requiring you to use your own symmetric keys (certificate and "
                "private key) for authentication!")

    st.subheader("Sample Code")
    py, java, js = st.tabs(["Python", "Java", "Node.js"])

    with py:
        st.markdown("### Python")
        st.code(
            body=CERT_AUTH_PYTHON
        )

    with java:
        st.markdown("### Java")
        st.code(
            language="java",
            body=CERT_AUTH_JAVA
        )

    with js:
        st.markdown("### Node.js")
        st.code(
            language="javascript",
            body=CERT_AUTH_NODE
        )

    st.divider()
    st.subheader("Try this API out!")
    test_url = st.text_input("Enter the Certificate Authentication endpoint URL: ")
    cert_key = st.file_uploader("Certificate Key", accept_multiple_files=False, type=["pem"], key="cert")
    secret_key = st.file_uploader("Secret Key", accept_multiple_files=False, type=["pem"], key="key")

    if st.button("Request!", key="cert_button"):
        LOGGER.info("Certificate Authentication requested...")
        if all([test_url, cert_key, secret_key]):
            try:
                with tempfile.NamedTemporaryFile() as certfile, tempfile.NamedTemporaryFile() as keyfile:
                    certfile.write(cert_auth)
                    LOGGER.info("Loaded Certificate...")

                    keyfile.write(secret_key)
                    LOGGER.info("Loaded Private Key...")

                    LOGGER.info(f"Sending GET request to {test_url}...")
                    req = requests.get(test_url, cert=(certfile.name, keyfile.name))
                    st.success(f"Response code: {req.status_code}")

                    LOGGER.info(f"Response received: {req.text}")
                    st.json(req.json())
            except Exception as ex:
                LOGGER.error(f"Unable to send request, error: {ex}")
                st.error("Please check to make sure that the endpoint URL or the path to certificates is valid!",
                         icon="🚨")
        else:
            LOGGER.error("Missing certificate or private key file!")
            st.error("Please check to ensure that you fill in all fields before submitting the API request!",
                     icon="🚨")

with open_auth:
    st.subheader("Open Authentication")
    st.markdown("Open Authentication uses OAuth 2.0 to authenticate your client to SSG APIs, "
                "without the need to create your own symmetric keys (certificate and keys) as with "
                "Certificate Authentication!")

    st.subheader("Sample Code")
    py, java, js = st.tabs(["Python", "Java", "Node.js"])

    with py:
        st.markdown("### Python")
        st.code(
            language="python",
            body=OPEN_AUTH_PYTHON
        )

    with java:
        st.markdown("### Java")
        st.code(
            language="java",
            body=OPEN_AUTH_JAVA
        )

    with js:
        st.markdown("### Node.js")
        st.code(
            language="javascript",
            body=OPEN_AUTH_NODE
        )

    st.divider()
    st.subheader("Try this API out!")
    request_url = st.text_input("Enter the URL to continue: ")
    client_id = st.text_input("Enter Client Id: ")
    client_secret = st.text_input("Input Secret Key: ")

    if st.button("Request!", key="open_button"):
        LOGGER.info("Open Authentication requested...")
        if all([request_url, client_id, client_secret]):
            try:
                LOGGER.info("Creating backend application...")
                client = BackendApplicationClient(client_id=client_id)

                LOGGER.info("Creating OAuth2.0 Session...")
                oauth = OAuth2Session(client=client)

                LOGGER.info("Fetching token...")
                token = oauth.fetch_token(
                    token_url='https://public-api.ssg-wsg.sg/dp-oauth/oauth/token',
                    client_id=client_id,
                    client_secret=client_secret
                )

                LOGGER.info("Sending GET request with OAuth token...")
                response = oauth.get(request_url)
                st.success(f"Response code: {response.status_code}")

                LOGGER.info(f"Response received: {response.text}")
                st.code(response.json())
            except:
                LOGGER.error(f"Unable to send request, error: {ex}")
                st.error("An error has occurred. Please check data input!", icon="🚨")
        else:
            LOGGER.error("Missing certificate or private key file!")
            st.error("Please check to ensure that you fill in all fields before submitting the API request!", icon="🚨")
