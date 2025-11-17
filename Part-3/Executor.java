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

        // Skip element 0 which is "PROGRAM"
        for (int i = 1; i < program.size(); i++) {
            executeStatement((JSONArray) program.get(i));
        }

        System.out.println("\nExecution completed.");
        System.out.println("\nFinal memory state:");
        for (String var : memory.keySet()) {
            System.out.println("  " + var + " = " + memory.get(var));
        }
    }

    private void executeStatement(JSONArray stmt) {
        String type = (String) stmt.get(0);

        if (type.equals("DECLARATION")) {
            // ["DECLARATION", "int", "varname"] ex. int x
            String varName = (String) stmt.get(2);
            memory.put(varName, 0);
            System.out.println("Declared " + varName + " = 0");
        }
        else if (type.equals("DECLARATION_INIT")) {
            // TODO: Implement ex . int x = 3
            System.out.println("TODO: Execute " + type);
        }
        else if (type.equals("ASSIGNMENT")) {
            // TODO: Implement
            System.out.println("TODO: Execute " + type);
        }
        else if (type.equals("IF")) {
            // TODO: Implement
            System.out.println("TODO: Execute " + type);
        }
        else if (type.equals("WHILE")) {
            // TODO: Implement
            System.out.println("TODO: Execute " + type);
        }
        else {
            System.out.println("Unknown statement type: " + type);
        }
    }

    private void executeBlock(JSONArray block) {
        // TODO: Execute each statement in the block
        // ["BLOCK", [statement1, statement2, ...]]
    }

    private int evaluateExpression(JSONArray expr) {
        // TODO: Evaluate expressions
        // Handle: INT, IDENTIFIER, BINOP
        return 0;
    }

    private boolean evaluateCondition(JSONArray cond) {
        // TODO: Evaluate conditions
        // Handle: RELOP (==, <, >)
        return false;
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