# from lexer.scanner import Scanner
from lexer.lexer import Lexer

if __name__ == '__main__':
    # scanner = Scanner('holas a todos\nsipi')
    lexer = Lexer("""
decimal xoy=35.5
entero m = 3
logico true = verdadero
x y m
imprime(1+2)
a="sipi"
    """)

    for token in lexer:
    # for (char, char_ahead) in scanner:
        print(token.show(True))
        # print('CURRENT', char)
        # print('AHEAD  ', char_ahead)
