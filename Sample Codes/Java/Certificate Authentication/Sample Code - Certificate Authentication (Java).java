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
