
import numpy as np

class Agent(object):

    def __init__(self, values=np.zeros(3), neighbour_like=np.zeros(4)):
        assert(values.size == 3)
        values = values / sum(values) if sum(values) != 0 else values
        self.rock = values[0]
        self.pop = values[1]
        self.techno = values[2]
        self.neighbour_like = neighbour_like

    def getFavourite(self):
        _max = max(self.rock, self.pop, self.techno)
        if _max == self.rock:
            return ("ROCK", self.rock)
        elif _max == self.pop:
            return ("POP", self.pop)
        elif _max == self.techno:
            return ("TECHNO", self.techno)
        return

    def getValue(self, value):
        if value == "ROCK":
            return self.rock
        elif value == "POP":
            return self.pop
        elif value == "TECHNO":
            return self.techno

    def getColor(self):
        fav = self.getFavourite()
        if fav[0] == "ROCK":
            return (255,0,0)
        elif fav[0] == "POP":
            return (0,255,0)
        elif fav[0] == "TECHNO":
            return (0,0,255)
        # When we get here something went wrong, but we give a white color back
        return (255,255,255)
