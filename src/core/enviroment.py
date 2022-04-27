import pygame
from ..base import GameObject


TILE_SIZE = 10


class Tile(GameObject):
    row_x: int
    column_y: int
    sprite: pygame.Surface
    rect: pygame.Rect

    def __init__(self, sprite_file: str, x: int, y: int):
        super().__init__(sprite_file)
        self.sprite = pygame.image.load(sprite_file).convert_alpha()
        self.rect = self.sprite.get_rect(center=(x, y))
        self._x = x
        self._y = y

    @property
    def row(self):
        return self.row_x

    @property
    def column(self):
        return self.column_y


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

    def draw(self, display, dx, dy):
        for i in self._cont:
            for j in i:
                j.draw(display, dx, dy)

    def set(self, coords: tuple[int, int], new: Tile):
        if coords[0] > self.width or coords[1] > self.height:
            raise Exception("Invalid coordinates")

        self._cont[coords[1]][coords[0]] = new

    def get(self, coords: tuple[int, int]):
        if coords[0] > self.width or coords[1] > self.height:
            raise Exception("Invalid coordinates")

        return self._cont[coords[1]][coords[0]]