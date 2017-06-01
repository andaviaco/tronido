from lexer import lang
from ..tree import Node

BOOL_MAP = {
    'verdadero': 'V',
    'falso': 'F',
}

class Bool(Node):
    datatype = lang.SEMANTIC_LOGIC_TYPE

    """docstring for Bool."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

    def generate_code(self, **cond):
        array, line = Node.assignated_array()

        bool_symbol = BOOL_MAP[self.symbol]
        Node.array_append(array, f'{line} LIT {bool_symbol}, 0')
