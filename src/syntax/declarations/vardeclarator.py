from ..tree import Node

class VarDeclarator(Node):
    """docstring for VarDeclarator."""
    def __init__(self, identifier, init, token, cond):
        super().__init__(None, token)
        self.identifier = identifier
        self.init = init
        self.cond = cond
