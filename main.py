import random

import pygame.sprite

from src.core import *

world_size = 20
display = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Castle Capture")
running = True
player = Player()
cam_x = -400
cam_y = 100
tiles = Tiles(world_size)
clock = pygame.time.Clock()
state = "menu"


def onclick_strt(but):
    global state
    state = "game"


def onclick_exit(but):
    global state
    pygame.quit()


button_exit = Button(onclick_exit, x=500, y=400, width=120, height=50, text="Exit", sprite_path="./sprites/button.png")
button_strt = Button(onclick_strt, x=500, y=280, width=120, height=50, text="Start", sprite_path="./sprites/button.png")
menu_widgets = [button_strt, button_exit]
units = []
enemys = []
castle = None


def spawn():
    while True:
        if state != "game": continue
        time.sleep(5)
        enemy = EnemyUnit(UnitType("sprites/ships/ship (3).png", 1,
                                   "sprites/ships/ship (21).png",
                                   "sprites/ships/ship (9).png"),
                          random.randint(0, 1000),
                          random.randint(900, 1000),
                          team="enemy")
        units.append(enemy)
        enemys.append(enemy)


def init():
    pygame.init()
    threading.Thread(target=spawn, daemon=True).start()
    threading.Thread(target=listen_keys, daemon=True).start()


def draw_fps():
    f1 = pygame.font.Font(None, 20)
    text = f1.render(str(int(clock.get_fps())), True, (0, 0, 0))
    display.blit(text, (0, 0))


def draw_ui():
    display.fill((130, 20, 144))
    for i in menu_widgets:
        i.draw(display, cam_x, cam_y)
    pygame.display.flip()


def draw():
    display.fill((0, 0, 0))
    tiles.draw(display, cam_x, cam_y)
    for i in units:
        i.draw(display, cam_x, cam_y)
    draw_fps()
    pygame.display.flip()


def check_shots():
    for _ in units:
        for bullet in _.bullets:
            for unit in units:
                if not unit.is_owner(bullet) and pygame.sprite.collide_rect(bullet, unit) and not bullet.destroying:
                    bullet.lifetime = 0
                    unit.health -= bullet.damage
                    if unit.health <= 0:
                        unit.destroy()


def physics():
    check_shots()
    global cam_y
    global cam_x
    pl_coords = (player.unit.x + 30, player.unit.y + 30)
    pl_coords2 = (player.unit.x, player.unit.y)
    coords = ((player.unit.x + 30) // TILESIZE, (player.unit.y + 30) // TILESIZE)
    nearby = tiles.get_nearby_tiles(coords)
    for i in nearby:
        if i.is_water:
            continue
        if gen.in_range(pl_coords, (i.x, i.y), TILESIZE) or gen.in_range(pl_coords2, (i.x, i.y), TILESIZE):
            if player.unit.x - i.x > player.unit.y - i.y:
                dx = player.unit.x - i.x
                player.unit.x -= dx
                cam_x -= dx
            else:
                dy = player.unit.y - i.y
                player.unit.y -= dy
                cam_y -= dy


def update_ui():
    for i in menu_widgets:
        if i.update():
            time.sleep(0.1)
            continue


def menu():
    draw_ui()
    update_ui()


def update():
    global state
    idx = None
    for i in range(len(units)):
        if units[i].to_remove:
            idx = i
        units[i].update()
    if idx != None:
        try:
            enemys.remove(units[idx])
        except:
            pass
        units.pop(idx)
    for i in enemys:
        if i.destroyed: continue
        castle.ai(i.x, i.y)
        i.ai(player.unit.x, player.unit.y)
    if player.unit not in units:
        state = "gameover"


def draw_gameover():
    display.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    display.blit(font.render("Game over", True, (0, 255, 0)), (500, 250))
    pygame.display.flip()


def main():
    global units
    global tiles
    global enemys
    global castle
    player.unit = Unit(UnitType("sprites/ships/ship (1).png", 1,
                                "sprites/ships/ship (19).png",
                                "sprites/ships/ship (7).png"), 700, 200)
    castle = Castle(700, 200)
    units = [player.unit]
    units.extend(castle.tiles)
    tiles = gen.generate_map(world_size)
    while is_quit(pygame.event.get()):
        clock.tick(60)
        if state == "menu":
            menu()
        elif state == "game":
            update()
            physics()
            draw()
        elif state == "gameover":
            print("a")
            draw_gameover()


def move(self, direction: str):
    global cam_x
    global cam_y
    if True:
        if direction == "forward":
            if self.unit.rot_angle < 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle > 180:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y += 1
            cam_y += 1
        if direction == "back":
            if self.unit.rot_angle >= 180:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            elif self.unit.rot_angle < 180 and self.unit.rot_angle != 0:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            self.unit.y -= 1
            cam_y -= 1
        if direction == "right":
            if 90 < self.unit.rot_angle < 270:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            elif self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            self.unit.x += 1
            cam_x += 1
        if direction == "left":
            if self.unit.rot_angle > 270 or self.unit.rot_angle < 90:
                self.unit.rot_angle = (self.unit.rot_angle - 1) % 360
            elif self.unit.rot_angle < 270:
                self.unit.rot_angle = (self.unit.rot_angle + 1) % 360
            self.unit.x -= 1
            cam_x -= 1


def listen_keys():
    while True:
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            global state
            state = "menu"
        if mouse[0]:
            pos = pygame.mouse.get_pos()
            conv_x = pos[0] + (display.get_width() / 2) + cam_x
            mconv_y = pos[1] - (display.get_height() / 2) - cam_y
            player.unit.shoot(conv_x, -mconv_y)
        if keys[pygame.K_w]:
            move(player, "forward")
        if keys[pygame.K_a]:
            move(player, "left")
        if keys[pygame.K_s]:
            move(player, "back")
        if keys[pygame.K_d]:
            move(player, "right")
        time.sleep(0.01)


if __name__ == "__main__":
    init()
    main()
