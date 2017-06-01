from lexer import lang
from ..tree import Node

class IfStat(Node):
    """docstring for IfStat."""
    def __init__(self, exp, stats, else_stat, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.stats = stats
        self.else_stat = else_stat

    def process_semantic(self, **cond):
        self.exp.process_semantic()

        if self.exp.datatype != lang.SEMANTIC_LOGIC_TYPE:
            Node.raise_error(f'Condition must be of type {lang.SEMANTIC_LOGIC_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')
        else:
            self.datatype = lang.SEMANTIC_VOID_TYPE

        Node.proccess_traversal_semantics(self.stats, **cond)
        Node.proccess_traversal_semantics(self.else_stat, **cond)

    def generate_code(self, **cond):
        self.exp.generate_code()

        false_label = Node.get_unique_label('false')
        end_label = Node.get_unique_label('endif')

        array, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMC F, {false_label}')
        Node.cascade_code(self.stats, **cond)

        _, endstatement_line = Node.assignated_array()
        Node.array_append(array, f'{endstatement_line} JMP 0, {end_label}')

        endstatement_line += 1

        Node.code_labels.append(f'{false_label},I,I,{endstatement_line},0,#,')
        Node.cascade_code(self.else_stat, **cond)

        _, end_else_line = Node.assignated_array()
        Node.code_labels.append(f'{end_label},I,I,{end_else_line},0,#,')
