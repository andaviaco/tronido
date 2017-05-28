from ..tree import Node

class UnaryExp(Node):
    """docstring for UnaryExp."""
    def __init__(self, symbol, expr, token):
        super().__init__(None, token)
        self.symbol = symbol
        self.exp = exp or Node(None, token)
