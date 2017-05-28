from ..tree import Node

class WhileStat(Node):
    """docstring for WhileStat."""
    def __init__(self,  exp, stats, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.stats = stats
