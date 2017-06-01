from ..tree import Node

class Declaration(Node):
    """docstring for Declaration."""
    def __init__(self, datatype, declarator, token):
        super().__init__(None, token)

        self.datatype = datatype
        self.declarator = declarator

    def process_semantic(self, **cond):
        datatype = self.datatype.get_type()

        Node.proccess_traversal_semantics(self.declarator, datatype=datatype)
