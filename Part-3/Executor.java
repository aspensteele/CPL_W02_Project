import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.*;
import java.util.*;

public class Executor {
    private JSONArray program;
    private Map<String, Integer> memory;  // Symbol table: variable names → values

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
        String type = (String) stmt.get(0);  // Position 0: statement type

        if (type.equals("DECLARATION")) {
            // ["DECLARATION", "int", "varname"] ex. int x;
            String varName = (String) stmt.get(2);  // Position 2: variable name
            memory.put(varName, 0);
            System.out.println("Declared " + varName + " = 0");
        }
        else if (type.equals("DECLARATION_INIT")) {
            // ["DECLARATION_INIT", "int", "varname", expression] ex. int x = 5;
            String varName = (String) stmt.get(2);  // Position 2: variable name
            int value = evaluateExpression((JSONArray) stmt.get(3));  // Position 3: expression
            memory.put(varName, value);
            System.out.println("Declared " + varName + " = " + value);
        }
        else if (type.equals("ASSIGNMENT")) {
            // ["ASSIGNMENT", "varname", expression] ex. x = 10;
            String varName = (String) stmt.get(1);
            int value = evaluateExpression((JSONArray) stmt.get(2));
            memory.put(varName,value);
            System.out.println("Assigned: " + varName + " = " + value);
        }
        else if (type.equals("IF")) {
            // ["IF", condition, then_block, else_block]
            // TODO: Implement
            System.out.println("TODO: Execute " + type);
        }
        else if (type.equals("WHILE")) {
            // ["WHILE", condition, body_block]
            // TODO: Implement
            System.out.println("TODO: Execute " + type);
        }
        else {
            System.out.println("Unknown statement type: " + type);
        }
    }

    private void executeBlock(JSONArray block) {
        // ["BLOCK", [statement1, statement2, ...]]
        // TODO: Execute each statement in the block
    }

    private int evaluateExpression(JSONArray expr) {
        String type = (String) expr.get(0);  // Position 0: expression type

        if (type.equals("INT")){
            // ["INT", "value"] - Position 1: string number → parse to int
            return Integer.parseInt((String) expr.get(1));
        }
        else if (type.equals("IDENTIFIER")){
            // ["IDENTIFIER", "varname"] - Position 1: variable name → lookup in memory
            String varName = (String) expr.get(1);
            return memory.get(varName);
        }
        else if (type.equals("BINOP")){
            // ["BINOP", "operator", left_expr, right_expr]
            String op = (String) expr.get(1);  // Position 1: operator
            int left = evaluateExpression((JSONArray) expr.get(2));  // Position 2: left (recursive)
            int right = evaluateExpression((JSONArray) expr.get(3));  // Position 3: right (recursive)

            if (op.equals("+")) return left + right;
            if (op.equals("-")) return left - right;
            if (op.equals("*")) return left * right;
            if (op.equals("/")) return left / right;
        }
        return 0;
    }

    private boolean evaluateCondition(JSONArray cond) {
        // ["RELOP", "operator", left_expr, right_expr]
        String op = (String) cond.get(1);
        int left = evaluateExpression((JSONArray) cond.get(2));
        int right = evaluateExpression((JSONArray) cond.get(3));

        if (op.equals("==")) return left == right;
        if (op.equals("!=")) return left != right;
        if (op.equals(">")) return left > right;
        if (op.equals(">=")) return left >= right;
        if (op.equals("<")) return left < right;
        if (op.equals("<=")) return left <= right;

        else {
            return false;
        }
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