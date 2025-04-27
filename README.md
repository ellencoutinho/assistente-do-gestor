# assistente-do-gestor
Linguagem de programação criada com o intuito de permitir que gestores atribuam tarefas à participantes de um projeto e gerem mensagens automáticas especificando-as a cada participante.

#### Funcionamento
A linguagem possibilita atribuir um nome ao projeto, lista de pessoas envolvidas, valores globais ou atributos associados a participantes, atribuição de tarefas (opcionalmente com prazos) e condicionais (lógica simples para alocar tarefas com base em quantidade de tarefas de cada participante ou outros atributos). O compilador validará o programa de entrada e gerará arquivos de saída (<Participante>.txt), um para cada participante, contendo um e‑mail explicando as tarefas e prazos.

#### EBNF
```ebnf
PROGRAMA = ( BLOCO_VARIAVEIS | λ ),
            "iniciar projeto ", NOME_PROJETO, "\n",
            "definir participantes do projeto ", NOME_PROJETO, "\n",
            PARTICIPANTE, { PARTICIPANTE }, "\n",
            "participantes adicionados", "\n",
            "definir tarefas", "\n",
            ACAO, { ACAO }, "\n",
            "tarefas adicionadas" ;

BLOCO_VARIAVEIS = DECLARACAO_VARIAVEL, { DECLARACAO_VARIAVEL } ;

DECLARACAO_VARIAVEL = "definir ", ( VAR_GLOBAL | VAR_POR_PARTICIPANTE ), "\n" ;

VAR_GLOBAL = IDENTIFICADOR, " = ", VALOR ;

VAR_POR_PARTICIPANTE = '"', NOME_PARTICIPANTE, '"', ".", IDENTIFICADOR, " = ", VALOR ;

ACAO = ( TAREFA | CONDICIONAL ) ;

TAREFA = '"', NOME_PARTICIPANTE, '"', " fará ", '"', NOME_TAREFA, '"',
         ( " até ", ( DATA | IDENTIFICADOR ) | λ ), "\n" ;

CONDICIONAL = "se ", EXPRESSAO, " então", TAREFA, "\n",
              ( "senão", "\n", TAREFA | λ ) ;

EXPRESSAO = '"', NOME_PARTICIPANTE, '"', ".", IDENTIFICADOR, OPERADOR, VALOR ;

NOME_PROJETO = { CARACTERE_PROJETO } ;

PARTICIPANTE = '"', NOME_PARTICIPANTE, '"', "\n" ;

NOME_PARTICIPANTE = { CARACTERE_NOME } ;

NOME_TAREFA = { CARACTERE_TAREFA } ;

VALOR = ( '"', { CARACTERE_TAREFA }, '"' | NUMERO ) ;

NUMERO = DIGITO, { DIGITO } ;

DATA = DIGITO, DIGITO, "/", DIGITO, DIGITO, "/", DIGITO, DIGITO, DIGITO, DIGITO ;

IDENTIFICADOR = LETRA, { LETRA | DIGITO | "_" } ;

CARACTERE_PROJETO = ( LETRA | DIGITO | " " ) ;

CARACTERE_NOME = ( LETRA | " " ) ;

CARACTERE_TAREFA = ( LETRA | DIGITO | " " | "." | "," | "-" ) ;

OPERADOR = ( "<" | ">" | "<=" | ">=" | "==" ) ;

LETRA = ( "a" | ... | "z" | "A" | ... | "Z" ) ;

DIGITO = ( "0" | "1" | ... | "9" ) ;
```

#### Exemplo de código de entrada
```python
definir prazo_padrao = "30 dias"
definir "Ellen".experiencia = "Alta"

iniciar projeto Jogos

definir participantes do projeto Jogos
"Ellen"
"Carlos"
participantes adicionados

definir tarefas
"Ellen" fará "Rotação do personagem" até 22/01/2024
"Ellen" fará "Animação de personagem andando"

se "Carlos".qtd_tarefas < 2 então "Carlos" fará "Documentar lógica da animação"
senão "Carlos" fará "Encontrar arquivos" até prazo_padrao

tarefas adicionadas
```

#### Exemplo de arquivo gerado (Ellen.txt)
``` 
Olá Ellen,

Esta mensagem traz as suas tarefas e prazos no projeto "Jogos". Por favor, avalie se terá disponibilidade para lidar com os entregáveis abaixo no prazo proposto. Caso haja algum problema, fale com seu gestor.

Entregáveis:
1. Rotação do personagem até 22/01/2024
2. Animação de personagem andando (sem prazo definido)

Colegas de projeto: Carlos (1 tarefa atribuída).

Atenciosamente,
Equipe de Gestão de Projetos
```
