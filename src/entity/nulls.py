from src.entity import unitc
import pygame

class _NullUnit(unitc.Unit):
    
    def __init__(self):
        pass

    def set_position(self, coord: tuple[int, int]):
        pass

    def draw(self, screen: pygame.Surface):
        pass
    

NULL_UNIT = _NullUnit()