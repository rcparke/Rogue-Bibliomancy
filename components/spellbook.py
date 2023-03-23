from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.spell import Spell
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item

class Spellbook(BaseComponent):
    parent: Item

    def __init__(self, flow_rate: int, spell_capacity: int, spell_inventory=[Spell]):
        self.flow_rate=flow_rate
        self.spell_capacity=spell_capacity
        self.spell_inventory=spell_inventory

    # I need to implement the spell_inventory, it should be a list
    # I will also need a bunch of actions/interface stuff
    # similar to the equipping actions?
    # Finally, I also need to have a way to have spellbooks spawn with semi random statistics/spell contents