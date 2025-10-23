import json
import sys


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens #store tokens to parse
        self.pos = 0        # current position in token list
        self.symbols = set()

    """In rubric: get the current token and advance to the next. NOTE: this will REMOVE the token from the list"""
    def nextToken(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    """Look at current token. Does not advance or remove from list"""
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    """In rubric: Used to catch errors like using a variable before declaring it or declaring again"""
    def identifierExists(self, name):
        return name in self.symbols

    """main entry point for parsing"""
    def begin(self):
        print("Parsing started...")
        tree = ["PROGRAM"]
        while self.pos < len(self.tokens):
            stmt_tree = self._statement()
            if stmt_tree:
                tree.append(stmt_tree)
        print("Parse tree:")
        print(json.dumps(tree, indent=2))
        return tree

    """acts as a dispatcher- figures out what kind of statement it is and calls the appropriate method"""
    def _statement(self):
        token = self.peek()
        if not token:
            return None

        if token['type'] == 'KEYWORD' and token['value'] in ['int', 'float', 'char', 'bool', 'string']:
            return self._declaration()
        elif token['type'] == 'IDENTIFIER':
            return self._assignment()
        elif token['value'] == 'if':
            return self._if_stmt()  # Partner will implement this
        elif token['value'] == 'while':
            return self._while_stmt()  # Partner will implement this
        else:
            print(f"Unexpected token: {token}")
            self.pos += 1
            return None

    """parses a variable declar statement. e.g. int x;"""
    def _declaration(self):
        type_token = self.nextToken()
        var_type = type_token['value']

        ident_token = self.nextToken()
        if not ident_token or ident_token['type'] != 'IDENTIFIER':
            print("Error: expected identifier")
            return None

        var_name = ident_token['value']

        if self.identifierExists(var_name):
            print(f"Error: identifier '{var_name}' already declared")
            return None

        self.symbols.add(var_name)

        semi = self.nextToken()
        if not semi or semi['value'] != ';':
            print(f"Error: expected ';', got {semi}")
            return None

        return ["DECLARATION", var_type, var_name]

    """parse an assignment statement e.g. x = 10 + 5;"""
    def _assignment(self):
        var_token = self.nextToken()
        if not self.identifierExists(var_token['value']):
            print(f"Error: variable '{var_token['value']}' not declared")
            return None

        eq = self.nextToken()
        if not eq or eq['value'] != '=':
            print(f"Error: expected '=', got {eq}")
            return None

        expr_tree = self._expression()
        if not expr_tree:
            return None

        semi = self.nextToken()
        if not semi or semi['value'] != ';':
            print(f"Error: expected ';', got {semi}")
            return None

        return ["ASSIGNMENT", var_token['value'], expr_tree]

    """parse an expression with low precedence operators, left to right, e.g. x + 5 - 2 becomes ((x+5) -2)"""
    def _expression(self):
        """Parse expressions with binary operators meaning it requires 2 operands (+, -, *, /, ==, <, >)"""
        left = self._term()
        if not left:
            return None

        while self.peek() and self.peek()['type'] == 'OPERATOR':
            op_token = self.peek()
            if op_token['value'] in ['+', '-', '==', '<', '>']:
                self.nextToken()
                right = self._term()
                if not right:
                    print("Error: expected expression after operator")
                    return None
                left = ["BINOP", op_token['value'], left, right]
            else:
                # Not a low precedence operator
                break

        return left

    def _term(self):
        """Parse multiplication and division (higher precedence)"""
        left = self._factor()
        if not left:
            return None

        while self.peek() and self.peek()['type'] == 'OPERATOR':
            op_token = self.peek()
            if op_token['value'] in ['*', '/']:
                self.nextToken()
                right = self._factor()
                if not right:
                    print("Error: expected expression after operator")
                    return None
                left = ["BINOP", op_token['value'], left, right]
            else:
                break

        return left

    def _factor(self):
        """Parse primary expressions: integers, identifiers, or parenthesized expressions (stuff that cannot be broken down further"""
        token = self.peek()
        if not token:
            return None

        if token['value'] == '(':
            self.nextToken()
            expr = self._expression()
            close_paren = self.nextToken()
            if not close_paren or close_paren['value'] != ')':
                print(f"Error: expected ')', got {close_paren}")
                return None
            return expr

        if token['type'] == 'INTEGER':
            self.nextToken()
            return ["INT", token['value']]

        if token['type'] == 'IDENTIFIER':
            if not self.identifierExists(token['value']):
                print(f"Error: variable '{token['value']}' not declared")
                return None
            self.nextToken()
            return ["IDENTIFIER", token['value']]

        print(f"Error: unexpected token in expression: {token}")
        return None

    # TODO: implement methods below
    def _if_stmt(self):
        """Parse if statement: if (condition) { statements } [else { statements }]"""

    def _while_stmt(self):
        """Parse while statement: while (condition) { statements }"""


    def _block(self):
        """Parse a block of statements (inside braces)"""


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
    tree = parser.begin()


    # save the parse tree as json file (?) rubric says parse tree
    output_file = json_file.replace('_tokens.json', '_parse_tree.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tree, f, indent=2)
        print(f"\nParse tree saved to {output_file}")
    except Exception as e:
        print(f"Error saving parse tree: {e}")


if __name__ == "__main__":
    main()