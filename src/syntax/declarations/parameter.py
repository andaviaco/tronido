from ..tree import Node

class Parameter(Node):
    """docstring for Parameter."""
    def __init__(self, datatype, identifier, token):
        super().__init__(None, token)

        self.datatype = datatype
        self.identifier = identifier
