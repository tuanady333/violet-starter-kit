from vi import Agent, Simulation
import random
import vi



class CockroachAgent(Agent):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = "Wandering"
        self.timer = 0

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
            if self.should_leave():
                self.state = "Leaving"
                self.timer = 0

        elif self.state == "Leaving":
            self.leave_site()
            self.timer += 1
            if self.timer >= self.Tleave:
                self.state = "Wandering"


        # Ensure agents stay within the boundary
        self.pos.x = max(0, min(self.pos.x, self.width))
        self.pos.y = max(0, min(self.pos.y, self.height))


    def wander(self):
        # Implement random walk behavior
        self.pos += self.random_direction()

    def detect_site(self):
        # Implement site detection logic (simplified example)
        return self.in_site()

    def should_join(self):
        # Implement joining probability based on local density
        neighbors = self.count_neighbors()
        return random.random() < self.Pjoin(neighbors)

    def move_towards_center(self):
        # Implement logic to move towards the center of the site
        center = self.site_center()
        self.pos += (center - self.pos) * 0.1  # Move 10% closer to center

    def should_leave(self):
        # Implement leaving probability based on local density
        neighbors = self.count_neighbors()
        return random.random() < self.Pleave(neighbors)

    def leave_site(self):
        # Implement logic to leave the site
        self.pos += self.random_direction()

    def random_direction(self):
        # Return a random direction vector
        return vi.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    def in_site(self):
        # Check if the agent is in a site (simplified example)
        return self.pos.distance_to(self.site_center()) < self.site_radius()

    def count_neighbors(self):
        # Count the number of neighbors within a given range
        return len(self.neighbors_within_range(self.sensing_range))

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



# Initialize and run the simulation
simulation = (
    Simulation()
    .batch_spawn_agents(100, CockroachAgent, ["images/white.png", "images/red.png"])
    .run()
)
