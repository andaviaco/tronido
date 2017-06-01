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
                Node.raise_error(f'{self.init.datatype} type cannot be assigned to {datatype}. Line: {self.token.line_index} - Col: {self.token.col_index}')

        sizes = []
        if dimensions:
            for dimension in self.dimensions_sizes:
                dimension_datatype = lang.SEMANTIC_ERROR_TYPE

                if dimension:
                    dimension.process_semantic()
                    dimension_datatype = dimension.datatype

                if dimension_datatype != lang.SEMANTIC_INT_TYPE:
                    Node.raise_error(f'Vector dimensions must be of type {lang.SEMANTIC_INT_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')
                    return

                dimension_size = dimension.symbol
                if not dimension_size.isdigit():
                    record = Node.symtable.get(dimension.symbol)
                    dimension_size = record['value']

                sizes.append(dimension_size)

        if isconstant:
            record_value = self.init.symbol
        else:
            record_value = None

        try:
            Node.symtable.set(
                symbol_id,
                symtype=symtype,
                datatype=datatype,
                value=record_value,
                dimensions=self.dimensions,
                sizes=sizes
            )
        except SymTableError as e:
            Node.raise_error(f'{symbol_id} is already defined. Line: {self.init.token.line_index} - Col: {self.init.token.col_index}')

    def generate_code(self, **cond):
        if not self.init:
            return None
            
        key = f'{Node.symtable.current_contex}@${self.identifier.symbol}'
        self.init.generate_code()
        array, line = Node.assignated_array()
        Node.array_append(array, f'{line} STO 0, {key}')
