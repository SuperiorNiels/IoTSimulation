
import pygame
import numpy as np
import numpy.random as npr
from simulation2.Agent import Agent
import random, time, json, copy, datetime, uuid
from simulation2.mqtt import mqtt

screen_x = 500        # number of tiles on x as
screen_y = 500         # number of tiles on y as
agents = 100         # number of agents
mqtt = mqtt("broker.hivemq.com",1883)

Agent()
# Create new cells
_agents = [Agent(npr.uniform(0, 1, 3), (npr.randint(screen_x), npr.randint(screen_y))) for x in range(agents)]

def visualizeCells():
    for c in _agents:
        color = c.getColor()
        pygame.draw.circle(screen, color, (c.x, c.y), 10)
    pygame.display.update()

def updateCells():
    d = 75
    for c in _agents:
        if c.x < 0 or c.x > screen_x:
            _agents.remove(c)
            continue
        if c.y < 0 or c.y > screen_y:
            _agents.remove(c)
            continue

        neigbours = {}
        for n in _agents:
            dist = distance(c.x, c.y, n.x, n.y)
            if dist < d: neigbours.update({dist: n})
        c.update(neigbours)
        c.move()

def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def mqttCallback(msg):
    print("MQTT message recieved")
    msg = msg.decode("utf-8")
    in_message = json.loads(msg)
    genres = ["ROCK", "POP", "TECHNO"]
    genre = genres[npr.randint(3)]
    for row in _agents:
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
    screen = pygame.display.set_mode((screen_x, screen_y))
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

        if npr.uniform(0,1) < 0.15: # add new agent with random chance
            _agents.append(Agent(npr.uniform(0, 1, 3), (npr.randint(screen_x), npr.randint(screen_y))))

        updateCells()
        screen.fill((0,0,0,0))
        visualizeCells()
