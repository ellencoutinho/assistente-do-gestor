/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 1
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 18 "parser.y"

    typedef struct { char *str; int num; } valor_misto_t;

#line 53 "parser.tab.h"

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    INICIAR_PROJETO = 258,         /* INICIAR_PROJETO  */
    DEF_PARTICIPANTES = 259,       /* DEF_PARTICIPANTES  */
    PARTICIPANTES_ADICIONADOS = 260, /* PARTICIPANTES_ADICIONADOS  */
    DEF_TAREFAS = 261,             /* DEF_TAREFAS  */
    TAREFAS_ADICIONADAS = 262,     /* TAREFAS_ADICIONADAS  */
    DEFINIR = 263,                 /* DEFINIR  */
    FARA = 264,                    /* FARA  */
    ATE = 265,                     /* ATE  */
    SE = 266,                      /* SE  */
    ENTAO = 267,                   /* ENTAO  */
    SENAO = 268,                   /* SENAO  */
    IGUAL = 269,                   /* IGUAL  */
    MENOR_IGUAL = 270,             /* MENOR_IGUAL  */
    MAIOR_IGUAL = 271,             /* MAIOR_IGUAL  */
    MENOR = 272,                   /* MENOR  */
    MAIOR = 273,                   /* MAIOR  */
    ATRIBUICAO = 274,              /* ATRIBUICAO  */
    PONTO = 275,                   /* PONTO  */
    NEWLINE = 276,                 /* NEWLINE  */
    BARRA = 277,                   /* BARRA  */
    ERROR = 278,                   /* ERROR  */
    NUMERO = 279,                  /* NUMERO  */
    DATA = 280,                    /* DATA  */
    IDENTIFICADOR = 281,           /* IDENTIFICADOR  */
    STRING = 282                   /* STRING  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 22 "parser.y"

    char *str;
    int   num;
    char *oper;
    valor_misto_t valor_misto;

#line 104 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
