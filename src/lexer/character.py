
class Character(object):
    """docstring for Character."""

    def __init__(self, value, line_index, col_index, source_index):
        super(Character, self).__init__()

        self.value = value
        self.source_index = source_index
        self.line_index = line_index
        self.col_index = col_index


    def __str__(self):
        value = self.value

        if value == ' ':
            value = '<space>'
        elif value == os.linesep:
            value = '<newline>'
        elif value == '\t':
            value = '<tab>'
        elif value == '\0':
            value = '<eof>'

        return f'{self.line_index:<3} {self.col_index:<3} {value}'
