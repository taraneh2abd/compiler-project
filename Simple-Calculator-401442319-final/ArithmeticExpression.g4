grammar ArithmeticExpression;

start: expr EOF;

expr: term ( (ADD | SUB) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: unaryMinus (POW unaryMinus)* ;
unaryMinus: (SUB)* atom ;
atom: NUMBER | LPAREN expr RPAREN ;

LPAREN: '(';
RPAREN: ')';
ADD: '+';
SUB: '-';
MUL: '*';
DIV: '/';
POW: '^';

NUMBER:INTEGER| DECIMAL| LEADING_DECIMAL| TRAILING_DECIMAL;

fragment INTEGER: DIGIT+ ;
fragment DECIMAL: DIGIT+ '.' DIGIT+ ;
fragment LEADING_DECIMAL: '.' DIGIT+ ;
fragment TRAILING_DECIMAL: DIGIT+ '.' ;
fragment DIGIT: [0-9];

WS: [ \t\r\n]+ -> skip;