from lexer import lang
from ..tree import Node

class Parameter(Node):
    """docstring for Parameter."""
    def __init__(self, datatype, identifier, token):
        super().__init__(None, token)

        self.datatype = datatype
        self.identifier = identifier

    def process_semantic(self):
        datatype = self.datatype.get_type()

        if datatype == lang.SEMANTIC_ERROR_TYPE:
            Node.raise_error(f'"{self.datatype}" is not a valid parameter type. Line: {self.token.line_index} - Col: {self.token.col_index}')
