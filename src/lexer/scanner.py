import os

from .character import Character

class Scanner(object):
    """docstring for Scanner."""
    ENDMARK = '\0'

    def __init__(self, source_text):
        super(Scanner, self).__init__()

        self.source_text = source_text
        self.last_index = len(source_text) - 1
        self.source_index = -1
        self.line_index = 0
        self.col_index = -1

    def get_next(self):
        self.source_index += 1

        if self.source_index > 0:
            if self.source_text[self.source_index-1] == os.linesep:  # the previous character was a newline
                self.line_index += 1
                self.col_index = -1

        self.col_index += 1

        if self.source_index > self.last_index: # end of source_text
            value = self.ENDMARK
        else:
            value = self.source_text[self.source_index]

        return Character(
            value,
            self.line_index,
            self.col_index,
            self.source_index
        )

    def peek_next(self):
        pass
