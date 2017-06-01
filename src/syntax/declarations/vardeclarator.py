from lexer import lang
from ..tree import Node
from ..symtable import SymTableError

class VarDeclarator(Node):
    """docstring for VarDeclarator."""
    def __init__(self, identifier, init, token, cond={}):
        super().__init__(None, token)
        self.identifier = identifier
        self.init = init
        self.isconstant = cond.get('isconstant', False)
        self.dimensions = cond.get('dimensions', None)
        self.dimensions_sizes = cond.get('dimensions_sizes', [])

    def process_semantic(self, **cond):
        datatype = cond.get('datatype', None)
        symbol_id = self.identifier.symbol
        isconstant = self.isconstant
        dimensions = self.dimensions
        symtype = 'CONST' if isconstant else 'VAR'

        if self.init:
            self.init.process_semantic()
            op_key = f'{datatype}:={self.init.datatype}'

            try:
                lang.SEMANTIC_VALID_OPS[op_key]
            except KeyError:
                Node.raise_error(f'{self.init.datatype} type cannot be assigned to {datatype}. Line: {self.init.token.line_index} - Col: {self.init.token.col_index}')

        try:
            Node.symtable.set(
                symbol_id,
                symtype=symtype,
                datatype=datatype,
            )
        except SymTableError as e:
            Node.raise_error(f'{symbol_id} is already defined. Line: {self.init.token.line_index} - Col: {self.init.token.col_index}')

    def generate_code(self, **cond):
        if self.init:
            key = f'{Node.symtable.current_contex}@${self.identifier.symbol}'
            self.init.generate_code()
            array, line = Node.assignated_array()
            Node.array_append(array, f'{line} STO 0, {key}')
