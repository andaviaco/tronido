from lexer import lang
from ..tree import Node

class String(Node):
    datatype = lang.SEMANTIC_STRING_TYPE

    """docstring for String."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

    def generate_code(self, **cond):
        array, line = Node.assignated_array()

        Node.array_append(array, f'{line} LIT {self.symbol}, 0')
