from lexer import lang
from ..tree import Node

class Bool(Node):
    datatype = lang.SEMANTIC_LOGIC_TYPE

    """docstring for Bool."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)
