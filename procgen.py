#procgen functions for generating a gamemap/level, with classes for structures (like rectangular room)

from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import tcod

from world_level import WorldLevel
import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class MainBranch1:
    def __init__(self, depth: int, branchdepth: int):
        self.depth = depth
        self.branchdepth = branchdepth
        #depth is the number of levels from the surface, branchdepth is the number of levels from the start of the branch
        #depth is potentially used for determining entity's (deeper=harder), branchdepth is used for different features at certain branch levels


    def generate_level(
        depth: int,
        branchdepth: int,

        level_width: int,
        level_height: int,
        engine: Engine,
    ) -> WorldLevel:

        player = engine.player
        level = WorldLevel(engine, level_width, level_height, entities=[player])



        level.tiles[slice(0,level_width), slice(0,level_height)] = tile_types.wall #fill entire level with wall
        level.tiles[slice(1,level_width-1), slice(1,level_width-1)] = tile_types.floor #fill entire level with floor except the outer edge?
#uses the worldlevel tiles object, not sure if I am using it correctly
