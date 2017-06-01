from lexer import lang
from ..tree import Node

ERROR_TYPE = lang.SEMANTIC_ERROR_TYPE

TYPES_MAP = {
    'entero': lang.SEMANTIC_INT_TYPE,
    'decimal': lang.SEMANTIC_DECIMAL_TYPE,
    'alfabetico': lang.SEMANTIC_STRING_TYPE,
    'logico': lang.SEMANTIC_LOGIC_TYPE,
    'void': lang.SEMANTIC_VOID_TYPE,
}

class DataType(Node):
    """docstring for DataType."""

    def get_type(self):
        try:
            return TYPES_MAP[self.symbol]
        except KeyError:
            return ERROR_TYPE
