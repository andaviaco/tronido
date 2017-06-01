from ..tree import Node

class BreakStat(Node):
    """docstring for BreakStat."""
    def __init__(self,  token):
        super().__init__(None, token)

    def process_semantic(self, **cond):
        if not cond.get('can_break', False):
            Node.raise_error(f'Cant break outsde for|while|switch. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        break_to = cond.get('break_to', None)
        array, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMP 0, {break_to}')
