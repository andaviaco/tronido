from ..tree import Node

class IfStat(Node):
    """docstring for IfStat."""
    def __init__(self,  exp, stats, else_stat, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.stats = stats
        self.else_stat = else_stat
