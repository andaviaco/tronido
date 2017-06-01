from ..tree import Node

class CaseStat(Node):
    """docstring for CaseStat."""
    def __init__(self,  cond, stats, token):
        super().__init__(None, token)

        self.cond = cond
        self.stats = stats

    def process_semantic(self, **cond):
        is_switch = cond.get('is_switch')
        datatype = cond.get('datatype')

        if not is_switch:
            Node.raise_error(f'Case ouside switch statement. Line: {self.token.line_index} - Col: {self.token.col_index}')


        if self.cond:
            self.cond.process_semantic()

            if datatype != self.cond.datatype:
                Node.raise_error(f'Cannot compare {datatype} with { self.cond.datatype}. Line: {self.token.line_index} - Col: {self.token.col_index}')

            Node.proccess_traversal_semantics(self.stats, **cond)
