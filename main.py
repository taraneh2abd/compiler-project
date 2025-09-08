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
        color = get_color(node.node_type)  # رنگ خودکار
        dot.node(node_id, label, style="filled", fillcolor=color)
        if parent_id:
            dot.edge(parent_id, node_id)
        for child in node.children:
            add_nodes_edges(child, node_id)

    add_nodes_edges(ast)
    dot.render("results/ast_output", format="png", cleanup=True)
    print("AST graph saved as results/ast_output.png")


def execute_dumle(input_stream):
    try:
        lexer = dUMLeLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = dUMLeParser(stream)
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print("Syntax errors detected.")
            exit(-1000)

        walker = ParseTreeWalker()
        error = ErrorMessage([])
        register = Register()
        output_generator = OutputGenerator()

        print("Indexing...")
        indexing_listener = IndexingdUMLeListener(register, output_generator, error)
        walker.walk(indexing_listener, tree)

        if error.errors:
            print("Fix the following errors:")
            print(error.errors)
            return

        print("Executing code...")
        content_listener = ContentdUMLeListener(register, output_generator)
        content_listener.set_global_listener()
        walker.walk(content_listener, tree)

        print("\nGenerating AST...")
        ast_builder = ASTBuilder()
        walker.walk(ast_builder, tree)
        ast = ast_builder.get_ast()

        # print("\nAST:")
        # print(ast)

        print("\nDrawing AST with Graphviz...")
        draw_ast(ast)

        # print("\nPost-order Traversal:")
        post_order_list = []
        def post_order(node):
            for child in node.children:
                post_order(child)
            post_order_list.append(node.node_type)
        post_order(ast)
        # print(post_order_list)

        # print("\nGenerating IL Code...")
        # il_code = [f"IL_{token}" for token in post_order_list]
        # with open("output.il", "w", encoding="utf-8") as f:
        #     f.write("\n".join(il_code))
        # print("IL code written to output.il")

    except Exception as e:
        print("Error message:", str(e))


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)
