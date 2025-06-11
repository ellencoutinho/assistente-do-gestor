from program import Code

class Node:
    id = 0

    def generate_id() -> int:
        Node.id += 1
        return Node.id
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.generate_id()
        
    def evaluate(self, st):
        pass

    def generate(self, st):
        pass

class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
        
    def evaluate(self, st):
        return ("string", str(self.value))
    
    def generate(self, st):
        pass

class NumVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
    def evaluate(self, st):
        return ("int", self.value) # Sempre int
    def generate(self, st):
        pass

class BinOp(Node):
    def evaluate(self, st):
        type1, val1 = self.children[0].evaluate(st)
        type2, val2 = self.children[1].evaluate(st)
        
        if type1 != type2:
            raise Exception(f"Operands at BinOp are different {type1} != {type2}")

        if self.value in ['<', 'greater_than']:
            return ("bool", val1 < val2)
        elif self.value in ['>', 'less_than']:
            return ("bool", val1 > val2)
        elif self.value == 'less_equal':
            return ("bool", val1 <= val2)
        elif self.value == 'greater_equal':
            return ("bool", val1 >= val2)
        elif self.value == 'equals':
            return ("bool", val1 == val2)
        else:
            raise Exception(f"Unsupported binary operator: {self.value}")

    def generate(self, st):
        pass

class Identifier(Node):
    def evaluate(self, st):
        type, value, _ = st.get(self.value)
        return type, value
    
    def generate(self, st):
        pass
    
class Block(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)
    
    def generate(self, st):
        for child in self.children:
            child.generate(st)

class Assignment(Node):
    def evaluate(self, st):
        var_name = self.children[0].value
        t_value, v_value = self.children[1].evaluate(st)
        st.set(key=var_name, type=t_value, value=v_value, shift=None)

    def generate(self, st):
        pass

class VarDec(Node):
    def evaluate(self, st):
        if self.children[0] in st.st.keys():
            raise Exception(f"Variable {self.children[0]} already declared")
        
        if self.children[1]:
            evaluated_type, evaluated_value = self.children[1].evaluate(st)
            return st.set(key=self.children[0],
                       type=evaluated_type,
                       value=evaluated_value,
                       shift=None)
        return st.set(key=self.children[0], type=None, value=None, shift=None)
    
    def generate(self, st):
        pass

class NoOp(Node):
    def evaluate(self, st):
        pass

class ProjectStart(Node):
    def evaluate(self, st):
        st.set(key="current_project", type="string", value=self.value, shift=None)
    
    def generate(self, st):
        pass

class ParticipantDeclaration(Node):
    def evaluate(self, st):
        if "participants" not in st.st:
            st.set(key="participants", type="list", value=[], shift=None)
        
        participants = st.get("participants")[1]
        participants.append(self.value)
        st.set(key="participants", type="list", value=participants, shift=None)
        st.set(key=f"{self.value}.qtd_tarefas", type="int", value=0, shift=None)
    
    def generate(self, st):
        pass

class ParticipantsAdded(Node):
    def evaluate(self, st):
        pass
    
    def generate(self, st):
        pass

class TaskDeclaration(Node):
    def evaluate(self, st):
        participant = self.children[0].value
        task = self.children[1].value
        deadline = self.children[2].value if len(self.children) > 2 else None
        
        if "tasks" not in st.st:
            st.set(key="tasks", type="dict", value={}, shift=None)
        
        tasks = st.get("tasks")[1]
        if participant not in tasks:
            tasks[participant] = []
        
        tasks[participant].append((task, deadline))
        st.set(key="tasks", type="dict", value=tasks, shift=None)
    
    def generate(self, st):
        pass

class ConditionalTask(Node):
    def evaluate(self, st):
        condition = self.children[0].evaluate(st)[1]
        if condition:
            self.children[1].evaluate(st)
        elif len(self.children) > 2:
            self.children[2].evaluate(st)
    
    def generate(self, st):
        pass

class TasksAdded(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

        if 'tasks' in st.st:
            tasks = st.get("tasks")[1]
            for participant in tasks.keys():
                st.set(key=f"{participant}.qtd_tarefas", 
                      type="int", 
                      value=len(tasks[participant]), 
                      shift=None)
    
    def generate(self, st):
        project_name = st.get("current_project")[1]
        participants = st.get("participants")[1]
        tasks = st.get("tasks")[1] if "tasks" in st.st else {}
        
        for participant in participants:
            participant_tasks = tasks.get(participant, [])
            other_participants = [p for p in participants if p != participant]
            
            other_tasks_counts = []
            for p in other_participants:
                count = st.get(f"{p}.qtd_tarefas")[1]
                other_tasks_counts.append(f"{p} ({count} tarefa{'s' if count != 1 else ''} atribuída{'s' if count != 1 else ''})")
            
            filename = f"{participant}.txt"
            content = [
                f"Olá {participant},",
                "",
                f"Esta mensagem traz as suas tarefas e prazos no projeto \"{project_name}\". "
                "Por favor, avalie se terá disponibilidade para lidar com os entregáveis abaixo no prazo proposto. "
                "Caso haja algum problema, fale com seu gestor.",
                "",
                "Entregáveis:"
            ]
            
            for i, (task, deadline) in enumerate(participant_tasks, 1):
                if deadline:
                    content.append(f"{i}. {task} até {deadline}")
                else:
                    content.append(f"{i}. {task} (sem prazo definido)")
            
            content.extend([
                "",
                f"Colegas de projeto: {', '.join(other_tasks_counts)}.",
                "",
                "Atenciosamente,",
                "Equipe de Gestão de Projetos"
            ])
            
            Code.add_to_file(filename, "\n".join(content))