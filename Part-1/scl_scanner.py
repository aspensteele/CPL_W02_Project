#!/usr/bin/env python3
import json
import sys
import re


def read_source_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print("File contents:\n", content)
            return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


class Scanner:
    def __init__(self, source_text):
        self.source = source_text
        print("Scanner created! Source length:", len(self.source))

    def tokenize(self):
        # Step 1: only grab integers for now
        pattern = r'\d+' #\d means digit 0-9 and + means one or more digits in a row
        matches = re.findall(pattern, self.source)

        tokens = []
        for m in matches:
            tokens.append({"type": "INTEGER", "value": m})

        print("Tokens:", tokens)
        return tokens


# main execution code
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        content = read_source_file(filename)
        if content:  # only if file successfully read
            scanner = Scanner(content)
            tokens = scanner.tokenize()

            # Create JSON filename from input
            json_filename = filename.rsplit(".", 1)[0] + "_tokens.json"

            with open(json_filename, "w") as f:
                json.dump(tokens, f, indent=2)

            print(f"\nTokens saved to {json_filename}")
    else:
        print("Usage: python scl_scanner.py <filename>")
