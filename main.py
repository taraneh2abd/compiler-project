import sys
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from graphviz import Digraph  

from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser

from compiler.IndexingdUMLeListener import IndexingdUMLeListener
from compiler.ContentdUMLeListener import ContentdUMLeListener
from compiler.ASTBuilder import ASTBuilder

from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.error_message import ErrorMessage

import hashlib
from graphviz import Digraph


from antlr4 import CommonTokenStream, FileStream
from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser
from compiler.ASTBuilder import ASTBuilder
from compiler.IndexingASTVisitor import IndexingASTVisitor
from compiler.ContentASTVisitor import ContentASTVisitor
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.error_message import ErrorMessage

def execute_dumle(input_stream):
    try:
        lexer = dUMLeLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = dUMLeParser(stream)
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print("Syntax errors detected.")
            exit(-1000)

        print("Building AST...")
        ast_builder = ASTBuilder()
        walker = ParseTreeWalker()
        walker.walk(ast_builder, tree)
        ast = ast_builder.get_ast()

        print("Drawing AST with Graphviz...")
        draw_ast(ast)

        error = ErrorMessage([])
        register = Register()
        output_generator = OutputGenerator()

        print("Indexing (AST)...")
        indexing_visitor = IndexingASTVisitor(register, output_generator, error)
        indexing_visitor.visit(ast)

        if error.errors:
            print("Fix the following errors:")
            print(error.errors)
            return

        print("Executing code (AST)...")
        content_visitor = ContentASTVisitor(register, output_generator)
        content_visitor.visit(ast)

        print("\nFinal Output:")
        print(output_generator.generate()) 

    except Exception as e:
        print("Error message:", str(e))




def draw_ast(ast):
    dot = Digraph(comment="AST")

    def get_color(node_type):
        colors = ["lightblue","lightgreen","lightpink","yellow","orange","cyan","magenta",
                  "lightcoral","lightgoldenrod","lightseagreen","lightsteelblue","plum",
                  "khaki","salmon","wheat","thistle","orchid","tan","palegreen","lightcyan"]
        h = int(hashlib.md5(node_type.encode()).hexdigest(), 16)
        return colors[h % len(colors)]

    def add_nodes_edges(node, parent_id=None):
        node_id = str(id(node))
        label = node.node_type if node.value is None else f"{node.node_type}: {node.value}"
        color = get_color(node.node_type)
        dot.node(node_id, label, style="filled", fillcolor=color)
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            add_nodes_edges(child, node_id)

    add_nodes_edges(ast)
    dot.render("results/ast_output", format="png", cleanup=True)
    print("AST graph saved as results/ast_output.png")


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)
