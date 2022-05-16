import pygame
from ..base import GameObject

TILESIZE = 60


class Tile(GameObject):
    sprite: pygame.Surface
    is_water: bool
    ttype: str
    rect: pygame.Rect

    def __init__(self, sprite_file: str, is_water: bool):
        super().__init__(sprite_file)
        self.sprite = pygame.image.load(sprite_file).convert_alpha()
        self.rect = self.sprite.get_rect()
        #self.ttype = ttype
        self.is_water = is_water
        self.x = 0
        self.y = 0


class Tiles:
    _cont: list
    size: int

    def __init__(self, size: int):
        self._cont = list()
        self.size = size

        for i in range(size):
            self._cont.append(list())
            for j in range(size):
                self._cont[i].append(None)

    def draw(self, display, dx, dy):
        for i in self._cont:
            for j in i:
                if j:
                    j.draw(display, dx, dy)

    def set(self, coords: tuple, new: Tile):
        if coords[0] > self.size or coords[1] > self.size:
            raise Exception("Invalid coordinates")

        new.x = coords[0] * TILESIZE
        new.y = coords[1] * TILESIZE
        self._cont[coords[1]][coords[0]] = new

    def get_nearby_tiles(self, coords: tuple) -> list:
        i = coords[0]
        j = coords[1]
        result = []
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                try:
                    result.append(self._cont[j + dj][i + di])
                except IndexError:
                    pass
        return result

    def get(self, coords: tuple) -> Tile:
        if coords[0] > self.size or coords[1] > self.size:
            raise Exception("Invalid coordinates")

        return self._cont[coords[1]][coords[0]]

    def get_cont(self):
        return self._cont
