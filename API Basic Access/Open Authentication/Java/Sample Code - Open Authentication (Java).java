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
