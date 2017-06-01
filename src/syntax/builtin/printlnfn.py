from ..tree import Node

class PrintlnFn(Node):
    """docstring for PrintlnFn."""
    def __init__(self, params, token):
        super().__init__('', token)

        self.params = params or []

    def process_semantic(self, **cond):
        if self.params:
            for param in self.params:
                param.process_semantic()
        else:
            Node.raise_error(f'"imprime" function requires at least 1 parameter. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        array, line = Node.assignated_array()
        for i, param in enumerate(self.params):
            param.generate_code()
            _, line = Node.assignated_array()
            op_code = 21 if  len(self.params) - 1 == i else 20
            Node.array_append(array, f'{line} OPR 0, {op_code}')
