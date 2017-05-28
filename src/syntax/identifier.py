import pprint as pp

from .tree import Node

class Identifier(Node):
    """docstring for Identifier."""
    def __init__(self, symbol, token):
        super().__init__(symbol, token)

        self.array_values = {
            'dimensions': 0,
            'expressions': [],
        }

    def __str__(self):
        rep = dict(
            name=self.__class__.__name__,
            value=self.token.value,
            type=self.token.type,
            array_values=self.array_values,
            next_node=self.next
        )

        return pp.pformat(rep)
