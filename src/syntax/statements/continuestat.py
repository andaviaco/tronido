from ..tree import Node

class ContinueStat(Node):
    """docstring for ContinueStat."""
    def __init__(self,  token):
        super().__init__(None, token)

    def process_semantic(self, **cond):
        if not cond.get('can_continue', False):
            Node.raise_error(f'Cant "continue" outside for|while. Line: {self.token.line_index} - Col: {self.token.col_index}')

    def generate_code(self, **cond):
        continue_to = cond.get('continue_to', None)

        array, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMP 0, {continue_to}')
