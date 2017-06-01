from lexer import lang
from ..tree import Node

class UnaryExp(Node):
    """docstring for UnaryExp."""
    def __init__(self, symbol, expr, token):
        super().__init__(None, token)
        self.symbol = symbol
        self.exp = exp or Node(None, token)

    def process_semantic(self, **cond):
        self.exp.process_semantic()

        if self.exp.datatype in [lang.SEMANTIC_INT_TYPE, lang.SEMANTIC_DECIMAL_TYPE]:
            self.datatype = self.exp.datatype
        else:
            Node.raise_error(f'Unary operator is not valid for "{self.exp.datatype}" type. Line: {self.token.line_index} - Col: {self.token.col_index}')
