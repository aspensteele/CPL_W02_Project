import json
import sys

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 # current index in token list

    # Returns the next token, skips comments
    def getNextToken(self):
        pass # will implement later

    # Checks if a variable has already been declared
    def identifierExists(self, identifier):
        pass  # will implement later

    # Entry point; starts parsing by calling _start()
    def begin(self):
        pass  # will implement later

def main():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <tokens.json>")
        return

    json_file = sys.argv[1]

    #Read JSON File
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{json_file}' is not valid JSON.")
        return


    # Create parser object
    parser = Parser(tokens)

    # For now, just print the tokens
    print("Tokens loaded from JSON:")
    for t in parser.tokens:
        print(t)

if __name__ == "__main__":
    main()