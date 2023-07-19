from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Spell, Spellbook


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        #Return the engine this action belongs to
        return self.entity.worldlevel.engine
    
    def perform(self) -> None:
        #Perform this action with the objects needed to determine its scope
        #self.engine is the scope this action is being performed in
        #self.entity is the object performing the action
        #This method must be overridden by Action subclasses
        raise NotImplementedError()
    
class WaitAction(Action):
    def perform(self) -> None:
        pass

class TakeStairsAction(Action):
    def perform(self) -> None:
        #Take stairs, if any exist at the entities location

        #access the information in the stair entity, and then place the entity
        #use the place entity method to move between WorldLevels
        raise NotImplementedError()
class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    
    @property
    def dest_xy(self) -> Tuple[int, int]:
        #Returns this actions destination
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property
    def blocking_entity(self) -> Optional[Entity]:
        #Return the blocking entity at this actions destination
        return self.engine.world_level.get_blocking_entity_at_location(*self.dest_xy)
    
    def target_actor(self) -> Optional[Actor]:
        #Return the actor at this actions destination
        return self.engine.world_level.get_actor_at_location(*self.dest_xy)
    
    def perform(self) -> None:
        raise NotImplementedError()
    

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.world_level.in_bounds(dest_x, dest_y):
            #Destination is out of bounds
            raise exceptions.Impossible("That direction doesnt exist.")
        
        if not self.engine.world_level.tiles["walkable"][dest_x, dest_y]:
            #Destination is blocked by a tile
            raise exceptions.Impossible("That direction is blocked by a tile.")
        if self.engine.world_level.get_blocking_entity_at_location(dest_x, dest_y):
            #Destination is blocked by an entity
            raise exceptions.Impossible("That direction is blocked by an entity.")
        
        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        #Used to differentiate different directional actions, maybe Ill want a default kick attack?
        #if self.target_actor:
            #return MeleeAction(self.entity, self.dx, self.dy).perform()

        #else:
            return MovementAction(self.entity, self.dx, self.dy).perform()