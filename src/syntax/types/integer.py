from lexer import lang
from ..tree import Node

class Integer(Node):
    datatype = lang.SEMANTIC_DECIMAL_TYPE

    """docstring for Integer."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)
