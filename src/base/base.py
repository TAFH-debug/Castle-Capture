import pygame


class GameObject:
    sprite: pygame.Surface
    rect: pygame.Rect
    x: int
    y: int
    rot_angle: int

    def __init__(self, sprite="sprites/ohno.png", x=0, y=0):
        self.x = x
        self.y = y
        self.rot_angle = 0
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.rect = self.sprite.get_rect()

    def draw(self, display: pygame.Surface, dx, dy):
        sprite = pygame.transform.rotate(self.sprite, self.rot_angle)
        self.rect.x = -(display.get_width() / 2) + (self.x - dx)
        self.rect.y = (display.get_height() / 2) - (self.y - dy)
        display.blit(sprite, self.rect)

    def update(self):
        pass


class Camera:
    lock_obj: GameObject
    x: int
    y: int

    def __init__(self, lock_object=None):
        self.lock_obj = lock_object
        self.x = 0
        self.y = 0
