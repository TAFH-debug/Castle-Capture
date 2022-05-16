from . import Unit
import math
from ..base import zero


class EnemyUnit(Unit):

    def destroy(self):
        super().destroy()
        self.ai = zero

    def ai(self, targetx, targety):
        dx = targetx - self.x
        dy = targety - self.y
        if dx == 0:
            k = 0
        else:
            k = math.degrees(math.atan(dy / dx))
        self.rot_angle = int(k + 90)
        if dx < 0:
            self.rot_angle += 180
        rng = math.sqrt(dx**2 + dy**2)
        if rng > 200:
            self.x += (1 / rng) * dx
            self.y += (1 / rng) * dy
        else:
            self.shoot(targetx, targety)



