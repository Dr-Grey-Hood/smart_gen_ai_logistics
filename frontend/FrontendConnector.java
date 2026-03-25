package frontend;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class FrontendConnector {

    // Flask server URL
    private static final String SERVER_URL = "http://127.0.0.1:5000/predict";

    public static String sendToServer(String userInput) {
        try {
            // 1. Setup connection
            URL url = new URL(SERVER_URL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // 2. Send JSON body
            String jsonInput = "{\"prompt\": \"" + userInput + "\"}";
            try (OutputStream os = conn.getOutputStream()) {
                os.write(jsonInput.getBytes());
                os.flush();
            }

            // 3. Read response
            Scanner sc = new Scanner(conn.getInputStream());
            StringBuilder response = new StringBuilder();
            while (sc.hasNext()) {
                response.append(sc.nextLine());
            }
            sc.close();

            // 4. Extract only the message
            String result = response.toString();
            result = result.replace("{\"response\":\"", "").replace("\"}", "");

            return result;

        } catch (Exception e) {
            e.printStackTrace();
            return "⚠️ Connection Error: " + e.getMessage();
        }
    }
}
