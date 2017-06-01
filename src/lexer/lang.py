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

DATA_TYPES = [
    STRING,
    INTEGER,
    DECIMAL,
    LOGIC_CONST,
]

SEMANTIC_INT_TYPE = 'I'
SEMANTIC_DECIMAL_TYPE = 'F'
SEMANTIC_STRING_TYPE = 'S'
SEMANTIC_LOGIC_TYPE = 'B'
SEMANTIC_VOID_TYPE = 'V'
SEMANTIC_ERROR_TYPE = 'E'

SEMANTIC_VALID_OPS = {
    'I:=I': 'V',
    'S:=S': 'V',
    'F:=F': 'V',
    'B:=B': 'V',
    'F:=I': 'V',
    'I:=F': 'V',
    'I+I': 'I',
    'I+F': 'F',
    'F+I': 'F',
    'F+F': 'F',
    'S+S': 'S',
    'I-I': 'I',
    'I-F': 'F',
    'F-I': 'F',
    'F-F': 'F',
    'I*I': 'I',
    'I*F': 'F',
    'F*I': 'F',
    'F*F': 'F',
    'I/I': 'F',
    'I/F': 'F',
    'F/I': 'F',
    'F/F': 'F',
    'I^I': 'I',
    'I^F': 'F',
    'F^I': 'F',
    'F^F': 'F',
    'I%%I': 'I',
    '-I': 'I',
    '-F': 'F',
    'ByB': 'B',
    'BoB': 'B',
    'noB': 'B',
    'I>I': 'B',
    'F>I': 'B',
    'I>F': 'B',
    'F>F': 'B',
    'I<I': 'B',
    'F<I': 'B',
    'I<F': 'B',
    'F<F': 'B',
    'I>=I': 'B',
    'F>=I': 'B',
    'I>=F': 'B',
    'F>=F': 'B',
    'I<=I': 'B',
    'F<=I': 'B',
    'I<=F': 'B',
    'F<=F': 'B',
    'I<>I': 'B',
    'F<>I': 'B',
    'I<>F': 'B',
    'F<>F': 'B',
    'S<>S': 'B',
    'I=I': 'B',
    'F=I': 'B',
    'I=F': 'B',
    'F=F': 'B',
    'S=S': 'B',
}
