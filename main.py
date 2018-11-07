
import pygame
import numpy.random as npr
from Agent import Agent

sim_x = 50          # number of tiles on x as
sim_y = 50          # number of tiles on y as
cell_width = 10     # 10 pixels per tile

Agent()
# Create new cells
cells = [[Agent(npr.uniform(0, 1, 3), npr.uniform(0, 1, 4)) for y in range(sim_x)] for x in range(sim_y)]

def visualizeCells():
    for x in range(sim_x):
        for y in range(sim_y):
            color = cells[x][y].getColor()
            pygame.draw.rect(screen, color, pygame.Rect(x * cell_width, y * cell_width, cell_width, cell_width))

    pygame.display.update()

def updateCells():
    for x in range(sim_x):
        for y in range(sim_y):
            neighbours = []
            try: neighbours.append(cells[x - 1][y])
            except IndexError: neighbours.append(Agent())
            try: neighbours.append(cells[x + 1][y])
            except IndexError: neighbours.append(Agent())
            try: neighbours.append(cells[x][y - 1])
            except IndexError: neighbours.append(Agent())
            try: neighbours.append(cells[x][y + 1])
            except IndexError: neighbours.append(Agent())

            for neighbour in neighbours:
                influence = 0.25 * neighbour.getFavourite()[1] + 0.25 * npr.uniform(0,1)
                print(influence)




if __name__ == '__main__':
    (width, height) = (sim_x * cell_width, sim_y * cell_width)
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()

    running = True

    while running:
        # First check eventsx - 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        updateCells()
        visualizeCells()

