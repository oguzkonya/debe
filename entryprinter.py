class Printer():

    def __init__(self):
        self.entryTemplate = self.readContents("includes/entry.html")
        self.homeTemplate = self.readContents("layouts/home.html")


    def readContents(self, filename):
        f = open(filename, "r")
        contents = f.read()
        f.close()
        return contents


    def printEntry(self, entry):
        return self.entryTemplate\
            .replace("{id}", entry.id)\
            .replace("{next}", entry.nextId)\
            .replace("{title}", entry.title)\
            .replace("{date}", entry.date)\
            .replace("{authorlink}", entry.authorLink)\
            .replace("{author}", entry.author)\
            .replace("{link}", entry.link)\
            .replace("{content}", entry.content)

    def printIndex(self, debe, date):
        return self.homeTemplate.replace("{debe}", debe).replace("{date}", date)