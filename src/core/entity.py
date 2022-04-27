import pygame

from ..base import GameObject


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

    def move(self, direction: str):
        match direction:
            case "forward":
                if self.unit.rot_angle < 180:
                    self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
                elif self.unit.rot_angle > 180:
                    self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
                self.unit.y += 1
            case "back":
                if self.unit.rot_angle >= 180:
                    self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
                elif self.unit.rot_angle < 180 and self.unit.rot_angle != 0:
                    self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
                self.unit.y -= 1
            case "right":
                if 90 < self.unit.rot_angle < 270:
                    self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
                elif self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                    self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
                self.unit.x += 1
            case "left":
                if self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                    self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
                elif self.unit.rot_angle < 270:
                    self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
                self.unit.x -= 1