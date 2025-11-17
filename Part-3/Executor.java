import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.*;
import java.util.*;

public class Executor {
    private JSONArray program;
    private Map<String, Integer> memory;

    public Executor(JSONArray program) {
        this.program = program;
        this.memory = new HashMap<>();
    }

    public void execute() {
        System.out.println("Execution started...");
        System.out.println("Program has " + program.size() + " elements");

        // Just print what we see for now
        for (int i = 0; i < program.size(); i++) {
            System.out.println("Element " + i + ": " + program.get(i));
        }

        System.out.println("\nExecution completed.");
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Usage: java Executor <parse_tree.json>");
            return;
        }

        System.out.println("Reading file: " + args[0]);

        JSONParser parser = new JSONParser();
        FileReader reader = new FileReader(args[0]);
        JSONArray parseTree = (JSONArray) parser.parse(reader);
        reader.close();

        System.out.println("Parse tree loaded successfully!\n");

        Executor executor = new Executor(parseTree);
        executor.execute();
    }
}