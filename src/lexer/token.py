
class Token(object):
    """docstring for Token."""

    def __init__(self, start_char):
        super(Token, self).__init__()


        self.value = start_char.value
        self.line_index = start_char.line_index
        self.col_index = start_char.col_index

        self.type = None

    def __str__(self):
        return self.show()

    def show(self, line_numbers=False):
        if line_numbers:
            res = f'{self.line_index:<4} {self.col_index:<4} {self.type:<13} {self.value}'
        else:
            res = f'{self.type} {self.value}'


        return res
