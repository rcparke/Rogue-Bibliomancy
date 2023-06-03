# incorporates entity, entity related components
from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from engine import RenderOrder

#if TYPE_CHECKING:
    #imported components+gamemap in past

T = TypeVar("T", bound="Entity")

#generic entity class with lots of generic variables and methods?
class Entity:
    #Generic object to represent players, npcs, items, spells, spellbooks

    #parent: Union[WorldMap, Inventory] how are we implementing different kinds of inventories?
    #parent is basically saying where the entity is located, is it currently on the map or in the inventory


    def __init__(
        self,
        parent: Optional[WorldMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            #if parent isnt provided now then it will be set later
            self.parent = parent
            parent.entities.add(self)
    @property
    def worldmap(self) -> WorldMap:
        return self.parent.worldmap
    
    def spawn(self: T, worldmap: WorldMap, x: int, y: int) -> T:
        #Spawn a copy of this instance at the given location
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = worldmap
        worldmap.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, worldmap: Optional[WorldMap] = None) -> None:
        #Place this entity at a new location. Handles moving across WorldMaps
        self.x = x
        self.y = y
        if worldmap:
            if hasattr(self, "parent"): #Possibly unitialized
                if self.parent is self.worldmap:
                    self.worldmap.entities.remove(self)
            self.parent = worldmap
            worldmap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        #Return distance between the current entity and the given (x, y) coordinates
        return math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
    
    def move(self, dx: int, dy: int) -> float:
        #Move the entity by a given amount
        self.x += dx
        self.y += dy

#actor entity class
class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int],
        name: str = "<Unnamed>",
        #ai_cls: Type[BaseAI],

        #equipment: Equipment,
        #fighter: Fighter,
        #inventory: Inventory,
        #level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        #instanced component variables, need to be reworked for rework of components

        #self.ai: Optional[BaseAI] = ai_cls(self)

        #self.equipment: Equipment = equipment
        #self.equipment.parent = self

        #self.fighter = fighter
        #self.fighter.parent = self

        #self.inventory = inventory
        #self.inventory.parent = self

        #self.level = level
        #self.level.parent = self

        @property
        def is_alive(self) -> bool:
            #Returns true while this actor can perform actions
            return bool(self.ai)
        
#item entity class (will the spell and spellbook be separate kinds of entities or special items?)
class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        #consumable: Optional[Consumable] = None,
        #equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        #self.consumable = consumable

        #if self.consumable:
            #self.consumable.parent = self

        #self.equippable = equippable

        #if self.equippable:
            #self.equippable.parent = self

#entity factories (definition+constructors)

#item related components like equipment/consumable that gives methods to items

#ai component defining actor entity behaviors
