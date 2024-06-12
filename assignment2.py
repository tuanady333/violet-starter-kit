from vi import Agent, Simulation
import random
import vi
from vi.config import Config
import pygame



class CockroachAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = "Wandering"
        self.timer = 0
        self.simulation = simulation
        self.boundary_center = vi.Vector2(300, 300)  # Center of the circular boundary
        self.boundary_radius = 100  # Radius of the circular boundary
        self.inside_boundary = random.choice([True, False])  # Randomly start inside or outside the boundary

    def update(self):
        if self.state == "Wandering":
            self.wander()
            if self.detect_site():
                if self.should_join():
                    self.state = "Joining"
                    self.timer = 0

        elif self.state == "Joining":
            self.move_towards_center()
            self.timer += 1
            if self.timer >= self.Tjoin:
                self.state = "Still"

        elif self.state == "Still":
            if self.leave_site():
                self.state = "Leaving"
                self.timer = 0

        elif self.state == "Leaving":
            self.leave_site()
            self.timer += 1
            if self.timer >= self.Tleave:
                self.state = "Wandering"

        self.restrict_movement()

    def wander(self):
        # Implement random walk behavior
        self.pos += self.random_direction()

    def detect_site(self):
        # Implement site detection logic (simplified example)
        return self.in_site()

    def should_join(self):
        # Implement joining probability based on local density
        proximity_iter = self.in_proximity_accuracy()
    
    # Count the number of neighbors within range
        num_neighbors = sum(1 for _ in proximity_iter)
    
    # Calculate the joining probability based on the number of neighbors
        return random.random() < self.Pjoin(num_neighbors)

    def move_towards_center(self):
        # Implement logic to move towards the center of the site
        center = self.site_center()
        self.pos += (center - self.pos) * 0.1  # Move 10% closer to center

    def count_neighbors(self):
        # Count the number of neighbors within a given range
        proximity_iter = self.in_proximity_accuracy()
        num_neighbors = sum(1 for _ in proximity_iter)
        return num_neighbors

    def leave_site(self):
        # Implement logic to leave the site
        self.pos += self.random_direction()

    def random_direction(self):
        # Return a random direction vector
        return vi.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def in_site(self):
        # Check if the agent is in a site (simplified example)
        return self.pos.distance_to(self.site_center()) < self.site_radius()

    def in_proximity_accuracy(self):
        """Retrieve other agents that are in proximity of the current agent."""
        return self.simulation._proximity.in_proximity_accuracy(self)

    def restrict_movement(self):
        # Restrict the movement based on initial position inside or outside the circular boundary
        distance_to_center = self.pos.distance_to(self.boundary_center)
        if self.inside_boundary:
            if distance_to_center > self.boundary_radius:
                direction_to_center = self.boundary_center - self.pos
                direction_to_center = direction_to_center.normalize()
                self.pos = self.boundary_center + direction_to_center * self.boundary_radius
        else:
            if distance_to_center < self.boundary_radius:
                direction_to_outside = self.pos - self.boundary_center
                direction_to_outside = direction_to_outside.normalize()
                self.pos = self.boundary_center + direction_to_outside * self.boundary_radius


    def is_within_bounds(self, pos):
        # Check if a given position is within the circular boundary for initial state
        distance_to_center = pos.distance_to(self.boundary_center)
        if self.inside_boundary:
            return distance_to_center <= self.boundary_radius
        else:
            return distance_to_center >= self.boundary_radius

    
    def site_center(self):
        # Return the center of the site (simplified example)
        return vi.Vector2(50, 50)  # Example center position

    def site_radius(self):
        # Return the radius of the site (simplified example)
        return 10

    def sensing_range(self):
        # Return the sensing range of the agent
        return 5

    def Pjoin(self, neighbors):
        # Calculate the joining probability based on the number of neighbors
        return min(1, neighbors / 10)

    def Pleave(self, neighbors):
        # Calculate the leaving probability based on the number of neighbors
        return max(0, 1 - neighbors / 10)

    @property
    def Tjoin(self):
        # Return the joining time threshold
        return 10

    @property
    def Tleave(self):
        # Return the leaving time threshold
        return 10



class AggregationSimulation(Simulation):
    def draw(self, screen):
        # Draw the circular boundary in white with a bold outline
        pygame.draw.circle(screen, (255, 255, 255, [255]), width=2, draw_top_right= True, draw_top_left=None, draw_bottom_left=None, draw_bottom_right=None)
        super().draw(screen)
        
# Initialize the simulation
simulation = AggregationSimulation(Config())

# Initialize and run the simulation
simulation = (
    simulation
    .batch_spawn_agents(100, CockroachAgent, ["images/white.png", "images/red.png"])
    .run()
) .run()


