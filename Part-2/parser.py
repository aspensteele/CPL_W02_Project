import json
import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # current index
        self.symbols = set()  # to track declared identifiers

    # Return the current token
    def getNextToken(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # Advance to the next token
    def scan(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    # Check if an identifier has already been declared
    def identifierExists(self, name):
        return name in self.symbols

    # Entry point
    def begin(self):
        print("Parsing started...")
        declarations = []
        while self.pos < len(self.tokens):
            decl_tree = self.parseDeclaration()
            if decl_tree:
                declarations.append(decl_tree)
        print("Parse tree:")
        for d in declarations:
            print(d)

    # Parse a single declaration: e.g., int x
    def parseDeclaration(self):
        token = self.getNextToken()
        if token and token['type'] == 'KEYWORD':  # e.g., "int"
            var_type = token['value']
            self.scan()

            token = self.getNextToken()
            if token and token['type'] == 'IDENTIFIER':
                var_name = token['value']

                # Check if already declared
                if self.identifierExists(var_name):
                    print(f"Error: identifier '{var_name}' already declared")
                    self.scan()
                    return None

                # Add to symbol table
                self.symbols.add(var_name)
                self.scan()
                return ["DECLARATION", var_type, var_name]

            else:
                print("Error: expected identifier")
                self.scan()  # <--- advance to avoid infinite loop
                return None
        else:
            print("Error: expected type (e.g., int)")
            self.scan()  # <--- advance to avoid infinite loop
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
