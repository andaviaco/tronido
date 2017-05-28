from ..tree import Node

class ReturnStat(Node):
    """docstring for ReturnStat."""
    def __init__(self,  exp, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
