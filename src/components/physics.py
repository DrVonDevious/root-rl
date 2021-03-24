class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class Collision:
    def __init__(self, isSolid):
        self.isSolid = isSolid

class Grabbable:
    def __init__(self, size):
        self.size = size

class Opaque:
    pass

class Translucent:
    pass
