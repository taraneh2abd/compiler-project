# Generated from ArithmeticExpression.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ArithmeticExpressionParser import ArithmeticExpressionParser
else:
    from ArithmeticExpressionParser import ArithmeticExpressionParser

# This class defines a complete listener for a parse tree produced by ArithmeticExpressionParser.
class ArithmeticExpressionListener(ParseTreeListener):

    # Enter a parse tree produced by ArithmeticExpressionParser#start.
    def enterStart(self, ctx:ArithmeticExpressionParser.StartContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#start.
    def exitStart(self, ctx:ArithmeticExpressionParser.StartContext):
        pass


    # Enter a parse tree produced by ArithmeticExpressionParser#expr.
    def enterExpr(self, ctx:ArithmeticExpressionParser.ExprContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#expr.
    def exitExpr(self, ctx:ArithmeticExpressionParser.ExprContext):
        pass


    # Enter a parse tree produced by ArithmeticExpressionParser#term.
    def enterTerm(self, ctx:ArithmeticExpressionParser.TermContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#term.
    def exitTerm(self, ctx:ArithmeticExpressionParser.TermContext):
        pass


    # Enter a parse tree produced by ArithmeticExpressionParser#factor.
    def enterFactor(self, ctx:ArithmeticExpressionParser.FactorContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#factor.
    def exitFactor(self, ctx:ArithmeticExpressionParser.FactorContext):
        pass


    # Enter a parse tree produced by ArithmeticExpressionParser#unaryMinus.
    def enterUnaryMinus(self, ctx:ArithmeticExpressionParser.UnaryMinusContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#unaryMinus.
    def exitUnaryMinus(self, ctx:ArithmeticExpressionParser.UnaryMinusContext):
        pass


    # Enter a parse tree produced by ArithmeticExpressionParser#atom.
    def enterAtom(self, ctx:ArithmeticExpressionParser.AtomContext):
        pass

    # Exit a parse tree produced by ArithmeticExpressionParser#atom.
    def exitAtom(self, ctx:ArithmeticExpressionParser.AtomContext):
        pass



del ArithmeticExpressionParser