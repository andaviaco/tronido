from lexer import lang
from ..tree import Node
from ..symtable import SymTableError

class FunctionCall(Node):
    """docstring for FunctionCall."""
    def __init__(self, identifier, args, token):
        super().__init__(None, token)

        self.identifier = identifier
        self.args = args or []

    def process_args(self, func_def, args):
        params = func_def['params']
        identifier = func_def['symbol']
        args_len = len(args)
        params_len = len(params)

        if args_len != params_len:
            Node.raise_error(f'{identifier} takes {params_len} parameter(s). {args_len} given. Line: {self.token.line_index} - Col: {self.token.col_index}')

        for param, arg in zip(params, args):
            arg.process_semantic()

            if arg.datatype != param:
                Node.raise_error(f'{identifier} expected {param}, got {arg.datatype}. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def process_semantic(self, **cond):
        identifier = self.identifier.symbol

        try:
            func_def = Node.symtable.get(identifier)
        except SymTableError:
            Node.raise_error(f'{identifier} is not defined. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return None

        if func_def['symtype'] == 'FUNC':
            self.process_args(func_def, self.args)
            self.datatype = func_def['datatype']
        else:
            Node.raise_error(f'{identifier} is not a function. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        return_label = Node.get_unique_label('return')
        array, _ = Node.assignated_array()
        func_def = Node.symtable.get(self.identifier.symbol)

        _, line = Node.assignated_array()

        Node.array_append(array, f'{line} LOD {return_label}, 0')

        for arg in self.args:
            arg.generate_code()

        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} CAL g@${self.identifier.symbol}, 0')

        line += 1

        if func_def['datatype'] != 'V':
            Node.array_append(array, f'{line} LOD g@${self.identifier.symbol}, 0')

        Node.code_labels.append(f'{return_label},I,I,{line},0,#,')
