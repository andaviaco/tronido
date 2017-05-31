from ..tree import Node

ERROR_TYPE = 'E'

TYPES_MAP = {
    'entero': 'I',
    'decimal': 'D',
    'alfabetico': 'S',
    'logico': 'B',
    'void': 'V',
}

class DataType(Node):
    """docstring for DataType."""

    def get_type(self):
        try:
            return TYPES_MAP[self.symbol]
        except KeyError:
            return ERROR_TYPE
