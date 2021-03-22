from chunk import Chunk

class ChunkCoords(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map():
    def __init__(
        self,
        world,
        player,
        mapWidth,
        mapHeight,
        chunkWidth,
        chunkHeight
    ):
        self.world = world
        self.player = player
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.chunkWidth = chunkWidth
        self.chunkHeight = chunkHeight

        self.loadedChunks = []

    def generate_map(self):
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                newX = (x - int(self.mapWidth / 2))
                newY = (y - int(self.mapHeight / 2))

                Chunk.generate_chunk(
                    self.world,
                    newX,
                    newY,
                    self.chunkWidth,
                    self.chunkHeight
                )

                self.loadedChunks.append([newX, newY])



    def generate_new_chunks(self, direction = None):
        self.currentChunk = self.current_player_chunk()

        self.new_x_coord = self.currentChunk.x
        self.new_y_coord = self.currentChunk.y

        if (direction == "north"):
            self.new_y_coord = (self.currentChunk.y - int(self.mapHeight / 2))
            self.generate_chunk_line_y(self.new_y_coord)
        elif (direction == "south"):
            self.new_y_coord = (self.currentChunk.y + int(self.mapHeight / 2))
            self.generate_chunk_line_y(self.new_y_coord)
        elif (direction == "west"):
            self.new_x_coord = (self.currentChunk.x - int(self.mapWidth / 2))
            self.generate_chunk_line_x(self.new_x_coord)
        elif (direction == "east"):
            self.new_x_coord = (self.currentChunk.x + int(self.mapWidth / 2))
            self.generate_chunk_line_x(self.new_x_coord)

    def generate_chunk_line_y(self, y):
        self.currentChunk = self.current_player_chunk()

        for x in range(self.mapWidth):
            if not (self.loadedChunks.count([x + (self.currentChunk.x - int(self.mapWidth / 2)), y])):
                Chunk.generate_chunk(
                    self.world,
                    x + (self.currentChunk.x - int(self.mapWidth / 2)),
                    y,
                    self.chunkWidth,
                    self.chunkHeight
                )

                self.loadedChunks.append([x + self.currentChunk.x - int(self.mapWidth / 2), y])

    def generate_chunk_line_x(self, x):
        self.currentChunk = self.current_player_chunk()

        for y in range(self.mapHeight):
            if not (self.loadedChunks.count([x, y + (self.currentChunk.y - int(self.mapHeight / 2))])):
                Chunk.generate_chunk(
                    self.world,
                    x,
                    y + (self.currentChunk.y - int(self.mapHeight / 2)),
                    self.chunkWidth,
                    self.chunkHeight
                )

                self.loadedChunks.append([x, y + self.currentChunk.y - int(self.mapHeight / 2)])

    def current_player_chunk(self):
        self.coords = ChunkCoords(
            int(self.player.x / self.chunkWidth),
            int(self.player.y / self.chunkHeight)
        )

        return self.coords
