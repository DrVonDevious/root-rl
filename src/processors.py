import esper
import tcod.event
import sys

from components.physics import Velocity, Position, Collision, Grabbable
from components.graphics import Render, TileLayer, GroundLayer, MobLayer


class MovementProcessor(esper.Processor):
    def process(self, scene):
        self.scene = scene
        self.camera = self.scene.camera

        if (self.scene.action.get("move")):
            self.action = self.scene.action.get("move")

            self.scene.playerVel.dx = self.action[0]
            self.scene.playerVel.dy = self.action[1]

            if (self.action[0] == 1):
                self.scene.game_map.generate_new_chunks("east")
            elif (self.action[0] == -1):
                self.scene.game_map.generate_new_chunks("west")
            elif (self.action[1] == 1):
                self.scene.game_map.generate_new_chunks("south")
            elif (self.action[1] == -1):
                self.scene.game_map.generate_new_chunks("north")

            self.scene.action = {}

        self.components = self.world.get_components(Velocity, Position)
        self.solid_components = self.world.get_components(Position, Collision)
        self.collideables = []

        for entity, (position, collision) in self.solid_components:
            if collision.isSolid:
                self.collideables.append((position.x, position.y))

        for entity, (velocity, position) in self.components:
            new_x = position.x + velocity.dx
            new_y = position.y + velocity.dy

            if not (self.collideables.count((new_x, new_y))):
                position.x = new_x
                position.y = new_y
                self.camera.x += -velocity.dx
                self.camera.y += -velocity.dy

        self.scene.playerVel.dx = 0
        self.scene.playerVel.dy = 0


class ActionProcessor(esper.Processor):
    def process(self, scene):
        self.scene = scene

        if (self.scene.action.get("grab")):
            self.grabbables = self.world.get_components(Grabbable, Position)

            for entity, (grabbable, position) in self.grabbables:
                player_position = (self.scene.playerPos.x, self.scene.playerPos.y)
                entity_position = (position.x, position.y)
                if entity_position == player_position:
                    self.world.remove_component(entity, Position)
                    self.world.remove_component(entity, Render)

            self.scene.action = {}


class CommandProcessor(esper.Processor):
    def process(self, scene):
        self.scene = scene

        if (self.scene.action.get("look_at_inventory")):
            print("INVENTORY!")

            self.scene.action = {}

class MapProcessor(esper.Processor):
    def process(self, scene):
        self.scene = scene
        self.console = self.scene.console
        self.camera = self.scene.camera

        self.process_tile_layer()
        self.process_ground_layer()
        self.process_mob_layer()

    def process_tile_layer(self):
        self.components = self.world.get_components(Position, Render, TileLayer)

        for entity, (position, render, layer) in self.components:
            if (
                (position.x + self.camera.x) >= 0
                and (position.y + self.camera.y) >= 0
            ):
                self.console.print(
                    position.x + self.camera.x,
                    position.y + self.camera.y,
                    render.icon,
                    render.color
                )

    def process_ground_layer(self):
        self.components = self.world.get_components(Position, Render, GroundLayer)

        for entity, (position, render, layer) in self.components:
            if (
                (position.x + self.camera.x) >= 0
                and (position.y + self.camera.y) >= 0
            ):
                self.console.print(
                    position.x + self.camera.x,
                    position.y + self.camera.y,
                    render.icon,
                    render.color
                )

    def process_mob_layer(self):
        self.components = self.world.get_components(Position, Render, MobLayer)

        for entity, (position, render, layer) in self.components:
            if (
                (position.x + self.camera.x) >= 0
                and (position.y + self.camera.y) >= 0
            ):
                self.console.print(
                    position.x + self.camera.x,
                    position.y + self.camera.y,
                    render.icon,
                    render.color
                )


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self, scene):
        self.scene = scene

        for event in tcod.event.get():
            if event.type == "QUIT":
                raise SystemExit()

            if event.type == "KEYDOWN":
                if event.sym == tcod.event.K_ESCAPE:
                    sys.exit()

                elif event.sym == tcod.event.K_UP:
                    self.scene.action = {"move": (0, -1)}
                elif event.sym == tcod.event.K_DOWN:
                    self.scene.action = {"move": (0, 1)}
                elif event.sym == tcod.event.K_LEFT:
                    self.scene.action = {"move": (-1, 0)}
                elif event.sym == tcod.event.K_RIGHT:
                    self.scene.action = {"move": (1, 0)}

                elif event.sym == tcod.event.K_g:
                    self.scene.action = {"grab": "self"}

                elif event.sym == tcod.event.K_i:
                    self.scene.action = {"look_at_inventory": "self"}

                elif event.sym == tcod.event.K_d and event.mod == tcod.event.KMOD_LSHIFT:
                    self.scene.debug_mode = not self.scene.debug_mode

                else:
                    self.scene.action = {}
