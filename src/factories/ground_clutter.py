from components.graphics import Render, GroundLayer
from components.physics import Position, Grabbable

class Rock:
    def __init__(self, world, rock_type, x, y):
        self.world = world
        self.rock_type = rock_type
        self.x = x
        self.y = y

    def assemble_rock(self):
        self.rock = self.world.create_entity()

        self.world.add_component(self.rock, Position(self.x, self.y))
        self.world.add_component(self.rock, Grabbable("small"))
        self.world.add_component(self.rock, Render("*", (80, 80, 80)))
        self.world.add_component(self.rock, GroundLayer())

        return self.rock
