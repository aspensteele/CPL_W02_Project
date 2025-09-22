import json
import sys

def read_source_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occured: {e}")

class Scanner:
    def __init__(self):
            print("Scanner created!")

        #main execution code
if __name__ == "__main__":
          if len(sys.argv) > 1:
              filename = sys.argv[1] # get the first command line arg
              read_source_file(filename)
          else:
              print("Usage: python scl_scanner.py <filename>")

