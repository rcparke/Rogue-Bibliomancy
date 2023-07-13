# incorporates the render functions, render order, engine.py, message log?

#engine class from engine.py

from __future__ import annotations

from typing import Tuple, Iterable, List, Reversible, TYPE_CHECKING
from enum import auto, Enum
import lzma
import pickle

import textwrap
from tcod.console import Console
from tcod.map import compute_fov
#message log originally imported entire tcod, might need adjust
import color

import exceptions


if TYPE_CHECKING:
    from entity import Actor
    from world_level import WorldMap, WorldLevel

class Engine:
    world_level: WorldLevel
    world_map: WorldMap

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0,0)
        self.player = player
    
    def handle_npc_turns(self) -> None:
        for entity in set(self.world_level.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass # ignore impossible actions from ai

    def update_fov(self) -> None:
        #Recompute the visible area based on the players point of view
        #might want to adjust to allow for other mechanics to give additional/remote sight?
        self.world_level.visible[:] = compute_fov(
            self.world_level.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        #if a tile is "visible" it should be added to "explored"
        self.world_level.explored |= self.world_level.visible

    def render(self, console: Console) -> None:
        self.world_level.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar( #health bar, pulled hp current and max values from fighter component, now empty
            console=console,
            current_value=10,#update
            maximum_value=20,#update
            total_width=20,
        )

        render_world_level(
            console=console,
            world_level=self.world_level.depth,
            location=(0,47),
        )

        render_names_at_mouse_location( #could expand to not be just names?
            console=console, x=21, y=44, engine=self
        )

def save_as(self, filename: str) -> None:
    #Save this Engine instance as a compressed file
    save_data = lzma.compress(pickle.dumps(self))
    with open(filename, "wb") as f:
        f.write(save_data)

#render functions from render functions

def get_names_at_location(x: int, y: int, world_level: WorldLevel) -> str:
    if not world_level.in_bounds(x, y) or not world_level.visible[x, y]:
        return ""
    
    names = ", ".join(
        entity.name for entity in world_level.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def render_bar( #bar that displays fill from left to right being used for hp, location on screen predefined
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=0, y=45, width=20, height=1, ch=1, bg=color.white) #will need to update colors

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.red
        )
    
    console.print(
        x=1, y=45, string=f"HP: {current_value}/{maximum_value}", fg=color.white
    )

def render_world_level(
    console: Console, world_level: int, location: Tuple[int, int]
) -> None:
    #Render the level the player is currently on, at the given location
    x, y = location

    console.print(x=x, y=y, string=f"Current World Level: {world_level}")

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, world_level=engine.world_level
    )

    console.print(x=x, y=y, string=names_at_mouse_location)
#render order class
class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

#message and messagelog classes
class Message:
    def __init__(self, text:str, fg:Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        #the full text of this message, including the count if necessary
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text
    
class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = color.white, *, stack: bool = True,
    ) -> None:
        #add a message to the log
        #"text" is the message text, "fg" is the text color
        #if "stack" is true then the message can stack with a previous message of the same text
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: Console, x: int, y: int, width: int, height: int,
    ) -> None:
        #render this log over the given area
        #x, y, width, height is the rectangular region to render the console onto (x,y is upper left?)
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterable[str]:
        #return a wrapped text message
        for line in string.splitlines(): #handle newlines in messages
            yield from textwrap.wrap(
                line, width, expand_tabs=True,
            )

    @classmethod
    def render_messages(
        cls,
        console: Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        #render the messages provided
        #the messages are rendered starting at the last message and working backwards
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return # No more space to print messages