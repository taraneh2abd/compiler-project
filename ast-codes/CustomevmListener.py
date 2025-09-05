from gen.evmListener import evmListener
from gen.evmParser import evmParser
from ast_required_code_collection.ast import AST
from ast_required_code_collection.make_ast_subtree import make_ast_subtree

class CustomevmListener(evmListener):
	def __init__(self):
		self.overridden_rules = ['program','print_variable','for_increment']
		self.binary_operator_list = ['term','expression','variable_assignment','comparison_statement']
		self.rule_names = []
		self.ast = AST()


	def exitEveryRule(self, ctx):
		rule_name = self.rule_names[ctx.getRuleIndex()]
		if rule_name not in self.overridden_rules:
			if rule_name in self.binary_operator_list and ctx.getChildCount() > 1:
				make_ast_subtree(self.ast, ctx, ctx.getChild(1).getText())
			else:
				make_ast_subtree(self.ast, ctx, rule_name)


	def exitProgram(self, ctx):
		make_ast_subtree(self.ast, ctx, "program", keep_node=True)


	def exitPrint_variable(self, ctx):
		make_ast_subtree(self.ast, ctx, "print_variable", keep_node=True)


	def exitFor_increment(self,ctx):
		make_ast_subtree(self.ast, ctx, "increment", keep_node=True)

	def exitFunction_declaration(self, ctx):
		make_ast_subtree(self.ast, ctx, "function_declaration", keep_node=True)

	def exitReturn_statement(self, ctx):
		make_ast_subtree(self.ast, ctx, "return_statement", keep_node=True)
