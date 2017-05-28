from ..tree import Node

class FunctionCall(Node):
    """docstring for FunctionCall."""
    def __init__(self, identifier, args, token):
        super().__init__(None, token)

        self.identifier = identifier
        self.args = args or []
