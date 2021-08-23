import os
import argparse
import warnings

from lexer import Lexer
from syntax import Syntax
from syntax.tree import Node

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    script_dir = os.path.dirname(__file__)

    group.add_argument('source', help='Source file relative path' , nargs='?', default=None)
    group.add_argument('-c', '--cmd', help='program passed in as string')

    args = parser.parse_args()

    if args.source:
        abs_file_path = os.path.join(script_dir, args.source)

        with open(abs_file_path) as src:
            source_code = src.read()

    elif args.cmd:
        source_code = args.cmd

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')

        lexer = Lexer(source_code)
        syntax = Syntax(lexer)

        parse_tree = syntax.parse()

        print(1, parse_tree.declarator)
        print(2, parse_tree.declarator.identifier)
        print(3, parse_tree.next)
        print(parse_tree.next.next)
        print(parse_tree.next.next.next)
        # for node in parse_tree:
        #     print(node)

        Node.proccess_traversal_semantics(parse_tree)
        Node.symtable.show()

        for error in w:
            print(f'{error.category.__name__}: {error.message}')
        else:
        # if not w:
            code = Node.get_code(parse_tree)

            with open('output_test.trono', 'w') as f:
                print('\n'.join(code), file=f)
                print('Done!')



    # for token in lexer:
    #     print(token.show(True))
