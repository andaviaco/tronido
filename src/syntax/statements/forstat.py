from ..tree import Node

class ForStat(Node):
    """docstring for ForStat."""
    def __init__(self, initializer, condition, step, stats, token):
        super().__init__(None, token)

        self.initializer = initializer or Node(None, token)
        self.condition = condition or Node(None, token)
        self.step = step or Node(None, token)
        self.stats = stats
