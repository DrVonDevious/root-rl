import random

from components.physics import Position, Collision, Opaque, Translucent
from components.graphics import Render, TileLayer

class Chunk:
    def generate_chunk(
        world = None,
        chunkX = 0,
        chunkY = 0,
        chunkWidth = 16,
        chunkHeight = 16
    ):
        for x in range(chunkWidth):
            for y in range(chunkHeight):
                tile = world.create_entity()

                world.add_component(tile, Position(
                    x + (chunkWidth * chunkX),
                    y + (chunkHeight * chunkY)
                ))

                randNum = random.randint(1, 60)

                if (randNum in range(1, 19)):
                    world.add_component(tile, Render(",", (100, 100, 0)))
                    world.add_component(tile, TileLayer())
                    world.add_component(tile, Translucent())
                elif (randNum in range(20, 59)):
                    world.add_component(tile, Render(".", (20, 100, 0)))
                    world.add_component(tile, TileLayer())
                    world.add_component(tile, Translucent())
                elif (randNum == 60):
                    world.add_component(tile, Render("♣", (130, 150, 0)))
                    world.add_component(tile, TileLayer())
                    world.add_component(tile, Collision(True))
                    world.add_component(tile, Opaque())
