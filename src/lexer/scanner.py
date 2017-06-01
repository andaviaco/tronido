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
        self.line_index = 1
        self.col_index = 0


    def __iter__(self):
        while True:
            char = self.get_next()
            char_ahead = self.peek_next();

            yield (char, char_ahead)

            if char.value is self.ENDMARK or char_ahead.value is None:
                raise StopIteration



    def get_next(self):
        self.source_index += 1

        if self.source_index > 0 and self.source_index-1 < len(self.source_text):
            if self.source_text[self.source_index-1] == os.linesep:  # the previous character was a newline
                self.line_index += 1
                self.col_index = 0

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
        source_index = self.source_index
        line_index = self.line_index
        col_index = self.col_index
        value = None

        source_index += 1

        if source_index > 0 and source_index-1 < len(self.source_text):
            if self.source_text[source_index-1] == os.linesep:  # the previous character was a newline
                line_index += 1
                col_index = 0

            col_index += 1

            if source_index > self.last_index: # end of source_text
                value = self.ENDMARK
            else:
                value = self.source_text[source_index]
        else:
            line_index = -1
            col_index = 0
            source_index = -1

        return Character(
            value,
            line_index,
            col_index,
            source_index
        )

    def lookahead(self, offset=1):
        index = self.source_index + offset

        if index > self.last_index:
            return self.ENDMARK

        return self.source_text[index]
