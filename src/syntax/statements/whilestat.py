from lexer import lang
from ..tree import Node

WHILE_COND = dict(
    canBreak=True,
    canContinue=True
)

class WhileStat(Node):
    """docstring for WhileStat."""
    def __init__(self,  exp, stats, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.stats = stats


    def process_semantic(self, **cond):
        self.exp.process_semantic()

        if self.exp.datatype != lang.SEMANTIC_LOGIC_TYPE:
            Node.raise_error(f'Condition must be of type {lang.SEMANTIC_LOGIC_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')

        Node.proccess_traversal_semantics(self.stats, **WHILE_COND)
        self.datatype = lang.SEMANTIC_VOID_TYPE
