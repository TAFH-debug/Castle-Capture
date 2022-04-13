from src.entity import unitc
from src.entity.nulls import NULL_UNIT

class Player():
    unit: unitc.Unit

    def __init__(self):
        self.unit = NULL_UNIT