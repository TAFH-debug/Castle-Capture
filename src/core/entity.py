from ..base import GameObject
import pygame


class UnitType:
    sprite_file: str
    speed: int

    def __init__(self, sprite_file: str, speed: int):
        self.speed = speed
        self.sprite_file = sprite_file


class Unit(GameObject):
    type: UnitType

    def __init__(self, _type: UnitType, x: int, y: int):
        super().__init__(_type.sprite_file)
        self.x = x
        self.y = y
        self.type = _type


class Player:
    unit: Unit

    def __init__(self, unit=None):
        self.unit = unit
