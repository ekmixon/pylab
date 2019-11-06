#!/usr/bin/env python3

import argparse


def get_opt():
    progdesc = """
        Search for PATTERN in each source file in the tree from the current
        directory on down.  If any files or directories are specified, then
        only those files and directories are checked.  ack may also search
        STDIN, but only if no file or directory arguments are specified,
        or if one of them is "-".

        Default switches may be specified in an .ackrc file. If you want no dependency
        on the environment, turn it off with --noenv.
    """
    parser = argparse.ArgumentParser(
        prog='ack',
        description=progdesc,
        usage='ack [OPTION]... PATTERN [FILES OR DIRECTORIES]',
    )

    group_searching = parser.add_argument_group('Searching')
    group_searching.add_argument(
        '-i', '--ignore-case',
        help='Ignore case distinctions in PATTERN.',
        dest='i',
        action='store_true'
    )
    group_searching.add_argument(
        '-I',
        help='Turns on case-sensitivity in PATTERN.',
        dest='i',
        action='store_false',
    )
    # XXX How do we do the negate?
    group_searching.add_argument(
        '-S', '--smart-case',
        help='Ignore case distinctions in PATTERN, only if PATTERN contains no upper case.',
        dest='S',
        action='store_true',
    )

    group_searching.add_argument(
        '-v', '--invert-match',
        help='Invert match: Show non-matching lines',
        dest='v',
        action='store_true',
        default=False,
    )
    group_searching.add_argument(
        '-w', '--word-regexp',
        help='Force PATTERN to match only whole word',
        dest='w',
        action='store_true',
        default=False,
    )

    group_searching.add_argument(
        '-t', '--type',
        help='Include only files of type TYPE, e.g. python, html, markdown, etc',
        dest='type',
    )

    group_output = parser.add_argument_group('Search output')
    group_output.add_argument(
        '-A', '--after-context',
        help='Print NUM lines of trailing context after matching lines',
        type=int,
        metavar='NUM',
        dest='A'
    )
    group_output.add_argument(
        '-B', '--before-context',
        help='Print NUM lines of leading context before matching lines',
        type=int,
        metavar='NUM',
        dest='B'
    )
    group_output.add_argument(
        '-C', '--context',
        help='Print NUM lines (default 2) of output context',
        type=int,
        metavar='NUM',
        dest='C'
    )
    group_output.add_argument(
        '-m', '--max-count',
        help='Stop searching in each file after NUM matches',
        type=int,
        metavar='NUM',
        dest='m'
    )

    group_finding = parser.add_argument_group('File finding')
    group_finding.add_argument(
        '-f',
        help='Only print the files selected, without searching.  The PATTERN must not be specified.',
        dest='f',
        action='store_true',
    )
    group_finding.add_argument(
        '-g',
        help='Same as -f, but only select files matching PATTERN.',
        metavar='PATTERN',
        dest='g',
    )

    group_misc = parser.add_argument_group('Miscellaneous')
    group_misc.add_argument(
        '--thpppt',
        help='Bill the Cat',
    )
    group_misc.add_argument(
        '--bar',
        help='The warning admiral',
    )
    group_misc.add_argument(
        '--cathy',
        help='Chocolate! Chocolate! Chocolate!',
    )

    # Not all options need pattern or starting points
    opt = parser.parse_known_args()

    return opt


def main():
    opt, extra = get_opt()
    print(opt)
    print(extra)


main()
