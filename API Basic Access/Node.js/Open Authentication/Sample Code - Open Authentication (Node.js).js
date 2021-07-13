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

        //Buffer() requires a number, array or string as the first parameter, and an optional encoding type as the second parameter. 
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

        // "application/x-www-form-urlencoded" represents an URL encoded form. This is the default value if enctype attribute is not set to anything.
        reqtoken.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        // The "Basic" authentication scheme is used, the credentials are constructed like - The resulting string is (base64 encoded).
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
