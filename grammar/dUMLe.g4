grammar dUMLe;

program
    : ((BR | NL)* (instruction | diagcreation) (BR | NL)*)* EOF;

diagcreation
    : class_diagram
    | seq_diagram
    | use_case_diagram;
    
class_diagram
    : 'diagclass' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;

seq_diagram
    : 'diagseq' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;

use_case_diagram
    : 'diagusecase' BR+ NAME BR* ':' BR* NL
    (NL* IND+ instruction BR* NL*)+;
    
instruction
    : obj_declaration
    | list_declaration
    | list_access
    | assignment
    | fun_declaration
    | execution
    | loop
    | connection;

obj_declaration
    : class_declaration
    | note
    | actor
    | theme
    | package_declaration
    | block
    | use_case;

list_declaration
    : '[' BR* ((name | obj_access) BR* (',' BR* (name | obj_access))*)? BR* ']';
    
list_access
    : name '[' NUMBER ']' BR*;
    
assignment
    : arg_list BR+ '=' BR+ (fun_call | list_declaration | arg_list_include_scope) BR* NL;

fun_declaration
    : 'def' BR+ NAME '(' BR* arg_list* BR* ')' BR* ':' BR* NL
        (NL* IND+ instruction NL*)*
        IND+ 'return' BR+ arg_list BR* NL;
        
fun_call
    : name '(' BR* arg_list_include_scope BR* ')' BR* NUMBER? BR*;

execution
    : 'exec' (BR+ NAME)? (BR+ MODE)? (BR+ (list_declaration | list_access | NAME))? (BR+ TEXT)? BR* NL;

loop
    : 'for' BR+ NAME BR+ 'in' BR+ (name | list_declaration | fun_call) BR* ':' BR* NL
        (NL* IND+ instruction NL*)+;
        
connection
    : (name | obj_access | list_access) BR+ (ARROW | CONNECTION_TYPE) BR+ (name | obj_access | list_access) (BR+ 'labeled' BR+ TEXT )? BR* NL*;
    
obj_access
    : name '.' (name | obj_access);

class_declaration
    : CLASS_TYPE (BR+ name)? BR+ NAME BR* ':' BR* NL
    (class_declaration_line)+;

class_declaration_line:
    NL* IND+ (MODIFIER BR+)? TEXT BR* NL*;

note
    : 'note' (BR+ name)? BR+ NAME BR* ':' BR* NL
    (NL* IND+ TEXT BR* NL*)+;

actor
    : 'actor' (BR+ name)? BR+ NAME BR* NL;

theme
    : 'theme' BR+ NAME BR* ':' BR* NL
    (NL* IND+ PARAM_TYPE BR+ TEXT BR* NL*)+;

package_declaration
    : 'package' BR+ PACKAGE_TYPE BR+ NAME BR* ':' BR* NL
    (NL* IND+ NAME BR* NL*)+;

arg_list
    : NAME BR* (',' BR* NAME)*;

arg_list_include_scope
    : (arg_name BR* (',' BR* arg_name)*)?;
    
block
    : 'block' (BR+ name)? BR+ NAME BR* NL;

use_case
    : 'usecase' (BR+ name)? BR+ NAME BR* ':' BR* NL
    (NL* IND+ TEXT BR* NL*)+;

name
    : SCOPE_NAME?NAME;

arg_name
    : DEEP_COPY?name;

PACKAGE_TYPE
    : 'CLASS'
    | 'USECASE'
    | 'SEQ';

CLASS_TYPE
    : 'class'
    | 'abstract'
    | 'interface';

PARAM_TYPE
    : 'fontcolor'
    | 'backgroundcolor'
    | 'fontsize'
    | 'font'
    | 'bordercolor';

CONNECTION_TYPE
    :
    'inherit'
     | 'implement'
     | 'associate'
     | 'depend'
     | 'aggregate'
     | 'compose';

MODIFIER
    : 'public'
    | 'protected'
    | 'private';

CR
	: 
	'\r' -> skip;


MODE
    :
    'brief' | 'all';

COM_SIGN 		
	: 
	'#' ~[\r\n]* -> skip;

DEEP_COPY
    :
    '$';

BR
    :
    ' ';

SCOPE_NAME
    :
    [A-Za-z_][a-zA-Z0-9_]*'&';

NAME
    :
    [A-Za-z_][a-zA-Z0-9_]*;

NUMBER
    :
    [0-9]+;
    
NL
    :
    '\n';
    
IND
    :
    '\t'
    | '    ';
    
QUOTE
    :
    '\''|
    '"';
    
ARROW
    : 
    ('x<' | '<' | '<<' | '\\' | '//' | '\\\\' | 'o<' | '\\\\o')?
    ('.' | '-' | '_')
    ('>x' | '>' | '>>' | '\\' | '//' | '\\\\' | '>o' | 'o\\\\');
    
TEXT
    : 
    QUOTE (~[\r\n"])+ QUOTE;