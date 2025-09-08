from antlr4 import ParseTreeListener
from compiler.dUMLeParser import dUMLeParser

class ASTNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self, level=0):
        ret = "\t" * level + f"{self.node_type}: {self.value}\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


class ASTBuilder(ParseTreeListener):
    def __init__(self):
        self.stack = []
        self.root = None

    def enterEveryRule(self, ctx):
        rule_name = type(ctx).__name__.replace("Context", "")
        node = ASTNode(rule_name)
        self.stack.append(node)

    def exitEveryRule(self, ctx):
        node = self.stack.pop()
        if len(self.stack) > 0:
            self.stack[-1].add_child(node)
        else:
            self.root = node

    def visitTerminal(self, node):
        if self.stack:
            self.stack[-1].add_child(ASTNode("Terminal", node.getText()))

    def get_ast(self):
        return self.root