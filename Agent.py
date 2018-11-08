
import numpy as np

class Agent():

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
            return (int(self.rock * 255) % 255,0,0)
        elif fav[0] == "POP":
            return (0,int(self.pop * 255) % 255,0)
        elif fav[0] == "TECHNO":
            return (0,0,int(self.techno * 255) % 255)
        # When we get here something went wrong, but we give a white color back
        return (255,255,255)

    def update(self, neighbour_fav):
        influence =  0.25 * neighbour_fav[1] + 0.25 * np.random.uniform(0,1)
        if neighbour_fav[0] == "ROCK":
            self.rock = 0.5 * self.rock + influence
            self.pop = self.pop - influence * 0.5
            self.techno = self.techno - influence * 0.5
        elif neighbour_fav[0] == "POP":
            self.rock = self.rock - influence * 0.5
            self.pop = 0.5 * self.pop + influence
            self.techno = self.techno - influence * 0.5
        elif neighbour_fav[0] == "TECHNO":
            self.rock = self.rock - influence * 0.5
            self.pop = self.pop - influence * 0.5
            self.techno = 0.5 * self.techno + influence

        self.rock = max(0, self.rock)
        self.pop = max(0, self.pop)
        self.techno = max(0, self.techno)

        if np.random.uniform(0,1,1) < .005:
            values = np.random.uniform(0,1,3)
            values = values / sum(values) if sum(values) != 0 else values
            self.rock = values[0]
            self.pop = values[1]
            self.techno = values[2]
            self.neighbour_like = np.random.uniform(0,1,4)



