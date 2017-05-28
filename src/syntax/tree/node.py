import pprint as pp

class Node(object):
    """docstring for Node."""
    def __init__(self, symbol, token):
        super().__init__()

        self.symbol = symbol
        self.token = token
        self.next = None

        if token:
            self.line_index = token.line_index
            self.col_index = token.col_index

    def __iter__(self):
        node = self

        while node:
            yield node
            node = node.next

    def __str__(self):
        rep = dict(
            name=self.__class__.__name__,
            value=self.token.value,
            type=self.token.type,
            next_node=self.next
        )
        
        return pp.pformat(rep)
