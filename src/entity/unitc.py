import pygame

class UnitType:
    sprite: pygame.Surface
    speed: int

    def __init__(self, sprite_file: str, speed: int):
        self.speed = speed
        self.sprite = pygame.image.load(sprite_file).convert_alpha()


class Unit(pygame.sprite.Sprite):
    type: UnitType
    x: int
    y: int

    def __init__(self, type: UnitType, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        self.type = type
        self.image = type.sprite
        self.rect = type.sprite.get_rect()

    def set_position(self, coord: tuple[int, int]):
        self.x = coord[0]
        self.y = coord[1]
            
    def draw(self, screen: pygame.Surface):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)
