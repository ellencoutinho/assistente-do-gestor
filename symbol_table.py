class SymbolTable:
    def __init__(self):
        self.st = {}
        self.next_shift = 0
            
    def get(self, key):
        try:
            if '.' in key:
                participant, prop = key.split('.')
                if prop == 'qtd_tarefas':
                    if 'tasks' in self.st and participant in self.st['tasks'][1]:
                        return ("int", len(self.st['tasks'][1][participant]), None)
                    return ("int", 0, None)
            return self.st[key]
        except:
            raise Exception(f"The key {key} doesn't exists at the SymbolTable")

    def set(self, key, type, value, shift):
        self.st[key] = (type, value, shift)