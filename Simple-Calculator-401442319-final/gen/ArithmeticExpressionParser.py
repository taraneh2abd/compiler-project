# Generated from ArithmeticExpression.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,9,55,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,0,
        1,0,1,1,1,1,1,1,5,1,19,8,1,10,1,12,1,22,9,1,1,2,1,2,1,2,5,2,27,8,
        2,10,2,12,2,30,9,2,1,3,1,3,1,3,5,3,35,8,3,10,3,12,3,38,9,3,1,4,5,
        4,41,8,4,10,4,12,4,44,9,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,3,5,53,8,5,
        1,5,0,0,6,0,2,4,6,8,10,0,2,1,0,1,2,1,0,3,4,53,0,12,1,0,0,0,2,15,
        1,0,0,0,4,23,1,0,0,0,6,31,1,0,0,0,8,42,1,0,0,0,10,52,1,0,0,0,12,
        13,3,2,1,0,13,14,5,0,0,1,14,1,1,0,0,0,15,20,3,4,2,0,16,17,7,0,0,
        0,17,19,3,4,2,0,18,16,1,0,0,0,19,22,1,0,0,0,20,18,1,0,0,0,20,21,
        1,0,0,0,21,3,1,0,0,0,22,20,1,0,0,0,23,28,3,6,3,0,24,25,7,1,0,0,25,
        27,3,6,3,0,26,24,1,0,0,0,27,30,1,0,0,0,28,26,1,0,0,0,28,29,1,0,0,
        0,29,5,1,0,0,0,30,28,1,0,0,0,31,36,3,8,4,0,32,33,5,5,0,0,33,35,3,
        8,4,0,34,32,1,0,0,0,35,38,1,0,0,0,36,34,1,0,0,0,36,37,1,0,0,0,37,
        7,1,0,0,0,38,36,1,0,0,0,39,41,5,2,0,0,40,39,1,0,0,0,41,44,1,0,0,
        0,42,40,1,0,0,0,42,43,1,0,0,0,43,45,1,0,0,0,44,42,1,0,0,0,45,46,
        3,10,5,0,46,9,1,0,0,0,47,53,5,8,0,0,48,49,5,6,0,0,49,50,3,2,1,0,
        50,51,5,7,0,0,51,53,1,0,0,0,52,47,1,0,0,0,52,48,1,0,0,0,53,11,1,
        0,0,0,5,20,28,36,42,52
    ]

class ArithmeticExpressionParser ( Parser ):

    grammarFileName = "ArithmeticExpression.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'+'", "'-'", "'*'", "'/'", "'^'", "'('", 
                     "')'" ]

    symbolicNames = [ "<INVALID>", "ADD", "SUB", "MUL", "DIV", "POW", "LPAREN", 
                      "RPAREN", "NUMBER", "WS" ]

    RULE_start = 0
    RULE_expr = 1
    RULE_term = 2
    RULE_factor = 3
    RULE_unaryMinus = 4
    RULE_atom = 5

    ruleNames =  [ "start", "expr", "term", "factor", "unaryMinus", "atom" ]

    EOF = Token.EOF
    ADD=1
    SUB=2
    MUL=3
    DIV=4
    POW=5
    LPAREN=6
    RPAREN=7
    NUMBER=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ArithmeticExpressionParser.ExprContext,0)


        def EOF(self):
            return self.getToken(ArithmeticExpressionParser.EOF, 0)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_start

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)




    def start(self):

        localctx = ArithmeticExpressionParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.expr()
            self.state = 13
            self.match(ArithmeticExpressionParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArithmeticExpressionParser.TermContext)
            else:
                return self.getTypedRuleContext(ArithmeticExpressionParser.TermContext,i)


        def ADD(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.ADD)
            else:
                return self.getToken(ArithmeticExpressionParser.ADD, i)

        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.SUB)
            else:
                return self.getToken(ArithmeticExpressionParser.SUB, i)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)




    def expr(self):

        localctx = ArithmeticExpressionParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.term()
            self.state = 20
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==2:
                self.state = 16
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 17
                self.term()
                self.state = 22
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArithmeticExpressionParser.FactorContext)
            else:
                return self.getTypedRuleContext(ArithmeticExpressionParser.FactorContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.MUL)
            else:
                return self.getToken(ArithmeticExpressionParser.MUL, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.DIV)
            else:
                return self.getToken(ArithmeticExpressionParser.DIV, i)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)




    def term(self):

        localctx = ArithmeticExpressionParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 23
            self.factor()
            self.state = 28
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3 or _la==4:
                self.state = 24
                _la = self._input.LA(1)
                if not(_la==3 or _la==4):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 25
                self.factor()
                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryMinus(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArithmeticExpressionParser.UnaryMinusContext)
            else:
                return self.getTypedRuleContext(ArithmeticExpressionParser.UnaryMinusContext,i)


        def POW(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.POW)
            else:
                return self.getToken(ArithmeticExpressionParser.POW, i)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)




    def factor(self):

        localctx = ArithmeticExpressionParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_factor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.unaryMinus()
            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==5:
                self.state = 32
                self.match(ArithmeticExpressionParser.POW)
                self.state = 33
                self.unaryMinus()
                self.state = 38
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryMinusContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(ArithmeticExpressionParser.AtomContext,0)


        def SUB(self, i:int=None):
            if i is None:
                return self.getTokens(ArithmeticExpressionParser.SUB)
            else:
                return self.getToken(ArithmeticExpressionParser.SUB, i)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_unaryMinus

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryMinus" ):
                listener.enterUnaryMinus(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryMinus" ):
                listener.exitUnaryMinus(self)




    def unaryMinus(self):

        localctx = ArithmeticExpressionParser.UnaryMinusContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_unaryMinus)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 42
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 39
                self.match(ArithmeticExpressionParser.SUB)
                self.state = 44
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 45
            self.atom()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(ArithmeticExpressionParser.NUMBER, 0)

        def LPAREN(self):
            return self.getToken(ArithmeticExpressionParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(ArithmeticExpressionParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(ArithmeticExpressionParser.RPAREN, 0)

        def getRuleIndex(self):
            return ArithmeticExpressionParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)




    def atom(self):

        localctx = ArithmeticExpressionParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_atom)
        try:
            self.state = 52
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 47
                self.match(ArithmeticExpressionParser.NUMBER)
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 2)
                self.state = 48
                self.match(ArithmeticExpressionParser.LPAREN)
                self.state = 49
                self.expr()
                self.state = 50
                self.match(ArithmeticExpressionParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





