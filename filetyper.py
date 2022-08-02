"""

The Filetyper gets created and then fed a bunch type identifiers, like perl:ext:pm,pl,t.

Then, once that set up is done, it can be given a filename and be given a list of types.

Some of the types are not real types, like '__TEXT__' and '__IGNORE__', which comes from --ignore-file specs.


"""

from enum import Enum
from collections import namedtuple
import re
import os

TypeSpec = namedtuple('TypeSpec', ['method', 'filetype', 'arg'])

class TypeMethod(Enum):
    IS = 0,
    EXT = 1,
    MATCH = 2,
    FLM = 3, # firstlinematch


class Filetyper:

    def __init__(self):
        self.matchers = []

    def add_typespec(self, typespec):
        typespec_re = re.compile('^(\w+):(ext|is|match|firstlinematch):(.+)$')
        matches = typespec_re.match(typespec)
        if not matches:
            return f'Invalid typespec "{typespec}"'

        filetype = matches[1]
        filtermethod = matches[2]
        args = matches[3]
        if filtermethod == 'ext':
            extensions = args.split(',')
            for ext in extensions:
                self.matchers.append(TypeSpec(TypeMethod.EXT, filetype, ext))
        elif filtermethod == 'is':
            self.matchers.append(TypeSpec(TypeMethod.IS, filetype, args))
        elif filtermethod == 'match':
            self.matchers.append(TypeSpec(TypeMethod.MATCH, filetype, re.compile(args)))
        elif filtermethod == 'firstlinematch':
            self.matchers.append(TypeSpec(TypeMethod.FLM, filetype, re.compile(args)))
        else:
            return f'Unknown filter type "{filtermethod}.  Type must be one of: ext, firstlinematch, is, match.'

        return

    def filetypes(self, filename):
        basename, file_extension = os.path.splitext(filename)

        filetypes = []
        if file_extension is not None:
            file_extension = file_extension[1:]
            filetypes.extend(
                matcher.filetype
                for matcher in self.matchers
                if matcher.method == TypeMethod.EXT
                and file_extension == matcher.arg
                or matcher.method != TypeMethod.EXT
                and matcher.method == TypeMethod.IS
                and filename == matcher.arg
                or matcher.method != TypeMethod.EXT
                and matcher.method != TypeMethod.IS
                and matcher.method == TypeMethod.MATCH
                and matcher.arg.search(filename)
            )

        return filetypes
