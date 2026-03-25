import javaModules.M1_DatabaseConnector;

public class TestM1 {
    public static void main(String[] args) {
        M1_DatabaseConnector db = new M1_DatabaseConnector("brain_data.csv");

        db.addRecord("1", "What is AI?", "AI is Artificial Intelligence", "AI means Artificial Intelligence");

        System.out.println("All records:");
        for (String line : db.getAllRecords()) {
            System.out.println(line);
        }
    }
}
