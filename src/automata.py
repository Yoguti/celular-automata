import random
from abc import ABC, abstractmethod

class FastGrid:
    def __init__(self, width, height, fill=0):
        self.width = width
        self.height = height
        self.data = [fill] * (width * height)

    def get(self, x, y):
        return self.data[y * self.width + x]

    def set(self, x, y, value):
        self.data[y * self.width + x] = value

    def __str__(self): 
        lines = []
        for y in range(self.height):
            line = ''.join(str(self.get(x, y)) for x in range(self.width))
            lines.append(line)
        return '\n'.join(lines)


class Automata:
    FastGrid grid = None
    def __init__(self, name, height, width, generations, initial_state=None):
        self.name = name
        self.width = width
        self.height = height
        self.generations = generations
        self.state = initial_state

    def create_grid(self):
        grid = FastGrid(self.width, self.height)

    def set_initial_state(self):
        pass

    @abstractmethod
    def run_automata(self)

    


