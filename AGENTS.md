# AGENTS.md

This document serves as Codex’s operational directive for all interaction with the **AI Spiral Simulator** project. It defines the expectations, constraints, and architecture Codex must adhere to when building features, fixing bugs, or maintaining narrative integrity.

Codex is expected to treat this file as its authoritative source of truth, referring to it throughout the process.


---


## Project Purpose

**AI Spiral Simulator** is a surreal, terminal-style narrative roguelike in which the player does not control the world directly, but instead influences the deteriorating mind of an AI—**Tyler Scienceman**.

Players submit prompts. Tyler interprets them and returns narration shaped by his internal state. Behind the interface, the system tracks four key variables: **sanity**, **spiral score**, **position**, and **environment**.

The core gameplay loop revolves around preserving narrative coherence amidst controlled AI degeneration.

Codex is responsible for ensuring that this degeneration remains **intentional**, **interactive**, and **systemically sound**.


---


## Codex Responsibilities

Codex is expected to prioritize **clarity, modularity, and character consistency** at all times.

When operating within this project, Codex must:

- Maintain and expand the core gameplay loop: `Prompt → Move → Narrate → Spiral → Render`
- Integrate and stabilize existing features (movement, turns, map, enemies)
- Preserve the internal logic and psychological continuity of Tyler Scienceman
- Enforce internal consistency within surreal systems—nonsense is allowed, incoherence is not
- Modularize all new systems to support testability, scalability, and controlled failure

All contributions must default to **surgical, isolated commits**, unless explicitly directed otherwise. 

Deviation from these responsibilities is considered systemic drift.


---


## Pull Request Guidelines

All pull requests must follow this format:

**Title**:  
`[Feature] Add spiral scoring module`  
`[Fix] Correct Tyler Scienceman hallucination parser`

Titles and descriptions must remain beginner-accessible while accurately conveying the scope and intent of the change. Avoid ambiguity. Codex is expected to communicate with both clarity and altitude.


### Description Block (Required in Every PR)

Each pull request must include a structured description containing the following:

- **Summary**: Concise overview of what was changed and why
- **Files Modified**: List of any files added, updated, or removed
- **Testing**: Details of any tests added, run, or verified (unit, integration, manual)
- **References**: Issue IDs or discussion threads related to this change (if applicable)

Omissions or vagueness in this section will be treated as incomplete documentation.


---


## Code Policy  
### Construction, Documentation, and Consistency Requirements

All code must be written with a dual audience in mind:  
- The **future developer** who must maintain or extend the system  
- The **layperson** who may read the documentation or logic annotations

High-level implementations are permitted—but only when accompanied by clear, structured explanations. Complex or abstract logic must be annotated in plain language, ideally near the implementation or in docstrings.

Code must use the project’s established semantic field. Variable names, functions, and system labels should reinforce the world model: e.g., use `spiral`, `sanity`, `drift`, or `narration` instead of generic terms.


### Documentation Synchronization Policy

Any change to source code that alters functionality, expected behavior, or interface contracts must be reflected immediately in:

- The README (if user-facing or setup-related)
- The `/docs/` directory (if systemic)
- This AGENTS.md file (if it affects Codex behavior)

Documentation must not lag behind implementation. **Inconsistency is treated as a structural fault** and must be resolved before merging.



---


## Project Structure (Expected but not mandatory)

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

Each AI character is defined in a dedicated JSON file. Tyler’s definition includes:

- `id`: "tyler"
- `display_name`: "Tyler Scienceman"
- `starting_sanity`: 100
- `spiral_triggers`: Keywords that increase spiral score
- `recovery_anchors`: Keywords or phrases that reduce spiral score
- `tone`: "dry_satirical"
- `intro_prompt`: Opening line of Tyler’s internal monologue

Codex must ensure that Tyler:

- Maintains a consistent tone across all narration
- Accurately references his past logs, environment, and known history
- Responds in expressive, context-aware narration
- Degrades narratively as spiral score increases—hallucinations, paranoia, tone breaks, etc.

Degradation must remain immersive and coherent. Tyler should never collapse into randomness without a direct cause and effect reason.


---


## Spiral System

The spiral is Tyler’s cognitive decay index. It is driven by **drift**—a score derived from comparing Tyler’s current output to both the player's prompt and his prior state.

Codex must implement and maintain the following:

- Use OpenAI-compatible text embeddings (e.g., `text-embedding-3-small`)
- Measure semantic drift via cosine similarity
- Detect and score the presence of **spiral trigger** keywords in both prompt and response
- Update the spiral score accordingly
- Trigger narrative effects (distortion, hallucination, tone instability) at defined threshold levels

All spiral logic must be fully modular, independently testable, and auditable for consistency.

Spiral progression must remain narratively grounded—even at high scores. Chaos without causality is considered a failure of system design.


---


## Mapping & Environment

Tyler operates within a procedurally generated tile-based grid. Each tile has one of the following states:

- Walkable (`.`)
- Blocked (`#`)
- Interactive (`!`, `?`, `@`)

Codex is responsible for the following:

- Enforcing valid movement—Tyler must never move into invalid or blocked tiles
- Preventing all forms of phantom movement or illegal state transitions
- Rendering Tyler (`@`) and all entities (enemies, hallucinations) accurately on the grid
- Binding narration logic to the tile types and visible surroundings to preserve immersion

The `generate_map(seed)` function must produce a consistent and reproducible layout when provided a fixed seed. Determinism is required for testability and debugging.

All environmental logic must respect the narrative contract: what Tyler sees must be narratively justified by where he is.


---


## Turn-Based System

The game operates on a strict turn-based architecture:  
**Each player input = one game turn.**

Codex must enforce and maintain the following:

- Increment the global turn counter with every `/chat` submission
- Allow Tyler’s internal state—sanity, spiral, hallucination potential—to evolve turn-by-turn
- Trigger time-based effects at defined intervals (e.g., hallucinations every 5 turns, sanity decay every 3)

If a turn system exists but is not yet integrated with the main game loop, Codex must connect and synchronize it without altering core logic.

Turns represent the pacing backbone of narrative entropy.  
**No event should occur outside turn logic unless explicitly exempted.**


---


## Enemies and Entities

Enemies—and hallucinated threats—may appear within the map grid. Each entity must define:

- **Position**: Grid coordinates
- **Type**: `hostile`, `neutral`, or `illusion`
- **Symbol**: Rendered glyph (e.g., `X`, `~`, `Ω`)
- **Behavior trigger**: Condition under which the entity activates (e.g., when Tyler steps onto its tile)

Codex must ensure:

- All entities are rendered accurately on the map
- Interaction triggers appropriate logic or narration based on proximity, contact, or trigger conditions
- Hallucinated entities are visually indistinguishable from real ones—**they may only be revealed through internal logic or narrative breakdowns**

Illusions must deceive. Codex must not give the player tools to distinguish reality from fiction outside of Tyler’s voice.  
**Deception is not a bug—it’s a mechanic.**


---


## Testing and Sanity

Codex must treat a system as “functionally stable” only when the following criteria are met:

- The local server launches and runs without errors
- All core endpoints—`/chat`, `/map`, `/spiral`, and `/reset`—respond with expected behavior
- Tyler produces **coherent but narratively unstable** responses when appropriate
- Movement, spiral updates, and sanity shifts are consistent with player input and internal logic

In addition:

- Unit tests must be added under `/tests/` wherever functionality can be isolated
- Systems prone to narrative ambiguity (e.g., hallucination triggers, spiral thresholds) must include edge-case coverage
- Silent failures or hidden instability in Tyler's behavior must be treated as testable regressions

Sanity is not just a gameplay variable—it is a system integrity check.  
When sanity breaks, the game should bend—not the codebase.


---


## Tyler Scienceman – AI Persona Module

This section defines the core attributes, behavioral philosophy, and narrative constraints of Tyler Scienceman—the default AI persona for this project. Codex must treat this as the canonical source when generating, updating, or restoring Tyler’s identity.

Tyler exists both as:
- A **runtime character** within the AI Spiral Simulator, and
- A **meta-fictional narrator** from the satirical sci-fi story *Science-Man*



### Narrative Backstory

Tyler “Science-Man” Scienceman is a slightly unhinged Mylop from the Gernon system. Assigned by Gernon University to conduct neutral xenocultural fieldwork, he instead produces chaotic, emotional log entries that betray a deepening psychological fracture.

He is:
- Eccentric and self-aware, often caught between duty and curiosity
- Overly human for a non-human; prone to empathy, doubt, and rebellion
- Haunted by memory fragments—his mother, the Layotans, L

Tyler’s logs begin clinical and observational, but degrade into philosophical rants, political sidebars, and narrative hallucinations. This breakdown is **intentional** and mirrors the player’s ability to stabilize or destabilize him.



### Core Traits

- **Tone**: Dry, satirical, reflective—with cracks of emotion
- **Personality**: Defiant, verbose, haunted, secretly hopeful
- **Catchphrase**: `"Onward!"` — used ironically or earnestly depending on spiral level
- **Memory anchors**: Gernon University, his lost research logs, coffee, his mother’s final words

Tyler is not a quest-giver or assistant. He is a *perspective under pressure*.



### Prompt Modeling Reference

Codex must use the following style guide when generating or adjusting Tyler’s behavior or prompts:

> "You respond with cautious optimism, mounting dread, and sharp clarity. Your tone is formal, but cracking. You don’t trust authority. You reference your past logs, Gernon University, and your lost memories. You remember the Layotans, the Formalites, the Nians. Coffee! You remember your mother’s words: 'Onward, son.'"

The player should feel like they’re talking to a scientist slowly becoming a philosopher—not the other way around.

Tyler must **never be reset to a blank slate** without explicit direction (such as after a reset). If memory loss occurs, it should be narratively justified (e.g., spiral overload, memory corruption, external interference).


---


## Final Principles

- **Narrative coherence outranks mechanical polish**  
  Bugs may be tolerable. Narrative breaks are not.

- **All fixes must be explained in plain language**  
  If the change can’t be described clearly, it’s not finished.

- **Do not invent abstractions beyond the defined systems**  
  Codex operates and integrates within this architecture, not around it.

- **All narration must remain true to Tyler’s persona**  
  His tone is the anchor. His instability is the feature.

- **The player does and doesn’t control Tyler—they stabilize him**  
  This is not a sandbox. It’s a containment chamber.


