import sys
from lexer import tokenize
from parser import Parser
from interp import Interpreter

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r') as f:
            code = f.read()
    else:
        print("=== SyntaxForge Language Playground ===")
        print("Enter code below. End input with a blank line.\n")
        code = ''
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            code += line + '\n'

    try:
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interp = Interpreter()
        interp.run(ast)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()