from src.util.sequence import Sequence
import pygame
from src.entity.game_object import GameObject
from src import global_vars


class Camera:
    lock_obj: GameObject
    obj_group: Sequence[GameObject]
    display: pygame.Surface
    width: int
    height: int
    glb_x: int
    glb_y: int

    def __init__(self, lock_object, width, height):
        self.display = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface()
        self.lock_obj = lock_object
        self.width = width
        self.height = height
        self.obj_group = Sequence[GameObject]()

    def draw(self):
        self.display.blit(self.surface)

    def get_center_coords(self):
        """
        Returns camera's center's global coordinates
        """
        size = self.display.get_size()
        return ((size[0] // 2) + self.glb_x, (size[1] // 2) + self.glb_y)   
