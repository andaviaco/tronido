from ..tree import Node

class PrintlnFn(Node):
    """docstring for PrintlnFn."""
    def __init__(self, params, token):
        super().__init__('', token)

        self.params = params or []
