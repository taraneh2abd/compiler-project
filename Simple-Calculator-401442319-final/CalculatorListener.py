from antlr4.tree.Tree import TerminalNode
from gen.ArithmeticExpressionListener import ArithmeticExpressionListener
from gen.ArithmeticExpressionParser import ArithmeticExpressionParser


class CalculatorListener(ArithmeticExpressionListener):
    def __init__(self, rule_names):
        self.rule_names = rule_names
        self.stack = []

    def exitUnaryMinus(self, ctx):
        negations = ctx.SUB()
        if len(self.stack) == 0:
            raise RuntimeError("Error: UnaryMinus stack empty")
        number = self.stack.pop()
        if len(negations) % 2:
            number *= -1
        self.stack.append(number)

    def exitAtom(self, ctx):
        token = ctx.NUMBER()
        if token:
            text = token.getText()
            value = float(text) if '.' in text else int(text)
            self.stack.append(value)

    def exitFactor(self, ctx):
        powers = ctx.POW()
        if not powers:
            return
        exp_list = [self.stack.pop() for _ in powers]
        base_val = self.stack.pop()
        for exponent in reversed(exp_list):
            base_val = base_val ** exponent
        self.stack.append(base_val)

    def exitTerm(self, ctx):
        operands = [self.stack.pop() for _ in ctx.factor()]
        operands = operands[::-1]
        product = operands[0]
        operators = [tok.getText() for tok in ctx.children if tok.getText() in {'*', '/'}]
        for idx, symbol in enumerate(operators):
            operand = operands[idx + 1]
            product = product * operand if symbol == '*' else product / operand
        self.stack.append(product)

    def exitExpr(self, ctx):
        terms = [self.stack.pop() for _ in ctx.term()]
        terms.reverse()
        result = terms[0]
        symbols = [c.getText() for c in ctx.children if c.getText() in {'+', '-'}]
        for idx, op in enumerate(symbols):
            operand = terms[idx + 1]
            result = result + operand if op == '+' else result - operand
        self.stack.append(result)

    def get_result(self):
        if self.stack:
            return self.stack[0]
        return None

