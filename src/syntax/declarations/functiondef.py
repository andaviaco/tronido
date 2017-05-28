from ..tree import Node

class FunctionDef(Node):
    """docstring for FunctionDef."""
    def __init__(self, dataType, identifier, params, stats, token):
        super().__init__(None, token)

        self.dataType = dataType
        self.identifier = identifier
        self.params = params
        self.stats = stats
