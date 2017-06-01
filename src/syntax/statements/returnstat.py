from lexer import lang
from ..tree import Node
from ..symtable import GLOBAL_CONTEXT

class ReturnStat(Node):
    """docstring for ReturnStat."""
    def __init__(self,  exp, token):
        super().__init__(None, token)

        self.exp = exp or None

    def process_semantic(self, **cond):
        exp_type = lang.SEMANTIC_VOID_TYPE

        if self.exp:
            self.exp.process_semantic()
            exp_type = self.exp.datatype

        parent_context = Node.symtable.current_contex
        self.parent_context = parent_context

        if parent_context != GLOBAL_CONTEXT:
            parent_func = Node.symtable.get(parent_context)
            parent_datatype = parent_func['datatype']
            op_key = f'{parent_datatype}:={exp_type}'

            if not op_key in lang.SEMANTIC_VALID_OPS:
                Node.raise_error(f'Return value must be of type {parent_datatype}. Got type {exp_type}. Line: {self.token.line_index} - Col: {self.token.col_index}')
        else:
            Node.raise_error(f'Return statement outside a function. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        array, line = Node.assignated_array()

        if self.exp:
            self.exp.generate_code()
            _, line = Node.assignated_array()
            Node.array_append(array, f'{line} STO 0, {GLOBAL_CONTEXT}@${self.parent_context}')

        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} OPR 0, 1')
