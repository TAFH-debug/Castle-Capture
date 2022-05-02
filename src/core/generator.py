from . import Tiles, Tile
from . import TileSprites
import random


def bool_chance(probability: float):
    return random.random() <= probability


def generate_map(world_size: int) -> Tiles:
    tiles = Tiles(world_size)
    island_size = random.randint(5, 10)
    island_coords = (random.randint(world_size // 20, world_size - world_size // 20),
                     random.randint(world_size // 20, world_size - world_size // 20))

    for i in range(world_size):
        for j in range(world_size):
            if in_range((i, j), island_coords, island_size):
                nearby = tiles.get_nearby_tiles((i, j))
                chance = 0.3
                for ti in nearby:
                    if not ti:
                        continue
                    if not ti.is_water:
                        chance += 0.20
                    else:
                        chance -= 0.005
                is_sand = bool_chance(chance)
                sprite = TileSprites.water
                if is_sand:
                    sprite = TileSprites.sand
                tiles.set((i, j), Tile(sprite.to_str(), not is_sand))
            else:
                tiles.set((i, j), Tile(TileSprites.water.to_str(), True))
    return tiles


def in_range(coord: tuple[int, int], top_left: tuple[int, int], size: int):
    return (top_left[0] <= coord[0] <= top_left[0] + size) and (top_left[1] <= coord[1] <= top_left[1] + size)
