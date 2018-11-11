
import pygame
import numpy.random as npr
from simulation1.Agent import Agent
import random, time, json, copy, datetime, uuid
from simulation1.mqtt import mqtt

sim_x = 50        # number of tiles on x as
sim_y = 50          # number of tiles on y as
cell_width = 15     # 10 pixels per tile
mqtt = mqtt("broker.hivemq.com",1883)

Agent()
# Create new cells
cells = [[Agent(npr.uniform(0, 1, 3), npr.uniform(0, 1, 4)) for y in range(sim_y)] for x in range(sim_x)]

def visualizeCells():
    for x in range(sim_x):
        for y in range(sim_y):
            color = cells[x][y].getColor()
            pygame.draw.rect(screen, color, pygame.Rect(x * cell_width, y * cell_width, cell_width, cell_width))

    pygame.display.update()

def updateCells():
    global cells
    buffer = copy.deepcopy(cells)
    for x in range(sim_x):
        for y in range(sim_y):
            neighbours = []
            temp_x = x if x - 1 != -1 else 1
            neighbours.append(cells[temp_x - 1][y])
            try: neighbours.append(cells[temp_x + 1][y])
            except IndexError: pass
            temp_y = y if y - 1 != -1 else 1
            neighbours.append(cells[x][temp_y - 1])
            try: neighbours.append(cells[x][temp_y + 1])
            except IndexError: pass

            buffer[x][y].update(neighbours)

    cells = buffer

def mqttCallback(msg):
    print("MQTT message recieved")
    msg = msg.decode("utf-8")
    in_message = json.loads(msg)
    genres = ["ROCK", "POP", "TECHNO"]
    genre = genres[npr.randint(3)]
    for row in cells:
        for c in row:
            res = {"timestamp": datetime.datetime.now().isoformat(),
                   "value": -1,
                   "usename": "IoTsim",
                   "uid": str(uuid.uuid4()),
                   "songid": in_message["songid"]}
            if c.getFavourite()[0] == genre:
                res["value"] = 1
            mqtt.publish("votes", json.dumps(res))

if __name__ == '__main__':
    (width, height) = (sim_x * cell_width, sim_y * cell_width)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("IoT sim")
    pygame.display.flip()

    mqtt.connect()
    mqtt.add_listener_func(mqttCallback)

    running = True
    visualizeCells()
    while running:
        # First check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        updateCells()
        visualizeCells()
