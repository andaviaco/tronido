import os
import sys
import argparse

from lexer import Lexer
from syntax import Syntax

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

    lexer = Lexer(source_code)
    syntax = Syntax(lexer)

    parse_tree = syntax.parse()

    for node in parse_tree:
        print(node)

    # for token in lexer:
    #     print(token.show(True))
