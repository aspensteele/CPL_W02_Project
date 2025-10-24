#!/usr/bin/env python3
import json
import sys


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # store tokens to parse
        self.pos = 0          # current position in token list
        self.symbols = set()  # declared identifiers

    """In rubric: get the current token and advance to the next. NOTE: this will REMOVE the token from the list"""
    def nextToken(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    # rubric requires a public getNextToken that returns the next non-comment token
    # our scanner already strips comments, so we forward to nextToken
    def getNextToken(self):
        return self.nextToken()

    """Look at current token. Does not advance or remove from list"""
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    """In rubric: Used to catch errors like using a variable before declaring it or declaring again"""
    def identifierExists(self, name):
        return name in self.symbols

    # helpers
    def _expect_value(self, expected_val, ctx_msg):
        t = self.nextToken()
        if not t or t.get("value") != expected_val:

            print(f"Error: expected {expected_val} in {ctx_msg}, got {t}")
            return None
        return t

    def _expect_type(self, expected_type, ctx_msg):
        t = self.nextToken()
        if not t or t.get("type") != expected_type:
            print(f"Error: expected {expected_type} in {ctx_msg}, got {t}")
            return None
        return t

    """main entry point for parsing"""
    def begin(self):
        print("Parsing started...")
        tree = self._start()  # per rubric: begin calls start
        print("Parse tree:")
        print(json.dumps(tree, indent=2))
        return tree

    # start -> { Statement }
    def _start(self):
        tree = ["PROGRAM"]
        while self.pos < len(self.tokens):
            # stop if dangling or scanner appended sentinels we do not handle
            node = self._statement()

            if node:
                tree.append(node)
            else:
                
                # advance one token to avoid infinite loop on hard error
                if self.peek():
                    self.pos += 1
                else:
                    break
        return tree

    """acts as a dispatcher- figures out what kind of statement it is and calls the appropriate method"""
    def _statement(self):
        token = self.peek()
        if not token:
            return None

        # Statement = Declaration | Assignment | IfStatement | WhileStatement
        if token['type'] == 'KEYWORD' and token['value'] == 'int':
            return self._declaration()
        if token['type'] == 'KEYWORD' and token['value'] == 'if':
            return self._if_stmt()
        if token['type'] == 'KEYWORD' and token['value'] == 'while':
            return self._while_stmt()
        if token['type'] == 'IDENTIFIER':
            return self._assignment()

        print(f"Unexpected token at statement start: {token}")
        return None

    """parses a variable declar statement. e.g. int x; or int x = 5;  grammar allows exactly one identifier"""
    def _declaration(self):
        type_token = self.nextToken()  # 'int'
        var_type = type_token['value']

        ident_token = self.nextToken()
        if not ident_token or ident_token['type'] != 'IDENTIFIER':
            print("Error: expected identifier after 'int'")
            return None

        var_name = ident_token['value']
        if self.identifierExists(var_name):
            print(f"Error: identifier '{var_name}' already declared")
            return None

        # optional initializer: '=' Expression
        initializer = None
        if self.peek() and self.peek()['type'] == 'OPERATOR' and self.peek()['value'] == '=':
            self.nextToken()  # consume '='
            initializer = self._expression()
            if not initializer:
                return None

        semi = self.nextToken()
        if not semi or semi['value'] != ';':
            print(f"Error: expected ';' after declaration, got {semi}")
            return None

        self.symbols.add(var_name)
        if initializer is None:
            return ["DECLARATION", var_type, var_name]
        else:
            return ["DECLARATION_INIT", var_type, var_name, initializer]

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
        """Parse expressions with binary operators meaning it requires 2 operands (+, -, *, /)"""
        left = self._term()
        if not left:
            return None

        while self.peek() and self.peek()['type'] == 'OPERATOR':
            op_token = self.peek()
            if op_token['value'] in ['+', '-']:
                self.nextToken()
                right = self._term()
                if not right:
                    print("Error: expected expression after operator")
                    return None
                left = ["BINOP", op_token['value'], left, right]
            else:
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

    # relational condition used by if and while
    # Condition = Expression RelOp Expression ;  RelOp in < > ==
    def _rel(self):
        left = self._expression()
        if not left:
            return None

        op = self.peek()
        if not op or op['type'] != 'OPERATOR' or op['value'] not in ['==', '<', '>']:
            print(f"Error: expected relational operator (==, <, >), got {op}")
            return None
        self.nextToken()

        right = self._expression()
        if not right:
            return None

        return ["RELOP", op['value'], left, right]

    """Parse if statement: if (condition) { statements } [else { statements }]"""
    def _if_stmt(self):
        if_tok = self.nextToken()
        if not if_tok or if_tok['type'] != 'KEYWORD' or if_tok['value'] != 'if':

            print("Error: expected 'if'")
            return None

        lp = self.nextToken()
        if not lp or lp['value'] != '(':
            print(f"Error: expected '(', got {lp}")
            return None

        cond = self._rel()
        if not cond:
            return None

        rp = self.nextToken()
        if not rp or rp['value'] != ')':
            print(f"Error: expected ')', got {rp}")

            return None

        then_block = self._block()
        if not then_block:
            return None

        else_block = None
        if self.peek() and self.peek()['type'] == 'KEYWORD' and self.peek()['value'] == 'else':
            self.nextToken()
            else_block = self._block()
            if not else_block:
                return None

        return ["IF", cond, then_block, else_block]

    """Parse while statement: while (condition) { statements }"""
    def _while_stmt(self):
        w_tok = self.nextToken()
        if not w_tok or w_tok['type'] != 'KEYWORD' or w_tok['value'] != 'while':
            print("Error: expected 'while'")

            return None

        lp = self.nextToken()
        if not lp or lp['value'] != '(':

            print(f"Error: expected '(', got {lp}")
            return None

        cond = self._rel()
        if not cond:
            return None

        rp = self.nextToken()
        if not rp or rp['value'] != ')':

            print(f"Error: expected ')', got {rp}")
            return None

        body = self._block()
        if not body:
            return None

        return ["WHILE", cond, body]

    """Parse a block of statements (inside braces). Note:  this grammar only permits blocks after if/while."""
    def _block(self):
        lb = self.nextToken()
        if not lb or lb['value'] != '{':
            print(f"Error: expected '{{', got {lb}")
            return None

        items = []
        while self.peek() and not (self.peek()['type'] == 'PUNCTUATION' and self.peek()['value'] == '}'):
            node = self._statement()
            if node:

                items.append(node)
            else:
                # simple recovery advance one token to avoid infinite loop
                if self.peek():
                    self.pos += 1
                else:
                    break

        rb = self.nextToken()
        if not rb or rb['value'] != '}':
            print(f"Error: expected '}}', got {rb}")
            return None

        return ["BLOCK", items]


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

    output_file = json_file.replace('_tokens.json', '_parse_tree.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tree, f, indent=2)
        print(f"\nParse tree saved to {output_file}")
    except Exception as e:
        print(f"Error saving parse tree: {e}")


if __name__ == "__main__":
    main()
