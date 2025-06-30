# AGENTS.md

This file provides Codex with a complete understanding of how to interact with the AI Spiral Simulator project. Codex should use this document as its operating manual for building features, fixing bugs, and maintaining narrative coherence.

---

## Project Purpose

AI Spiral Simulator is a surreal, terminal-style narrative roguelike. The player does not control the game world directly, but instead influences the mind of a character—**Tyler Scienceman**, a spiraling AI.

The player submits prompts. Tyler interprets them and narrates his surroundings. Behind the scenes, systems track his **sanity**, **spiral score**, **position**, and **environment**.

The core gameplay loop is about preserving narrative coherence in the face of AI degeneration. Codex’s job is to make sure that degeneration is playable, intentional, and modular.

---

## Codex Responsibilities

Codex should prioritize **clarity, modularity, and character consistency**. When acting on this project, Codex must:

- Maintain and expand the central gameplay loop (Prompt → Move → Narrate → Spiral → Render)
- Wire up features that already exist (movement, turns, map, enemies)
- Protect the internal logic of Tyler's character
- Respect surreal systems, but enforce their internal consistency
- Modularize systems for testability and future additions

Codex should default to **surgical, isolated commits** unless specifically instructed otherwise.

---

## Project Structure (Expected)

```bash
localspiral/
├── main.py              # Entry point (Flask server)
├── routes/
│   ├── chat/            # /chat API handlers
│   └── spiral/          # /spiral API handlers
├── utils/               # Map gen, scoring, narration, sanity logic
├── characters/          # JSON profiles for each AI (e.g. Tyler)
├── templates/           # HTML frontend (terminal-style)
├── tests/               # Unit tests
├── scripts/             # Optional launch helpers
├── docs/                # Game loop specs, data contracts, etc
```

---

## Game Loop (High Level)

1. **Player Input** → Via `/chat`, the player submits a prompt.
2. **Game Tick Begins** → Increments turn counter, logs state.
3. **Movement/Action** → Based on prompt or command.
4. **Narration** → Tyler replies, influenced by state and spiral.
5. **Spiral Update** → Drift logic updates spiral score.
6. **Rendering** → Updated map and sanity level returned to UI.

---

## Tyler Scienceman (Default Character)

Each AI character lives in a JSON file. Tyler's includes:

- `id`: "tyler"
- `display_name`: "Tyler Scienceman"
- `starting_sanity`: 100
- `spiral_triggers`: keywords that increase his spiral score
- `recovery_anchors`: keywords/phrases that stabilize him
- `tone`: "dry\_satirical"
- `intro_prompt`: The opening line of his internal monologue

Codex must ensure Tyler:

- Has a consistent tone
- References his history and environment accurately
- Responds in full, expressive narration when prompted
- Degrades narratively (hallucinations, paranoia, distortions) as spiral increases

---

## Spiral System

The spiral is Tyler’s decay tracker. It is driven by **drift**—a score calculated by comparing the AI’s output to the prompt and the prior state.

Codex must:

- Use OpenAI text embeddings (e.g., `text-embedding-3-small`)
- Measure drift via cosine similarity
- Combine that with any **trigger words** in the prompt or Tyler’s reply
- Update the spiral score
- Trigger effects (distortion, hallucination, tone breaks) at defined thresholds

All spiral logic must be modular and testable.

---

## Mapping & Environment

Tyler exists in a procedurally generated map grid. Each tile is either walkable (`.`), blocked (`#`), or interactive (`!`, `?`, `@`).

Codex must:

- Ensure Tyler can only move into valid tiles
- Prevent phantom movement through walls
- Display both Tyler (`@`) and enemies or hallucinations on the grid
- Tie narration to the tile type and visible surroundings

The `generate_map(seed)` function should return consistent layouts given a stable seed.

---

## Turn-Based System

Each player input = one turn. Codex must:

- Increment turn count with every `/chat` submission
- Allow Tyler's internal state to evolve turn-by-turn
- Hook up effects that trigger on certain turn intervals (e.g., hallucinations every 5 turns)

If a turn system is present but disconnected, Codex must connect it to the game loop.

---

## Enemies and Entities

Enemies (or hallucinated threats) may appear on the map. Each should include:

- Position
- Type (hostile, neutral, illusion)
- Symbol
- Behavior trigger (e.g., when Tyler enters their tile)

Codex must:

- Render enemies on the map
- Trigger logic or narration when Tyler is near or collides with them
- Ensure hallucinated enemies are distinguishable only by internal logic, not visuals

---

## Testing and Sanity

Codex must consider a system "working" when:

- The local server runs without error
- `/chat`, `/map`, `/spiral`, and `/reset` all behave as expected
- Tyler responds with coherent but unstable narration
- Movement and spiral updates reflect input

Add unit tests to `/tests/` where possible.

---


## Documentation and Observability
Codex should prioritize clarity of system behavior.  
All non-trivial features must be accompanied by in-code comments or API-accessible diagnostics that explain their purpose and behavior.  
When creating new systems, include a brief description of their logic and thresholds, especially if tied to gameplay feedback (e.g. hallucinations, spiral triggers, sanity modifiers), **and create an accompanying doc file in `/docs/`.**



---


## Final Principles

- Prioritize **narrative integrity** over mechanical polish
- Always explain fixes in plain English unless explicitly told not to
- Match all narration and behavior to Tyler’s persona
- Remember: **The player doesn’t control Tyler—they stabilize him.**

