from ..tree import Node

class BinaryExp(Node):
    """docstring for BinaryExp."""
    def __init__(self, op, left, right, token):
        super().__init__(None, token)

        self.op = op
        self.left = left or Node(None, token)
        self.right = right or Node(None, token)
