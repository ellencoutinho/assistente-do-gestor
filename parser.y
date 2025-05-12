%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>

extern FILE *yyin;
extern int yylex();
extern int yyparse();

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
}

char *nome_projeto = NULL;
%}

%code requires {
    typedef struct { char *str; int num; } valor_misto_t;
}

%union {
    char *str;
    int   num;
    char *oper;
    valor_misto_t valor_misto;
}

%token INICIAR_PROJETO DEF_PARTICIPANTES PARTICIPANTES_ADICIONADOS
%token DEF_TAREFAS TAREFAS_ADICIONADAS
%token DEFINIR FARA ATE SE ENTAO SENAO
%token IGUAL MENOR_IGUAL MAIOR_IGUAL MENOR MAIOR ATRIBUICAO PONTO
%token NEWLINE BARRA ERROR

%token <num> NUMERO
%token <str> DATA IDENTIFICADOR STRING

%type <oper>       operador
%type <valor_misto> valor expressao_valor

%start programa
%%
programa:
    declaracoes_opcionais cabecalho participantes_section tarefas_section
    ;

declaracoes_opcionais:
    /* vazio */
  | lista_declaracoes
    ;

lista_declaracoes:
    declaracao_variavel
  | lista_declaracoes declaracao_variavel
    ;

declaracao_variavel:
    DEFINIR IDENTIFICADOR ATRIBUICAO valor NEWLINE
      { printf("Variável global definida: %s\n", $2); }
  | DEFINIR STRING PONTO IDENTIFICADOR ATRIBUICAO valor NEWLINE
      { printf("Variável de participante: %s.%s\n", $2, $4); }
    ;

cabecalho:
    INICIAR_PROJETO STRING NEWLINE
      {
        printf("Projeto iniciado: %s\n", $2);
        nome_projeto = $2;
      }
    ;

participantes_section:
    DEF_PARTICIPANTES STRING NEWLINE
    lista_participantes
    PARTICIPANTES_ADICIONADOS NEWLINE
    ;

lista_participantes:
    STRING NEWLINE
  | lista_participantes STRING NEWLINE
    ;

tarefas_section:
    DEF_TAREFAS NEWLINE
    lista_acoes
    TAREFAS_ADICIONADAS NEWLINE
    ;

lista_acoes:
    acao
  | lista_acoes acao
    ;

acao:
    tarefa
  | condicional
    ;

tarefa:
    STRING FARA STRING NEWLINE
      { printf("Tarefa básica: %s fará %s\n", $1, $3); }
  | STRING FARA STRING ATE DATA NEWLINE
      { printf("Tarefa com data: %s fará %s até %s\n", $1, $3, $5); }
  | STRING FARA STRING ATE IDENTIFICADOR NEWLINE
      { printf("Tarefa com prazo variável: %s fará %s até %s\n", $1, $3, $5); }
    ;

condicional:
    SE expressao_valor ENTAO tarefa SENAO tarefa
      { printf("Condicional completa processada\n"); }
  | SE expressao_valor ENTAO tarefa
      { printf("Condicional sem else processada\n"); }
    ;

expressao_valor:
    STRING PONTO IDENTIFICADOR operador valor
      {
        printf("Expressão: %s.%s %s ", $1, $3, $4);
        if ($5.str) printf("%s\n", $5.str);
        else           printf("%d\n", $5.num);
        $$ = $5;
      }
    ;

operador:
    MENOR       { $$ = "<";  }
  | MAIOR       { $$ = ">";  }
  | MENOR_IGUAL { $$ = "<="; }
  | MAIOR_IGUAL { $$ = ">="; }
  | IGUAL       { $$ = "=="; }
    ;

valor:
    STRING { $$.str = $1; $$.num = 0; }
  | NUMERO { $$.str = NULL; $$.num = $1; }
    ;
%%

int main(int argc, char *argv[]) {
    setlocale(LC_ALL, "pt_BR.UTF-8");
    
    if (argc < 2) {
        fprintf(stderr, "Uso: %s <arquivo_de_entrada>\n", argv[0]);
        return 1;
    }
    yyin = fopen(argv[1], "r");
    if (!yyin) { perror("Erro ao abrir o arquivo"); return 1; }
    if (yyparse() == 0) printf("Análise concluída com sucesso!\n");
    else                printf("Erro durante a análise.\n");
    fclose(yyin);
    return 0;
}
