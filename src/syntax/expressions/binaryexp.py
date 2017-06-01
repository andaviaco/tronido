from lexer import lang
from ..tree import Node
from ..symtable import SymTableError

OP_CODE = {
    '+': 2,
    '-': 3,
    '*': 4,
    '/': 5,
    '%': 6,
    '^': 7,
    '<': 9,
    '>': 10,
    '<=': 11,
    '>=': 12,
    '<>': 13,
    '=': 14,
    'y': 15,
    'o': 16,
    'no': 17,
};

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

    def process_semantic(self, **cond):
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

    def generate_assign_code(self, variables):
        record = Node.symtable.get(variables.symbol)
        record_symbol = record['symbol']
        record_context = record['context']

        array, line = Node.assignated_array()
        key = f'{record_context}@${record_symbol}'

        Node.array_append(array, f'{line} STO 0, {key}')


    def generate_code(self, **cond):
        if self.op == ':=':
            self.left.generate_code(lod=False)
            self.right.generate_code()
            self.generate_assign_code(self.left)
            return

        self.left.generate_code()
        self.right.generate_code()

        array, line = Node.assignated_array()
        op_code = OP_CODE[self.op]

        op_key = f'{self.left.datatype}{self.op}{self.right.datatype}'

        if lang.SEMANTIC_VALID_OPS[op_key] == lang.SEMANTIC_STRING_TYPE:
            op_code = 22

        Node.array_append(array, f'{line} OPR 0, {op_code}')
