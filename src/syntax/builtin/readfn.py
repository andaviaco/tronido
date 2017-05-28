from ..tree import Node

class ReadFn(Node):
    """docstring for ReadFn."""
    def __init__(self, params, token):
        super().__init__('', token)

        self.params = params or []
