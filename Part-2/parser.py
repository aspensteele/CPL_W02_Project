import json
import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbols = set()  # track declared identifiers

    # Return the current token and advance
    def nextToken(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    # Check if an identifier has already been declared
    def identifierExists(self, name):
        return name in self.symbols

    # Entry point
    def begin(self):
        print("Parsing started...")
        tree = ["PROGRAM"]
        while self.pos < len(self.tokens):
            decl_tree = self.parseDeclaration()
            if decl_tree:
                tree.append(decl_tree)
        print("Parse tree:")
        print(tree)

    # Parse a single declaration: e.g., int x
    def parseDeclaration(self):
        token = self.nextToken()
        if token and token['type'] == 'KEYWORD':  # e.g., "int"
            var_type = token['value']

            token = self.nextToken()
            if token and token['type'] == 'IDENTIFIER':
                var_name = token['value']

                if self.identifierExists(var_name):
                    print(f"Error: identifier '{var_name}' already declared")
                    return None

                self.symbols.add(var_name)
                return ["DECLARATION", var_type, var_name]

            else:
                print("Error: expected identifier")
                return None
        else:
            print("Error: expected type (e.g., int)")
            return None


# -------------------------
# Main function
# -------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <tokens.json>")
        return

    json_file = sys.argv[1]

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{json_file}' is not valid JSON.")
        return

    parser = Parser(tokens)
    parser.begin()

if __name__ == "__main__":
    main()
