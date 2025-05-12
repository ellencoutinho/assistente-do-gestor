%option noyywrap

%{
#include "parser.tab.h"
#include <stdlib.h>
#include <string.h>
%}

DIGITO    [0-9]
LETRA     [A-Za-záéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ]
ID_CONT   [A-Za-z0-9_áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ]
TEXTO     [A-Za-z0-9 .,\-áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ]

%%

^[ \t]*\n                       { /* ignora linha em branco */ }

"iniciar projeto"               { return INICIAR_PROJETO; }
"definir participantes do projeto" { return DEF_PARTICIPANTES; }
"participantes adicionados"     { return PARTICIPANTES_ADICIONADOS; }
"definir tarefas"               { return DEF_TAREFAS; }
"tarefas adicionadas"           { return TAREFAS_ADICIONADAS; }
"definir"                       { return DEFINIR; }
"fará"                         { return FARA; }
"até"                          { return ATE; }
"se"                           { return SE; }
"então"                        { return ENTAO; }
"senão"                        { return SENAO; }

"=="                            { return IGUAL; }
"<="                            { return MENOR_IGUAL; }
">="                            { return MAIOR_IGUAL; }
"<"                             { return MENOR; }
">"                             { return MAIOR; }
"="                             { return ATRIBUICAO; }
"."                             { return PONTO; }
"/"                             { return BARRA; }
\n                              { return NEWLINE; }

{DIGITO}{DIGITO}\/{DIGITO}{DIGITO}\/{DIGITO}{DIGITO}{DIGITO}{DIGITO} {
    yylval.str = strdup(yytext);
    return DATA;
}

{DIGITO}+ {
    yylval.num = atoi(yytext);
    return NUMERO;
}

\"{TEXTO}+\" {
    yylval.str = strndup(yytext+1, yyleng-2);
    return STRING;
}

{LETRA}{ID_CONT}* {
    yylval.str = strdup(yytext);
    return IDENTIFICADOR;
}

[ \t\r]+                        { /* ignora espaços */ }

. {
    fprintf(stderr, "Caractere inesperado: %s\n", yytext);
    return ERROR;
}

%%
