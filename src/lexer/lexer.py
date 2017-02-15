
from . import lang
from .scanner import Scanner
from .token import Token

class LexerError(Exception):
    pass


class Lexer(object):
    """docstring for Lexer."""
    def __init__(self, source_text):
        super(Lexer, self).__init__()

        self.source_text = source_text
        self.scanner = Scanner(source_text)

    def __iter__(self):
        while True:
            token, token_ahead = self.get_token()

            if token.value == self.scanner.ENDMARK:
                token.type = lang.EOF
                yield token

            if token.value in lang.IDENTIFIER_STARTCHARS:
                token.type = lang.IDENTIFIER

                token_next, x = self.get_token()
                while token_next.value in lang.IDENTIFIER_CHARS:
                    token.value += token_next.value
                    token_next, x = self.get_token()

                if token.value in lang.keywords:
                    token.type = lang.KEYWORD
                elif token.value in lang.logic_const:
                    token.type = lang.LOGIC_CONST
                elif token.value in lang.logic_operators:
                    token.type = lang.LOGIC_OP

                yield token


            if token.value in lang.NUMBER_STARTCHARS:
                token.type = lang.DIGIT
                has_digit_mark = False

                token_next, x = self.get_token()

                while token_next.value in lang.NUMBER_CHARS:
                    if token_next.value == '.':
                        if not has_digit_mark:
                            token.type = lang.DECIMAL
                        else:
                            yield token

                    token.value += token_next.value
                    token_next, x = self.get_token()

                yield token

            if token.value in lang.STRING_STARTCHARS:
                token_next, x = self.get_token()

                while token_next.value != lang.STRING_STARTCHARS:
                    if token_next.value == self.scanner.ENDMARK:
                        raise LexerError

                    token.value += token_next.value
                    token_next, x = self.get_token()

                token.value += token_next.value
                token.type = lang.STRING

                yield token

            # TODO: no funca
            if token.value in lang.aritmetic_chars:
                token.type = ARITMETIC
                yield token



            # print('TOOOOOOKEN 1', type(token.value), token.value)
            # if token_ahead.value is None:
            #     raise StopIteration
            # print('SALE')
            # yield token
            # print('ENTRA')

            # print('TOOOOOOKEN 2', type(token.value), token.value)
            if token.type is self.scanner.ENDMARK or token_ahead.value is None:
                # print('BREEEEAK')
                raise StopIteration



    def abort(self):
        pass

    def get_token(self):
        char1, char2 = next(iter(self.scanner))

        token_1 = Token(char1)
        token_2 = Token(char2)

        return (token_1, token_2)
