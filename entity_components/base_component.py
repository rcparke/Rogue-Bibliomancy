from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    from world_level import WorldLevel


class BaseComponent:
    parent: Entity  # Owning entity instance.

    @property
    def worldlevel(self) -> WorldLevel:
        return self.parent.worldlevel

    @property
    def engine(self) -> Engine:
        return self.worldlevel.engine