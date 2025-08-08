import sys
import traceback
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream

from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser

from compiler.IndexingdUMLeListener import IndexingdUMLeListener
from compiler.ContentdUMLeListener import ContentdUMLeListener

from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.error_message import ErrorMessage


def execute_dumle(input_stream):
    # creating objects
    try:
        lexer = dUMLeLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = dUMLeParser(stream)
        tree = parser.program()

        # syntax error
        if parser.getNumberOfSyntaxErrors() > 0:
            exit(-1000)

        # creating objects needed for code execution
        walker = ParseTreeWalker()
        error = ErrorMessage([])
        register = Register()
        output_generator = OutputGenerator()

        # indexing the code
        print("Indexing...")
        indexing_listener = IndexingdUMLeListener(register, output_generator, error)
        walker.walk(indexing_listener, tree)

        # handling the errors
        if error.errors:
            print("Fix the following errors:")
            print(error.errors)
            return

        # executing the code
        print("Executing code...")
        content_listener = ContentdUMLeListener(register, output_generator)
        content_listener.set_global_listener()
        walker.walk(content_listener, tree)
    except Exception as e:
        print("Error message: " + str(e))


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)
