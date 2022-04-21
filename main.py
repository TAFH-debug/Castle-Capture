import pygame
from src.enviroment.world import Tile
from src import global_vars as gv
from src.event import event
import threading


def init():
    pygame.init()
    gv.init()
    klisten_thread = threading.Thread(target = event.listen_keys)
    klisten_thread.daemon = True
    klisten_thread.start()

def main():
    while gv.running:
        gv.display.fill((0, 0, 0))
        event.on_event(pygame.event.get())
        gv.world.tiles.set(Tile("tile.png", 0, 0))
        gv.world.tiles.draw()
        gv.player.unit.draw(gv.display)
        pygame.display.flip()

if __name__ == "__main__":
    init()
    main()