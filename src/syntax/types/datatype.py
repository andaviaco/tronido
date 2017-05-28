from ..tree import Node

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
            return TYPES_MAP[this.symbol]
        except KeyError:
            return 'E'
