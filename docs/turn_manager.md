# Turn Manager

`turn_manager.run_turn` coordinates a single game loop iteration. It loads the
saved `GameState`, runs `process_turn` from `game_loop.py`, persists the updated
state, and packages the response for the `/chat` API.

The returned dictionary includes a map update when applicable, debug data, the
current turn number and chat prompt counter. Use this to drive the frontend so
that every user input represents one full cycle of prompt → move → render.
