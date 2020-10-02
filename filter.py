import re

class Filter():

    def __init__(self, filename):
        self.filteredTitles = self.readContents(filename)

    def readContents(self, filename):
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
            return lines

    def filterTitle(self, debe):
        for f in self.filteredTitles:
            if re.match(r"%s" % f, debe.title) is not None:
                return False
        
        return True