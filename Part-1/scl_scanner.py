import json
import sys

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
        # placeholder: right now just split by spaces
        tokens = self.source.split()
        print("Tokens:", tokens)
        return tokens


# main execution code
if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        content = read_source_file(filename)
        if content:  # only if file successfully read
            scanner = Scanner(content)
            scanner.tokenize()
    else:
        print("Usage: python scl_scanner.py <filename>")
