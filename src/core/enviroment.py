import pygame
from ..base import GameObject

TILESIZE = 60


class Tile(GameObject):
    sprite: pygame.Surface
    rect: pygame.Rect

    def __init__(self, sprite_file: str):
        super().__init__(sprite_file)
        self.sprite = pygame.image.load(sprite_file).convert_alpha()
        self.rect = self.sprite.get_rect()
        self.x = 0
        self.y = 0


class Tiles:
    _cont: list[list[Tile]]
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

    def set(self, coords: tuple[int, int], new: Tile):
        if coords[0] > self.size or coords[1] > self.size:
            raise Exception("Invalid coordinates")

        new.x = coords[0] * TILESIZE
        new.y = coords[1] * TILESIZE
        self._cont[coords[1]][coords[0]] = new

    def get(self, coords: tuple[int, int]):
        if coords[0] > self.size or coords[1] > self.size:
            raise Exception("Invalid coordinates")

        return self._cont[coords[1]][coords[0]]