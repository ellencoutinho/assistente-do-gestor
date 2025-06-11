class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        
    def selectNext(self):
        reserved_phrases = {
            "definir tarefas": "define_tasks",
            "definir": "define",
            "iniciar projeto": "start_project",
            "participantes adicionados": "participants_added",
            "tarefas adicionadas": "tasks_added",
            "fará": "will_do",
            "até": "until",
            "senão": "else",
            "se": "if",
            "então": "then",
            "do projeto": "of_project"
        }

        while self.position < len(self.source) and self.source[self.position] in [' ', '\t']:
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return

        for phrase, token_type in reserved_phrases.items():
            if self.source.startswith(phrase, self.position):
                self.position += len(phrase)
                print(f'gera next token {token_type} na frase {phrase} e position {self.position}')
                self.next = Token(token_type, None)
                return

        current_char = self.source[self.position]

        if (self.position + 9 < len(self.source) and 
            self.source[self.position+2] == '/' and 
            self.source[self.position+5] == '/' and
            self.source[self.position].isdigit() and
            self.source[self.position+1].isdigit() and
            self.source[self.position+3].isdigit() and
            self.source[self.position+4].isdigit() and
            self.source[self.position+6].isdigit() and
            self.source[self.position+7].isdigit() and
            self.source[self.position+8].isdigit() and
            self.source[self.position+9].isdigit()):
            date = self.source[self.position:self.position+10]
            self.position += 10
            self.next = Token('date', date)
            return

        if current_char == '"':
            end_pos = self.position + 1
            while end_pos < len(self.source) and self.source[end_pos] != '"':
                end_pos += 1
            if end_pos >= len(self.source):
                raise Exception("Unclosed string literal")
            string_value = self.source[self.position+1:end_pos]
            self.position = end_pos + 1
            self.next = Token('string', string_value)
            return

        if current_char.isalpha():
            end_pos = self.position
            while end_pos < len(self.source) and (self.source[end_pos].isalnum() or self.source[end_pos] == '_'):
                end_pos += 1
            identifier = self.source[self.position:end_pos]
            self.position = end_pos
            self.next = Token('identifier', identifier)
            return

        if current_char.isdigit():
            end_pos = self.position
            while end_pos < len(self.source) and self.source[end_pos].isdigit():
                end_pos += 1
            number_str = self.source[self.position:end_pos]
            self.position = end_pos
            self.next = Token('number', int(number_str))
            return

        if current_char == '=':
            if self.position + 1 < len(self.source) and self.source[self.position+1] == '=':
                self.position += 2
                self.next = Token('equals', None)
            else:
                self.position += 1
                self.next = Token('assignment', None)
            return

        if current_char == '<':
            if self.position + 1 < len(self.source) and self.source[self.position+1] == '=':
                self.position += 2
                self.next = Token('less_equal', None)
            else:
                self.position += 1
                self.next = Token('less_than', None)
            return

        if current_char == '>':
            if self.position + 1 < len(self.source) and self.source[self.position+1] == '=':
                self.position += 2
                self.next = Token('greater_equal', None)
            else:
                self.position += 1
                self.next = Token('greater_than', None)
            return

        if current_char == '.':
            self.position += 1
            self.next = Token('dot', None)
            return

        if current_char == '\n':
            self.position += 1
            self.next = Token('break_line', None)
            return

        print(f'next token {self.next}')
        raise Exception(f"Unknown token starting with '{current_char}' at position {self.position}")