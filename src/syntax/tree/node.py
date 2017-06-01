import warnings
import pprint as pp

from lexer import lang
from ..symtable import SymTable, GLOBAL_CONTEXT

class SemanticError(Warning):
    pass


class Node(object):
    symtable = SymTable()
    datatype = lang.SEMANTIC_ERROR_TYPE

    """docstring for Node."""
    def __init__(self, symbol, token):
        super().__init__()

        self.symbol = symbol
        self.token = token
        self.next = None

        if token:
            self.line_index = token.line_index
            self.col_index = token.col_index

    def __iter__(self):
        node = self

        while node:
            yield node
            node = node.next

    def __str__(self):
        rep = dict(
            name=self.__class__.__name__,
            value=self.token.value,
            type=self.token.type,
            next_node=self.next
        )

        return pp.pformat(rep)


    @staticmethod
    def raise_error(msg):
        warnings.warn(msg, SemanticError)

    @staticmethod
    def process_semantic(**cond):
        pass

    @staticmethod
    def proccess_traversal_semantics(node, **cond):
        cond_context = cond.get('context', None)

        if cond.get('context', None):
            Node.symtable.set_context(cond_context)

        while node:
            node.process_semantic(**cond)
            node = node.next
        #
        # if Node.symtable.current_contex != GLOBAL_CONTEXT:
        #     Node.symtable.exit_context()
