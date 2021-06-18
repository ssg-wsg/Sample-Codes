var https = require('https'),                  // Module for https
    fs =    require('fs');                     // Required to read certs and keys

    var options = {
       hostname: 'api.ssg-wsg.sg',			// Production Base URL
       path: '/skillsFramework/sectors',		// This API is to retrieve all Sectors
       method: 'GET',					// Method : Get or POST
       key: fs.readFileSync('C://exampleDirectory/MTLS-Sample/key.pem'),		//Input the directory for key.pem
       cert: fs.readFileSync('C://exampleDirectory/MTLS-Sample/cert.pem') 		//Input the directory for cert.pem
       //passphrase: 'InputPassWord' 						//Input the passphrase, please remember to put ',' End of Line for cert 		
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