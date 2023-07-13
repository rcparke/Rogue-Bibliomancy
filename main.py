#!/usr/bin/env python3
import traceback

import exceptions
import copy
import lzma
import pickle
from typing import Optional

import tcod

from engine import Engine
from world_level import WorldLevel
import entity
import input_handlers
import color

# incorporates main loop, setup_game

#save_game method, saves current active engine instance(invokes save_as in engine.py)

#define main loop (terminal info)
    #clear console
    #render
    #execute tcod events
    #handle in game exceptions
    #handle game ending exceptions(?)

#setup_game new game function, returns a new game session engine instance

def new_game() -> Engine:
    # Return a brand new game session as an Engine instance
    # need to modify the engine initialization code
    
    width=80
    height=43

    player = copy.deepcopy(entity.player)
    engine = Engine(player=player)

    engine.world_level = WorldLevel(
        engine=engine,
        width=width,
        height=height,
    )

    return engine
#setup_game load game function
def load_game(filename: str) -> Engine:
    #Load an Engine instance from a file
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

#mainmenu class, defines what to render as well as inputs

class MainMenu(input_handlers.BaseEventHandler):
    #handle the main menu rendering and input
    #also I should add mouse support

    def on_render(self, console: tcod.Console) -> None:
        #render the main menu on a background image
        #commenting out background image since I plan to replace it

        #console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2-4,
            "Rogue Bibliomancy",
            fg=color.white, #need to update color
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Robert Parke",
            fg=color.white,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2-2+i,
                text.ljust(menu_width),
                fg=color.white,
                bg=color.black, #bg because it is assuming its over an image
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc() #print to stderr
                return input_handlers.PopupMessage(self, f"Failed to load save:/n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())
        
        return None

#background_image = tcod.image.load("menu_background.png")[:,:,:3]
#dont want to use the previously existing image, maybe just have it be blank for now?

def save_game(handler: input_handlers.BaseEventHandler, filename:str) -> None:
    #If the current event handler has an active Engine then save it
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    screen_width = 80
    screen_height = 50
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = MainMenu()

    #Main game loop below
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Rogue Bibliomancy",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception: #In game exceptions
                    traceback.print_exc() #print error to stderr
                    #Then print error to message log
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.white #might not have a "error" color defined and will need to update later
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: #Save and quit
            save_game(handler, "savegame.sav")
            raise
        except BaseException: #Save on any other unexpected exception
            save_game(handler, "savegame.sav")
            raise

if __name__ == "__main__":
    main()


