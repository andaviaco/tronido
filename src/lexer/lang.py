import string

keywords = '''
    constante
    decimal
    entero
    alfabetico
    logico
    funcion
    si
    regresa
    sino
    fin
    inicio
    para
    en
    rango
    a
    incr
    decr
    iterar
    mientras
    haz
    opcion
    caso
    procedimiento
    imprime
    imprimenl
    lee
    programa
    interrumpe
    continua
    otro
'''.split()

logic_const = ['verdadero', 'falso']

logic_operators = """
    y
    n
    o
""".split()


one_char_symbols = '''
    =
    ( )
    [ ]
    < >
    : ; . ,
'''.split()

aritmetic_chars = '+-/*%^'

two_char_symbols = '''
    <=
    >=
    <>
'''.split()

IDENTIFIER_STARTCHARS = string.ascii_letters + '_'
IDENTIFIER_CHARS = string.ascii_letters + string.digits + '_'

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + '.'

STRING_STARTCHARS = '"'
WHITESPACE_CHARS = string.whitespace

STRING = '<CteAlf>'
IDENTIFIER = '<identifier>'
KEYWORD = '<PalRes>'
DIGIT = '<CteEnt>'
LOGIC_OP = '<OpeLog>'
LOGIC_CONST = '<CteLog>'
DECIMAL = '<CteDec>'
ARITMETIC = '<OpeAri>'
WHITESPACE = '<whitespace>'
COMMENT = '<comment>'
EOF = '<eof>'
