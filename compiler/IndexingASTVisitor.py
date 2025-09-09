from compiler.ASTBuilder import ASTNode

class IndexingASTVisitor:
    def __init__(self, register, output_generator, error):
        self.register = register
        self.output_generator = output_generator
        self.error = error

    def visit(self, node: ASTNode):
        # مثال: اگر rule تو AST اسمش Class_diagram باشه
        if node.node_type == "Class_diagram":
            self.handle_class_diagram(node)
        # ادامه پیمایش
        for child in node.children:
            self.visit(child)

    def handle_class_diagram(self, node: ASTNode):
        # اینجا دقیقا همون کارهایی رو بکن که توی IndexingdUMLeListener.enterClass_diagram می‌کردی
        self.output_generator.add_line(f"Indexing class diagram: {node.value}")
