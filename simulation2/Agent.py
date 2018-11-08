
import numpy as np
import random

class Agent():

    def __init__(self, values=np.zeros(3), coordinates=(0,0)):
        assert(values.size == 3 and len(coordinates) == 2)
        values = values / sum(values) if sum(values) != 0 else values
        self.rock = values[0]
        self.pop = values[1]
        self.techno = values[2]
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.moving = False
        self.target = (0,0)

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

    def move(self):
        if self.moving:
            if self.x == self.target[0]: pass
            elif self.x > self.target[0]: self.x -= 1
            else: self.x += 1

            if self.y == self.target[1]: pass
            elif self.y > self.target[1]: self.y -= 1
            else: self.y += 1

            if (self.x, self.y) == self.target:
                self.moving = False

    def update(self, neighbours):
        # update values
        desicion = np.random.uniform(0,1,1)
        if desicion > 0.05: # 5% change for a cell to have a opinion, thus not updating with neighbour values
            for neighbour in neighbours.values():
                neighbour_fav = neighbour.getFavourite()
                influence = 0.25 * neighbour_fav[1] + 0.25 * np.random.uniform(0, 1)

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
        elif desicion < 0.005: # 0.5% to have a completely new opinion
            values = np.random.uniform(0,1,3)
            values = values / sum(values) if sum(values) != 0 else values
            self.rock = values[0]
            self.pop = values[1]
            self.techno = values[2]

        # start moving
        if not self.moving:
            target = (0,0)
            if np.random.uniform(0,1) > 0.2:
                if(len(neighbours) != 1):
                    keys = sorted(neighbours.keys())
                    choice = np.random.randint(1, len(keys))
                    counter = 0
                    while self.getFavourite()[0] != neighbours[keys[choice]].getFavourite()[0] and counter < 10:
                        choice = np.random.randint(1, len(keys))
                        counter += 1
                    target = (neighbours[keys[choice]].x, neighbours[keys[choice]].y)
            else:
                target = (self.x + np.random.randint(-75, 75), self.y + np.random.randint(-75, 75))

            self.moving = True
            self.target = target
