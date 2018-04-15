import sys

class Context:
    def __init__(self, master, id):
        self.master = master
        self.id = id
        self.infos = ['', '']

    def print(self, index, info):
        self.infos[index] = info

    def redraw(self):
        for info in self.infos:
            sys.stdout.write(info + '\n')