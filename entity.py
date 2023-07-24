# incorporates entity, entity related components
from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, List, TYPE_CHECKING, Union

from engine import RenderOrder, MessageLog

if TYPE_CHECKING:
    from world_level import WorldLevel
    #imported components+gamemap in past

T = TypeVar("T", bound="Entity")

#generic entity class with lots of generic variables and methods?
class Entity:
    #Generic object to represent players, npcs, items, spells, spellbooks

    #parent: Union[WorldLevel, Inventory] how are we implementing different kinds of inventories?
    #parent is basically saying where the entity is located, is it currently on the map or in the inventory
    #parent: WorldLevel

    def __init__(
        self,
        parent: Optional[WorldLevel] = None,
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
    def worldlevel(self) -> WorldLevel:
        return self.parent.worldlevel
    
    def spawn(self: T, worldlevel: WorldLevel, x: int, y: int) -> T:
        #Spawn a copy of this instance at the given location
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = worldlevel
        worldlevel.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, worldlevel: Optional[WorldLevel] = None) -> None:
        #Place this entity at a new location. Handles moving across WorldLevels
        self.x = x
        self.y = y
        if worldlevel:
            if hasattr(self, "parent"): #Possibly unitialized
                if self.parent is self.worldlevel:
                    self.worldlevel.entities.remove(self)
            self.parent = worldlevel
            worldlevel.entities.add(self)

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
        iteminventory: List[Item] = [],
        itemcapacity: int = 0,
        spellbookinventory: List[Spellbook] = [],
        spellbookcapacity: int = 0,
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


    #def drop(self, list: List, entity: Entity) -> None: # you input which inventory list you are dropping from and the entity in that list
        #self.list.remove(entity)#hopefully it works?
        #entity.place(self.parent.x, self.parent.y, self.worldlevel)
        #self.engine.MessageLog.add_message(f"You dropped the {entity.name}.")

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

class Spell(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        manacost: int = 0,
        flowcost: float = 0,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM
        )

class Spellbook(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        manapool: int = 0,
        flowpool: float = 0,
        spellinventory: List[Spell] = [],
        spellcapacity: int = 0,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM
        )

    def drop(self, spell: Spell) -> None:
        #only one inventory list and only one type of entity to drop, so only needs which entity as input
        self.spellinventory.remove(spell)
        spell.place(self.parent.x, self.parent.y, self.worldlevel)
        self.engine.MessageLog.add_message(f"You dropped the {spell.name}.")

class Stair(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        dest_level: str = "Levelname?", #this maybe shouldnt be a string? needs to reference the destination world_level
        dest_x: int = 0,
        dest_y: int = 0,

    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.STAIR,
        )
    #implement stair destination
    #world_level destination
    #dest_level
    #dest_x
    #dest_y
    #x y destination
        self.dest_level = dest_level
        self.dest_x = dest_x
        self.dest_y = dest_y


#entity factories (definition+constructors)
player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    iteminventory=[],
    itemcapacity=26,
    spellbookcapacity=3,
)

gnome = Actor( #currently has no ai
    char="g",
    color=(63, 127, 63),
    name="Gnome",
    #ai_cls=HostileEnemy not implemented
    iteminventory=[],
    itemcapacity=26,
    spellbookcapacity=1,
)

healthpot = Item(
    char="!",
    color=[0, 255, 0],
    name="Health Pot",
    #how do we implement additional behavior?
    #implement component functionality into the item class?
)

sparkbolt = Spell(
    char="?",
    color=(127, 0, 127),
    name="Spark Bolt",
    manacost=5,
    flowcost=.1,
)

startspellbook1 = Spellbook(
    char="+",
    color=(127, 0, 0),
    name="Spellbook",
    manapool=70,
    flowpool=.5,
    spellinventory=[sparkbolt, sparkbolt],
    spellcapacity=3,
)


#maybe I have this stair code in the world_level level gen?
stairdown = Stair(
    char=">",
    color=(255,255,255),
    name="Stair",
    dest_level="Library-1",
    dest_x=1,
    dest_y=1,
)



#item related components like equipment/consumable that gives methods to items

#ai component defining actor entity behaviors

#should the item component functionality be in the item class,
#and the ai/fighter component functionality be in the actor class?