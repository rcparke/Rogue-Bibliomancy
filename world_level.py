from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import numpy as np
from tcod.console import Console

from entity import Actor, Item, Spell, Spellbook, Stair
import tile_types


if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor

#world generation, and filling up the world with entities
#worldlevel class, variables and methods dealing with a given level
#worldmap class, variables and methods for the current world


class WorldLevel: #functions as gamemap
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")


        self.depth=int(0)
        self.level_name=str("<Unnamed>")
        
        
        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        ) #Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        ) #tiles the player has seen before

        #self.downstairs_location = (0,0)
        #Ill need to rework the stair functionality to support
        #multiple downstair and upstair, as well as different destinations
    
    @property
    def worldlevel(self) -> WorldLevel:
        return self
    
    @property
    def actors(self) -> Iterator[Actor]:
        #Iterate over this levels living actors
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) #and entity.is_alive
        )

    @property
    def nonactors(self) -> Iterator[Entity]:
        #presumably this also does not grab corpses, do I even want corpses?
        #hopefully this is more useful than the items iterator method since I added nonitem nonactor types (spells+spellbooks)
        yield from (entity for entity in self.entities if not isinstance(entity, Actor))

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocks_movement
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity
        return None

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None
    
    def in_bounds(self, x: int, y: int) -> bool:
        #Return True if x and y are inside of the bounds of this level
        return 0 <= x < self.width and 0 <= y < self.height
    
    def render(self, console: Console) -> None:
        #Renders the level
        #if a tile is in the "visible" array, then draw it with "light" colors
        #if it is not visible but explored, then draw with "dark" colors
        #if not visible and not explored, then default to "SHROUD"
        #It is strange for this to be in the procgen file and not the engine file
        #but it might still belong here
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )


class WorldMap: #functions as gameworld
    #holds WorldLevel settings, and generates new WorldLevels
    #implement dungeon branch variables?

    def __init__(
        self,
        *,
        engine: Engine,
        level_width: int,
        level_height: int,
        #max_rooms: int,
        #room_min_size: int,
        #room_max_size: int,
        depth: int = 0,
        branchdepth: int = 0,

    ):
        self.engine=engine
        self.level_width=level_width
        self.level_height=level_height
        #max_rooms: int,
        #room_min_size: int,
        #room_max_size: int,

        self.depth=depth
        self.branchdepth=branchdepth
    #overall branch structure implementation?
    #




    #def generate_level(self) -> None:
        #passes the engine.world_level's worldmap parameters to the procgen level generation method


        #from procgen import generate_dungeon
        #self.depth += 1
        #self.engine.world_level = generate_dungeon(
    
    def generate_level(self) -> None:
        import procgen

        self.depth += 1

        #Add logic here to determining which level to generate?


        self.engine.world_level = procgen.MainBranch1.generate_level(
            depth=self.depth,
            branchdepth=self.branchdepth,
            level_width=self.level_width,
            level_height=self.level_height,
            engine=self.engine
        )

