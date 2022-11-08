//定义语法分析所使用的语法规范
grammar MiniDecaf;

import CommonLex;

prog: externalDecl+ EOF
    ;

externalDecl
    : func       # funcExternalDecl
    | decl ';'   # declExternalDecl
    ;

func: ty Indentifier '(' parameterList ')' block  #funcDef
    | ty Indentifier '(' parameterList ')' ';'    #funcDecl
    ;

parameterList
    : (decl (',' decl)*)?
    ;

ty: 'int'  # intType
    | ty '*' # ptrType
    ;

blockItem : stmt    #blockItemStmt
          | decl ';'    #blockItemDecl
          ;

block : '{' blockItem* '}';


stmt: 'return' expr ';' # returnCont
    | expr ';' # exprStmt
    | ';' # nullstmt
    | 'if' '(' expr ')' th=stmt ('else' el=stmt)?   # ifStmt
    |  block  # blockStmt
    | 'for' '(' init=decl ';' control=expr? ';' post=expr? ')' stmt    # forDeclStmt
    | 'for' '(' init=expr? ';' control=expr? ';' post=expr? ')' stmt   # forStmt
    | 'while' '(' expr ')' stmt # whileStmt
    | 'do' stmt 'while' '(' expr ')' ';' # doWhileStmt
    | 'break' ';' # breakStmt
    | 'continue' ';' # continueStmt
    ;

expr: asgn
    ;

decl: ty Indentifier ('[' Integer ']')* ('=' expr)?
    ;

asgn
    : cond # tAsgn
    | unary assignList asgn # cAssign
    ;

cond
    : logical_or # tCond
    | logical_or '?' expr ':' cond # cCond
    ;


logical_or
    : logical_and   # tLor
    | logical_or '||' logical_and   # cLor
    ;

logical_and
    : equality  # tLand
    | logical_and '&&' equality #   cLand
    ;

equality
    : relational    # tEq
    | equality equalList relational #cEq
    ;

relational
    : additive  # tRel
    | relational relationList additive #cRel
    ;

additive
    : multiplicative    # tAdd
    | additive addList multiplicative # cAdd
    ;

multiplicative
    : cast    # tMul
    | multiplicative mulList cast  #cMul
    ;

cast
    : unary    # tCast
    | '(' ty ')' cast # cCast
    ;

unary
    : postfix   #tUnary
    | unaryList cast   #cUnary
    ;

postfix
    : primary # tPostfix
    | postfix '[' expr ']' # postfixArray
    | Indentifier '(' argmentList ')' # postfixCall
    ;

primary
    : Integer   # primaryInteger
    | Indentifier   # primaryIndentifier
    | '(' expr ')'  # primaryParen
    ;

argmentList
    : (expr (',' expr)*)?
    ;

unaryList
    : '-'|'!'|'~'|'*'|'&'
    ;

addList
    : '+' | '-'
    ;

assignList
    : '='
    ;

mulList
    : '*' | '/' | '%'
    ;

relationList
    : '>' | '<' | '>=' | '<='
    ;

equalList
    : '==' | '!='
    ;
