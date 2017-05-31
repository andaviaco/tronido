from ..tree import Node

DEFAULT_VALUES = dict(
    dimensions=0,
    dimensions_sizes=[],
    isconstant=False
)

class VarDeclarator(Node):
    """docstring for VarDeclarator."""
    def __init__(self, identifier, init, token, cond=DEFAULT_VALUES):
        super().__init__(None, token)
        self.identifier = identifier
        self.init = init
        self.cond = cond

    def proccess_semantic(self, **cond):
        pass
