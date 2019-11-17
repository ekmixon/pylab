import argparse
import re
import sys
from filetyper import Filetyper

filetyperobject = Filetyper()
class TypeAdd(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        spec = values[0]

        err = filetyperobject.add_typespec(spec)
        if err:
            print(err)
            sys.exit(1)         # Need a utility function like die_and_exit

def get_options():

    parser = argparse.ArgumentParser(
        prog='ack',
        description='ack does such-and-such',
        usage='ack [OPTION]... PATTERN [FILES OR DIRECTORIES]',
    )

    group_searching = parser.add_argument_group('Searching')
    group_searching.add_argument(
        '-i', '--ignore-case',
        help='Ignore case distinctions in PATTERN.',
        dest='i',
        action='store_true'
    )

    group_output = parser.add_argument_group('Search output')
    group_output.add_argument(
        '-A', '--after-context',
        help='Print NUM lines of trailing context after matching lines',
        type=int,
        metavar='NUM',
        dest='A'
    )

    parser.add_argument(
        '--type-add',
        metavar='TYPE:FILTER:ARGS',
        dest='typespecs',
        action=TypeAdd,
        nargs=1,
        help='Files with the given ARGS applied to the given FILTER are recognized as being type TYPE.',
    )
    parser.add_argument(
        '--type-del',
        metavar='TYPE',
        nargs=1,
        #action=TypeDel,
        help='Removes specifiction for TYPE',
    )

    opt = parser.parse_args()

    print(opt)

    return opt

if __name__ == "__main__":
    opt = get_options()
    print(opt)
