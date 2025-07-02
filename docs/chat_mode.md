# Chat Mode Prompt Cycle

Tyler begins each game in *chat mode*. A turn consists of up to five prompts from the player. Each `/chat` call increments the prompt counter. When the counter reaches 5 (or when the `/skip` endpoint is used) the game enters a movement phase.

During the movement phase the frontend displays available directions. Picking a direction submits that word to `/chat` which resolves the move and advances `turn_count` by one. The prompt counter resets to `1` at the start of the next chat phase.

Use `/skip` if you want to move after a single prompt without waiting for the full five prompts.
