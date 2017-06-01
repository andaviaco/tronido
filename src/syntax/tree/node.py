import warnings
import pprint as pp

from lexer import lang
from ..symtable import SymTable, GLOBAL_CONTEXT

class SemanticError(Warning):
    pass


class Node(object):
    symtable = SymTable()
    datatype = lang.SEMANTIC_ERROR_TYPE
    code_labels = []
    code_funcs = []
    code_inits = []
    code_main = []
    labels = {}

    """docstring for Node."""
    def __init__(self, symbol, token):
        super().__init__()

        self.symbol = symbol
        self.token = token
        self.next = None

        if token:
            self.line_index = token.line_index
            self.col_index = token.col_index

    def __iter__(self):
        node = self

        while node:
            yield node
            node = node.next

    def __str__(self):
        rep = dict(
            name=self.__class__.__name__,
            value=self.token.value,
            type=self.token.type,
            next_node=self.next
        )

        return pp.pformat(rep)


    @staticmethod
    def raise_error(msg):
        warnings.warn(msg, SemanticError)

    @staticmethod
    def process_semantic(**cond):
        pass

    @staticmethod
    def proccess_traversal_semantics(node, **cond):
        cond_context = cond.get('context', None)

        if cond.get('context', None):
            Node.symtable.set_context(cond_context)

        while node:
            node.process_semantic(**cond)
            node = node.next
        #
        # if Node.symtable.current_contex != GLOBAL_CONTEXT:
        #     Node.symtable.exit_context()

    @staticmethod
    def get_code(tree):
        Node.cascade_code(tree)

        row_inits = ['{}{}'.format(len(Node.code_funcs) + i + 1, s) for s, i in enumerate(Node.code_inits)]

        return [
            *Node.get_vars_code(),
            *Node.code_labels,
            '@',
            *Node.code_funcs,
            *row_inits,
            *Node.code_main,
        ]

    @staticmethod
    def cascade_code(node, **cond):
        cond_context = cond.get('context', None)

        if cond_context:
            Node.symtable.current_contex = cond_context

        while node:
            node.generate_code(**cond)
            node = node.next

    @staticmethod
    def assignated_array():
        line = len(Node.code_funcs) + 1
        array = 'code_funcs'

        context = Node.symtable.get_context()

        if context == GLOBAL_CONTEXT:
            line = ''
            array = Node.code_inits
        elif context == 'main':
            line += len(Node.code_inits)
            line += len(Node.code_main)
            array = 'code_main'

        return (array, line)

    @staticmethod
    def array_append(array, value):
        if array == 'code_funcs':
            Node.code_funcs.append(value)
        elif array == 'code_labels':
            Node.code_labels.append(value)
        elif array == 'code_inits':
            Node.code_inits.append(value)
        elif array == 'code_main':
            Node.code_main.append(value)



    @staticmethod
    def get_vars_code():
        def format_var(key, record):
            class_name = lang.PL_CLASS_TYPES[record['symtype']]
            datatype = lang.PL_TYPES[record['datatype']]
            try:
                sizes = record['extras']['sizes']
            except KeyError:
                sizes = [0, 0]

            dim1 = sizes[0]
            dim2 = sizes[1]

            return Node.pl_format_var(
                key,
                class_name,
                datatype,
                dim1,
                dim2
            )

        symtable = Node.symtable.get_table()

        code = []
        for context, values in symtable.items():
            for var, record in values.items():
                if var.startswith('$'):
                    code.append(format_var(f'{context}@{var}', record))

        code.append(
            Node.pl_format_var(
                '_P',
                'I',
                'I',
                Node.symtable.get_table()[GLOBAL_CONTEXT]['$main']['extras']['sizes'][0])
            )

        return code

    @staticmethod
    def pl_format_var(identifier, class_type, datatype, dim1=0, dim2=0):
        return f'{identifier},{class_type},{datatype},{dim1},{dim2},#,'

    @staticmethod
    def get_unique_label(label):
        try:
            Node.labels[label] += 1
        except:
            Node.labels[label] = 1

        return f'_{label}_{Node.labels[label]}'


    def generate_code(self, **cond):
        context = Node.symtable.get_context()
        if context == 'main':
            assignated_array = Node.code_main
        else:
            assignated_array = Node.code_funcs

        assignated_array.append(self.__class__.__name__)
