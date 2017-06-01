from ..tree import Node

class ReadFn(Node):
    """docstring for ReadFn."""
    def __init__(self, params, token):
        super().__init__('', token)

        self.params = params or []

    def process_semantic(self, **cond):
        params_len = len(self.params)

        if params_len != 1:
                Node.raise_error(f'"lee" function takes 1 parameter, {params_len} given. Line: {self.token.line_index} - Col: {self.token.col_index}')
        param = self.params[0]

        # TODO: validate type of parameter to be an identifier

        record = param.process_semantic()

        if record and record['datatype'] == 'CONST':
            record_symbol = record['symbol']
            Node.raise_error(f'Constant {record_symbol} cannot be overrided. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        param = self.params[0]
        array, _ = Node.assignated_array()
        record = Node.symtable.get(param.symbol)
        _, line = Node.assignated_array()
        record_symbol = record['symbol']
        record_context = record['context']
        Node.array_append(array, f'{line} OPR {record_context}@${record_symbol}, 19')
