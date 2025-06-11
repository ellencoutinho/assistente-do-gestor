from tokenizer import Tokenizer
from nodes import *
import re

class PrePro:
    @staticmethod
    def filter(code):
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip() != '']
        return '\n'.join(non_empty_lines)

class Parser:
    tokenizer : Tokenizer

    @staticmethod
    def parseFactor():
        if Parser.tokenizer.next.type == 'string':
            value = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            # detecta acesso de propriedade:
            if Parser.tokenizer.next.type == 'dot':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'identifier':
                    prop = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    full = f"{value}.{prop}"
                    return Identifier(value=full, children=[])
            return StrVal(value=value)
        
        elif Parser.tokenizer.next.type == 'number':
            value = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            return NumVal(value)
        
        elif Parser.tokenizer.next.type == 'identifier':
            tree = Identifier(value=Parser.tokenizer.next.value, children=[])
            Parser.tokenizer.selectNext()
            return tree
        elif Parser.tokenizer.next.type == 'date':
            tree = StrVal(value=Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
            return tree
        else:
            raise Exception(f"Incorrect token at parseFactor: {Parser.tokenizer.next.type}")
    
    @staticmethod
    def parseRelExpression():
        left = Parser.parseFactor()
        if Parser.tokenizer.next.type in ['less_than', 'greater_than', 'less_equal', 'greater_equal', 'equals']:
            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            right = Parser.parseFactor()
            return BinOp(op, [left, right])
        return left


    @staticmethod
    def parseVariableDeclaration():
        # Já consumimos 'definir' antes de chegar aqui
        if Parser.tokenizer.next.type == 'string':
            participant = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'dot':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'identifier':
                    var_name = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'assignment':
                        Parser.tokenizer.selectNext()
                        value = Parser.parseFactor()
                        return VarDec(value=var_name, children=[f"{participant}.{var_name}", value])
        
        elif Parser.tokenizer.next.type == 'identifier':
            var_name = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'assignment':
                Parser.tokenizer.selectNext()
                value = Parser.parseFactor()
                return VarDec(value="var", children=[var_name, value])
        
        raise Exception(f"Invalid variable declaration. Unexpected token: {Parser.tokenizer.next.type}")

    @staticmethod
    def parseParticipant():
        if Parser.tokenizer.next.type == 'string':
            participant = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            return ParticipantDeclaration(value=participant, children=[])
        raise Exception("Expected participant name in quotes")

    @staticmethod
    def parseTask():
        if Parser.tokenizer.next.type == 'string':
            participant = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'will_do':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'string':
                    task = Parser.tokenizer.next.value
                    Parser.tokenizer.selectNext()
                    deadline_node = None
                    if Parser.tokenizer.next.type == 'until':
                        Parser.tokenizer.selectNext()
                        tok_type = Parser.tokenizer.next.type
                        tok_val  = Parser.tokenizer.next.value
                        if tok_type == 'date':
                            deadline_node = StrVal(tok_val)
                        elif tok_type == 'identifier':
                            deadline_node = Identifier(tok_val, [])
                        else:
                            raise Exception("Deadline inválido")
                        Parser.tokenizer.selectNext()
                    children = [StrVal(participant), StrVal(task)] 
                    if deadline_node:
                        children.append(deadline_node)    
                    return TaskDeclaration(value=None, children=children)
        raise Exception("Invalid task declaration")

    @staticmethod
    def parseConditionalTask():
        Parser.tokenizer.selectNext()  # skip 'se'
        condition = Parser.parseRelExpression()
        Parser.tokenizer.selectNext()  # skip 'então'
        then_task = Parser.parseTask()
        Parser.tokenizer.selectNext() # break line

        else_task = None
        if Parser.tokenizer.next.type == 'else':
            Parser.tokenizer.selectNext()
            else_task = Parser.parseTask()
        
        return ConditionalTask(value=None, children=[condition, then_task, else_task] if else_task else [condition, then_task])

    @staticmethod
    def parseStatement():
        # Bloco de variáveis
        if Parser.tokenizer.next.type == 'define':
            Parser.tokenizer.selectNext()

            # "definir participantes do projeto"
            if Parser.tokenizer.next.type == 'identifier' and Parser.tokenizer.next.value == 'participantes':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type == 'of_project':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.next.type == 'string':
                        project_name = Parser.tokenizer.next.value
                        Parser.tokenizer.selectNext()
                        # consome quebra de linha após o nome do projeto
                        if Parser.tokenizer.next.type == 'break_line':
                            Parser.tokenizer.selectNext()
                        # lê participantes
                        participants = []
                        while Parser.tokenizer.next.type == 'string':
                            participants.append(Parser.parseParticipant())
                            Parser.tokenizer.selectNext()
                        # token participantes adicionados
                        if Parser.tokenizer.next.type == 'participants_added':
                            Parser.tokenizer.selectNext()

                            # consome quebra de linha após participantes adicionados
                            if Parser.tokenizer.next.type == 'break_line':
                                Parser.tokenizer.selectNext()
                            # retorna array com declarações e nó de finalização
                            return Block(value=None,
                                         children=participants + [ParticipantsAdded(value=None, children=[])])

            # Declaração normal de variável
            else:
                return Parser.parseVariableDeclaration()

        # "definir tarefas"
        elif Parser.tokenizer.next.type == 'define_tasks':
            Parser.tokenizer.selectNext()
            # consome quebra de linha após "definir tarefas"
            if Parser.tokenizer.next.type == 'break_line':
                Parser.tokenizer.selectNext()
            tasks = []
            while Parser.tokenizer.next.type in ['string', 'if']:
                if Parser.tokenizer.next.type == 'string':
                    tasks.append(Parser.parseTask())
                    Parser.tokenizer.selectNext()
                else:
                    tasks.append(Parser.parseConditionalTask())
            
            while Parser.tokenizer.next.type == 'break_line':
                Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == 'tasks_added':
                Parser.tokenizer.selectNext()
                # consome quebra de linha após tarefas adicionadas
                if Parser.tokenizer.next.type == 'break_line':
                    Parser.tokenizer.selectNext()
                return TasksAdded(value=None, children=tasks)

        # Início de projeto
        elif Parser.tokenizer.next.type == 'start_project':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == 'string':
                project_name = Parser.tokenizer.next.value
                Parser.tokenizer.selectNext()
                return ProjectStart(value=project_name, children=[])

        # Linhas em branco / NoOp
        elif Parser.tokenizer.next.type == 'break_line':
            Parser.tokenizer.selectNext()
            return NoOp(value=None, children=[])
        # Se nada casou, erro de sintaxe
        raise Exception(f"Unexpected token at parseStatement: {Parser.tokenizer.next.type}")

    @staticmethod
    def run(code):
        processed_code = PrePro.filter(code)
        Parser.tokenizer = Tokenizer(processed_code)
        Parser.tokenizer.selectNext()

        statements = []
        while Parser.tokenizer.next.type != 'EOF':
            statements.append(Parser.parseStatement())
            
        return Block(value=None, children=statements)