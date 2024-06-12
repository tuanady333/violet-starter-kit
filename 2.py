from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.math import Vector2
import pygame as pg
import random
import vi

class AggregationEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def update(self):
        for agent in self.agents:
            agent.update()

class CockroachAgent(Sprite):
    def __init__(self, images, simulation, pos=None, move=None):
        Sprite.__init__(self, simulation._all, simulation._agents)

        self.__simulation = simulation

        self.id = simulation._agent_id()
        self.config = simulation.config
        self.shared = simulation.shared

        # Default to first image in case no image is given
        self._image_index = 0
        self._images = images

        self._obstacles = simulation._obstacles
        self._sites = simulation._sites

        self._area = simulation._area
        self.move = (
            move
            if move is not None
            else Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        )

        if pos is not None:
            self.pos = pos

        if not hasattr(self, "pos"):
            # Keep changing the position until the position no longer collides with any obstacle.
            while True:
                self.pos = Vector2(random.uniform(0, self._area.width), random.uniform(0, self._area.height))

                obstacle_hit = pg.sprite.spritecollideany(self, self._obstacles, pg.sprite.collide_mask)  # type: ignore
                if not bool(obstacle_hit) and self._area.contains(self.rect):
                    break

    def update(self):
        # Implement the update logic for the agent
        pass

# Initialize pygame
pg.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Swarm Aggregation Simulation")

# Create an instance of the AggregationEnvironment
environment = AggregationEnvironment(WIDTH, HEIGHT)

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Update the environment
    environment.update()

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw agents
    for agent in environment.agents:
        screen.blit(agent.image, agent.rect)

    # Update the display
    pg.display.flip()

# Quit pygame
pg.quit()
 