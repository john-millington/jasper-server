import os

from console.Context import Context
from threading import Timer

class Console:
    def __init__(self):
        self.contexts = []
        self.redraw()

    def context(self):
        context = Context(self, len(self.contexts))
        self.contexts.append(context)

        return context

    def redraw(self):
        os.system('clear')
        for context in self.contexts:
            context.redraw()

        Timer(1, self.redraw).start()