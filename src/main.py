from lexer.scanner import Scanner

if __name__ == '__main__':
    scanner = Scanner('holas a todos\nsipi')

    char = scanner.get_next()

    while char.value != scanner.ENDMARK:
        char = scanner.get_next()
        print(char)
