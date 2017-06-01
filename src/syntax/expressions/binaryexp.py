from lexer import lang
from ..tree import Node
from ..symtable import SymTableError

class BinaryExp(Node):
    """docstring for BinaryExp."""
    def __init__(self, op, left, right, token):
        super().__init__(None, token)

        self.op = op
        self.left = left or Node(None, token)
        self.right = right or Node(None, token)

    def is_valid_assign(self):
        try:
            record = Node.symtable.get(self.left.symbol)

            if record['symtype'] == 'CONST':
                Node.raise_error(f'{record.symbol} constant cannot be reassigned. Line: {self.token.line_index} - Col: {self.token.col_index}')
                return False
            return True
        except SymTableError:
            return False

    def process_semantic(self):
        self.left.process_semantic()
        self.right.process_semantic()

        if self.op == ':=' and not self.is_valid_assign():
            return None

        op_key = f'{self.left.datatype}{self.op}{self.right.datatype}'

        try:
            self.datatype = lang.SEMANTIC_VALID_OPS[op_key]
        except KeyError:
            Node.raise_error(f'{op_key} is not a valid operation. Line: {self.token.line_index} - Col: {self.token.col_index}')
            self.datatype = lang.SEMANTIC_ERROR_TYPE
