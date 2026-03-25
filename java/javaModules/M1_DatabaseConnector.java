package javaModules;

import java.io.*;
import java.util.*;

public class M1_DatabaseConnector {

    private String filePath;

    // Constructor
    public M1_DatabaseConnector(String filePath) {
        this.filePath = filePath;
        initializeFile();
    }

    // Create the file if it doesn’t exist
    private void initializeFile() {
        File file = new File(filePath);
        if (!file.exists()) {
            try (FileWriter writer = new FileWriter(file)) {
                writer.write("id,input,prediction,actual\n");
                System.out.println("[M1] Data file created: " + filePath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Add a new record (AI input/output pair)
    public void addRecord(String id, String input, String prediction, String actual) {
        try (FileWriter writer = new FileWriter(filePath, true)) {
            writer.write(id + "," + input + "," + prediction + "," + actual + "\n");
            System.out.println("[M1] Record added successfully!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Read all records
    public List<String> getAllRecords() {
        List<String> records = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                records.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return records;
    }
}
