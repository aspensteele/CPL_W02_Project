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

    # Look at the current token without consuming it (removing it)
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # Check if an identifier has already been declared
    def identifierExists(self, name):
        return name in self.symbols

    # Entry point
    def begin(self):
        print("Parsing started...")
        tree = ["PROGRAM"]
        while self.pos < len(self.tokens):
            stmt_tree = self._statement()  # call _statement
            if stmt_tree:
                tree.append(stmt_tree)
        print("Parse tree:")
        print(tree)

    def _statement(self):
        token = self.peek()
        if not token:
            return None
        if token['type'] == 'KEYWORD' and token['value'] in ['int', 'float', 'char', 'bool', 'string']:
            return self._declaration()
        elif token['type'] == 'IDENTIFIER':
            return self._assignment()
        elif token['value'] == 'if':
            return self._if_stmt()
        elif token['value'] == 'while':
            return self._while_stmt()
        else:
            print(f"Unexpected token: {token}")
            self.pos += 1
            return None

    # Parse a single declaration: type already confirmed
    def _declaration(self):
        type_token = self.nextToken()  # already a type keyword
        var_type = type_token['value']

        ident_token = self.nextToken()
        if ident_token and ident_token['type'] == 'IDENTIFIER':
            var_name = ident_token['value']

            if self.identifierExists(var_name):
                print(f"Error: identifier '{var_name}' already declared")
                return None

            self.symbols.add(var_name)
            return ["DECLARATION", var_type, var_name]
        else:
            print("Error: expected identifier")
            return None

    def _assignment(self):
        var_token = self.nextToken()  # consume identifier
        if not self.identifierExists(var_token['value']):
            print(f"Error: variable {var_token['value']} not declared")
            return None

        eq_token = self.nextToken()
        if not eq_token or eq_token['value'] != '=':
            print("Error: expected '='")
            return None

        expr_tree = self._expression()  # parse the right-hand side
        return ["ASSIGNMENT", var_token['value'], expr_tree]

    def _expression(self):
        # minimal version: just consume a number or identifier
        token = self.nextToken()
        if token['type'] == 'INTEGER':
            return ["INT", token['value']]
        elif token['type'] == 'IDENTIFIER':
            return ["IDENTIFIER", token['value']]
        else:
            print(f"Error: unexpected token in expression: {token}")
            return None

    # Placeholder for if statement
    def _if_stmt(self):
        token = self.nextToken()  # consume 'if'
        # In full parser, parse condition and block here
        return ["IF_STMT"]

    # Placeholder for while statement
    def _while_stmt(self):
        token = self.nextToken()  # consume 'while'
        # In full parser, parse condition and block here
        return ["WHILE_STMT"]



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
