#procgen functions for generating a gamemap/level, with classes for structures (like rectangular room)
#world generation, and filling up the world with entities

from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING

import tcod

from world_level import WorldLevel
import tile_types
import entity

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

#using a similar object structure to event handlers in input_handlers.py
class Branch:
    def __init__(self, branchdepth: int):
        self.branchdepth = branchdepth

        #I could move duplicate branch code to here


class Entrance(Branch):

    def generate_level(
        self,
        branchdepth: int,
        level_width: int,
        level_height: int,
        engine: Engine,
    ) -> WorldLevel:

        player = engine.player
        level = WorldLevel(engine, level_width, level_height, entities=[player])
        branch = "Entrance"

        level.level_name=f"{branch}-{branchdepth}"
        #use f strings to have it be accurate for subsequent levels in branch


        #outerwall = (slice(0,level_width), slice(0,level_height))
        innerfloor = (slice(1,level_width-1), slice(1,level_height-1))

        #level.tiles[outerwall] = tile_types.wall #fill entire level with wall
        level.tiles[innerfloor] = tile_types.floor #fill entire level with floor except the outer edge?

        #level.tiles[(42,42)] = tile_types.wall 42 is visible, 43 is a black empty border
        
        #player.place(1,1,level)
        stairdown = entity.stairdown
        
        stairdown.dest_branch = "Library"
        stairdown.dest_branchdepth = 1
        stairdown.dest_x = 1
        stairdown.dest_y = 1

        stairdown.place(1, 1, level)

        return level
    
class Library(Branch):

    def generate_level(
        self,
        branchdepth: int, #if 0, ignore and increment currentbranchdepth
        #if not 0, check if the level already exists?
        #if not 0 and does not exist, generate it
        level_width: int,
        level_height: int,
        engine: Engine,
    ) -> WorldLevel:

        #I need to double check if I am correctly using instance variables vs class variables

        player = engine.player
        level = WorldLevel(engine, level_width, level_height, entities=[player])
        
        branch = "Library"

        level.level_name=f"{branch}-{branchdepth}"
        #use f strings to have it be accurate for subsequent levels in branch


        #outerwall = (slice(0,level_width), slice(0,level_height))
        innerfloor = (slice(1,level_width-1), slice(1,level_height-1))

        #level.tiles[outerwall] = tile_types.wall #fill entire level with wall
        level.tiles[innerfloor] = tile_types.floor #fill entire level with floor except the outer edge?
        
        #player.place(1,1,level)

        return level