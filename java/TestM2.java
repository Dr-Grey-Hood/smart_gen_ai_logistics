import javaModules.M2_PythonBridge;

public class TestM2 {
    public static void main(String[] args) {
        String userInput = "What is AI?";
        String prediction = M2_PythonBridge.sendToPython(userInput);
        System.out.println("[M2] AI Response: " + prediction);
    }
}
