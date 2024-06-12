from enum import Enum, auto
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from vi.config import Config, dataclass, deserialize

# Configuration for Flocking Behavior
@deserialize
@dataclass
class FlockingConfig(Config):
    alignment_weight: float = 0.5
    cohesion_weight: float = 0.5
    separation_weight: float = 0.5
    delta_time: float = 0.5
    mass: int = 20

    def weights(self) -> tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)

# Agent Class for Bird
class Bird(Agent):
    config: FlockingConfig

    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        self.there_is_no_escape()


        # Get the neighbors within the radius R
        neighbors = list(self.in_proximity_accuracy())
        if not neighbors:
            return

        # Initialize vectors
        alignment_force = Vector2(0, 0)
        cohesion_force = Vector2(0, 0)
        separation_force = Vector2(0, 0)

        # Compute alignment, cohesion, and separation forces
        for neighbor, distance in neighbors:
            alignment_force += neighbor.move
            cohesion_force += neighbor.pos
            separation_force += self.pos - neighbor.pos

        num_neighbors = len(neighbors)

        if num_neighbors > 0:
            # Alignment: steer towards the average direction of local boids
            alignment_force /= num_neighbors
            alignment_force -= self.move
            alignment_force = alignment_force.normalize() if alignment_force.length() > 0 else alignment_force

            # Cohesion: steer towards the average position of local boids
            cohesion_force /= num_neighbors
            cohesion_force -= self.pos
            cohesion_force = cohesion_force.normalize() if cohesion_force.length() > 0 else cohesion_force

            # Separation: steer away to avoid being in too close proximity to local boids
            separation_force /= num_neighbors
            separation_force = separation_force.normalize() if separation_force.length() > 0 else separation_force

        # Combine the forces with their respective weights
        ftotal = (self.config.alignment_weight * alignment_force +
                  self.config.cohesion_weight * cohesion_force +
                  self.config.separation_weight * separation_force) / self.config.mass

        # Update the boid's velocity and position
        self.move += ftotal
        if self.move.length() > 1:  # Ensure the boid doesn't exceed max speed
            self.move.scale_to_length(1)
        self.pos += self.move * self.config.delta_time

# Enumeration for Parameter Selection
class Selection(Enum):
    ALIGNMENT = auto()
    COHESION = auto()
    SEPARATION = auto()

# Simulation Class for Flocking Behavior
class FlockingLive(Simulation):
    selection: Selection = Selection.ALIGNMENT
    config: FlockingConfig

    def handle_event(self, by: float):
        if self.selection == Selection.ALIGNMENT:
            self.config.alignment_weight += by
        elif self.selection == Selection.COHESION:
            self.config.cohesion_weight += by
        elif self.selection == Selection.SEPARATION:
            self.config.separation_weight += by

    def before_update(self):
        super().before_update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.handle_event(by=0.1)
                elif event.key == pg.K_DOWN:
                    self.handle_event(by=-0.1)
                elif event.key == pg.K_1:
                    self.selection = Selection.ALIGNMENT
                elif event.key == pg.K_2:
                    self.selection = Selection.COHESION
                elif event.key == pg.K_3:
                    self.selection = Selection.SEPARATION
        a, c, s = self.config.weights()
        print(f"A: {a:.1f} - C: {c:.1f} - S: {s:.1f}")

# Running the Simulation
(
    FlockingLive(
        FlockingConfig(
            image_rotation=True,  # Enable image rotation for direction visualization
            movement_speed=1,
            radius=50,
            seed=1,
        )
    )
    .batch_spawn_agents(50, Bird, images=["/Users/tuanadurmayuksel/Documents/GitHub/Oscar/images/red-bird.png"])
    .run()
)