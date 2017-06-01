from ..tree import Node
from ..symtable import SymTableError, GLOBAL_CONTEXT

class FunctionDef(Node):
    """docstring for FunctionDef."""
    def __init__(self, datatype, identifier, params, stats, token):
        super().__init__(None, token)

        self.datatype = datatype
        self.identifier = identifier
        self.params = params
        self.stats = stats

    def process_semantic(self, **cond):
        identifier = self.identifier.symbol
        definition_param = self.params
        params = []

        try:
            Node.symtable.set_context(identifier)
        except SymTableError:
            Node.raise_error(f'"{identifier}" Function is already defined. Line: {self.token.line_index} - Col: {self.token.col_index}')
            return

        while definition_param:
            param_datatype = definition_param.datatype.get_type()
            params.append(param_datatype)

            try:
                Node.symtable.set(
                    definition_param.identifier.symbol,
                    symtype='PARAM',
                    datatype=param_datatype,
                    bubble=False
                )
            except SymTableError:
                Node.raise_error(f'"{definition_param.identifier.symbol}" parameter is already defined. Line: {self.token.line_index} - Col: {self.token.col_index}')

            definition_param = definition_param.next

        Node.symtable.set(
            identifier,
            symtype='FUNC',
            datatype=self.datatype.get_type(),
            params=params,
            use_context=GLOBAL_CONTEXT,
            iscontext=True,
        )

        Node.proccess_traversal_semantics(self.stats)

        Node.symtable.exit_context()

    def generate_code(self, **cond):
        identifier = self.identifier.symbol
        func = Node.symtable.get(identifier)
        line = len(Node.code_funcs) + 1
        func['extras'] = {'sizes': [line, 0]}

        Node.symtable.set_record(GLOBAL_CONTEXT, identifier, func)

        params = []
        tmp_params = self.params

        while tmp_params:
            params.append(tmp_params)
            tmp_params = tmp_params.next

        for param in params[::-1]:
            param_id = param.identifier.symbol
            Node.code_funcs.append(f'{line} STO 0, {identifier}@${param_id}')
            line += 1

        Node.cascade_code(self.stats, context=identifier)
        array = 'code_funcs'
        line = len(Node.code_funcs) + 1
        op_code = 1

        if identifier == 'main':
            array = 'code_main'
            line += len(Node.code_main)
            line += len(Node.code_inits)
            op_code = 0

        Node.array_append(array, f'{line} OPR 0, {op_code}')
