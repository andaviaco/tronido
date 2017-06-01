import pprint as pp

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

    def process_semantic(self):
        try:
            record = Node.symtable.get(self.symbol)
        except SymTableError:
            Node.raise_error(f'"{self.symbol}" is not defined. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return None

        symtype = record['symtype']
        if not symtype in ['PARAM', 'CONST', 'VAR']:
            Node.raise_error(f'"{symtype}" is a function. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return None

        self.datatype = record['datatype']

        return record
