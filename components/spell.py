from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item

class Spell(BaseComponent): # I might need subcategories of spells, like projectile vs proj modifier vs multicast
    parent: Item
    def __init__(
        self,
        mana_cost: int,
        flow_capacity: int,
        lifetime: int,
        speed: int,
    ):
        self.mana_cost=mana_cost
        self.flow_capacity=flow_capacity
        self.lifetime=lifetime # Amount of turns spell lasts
        self.speed=speed # Amount of spaces spell travels per turn

class SparkBolt(Spell):
    def __init__(self) -> None:
        super().__init__(mana_cost=5, flow_capacity=.1, lifetime=1, speed=16)

class FireBolt(Spell):
    def __init__(self) -> None:
        super().__init__(mana_cost=10, flow_capacity=.15, lifetime=2, speed=4)