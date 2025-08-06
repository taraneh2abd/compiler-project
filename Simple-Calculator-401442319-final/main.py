import argparse
from antlr4 import *
from antlr4.InputStream import InputStream
from gen.ArithmeticExpressionLexer import ArithmeticExpressionLexer
from gen.ArithmeticExpressionParser import ArithmeticExpressionParser
from CalculatorListener import CalculatorListener

def evaluate_expression(expression):
    input_stream = InputStream(expression)
    lexer = ArithmeticExpressionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ArithmeticExpressionParser(stream)
    parse_tree = parser.start()

    listener = CalculatorListener(parser.ruleNames)
    walker = ParseTreeWalker()
    walker.walk(listener, parse_tree)

    return listener.get_result()


def main():
    parser = argparse.ArgumentParser(description='my calculator')
    parser.add_argument('-f', '--file', help='Input file with expressions', default=None)
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            result = evaluate_expression(line)
                            print(f"{line} = {result}")
                        except Exception as e:
                            print(f"Error processing '{line}': {str(e)}")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
    else:
        print("you could give the input as args like: python main.py -f input.txt")
        print("write inputs: (type 'exit' to quit)")
        while True:
            try:
                expr = input("> ").strip()
                if expr.lower() in ['exit', 'quit']:
                    break
                if not expr:
                    continue

                result = evaluate_expression(expr)
                print(f"Result: {result}")

            except Exception as e:
                print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()

