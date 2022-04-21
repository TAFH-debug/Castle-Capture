import pygame
from src import global_vars

TILE_SIZE = 10

class Tile:
    #global coordinates
    _x: int
    _y: int
    sprite: pygame.Surface
    rect: pygame.Rect

    def __init__(self, sprite_file: str, x: int , y: int):
        self.sprite = pygame.image.load(sprite_file).convert_alpha()
        self.rect = self.sprite.get_rect(center=(x, y))
        self._x = x
        self._y = y

    def draw(self):
        pyg_c = Tiles.to_pygame_coords((self._x, self._y))
        self.rect.x = pyg_c[0]
        self.rect.y = pyg_c[1]
        gv.display.blit(self.sprite, self.rect)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y 

class Tiles:
    _cont: list[list[Tile]]
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self._cont = list()
        self.width = width
        self.height = height

        for i in range(height):
            self._cont.append(list())

    def draw(self):
        for i in self._cont:
            for j in i:
                j.draw()

    def set(self, coords: tuple[int, int], new: Tile):
        if coords[0] > self.width or coords[1] > self.height:
            raise Exception("Invalid coordinates")

        self._cont[coords[1]][coords[0]] = new

    def get(self, coords: tuple[int, int]):
        if coords[0] > self.width or coords[1] > self.height:
            raise Exception("Invalid coordinates")

        return self._cont[coords[1]][coords[0]]

    @staticmethod    
    def to_global_coords(coords: tuple[int, int]):
        import global_vars as gv
        return (gv.camera.glb_x + coords[0], gv.camera.glb_y + coords[1])

    @staticmethod    
    def to_pygame_coords(coords: tuple[int, int]):
        import global_vars as gv
        return (gv.camera.glb_x + coords[0], gv.camera.glb_y + coords[1])

class World:
    tiles: Tiles

    def __init__(self, width: int, height: int):
        self.tiles = Tiles(width, height)

    def update(self):
        pass     