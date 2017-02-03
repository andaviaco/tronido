from lexer.scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner('holas a todos\nsipi')

    for char in scanner:
        print(char)
