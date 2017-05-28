import warnings

from lexer import lang

from .types import DataType
from .types import Integer
from .types import Decimal
from .types import String
from .types import Bool

from .declarations import Declaration
from .declarations import VarDeclarator
from .declarations import Identifier
from .declarations import FunctionDef
from .declarations import Parameter

from .statements import IfStat

from .expressions import UnaryExp
from .expressions import BinaryExp

from . import builtin


RESERVED_FUNCS_MAP = {
    'imprime': builtin.PrintFn,
    'imprimenl': None,
    'lee':  None,
}

def basic_expression(child_exp):
    def decorator(func):
        def wrapper(instance):
            try:
                exp_method = getattr(instance, child_exp)
            except AttributeError:
                raise NotImplementedError(f'Class `{instance.__class__.__name__}` does not implement "{child_exp}"')

            exp = exp_method()

            while instance.current_token.contains(func(instance)):
                symbol_token = instance.current_token
                instance.match(func(instance))

                exp = BinaryExp(symbol_token.value, exp, exp_method(), symbol_token)

            return exp
        return wrapper
    return decorator

class SyntaxError(Warning):
    pass

class Syntax(object):
    """docstring for Syntax."""
    def __init__(self, lexer):
        super().__init__()
        self.lexer = lexer

    def parse(self):
        self.current_token = self.lexer.next_token()

        tree = self.external_declaration()

        self.match_type(lang.EOF)

        return tree

    def _raise_expected(self, expected):
        warnings.warn(f'Expected {expected} but got {self.current_token.value}. Line: {self.current_token.line_index} - Col: {self.current_token.col_index}', SyntaxError)

    def _match_assing(self, value, expected):
        if value in expected:
            self.current_token = self.lexer.next_token()
            return True

        self._raise_expected(expected)

    def match_type(self, value):
        return self._match_assing(self.current_token.type, value)

    def match_value(self, value):
        return self._match_assing(self.current_token.value, value)

    def match(self, value):
        if self.current_token.contains(value):
            self.current_token = self.lexer.next_token()
            return True

        self._raise_expected(expected)

    def external_declaration(self):
        node = None
        token = self.current_token;

        if token.value == 'programa':
            datatype = DataType('void', token)
            identifier = Identifier('main', token)

            self.match_value('programa')

            node = self.compound_stat(ismain=True)

            return FunctionDef(datatype, identifier, None, node, token)

        if token.value == 'constante':
            self.match_type(lang.KEYWORD)
            declaration_type = self.type_def()
            node = self.constant_declaration(declaration_type)

        elif token.value == 'procedimiento':
            self.match_type(lang.KEYWORD)
            datatype = DataType('void', token)
            node = self.declaration(datatype, isfunc=True)

        elif token.value in lang.RESERVED_TYPES:
            datatype = self.type_def()
            isfunc = False

            if self.current_token.value == 'funcion':
                isfunc = True
                self.match_value('funcion')

            node = self.declaration(datatype, isfunc=isfunc)

        else:
            self._raise_expected('|'.join(lang.RESERVED_TYPES + ['constante']))

            self.current_token = self.lexer.next_token()

            return self.external_declaration()

        if node:
            node.next = self.external_declaration();

        return node

    def type_def(self):
        node = DataType(self.current_token.value, self.current_token)

        self.match_value(lang.RESERVED_TYPES)

        return node

    def constant_declaration(self, declaration_type):
        cond = {
            'isconstant': True,
            'dimensions': 0,
            'dimensionsSizes': []
        }

        stat_token = self.current_token
        identifier = Identifier(self.current_token.value, stat_token)

        self.match_type(lang.IDENTIFIER)
        assign_token = self.current_token
        self.match_type(lang.ASSING_OP)

        init = self.unary_exp(isconstant=True)
        statement = VarDeclarator(identifier, init, assign_token, cond)
        self.match_value(';')

        return Declaration(declaration_type, statement, stat_token)

    def declaration(self, declaration_type, **cond):
        if not cond.get('isfunc', False):
            declaration_token = self.current_token
            declaration = self.declarator_list()

            self.match_value(';')

            return Declaration(declaration_type, declaration, declaration_token)

        return self.function_def(declaration_type)

    def declarator_list(self):
        node = self.declarator()

        if self.current_token.value == ',':
            self.match_value(',')
            node.next = self.declarator_list()

        return node

    def declarator(self):
        id_token = self.current_token
        identifier = Identifier(id_token.value, id_token)

        self.match_type(lang.IDENTIFIER)

        array_def = self.array_def()
        init = None

        if self.current_token.type == lang.ASSING_OP:
            if array_def['dimensions']:
                self._raise_expected(';')

            self.match_type(lang.ASSING_OP)
            init = self.logical_or_exp()

        return VarDeclarator(identifier, init, id_token, array_def)

    def function_def(self, type_def):
        func_token = self.current_token
        identifier = Identifier(func_token.value, func_token)

        self.match_type(lang.IDENTIFIER)

        self.match_value('(')
        args = self.parameter_list()
        self.match_value(')')

        variables = None
        declaration = None
        if self.current_token.value != 'inicio':
            var_type = self.type_def()
            declaration = variables = self.declaration(var_type)

            while self.current_token.value != 'inicio':
                if declaration:
                    var_type = self.type_def()
                    declaration = declaration.next = self.declaration(var_type)


        if self.current_token.value == 'inicio':
            statement = self.compound_stat()

            if declaration:
                declaration.next = statement
                statement = variables

            return FunctionDef(type_def, identifier, args, statement, func_token)

        self._raise_expected('function|procedure body')
        return None

    def array_def(self):
        dimensions_sizes = []

        while self.current_token.value == '[':
            self.match_value('[')

            if self.current_token.type in [lang.INTEGER, lang.IDENTIFIER]:
                dimensions_sizes.append(self.primary_exp())
            else:
                self._raise_expected('enetro|constante')

            self.match_value(']')

        return dict(
            dimensions_sizes=dimensions_sizes,
            dimensions=len(dimensions_sizes)
        )

    def array_exp(self):
        expressions = []

        while self.current_token.value == '[':
            self.match_value('[')
            expressions.append(self.logical_or_exp())
            self.match_value(']')

        return dict(expressions=expressions, dimensions=len(expressions))

    def parameter_list(self):
        if self.current_token.value in lang.RESERVED_TYPES:
            arg_token = self.current_token
            type_def = self.type_def()
            identifier = Identifier(self.current_token.value, self.current_token)

            self.match_type(lang.IDENTIFIER)

            node = aux = Parameter(type_def, identifier, arg_token)

            while self.current_token.value == ',':
                self.match_value(',')

                arg_token = self.current_token
                type_def = self.type_def()
                identifier = Identifier(self.current_token.value, self.current_token)

                self.match_type(lang.IDENTIFIER)

                aux = aux.next = Parameter(type_def, identifier, arg_token)

        return None

    def compound_stat(self, **cond):
        self.match_value('inicio')
        node = self.stat_list()
        self.match_value('fin')

        if cond.get('ismain', False):
            self.match_value('programa')
            self.match_value('.')
        else:
            self.match_value(';')

        return node

    def stat_list(self):
        keywords_subset = [
            'iterar',
            'para',
            'regresa',
            'haz',
            'continua',
            'interrumpe',
            'caso',
            'otro',
        ]

        node = None
        token = self.current_token

        if (token.type == lang.IDENTIFIER or
            token.value in keywords_subset or
            token.value in lang.RESERVED_FUNCS):

            node = self.statement()

            if node:
                node.next = self.stat_list()

        return node

    def statement(self):
        STATS_MAP = {
            'si': self.if_statement,
            'iterar': self.while_statement,
            'para': self.for_statement,
            'continua': self.continue_statement,
            'haz': self.swich_statment,
            'caso': self.case_statement,
            'otro': self.defaultcase_statement,
            'interrumpe': self.break_statement,
            'regresa': self.return_statement,
            'inicio': self.start_statement,
        }

        try:
            return STATS_MAP[self.current_token.value]()
        except KeyError:
            node = self.assignment_expression()

            self.match_value(';')

            return node

    def if_statement(self):
        if_token = self.current_token

        self.match_value('si')
        self.match_value('(')
        exp = self.logical_or_exp()
        self.match_value(')')

        stat = self.statement()
        else_stat = self.else_statement()

        return IfStat(exp, stat, else_stat, if_token)

    def while_statement(self):
        pass

    def for_statement(self):
        pass

    def continue_statement(self):
        pass

    def swich_statment(self):
        pass

    def case_statement(self):
        pass

    def defaultcase_statement(self):
        pass

    def break_statement(self):
        pass

    def return_statement(self):
        pass

    def start_statement(self):
        return self.compound_stat()

    def else_statement(self):
        pass

    def primary_exp(self, **cond):
        isconstant = cond.get('isconstant', False)

        if self.current_token.type == lang.IDENTIFIER and not isconstant:
            identifier = Identifier(self.current_token.value, self.current_token)

            self.match_type(lang.IDENTIFIER)

            return self.function_call(identifier)

        elif self.current_token.value in lang.RESERVED_FUNCS and not isconstant:
            return self.reserved_function_call()

        elif self.current_token.type == lang.INTEGER:
            exp = Integer(self.current_token.value, self.current_token)
            self.match_type(lang.INTEGER)

        elif self.current_token.type == lang.DECIMAL:
            exp = Decimal(self.current_token.value, self.current_token)
            self.match_type(lang.DECIMAL)

        elif self.current_token.type == lang.STRING:
            exp = String(self.current_token.value, self.current_token)
            self.match_type(lang.STRING)

        elif self.current_token.type == lang.LOGIC_CONST:
            exp = Bool(self.current_token.value, self.current_token)
            self.match_type(lang.LOGIC_CONST)

        elif self.current_token.value == '(' and not isconstant:
            self.match_value('(')
            exp = self.logical_or_exp()
            self.match_value(')')
        else:
            self._raise_expected('Expression')

        return exp

    def assignment_expression(self):
        token_ahead = self.lexer.lookahead()


        if self.current_token.contains(lang.IDENTIFIER):
            identifier = Identifier(self.current_token.value, self.current_token)

        if token_ahead.contains(lang.ASSING_OP):
            self.match_type(lang.IDENTIFIER)
        elif token_ahead.contains('['):
            identifier.array_values = self.array_exp()
            self.match_type(lang.IDENTIFIER)

        if self.current_token.contains(lang.ASSING_OP):
            symbol_token = self.current_token
            self.match_type(lang.ASSING_OP)
            exp = self.logical_or_exp()

            return BinaryExp(symbol_token.value, identifier, exp, symbol_token)

        return self.logical_or_exp()

    def logical_or_exp(self):
        exp = self.logical_and_exp()

        while self.current_token.value == 'o':
            symbol_token = self.current_token
            self.match_value('o')

            exp = BinaryExp(symbol_token.value, exp, self.logical_and_exp(), symbol_token)

        return exp

    def logical_and_exp(self):
        exp = self.equality_exp()

        while self.current_token.value == 'y':
            symbol_token = self.current_token
            self.match_value('y')

            exp = BinaryExp(symbol_token.value, exp, self.equality_exp(), symbol_token)

        return exp

    def equality_exp(self):
        exp = self.relational_exp()

        while self.current_token.value == '=':
            symbol_token = self.current_token
            self.match_value('=')

            exp = BinaryExp(symbol_token.value, exp, self.relational_exp(), symbol_token)

        return exp

    def relational_exp(self):
        exp = self.additive_exp()

        while self.current_token.type == lang.RELATIONAL_OP:
            symbol_token = self.current_token
            self.match_type(RELATIONAL_OP)

            exp = BinaryExp(symbol_token.value, exp, self.additive_exp(), symbol_token)
        return exp

    @basic_expression('multiplicative_exp')
    def additive_exp(self):
        return ['+', '-']
        # exp = self.multiplicative_exp()
        #
        # while self.current_token.value in ['+', '-']:
        #     symbol_token = self.current_token
        #     self.match_value(self.current_token.value)
        #
        #     exp = BinaryExp(symbol_token.value, exp, self.multiplicative_exp(), symbol_token)
        # return exp

    @basic_expression('pow_exp')
    def multiplicative_exp(self):
        return ['*', '/', '%']
        # exp = self.pow_exp()
        #
        # while self.current_token.value in ['*', '/', '%']:
        #     symbol_token = self.current_token
        #     self.match_value(self.current_token.value)
        #
        #     exp = BinaryExp(symbol_token.value, exp, self.pow_exp(), symbol_token)
        # return exp

    @basic_expression('unary_exp')
    def pow_exp(self):
        return '^'
        # exp = self.unary_exp()
        #
        # while self.current_token.value == '^':
        #     symbol_token = self.current_token
        #     self.match_value(self.current_token.value)
        #
        #     exp = BinaryExp(symbol_token.value, exp, self.unary_exp(), symbol_token)
        # return exp

    def unary_exp(self, **cond):
        if self.current_token.value == '+' or self.current_token == '-':
            token_symbol = self.current_token
            self.match_value(token_symbol.value)

            return UnaryExp(token_symbol.value, self.unary_exp(**cond), token_symbol)

        return self.primary_exp(**cond)

    def function_call(self, identifier):
        if self.current_token.value == '(':
            func_token = self.current_token

            self.match_value('(')
            args = self.arg_list()
            self.match_value(')')

            return FunctionCall(identifier, args, func_token)

        identifier.array_values = self.array_exp()

        return identifier

    def reserved_function_call(self):
        id_token = self.current_token

        self.match_type(lang.KEYWORD)
        self.match_value('(')
        args = self.arg_list()
        self.match_value(')')

        try:
            return RESERVED_FUNCS_MAP[id_token.value](args, id_token)
        except KeyError:
            return None

    def arg_list(self):
        op_subset = [
            '+',
            '-',
            '(',
        ]

        types_subset = [
            lang.INTEGER,
            lang.DECIMAL,
            lang.LOGIC_CONST,
            lang.STRING,
            lang.IDENTIFIER,
        ]

        args = None
        token = self.current_token

        if token.value in op_subset or token.type in types_subset:
            args = []
            param = self.logical_or_exp()

            if param:
                args.append(param)

            while self.current_token.value == ',':
                self.match_value(',')
                param = self.logical_or_exp()

                if param:
                    args.append(param)

        return args
