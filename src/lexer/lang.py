import string

RESERVED_TYPES = [
    'entero',
    'decimal',
    'alfabetico',
    'logico',
]

RESERVED_FUNCS = [
    'imprime',
    'imprimenl',
    'lee',
]

RESERVED_WORDS = '''
    constante
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
    programa
    interrumpe
    continua
    otro
'''.split()


logic_const = ['verdadero', 'falso']

logic_operators = """
    y
    no
    o
""".split()


one_char_symbols = '''
    =
    ( )
    [ ]
    < >
    , : ; .
'''.split()

aritmetic_chars = '+-/*%^'

two_char_symbols = '''
    :=
    <=
    >=
    <>
    //
    /*
'''.split()

keywords = RESERVED_WORDS + RESERVED_TYPES + RESERVED_FUNCS

IDENTIFIER_STARTCHARS = string.ascii_letters + '_'
IDENTIFIER_CHARS = string.ascii_letters + string.digits + '_'
COMMENT_SINGLE_LINE_START = '//'
COMMENT_SINGLE_LINE_END = '\n'
COMMENT_MULTI_LINE_START = '/*'
COMMENT_MULTI_LINE_END = '*/'

NUMBER_STARTCHARS = string.digits
NUMBER_CHARS = string.digits + '.'

STRING_STARTCHARS = '"'
WHITESPACE_CHARS = string.whitespace

STRING = '<CteAlf>'
IDENTIFIER = '<identifier>'
KEYWORD = '<PalRes>'
INTEGER = '<CteEnt>'
LOGIC_OP = '<OpeLog>'
LOGIC_CONST = '<CteLog>'
DECIMAL = '<CteDec>'
ARITMETIC = '<OpeAri>'
WHITESPACE = '<whitespace>'
COMMENT = '<comment>'
EOF = '<eof>'
RELATIONAL_OP = '<OpeRel>'
DELIMIT = '<Delimi>'
ASSING_OP = '<OpeAsi>'
