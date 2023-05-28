# incorporates main loop, setup_game

#save_game method, saves current active engine instance(invokes save_as in engine.py)

#define main loop (terminal info)
    #clear console
    #render
    #execute tcod events
    #handle in game exceptions
    #handle game ending exceptions(?)

#setup_game new game function, returns a new game session engine instance

#setup_game load game function

#mainmenu class, defines what to render as well as inputs