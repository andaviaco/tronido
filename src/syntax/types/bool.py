from lexer import lang
from ..tree import Node

class Bool(Node):
    datatype = lang.SEMANTIC_LOGIC_TYPE

    """docstring for Bool."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

    def generate_code(self, **cond):
        array, line = Node.assignated_array()

        Node.array_append(array, f'{line} LIT {self.symbol}, 0')
