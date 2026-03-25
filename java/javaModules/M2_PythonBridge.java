package javaModules;

import java.io.*;
import java.net.*;
import org.json.JSONObject;

public class M2_PythonBridge {

    private static final String PYTHON_URL = "http://127.0.0.1:5000/predict";

    public static String sendToPython(String inputText) {
        try {
            // Create a JSON object with the input text
            JSONObject jsonInput = new JSONObject();
            jsonInput.put("input", inputText);

            // Open a connection to Flask
            URL url = new URL(PYTHON_URL);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // Send JSON data
            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInput.toString().getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            // Read response
            BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), "utf-8")
            );
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }

            // Convert response to JSON and extract prediction
            JSONObject jsonResponse = new JSONObject(response.toString());
            return jsonResponse.getString("prediction");

        } catch (Exception e) {
            e.printStackTrace();
            return "Error connecting to Python server.";
        }
    }
}
