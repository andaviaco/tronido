from lexer import lang
from ..tree import Node

WHILE_COND = dict(
    can_break=True,
    can_continue=True
)

class WhileStat(Node):
    """docstring for WhileStat."""
    def __init__(self,  exp, stats, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.stats = stats


    def process_semantic(self, **cond):
        self.exp.process_semantic()

        if self.exp.datatype != lang.SEMANTIC_LOGIC_TYPE:
            Node.raise_error(f'Condition must be of type {lang.SEMANTIC_LOGIC_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')

        Node.proccess_traversal_semantics(self.stats, **WHILE_COND)
        self.datatype = lang.SEMANTIC_VOID_TYPE

    def generate_code(self, **cond):
        false_label = Node.get_unique_label('false')
        while_label = Node.get_unique_label('while')
        array, _ = Node.assignated_array()
        cond = {'break_to': false_label, 'continua_to': while_label}
        _, line = Node.assignated_array()

        self.exp.generate_code()

        Node.code_labels.append(f'{while_label},I,I,{line},0,#')
        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMC F, {while_label}')

        Node.cascade_code(self.stats, **cond)
        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMP 0, {while_label}')

        line += 1
        Node.code_labels.append(f'{false_label},I,I,{line},0,#')
