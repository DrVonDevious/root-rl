from components.physics import Position, Velocity
from components.graphics import Render, MobLayer

class Player:
    def __init__(self, world):
        self.world = world

    def assemble_player(self):
        self.player = self.world.create_entity()
        self.world.add_component(self.player, Position(0, 0))
        self.world.add_component(self.player, Velocity(0, 0))
        self.world.add_component(self.player, Render("@", (255, 255, 255)))
        self.world.add_component(self.player, MobLayer())

        return self.player
