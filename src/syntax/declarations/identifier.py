import pprint as pp

from lexer import lang
from ..tree import Node
from ..symtable import SymTableError

class Identifier(Node):
    """docstring for Identifier."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

        self.array_values = {
            'dimensions': 0,
            'expressions': [],
        }

    def __str__(self):
        rep = dict(
            name=self.__class__.__name__,
            value=self.token.value,
            type=self.token.type,
            array_values=self.array_values,
            next_node=self.next
        )

        return pp.pformat(rep)

    def process_semantic(self, **cond):
        try:
            record = Node.symtable.get(self.symbol)
        except SymTableError:
            Node.raise_error(f'"{self.symbol}" is not defined. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return None

        symtype = record['symtype']
        if not symtype in ['PARAM', 'CONST', 'VAR']:
            Node.raise_error(f'"{symtype}" is a function. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return None

        if self.array_values['dimensions']:
            for expresion in self.array_values['expressions']:
                expresion.process_semantic()

                if expresion.datatype != lang.SEMANTIC_INT_TYPE:
                    Node.raise_error(f'Index must be of type {lang.SEMANTIC_INT_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')

        access_dimensions = self.array_values['dimensions']
        record_demensions = record['dimensions']

        if access_dimensions and not record_demensions:
            Node.raise_error(f'{self.symbol} is not an array. Line: {self.token.line_index} - Col: {self.token.col_index}')
        elif access_dimensions != record_demensions:
            Node.raise_error(f'{self.symbol} takes {record_demensions} dimensions. Line: {self.token.line_index} - Col: {self.token.col_index}')

        self.datatype = record['datatype']

        return record

    def generate_code(self, **cond):
        record = Node.symtable.get(self.symbol)
        record_symbol = record['symbol']
        record_context = record['context']

        for acces_exp in self.array_values['expressions']:
            acces_exp.generate_code()

        array, line = Node.assignated_array()
        if cond.get('lod', True):
            lod_code = f'{line} LOD {record_context}@${record_symbol}, 0'
            Node.array_append(array, lod_code)
