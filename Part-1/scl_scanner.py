#!/usr/bin/env python3
import json
import sys
import re

def read_source_file(filename):
    """
    Read the entire source file as text and return it.
    Prints basic errors and returns None on failure.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            print("File contents:\n", content)
            return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except PermissionError:
        print(f"Error: Permission denied reading '{filename}'.")
    except UnicodeDecodeError:
        print(f"Error: Could not decode '{filename}' as UTF-8.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


class Scanner:
    KEYWORDS = {"if", "else", "while", "int"}
    OPERATORS = {"+", "-", "*", "/", "=", "<", ">", "=="}
    PUNCTUATION = {";", "(", ")", "{", "}", ","}

    def __init__(self, source_text):
        self.source = source_text
        print("Scanner created! Source length:", len(self.source))

    def _strip_line_comments(self, text):
        """
        remove // comments (from '//' to end of line).
        keeps everything else unchanged.
        """
        return re.sub(r'//[^\n]*', '', text)

    def tokenize(self):
        """
        convert the (comment-stripped) source string into a flat list of tokens.
        Uses a single regex with findall; no position tracking.
        """
        # Remove // comments first
        cleaned = self._strip_line_comments(self.source)

        # Combined pattern for ==, single-char ops, integers, identifiers/keywords, punctuation
        pattern = r'==|[+\-*/=<>]|\d+|\b[a-zA-Z_]\w*\b|[;(){},]'
        matches = re.findall(pattern, cleaned)

        tokens = []
        for m in matches:
            if m.isdigit():
                tokens.append({"type": "INTEGER", "value": m})
            elif m in self.KEYWORDS:
                tokens.append({"type": "KEYWORD", "value": m})
            elif m in self.OPERATORS:
                tokens.append({"type": "OPERATOR", "value": m})
            elif m in self.PUNCTUATION:
                tokens.append({"type": "PUNCTUATION", "value": m})
            else:
                tokens.append({"type": "IDENTIFIER", "value": m})

        return tokens


def pretty_print(tokens):
    print("\nTokens:")
    print(f"{'TYPE':<12} VALUE")
    print("-" * 28)
    for t in tokens:
        print(f"{t['type']:<12} {t['value']}")
    print("-" * 28)


# main execution code
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        content = read_source_file(filename)
        if content:  # only if file successfully read
            scanner = Scanner(content)
            tokens = scanner.tokenize()
            pretty_print(tokens)

            # Create JSON filename from input
            json_filename = filename.rsplit(".", 1)[0] + "_tokens.json"

            try:
                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(tokens, f, indent=2)
                print(f"\nTokens saved to {json_filename}")
            except PermissionError:
                print(f"Error: Permission denied writing '{json_filename}'.")
            except Exception as e:
                print(f"Error writing '{json_filename}': {e}")
    else:
        print("Usage: python scl_scanner.py <filename>")
