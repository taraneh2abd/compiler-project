from antlr4 import *
import argparse
from CustomevmListener import CustomevmListener
from gen.evmLexer import evmLexer
from gen.evmParser import evmParser
from ast_required_code_collection.ast_to_networkx_graph import show_ast


def main(arguments):
	stream = FileStream(arguments.input, encoding='utf8')
	lexer = evmLexer(stream)
	token_stream = CommonTokenStream(lexer)
	parser = evmParser(token_stream)
	parse_tree = parser.program()
	ast_builder_listener = CustomevmListener()
	ast_builder_listener.rule_names = parser.ruleNames
	walker = ParseTreeWalker()
	walker.walk(t=parse_tree, listener=ast_builder_listener)
	ast = ast_builder_listener.ast
	show_ast(ast.root)
	traversal = ast.traverse_ast(ast.root)


if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-i', '--input', help='Input source', default=r'input/test_3.txt')
	argparser.add_argument('-o', '--output', help='Output path', default=r'output/test.evm-bytecode')
	args = argparser.parse_args()
	main(args)
