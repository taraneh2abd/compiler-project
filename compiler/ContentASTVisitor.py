from compiler.ASTBuilder import ASTNode

class ContentASTVisitor:
    def __init__(self, register, output_generator):
        self.register = register
        self.output_generator = output_generator

    def visit(self, node: ASTNode):
        if node.node_type == "Class_diagram":
            self.handle_class_diagram(node)
        for child in node.children:
            self.visit(child)

    def handle_class_diagram(self, node: ASTNode):
        self.output_generator.add_line(f"Generating content for class diagram: {node.value}")
