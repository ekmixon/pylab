import argparse

class TypeAdd(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        print('calling')
#        namespace.setattr('types','added-to')
        return
        print('%r %r %r' % (namespace, values, option_string))
        dest = getattr(namespace, self.dest)
        print(dest)
        key = option_string[1]
        dest.update(key = values[0])


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

    # Not all options need pattern or starting points
    opt = parser.parse_args()

    return opt

if __name__ == "__main__":
    opt = get_options()
    print(opt)
