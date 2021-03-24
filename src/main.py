#!/usr/bin/env python3
import configparser
import tcod
import esper
import time

from game_map import Map
from camera import Camera
from factories.player import Player
from factories.ground_clutter import Rock
from components.physics import Position, Velocity, Grabbable
from components.graphics import Render

from processors import\
    MovementProcessor,\
    MapProcessor,\
    InputProcessor,\
    ActionProcessor,\
    CommandProcessor


class SceneManager:
    def __init__(self, world = None, state = "game", context = None, console = None):
        self.world = world
        self.context = context
        self.console = console

        self.scenes = {
            "game": Game(self.world, self.context, self.console)
        }

        self.current_scene = self.scenes["game"]

    def run(self):
        while True:
            self.current_scene.update()


class Game():
    def __init__(self, world = None, context = None, console = None):
        self.world = world
        self.context = context
        self.console = console

        self.action = {}

        self.playerFactory = Player(self.world)
        self.rockFactory = Rock(self.world)
        self.camera = Camera()

        self.fps = 1.0
        self.start_time = time.time()
        self.fps_span = 1
        self.fps_counter = 0
        self.debug_mode = False

        # rock testing
        self.rock = self.rockFactory.assemble_rock("flint", 4, -10)
        self.rock = self.rockFactory.assemble_rock("stone", 14, 7)
        self.rock = self.rockFactory.assemble_rock("gneiss", 9, -1)
        self.rock = self.rockFactory.assemble_rock("sandstone", -4, 8)

        self.player = self.playerFactory.assemble_player()
        self.playerPos = self.world.component_for_entity(self.player, Position)
        self.playerVel = self.world.component_for_entity(self.player, Velocity)

        self.game_map = Map(
            self.world,
            self.playerPos,
            12,
            10,
            8,
            8
        )

        self.camera.initCamera(40, 25)

        self.world.add_processor(MovementProcessor())
        self.world.add_processor(ActionProcessor())
        self.world.add_processor(CommandProcessor())
        self.world.add_processor(MapProcessor())
        self.world.add_processor(InputProcessor())

        self.game_map.generate_map()

        self.console.print(
            0,
            49,
            f"Player Position: {self.playerPos.x}, {self.playerPos.y}",
            (255, 255, 255)
        )

    def update(self):
        self.world.process(self)

        self.fps_counter += 1
        if (time.time() - self.start_time) > self.fps_span:
            self.fps = int(self.fps_counter / (time.time() - self.start_time))
            self.fps_counter = 0
            self.start_time = time.time()

        if self.debug_mode:
            self.console.print(
                0,
                47,
                f"FPS: {self.fps}",
                (255, 255, 0)
            )

            self.console.print(
                0,
                48,
                f"Chunk: {int(self.playerPos.x / self.game_map.chunkWidth)}, {int(self.playerPos.y / self.game_map.chunkHeight)}",
                (255, 255, 255)
            )

            self.console.print(
                0,
                49,
                f"Player Position: {self.playerPos.x}, {self.playerPos.y}",
                (255, 255, 255)
            )

        self.context.present(self.console)
        self.console.clear()


def main() -> None:
    config = configparser.ConfigParser()
    config.read("root.ini")

    world = esper.World()

    title = "Root"

    vsync = config["graphics"]["vsyncEnabled"] == "True"

    screenWidth = int(config["graphics"]["screenWidth"])
    screenHeight = int(config["graphics"]["screenHeight"])

    tilesetWidth = int(config["graphics"]["tilesetWidth"])
    tilesetHeight = int(config["graphics"]["tilesetHeight"])

    tileset = tcod.tileset.load_tilesheet(
        "assets/" + config["graphics"]["tilesetfile"],
        tilesetWidth,
        tilesetHeight,
        tcod.tileset.CHARMAP_CP437
    )

    with tcod.context.new_terminal(
        screenWidth,
        screenHeight,
        tileset = tileset,
        title = title,
        vsync = vsync,
    ) as context:
        console = tcod.Console(screenWidth, screenHeight, order = "F")

        game = SceneManager(world, "main-menu", context, console)
        game.run()


if __name__ == "__main__":
    main()

