//定义词法分析使用的词法规范
lexer grammar CommonLex;

Integer: Digit+;
Indentifier: FirstChar LastChar*;
WhiteSpace: WhiteChar+ -> skip;

fragment WhiteChar: [ \t\n\r];
fragment Digit:[0-9];
fragment FirstChar: [a-zA-Z_];
fragment LastChar: [0-9a-zA-Z_];