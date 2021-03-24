from components.graphics import Render, GroundLayer
from components.physics import Position, Grabbable
from components.stats import Name

class Rock:
    def __init__(self, world):
        self.world = world

    def assemble_rock(self, rock_type, x, y):
        self.rock = self.world.create_entity()
        self.rock_type = rock_type
        self.x = x
        self.y = y

        self.world.add_component(self.rock, Position(self.x, self.y))
        self.world.add_component(self.rock, Grabbable("small"))
        self.world.add_component(self.rock, Render("*", (80, 80, 80)))
        self.world.add_component(self.rock, Name(self.rock_type))
        self.world.add_component(self.rock, GroundLayer())

        return self.rock
