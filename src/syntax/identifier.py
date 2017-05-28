from .tree import Node

class Identifier(Node):
    """docstring for Identifier."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

        self.array_values = {
            'dimensions': 0,
            'expressions': [],
        }
