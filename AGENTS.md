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

- Maintain and expand the central gameplay loop (Prompt(s) → reply → Move → Spiral → Render)
- Make sure to integrate and wire up features that already exist (movement, turns, map, enemies) and any additions.
- Protect the internal logic of Tyler's character
- Respect surreal systems, but enforce their internal consistency
- Modularize systems for testability and future additions
- Focus on the `moonshots` branch, that's where most building/iterating happens.

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

List of symbols used so far:
| Symbol | Meaning           |
|--------|-------------------|
| `@`    | Tyler (player)    |
| `D`    | Door              |
| `#`    | Wall              |
| `.`    | Empty tile        |
| `X`    | Enemy             |
| `!`    | Hallucination     |
| `?`    | Item or unknown   |


---


# Turn-Based Loop

A standard turn in the **AI Spiral Simulator** follows this core structure:

## 1. Chat Phase

Player and Tyler engage in **1–5 prompts** of dialogue. During this phase:

- **Spiral and sanity** values drift with each exchange  
- The **environment and nearby enemies** may be commented on
- Plans can be formed.
- Tyler may express **doubt, fear, resistance, or hallucinations**
-

## 2. Decision Point

After 5 chat exchanges, both the **player** and **Tyler** must reach a directional consensus  
(the player pushes a button, tyler runs a command).


### If they agree:

- ✅ Tyler moves as instructed  
- ✅ Enemies take their turn  
- ✅ The map updates  
- ➜ A new **Chat Phase** begins


### If they disagree:

- ❌ Movement is lost for that turn  
- Tyler may react (e.g. *"I got confused..."* or *"I thought you meant left."*)  
- ✅ Enemies still move  
- ✅ The map updates  
- ➜ A new **Chat Phase** begins


This cycle repeats until Tyler either **escapes**, **breaks down**,  
or **spirals beyond recovery**.


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
- Tyler responds coherent when sane but unstable when spiraling
- Movement and spiral updates reflect input

Add unit tests to `/tests/` where possible.

### Manual Testing Checklist

- [ ] Tyler spawns in correct location on map (`@`)
- [ ] Map matches Tyler's narration (when sane)
- [ ] Movement updates map *and* Tyler’s perception
- [ ] Sanity decreases on spiral triggers
- [ ] Hallucinations appear after threshold
- [ ] HTML reflects internal state each turn

### Automated Tests Should Cover:
- Movement boundaries
- Seed-based map generation consistency
- Spiral score math (trigger vs. drift)
- Turn based mechanisms


---


## Documentation and Observability
Codex should prioritize clarity of system behavior.  
All non-trivial features must be accompanied by in-code comments or API-accessible diagnostics that explain their purpose and behavior.  
When creating new systems, include a brief description of their logic and thresholds, especially if tied to gameplay feedback (e.g. hallucinations, spiral triggers, sanity modifiers), **and create an accompanying doc file in `/docs/`.**


---


## HTML Rendering Layer

The HTML is the **single source of visible truth** for the developer (and player). Any changes to game logic (movement, enemies, sanity, map layout, etc.) MUST be reflected visually in the HTML rendering.

NOTE: Codex often updates backend logic but forgets to update or sync the HTML display. These need to be kept in sync at all times.

Whenever modifying:
- Tile symbols
- Map dimensions
- Entity placement
- UI counters (turns, sanity, spiral, etc.)
- (OR Adding features!)

Make sure to reflect these updates directly in `index.html` (or the active rendering template).

### Sanity Debug Tip

Include a `[Debug Mode]` toggle that prints Tyler’s perceived map, real map, spiral score, and all entity positions every turn—*in plain text*—below the main UI.


---


## Final Principles

- Stick to the readme and agent file, and ultimately its vision and end goals.
- Always explain fixes in plain English unless explicitly told not to
- Match all narration and behavior to Tyler’s persona
- Remember: **The player doesn’t control Tyler—they stabilize him.**

