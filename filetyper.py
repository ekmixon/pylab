class Filetyper:
    def __init__(self):
        self.matchers = []

    def add_matcher(self, matcher):
        self.matchers.append(matcher)

class FiletypeExt:
    def __init__(self, filetype, ext):
        self.ext = ext

    def matches(self, ext):
        return ext in self.ext

