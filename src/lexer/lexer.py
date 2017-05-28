import warnings

from . import lang
from .scanner import Scanner
from .token import Token

class LexerError(Warning):
    pass


class Lexer(object):
    offsetstack = []

    """docstring for Lexer."""
    def __init__(self, source_text):
        super(Lexer, self).__init__()

        self.source_text = source_text
        self.scanner = Scanner(source_text)

    def __iter__(self):
        while True:
            token, token_ahead = self.get_token()

            if token.value is self.scanner.ENDMARK or token_ahead.value is None:
                token.type = lang.EOF
                yield token
                raise StopIteration


            composed = token.value + token_ahead.value

            if composed in lang.two_char_symbols:
                token.value = composed

                if composed in lang.COMMENT_SINGLE_LINE_START:
                    while True:
                        token_next, _ = self.get_token()

                        if token_next.value in lang.COMMENT_SINGLE_LINE_END:
                            break

                    continue

                if composed in lang.COMMENT_MULTI_LINE_START:
                    while True:
                        token_next, ahead = self.get_token()
                        composed_next = token_next.value + ahead.value

                        if token_next.value is self.scanner.ENDMARK or ahead.value is self.scanner.ENDMARK:
                            warnings.warn('Unexpected End Of File before end of comment', LexerError)

                        if composed_next in lang.COMMENT_MULTI_LINE_END:
                            token_next, _ = self.get_token()
                            break

                    continue


                if composed in '<= >= <>':
                    token.type = lang.RELATIONAL_OP

                if composed == ':=':
                    token.type = lang.ASSING_OP

                    self.get_token()

                yield token

            if token.value in lang.one_char_symbols:
                if token.value in '< = >':
                    token.type = lang.RELATIONAL_OP
                else:
                    token.type = lang.DELIMIT

                yield token


            if token.value in lang.IDENTIFIER_STARTCHARS:
                token.type = lang.IDENTIFIER

                if token_ahead.value in lang.IDENTIFIER_CHARS:
                    while True:
                        token_next, ahead = self.get_token()
                        token.value += token_next.value

                        if not ahead.value in lang.IDENTIFIER_CHARS:
                            break

                if token.value in lang.keywords:
                    token.type = lang.KEYWORD
                elif token.value in lang.logic_const:
                    token.type = lang.LOGIC_CONST
                elif token.value in lang.logic_operators:
                    token.type = lang.LOGIC_OP

                yield token


            if token.value in lang.NUMBER_STARTCHARS:
                token.type = lang.INTEGER
                has_digit_mark = False

                if token_ahead.value in lang.NUMBER_CHARS:
                    token_next, lookahead = self.get_token()

                    while token_next.value in lang.NUMBER_CHARS:
                        if token_next.value == '.':
                            if not has_digit_mark:
                                token.type = lang.DECIMAL
                            else:
                                yield token

                        token.value += token_next.value

                        if lookahead.value not in lang.NUMBER_CHARS:
                            break

                        token_next, lookahead = self.get_token()

                yield token

            if token.value in lang.STRING_STARTCHARS:
                while True:
                    token_next, _ = self.get_token()

                    if token_next.value is self.scanner.ENDMARK:
                        warnings.warn('Unexpected End Of File before end of string', LexerError)

                    if token_next.value is lang.STRING_STARTCHARS:
                        break

                    token.value += token_next.value

                token.value += token_next.value
                token.type = lang.STRING

                yield token

            if token.value in lang.aritmetic_chars:
                token.type = lang.ARITMETIC
                yield token

            if token.type is self.scanner.ENDMARK or token_ahead.value is None:
                raise StopIteration

    def next_token(self):
        if self.offsetstack:
            return self.offsetstack.pop()

        return next(iter(self))

    def get_token(self):
        char1, char2 = next(iter(self.scanner))

        token_1 = Token(char1)
        token_2 = Token(char2)

        return (token_1, token_2)

    def lookahead(self):
        token = next(iter(self))

        self.offsetstack.append(token)

        return token

    def abort(self):
        pass
