from ..tree import Node

class PrintFn(Node):
    """docstring for PrintFn."""
    def __init__(self, params, token):
        super().__init__('', token)

        self.params = params or []
