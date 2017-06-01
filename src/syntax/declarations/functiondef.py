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
                    datatype=param_datatype
                )
            except SymTableError:
                Node.raise_error(f'"{definition_param.identifier.symbol}" parameter it\'s already defined.')

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
