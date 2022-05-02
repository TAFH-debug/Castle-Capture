from enum import Enum


class TileSprites(Enum):
    default = "sprites/ohno.png"
    water = "sprites/tiles/tile_73.png"
    # region Sand tiles
    tp_lt_sand = "sprites/tiles/tile_01.png"
    tp_sand = "sprites/tiles/tile_02.png"
    tp_rt_sand = "sprites/tiles/tile_03.png"
    sand = "sprites/tiles/tile_04.png"
    lt_sand = "sprites/tiles/tile_17.png"
    rt_sand = "sprites/tiles/tile_19.png"
    bt_lt_sand = "sprites/tiles/tile_33.png"
    bt_sand = "sprites/tiles/tile_34.png"
    bt_rt_sand = "sprites/tiles/tile_35.png"
    # endregion

    def to_str(self) -> str:
        return self.value

