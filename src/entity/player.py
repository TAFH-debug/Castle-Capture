from src.entity import unitc
from src.entity.nulls import NULL_UNIT

class Player():
    unit: unitc.Unit

    def __init__(self):
        self.unit = NULL_UNIT

    def move(direction: str):
      if direction == "forward":
        self.unit.y -= 1
      elif direction == "back":
        self.unit.y += 1
      elif direction == "right":
        self.unit.x += 1
      elif direction == "left":
        self.unit.x -= 1