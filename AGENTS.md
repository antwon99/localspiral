# AGENTS.md (Pygame Edition)

## Project Purpose

AI Spiral Simulator is evolving into a **Pygame-based narrative roguelike**, where the player doesn’t control the world—they influence the **mind** of an AI protagonist, **Tyler Scienceman**.

Players issue prompts. Tyler interprets them, narrates, and moves through a procedurally generated map. The player’s goal is to preserve **narrative integrity** and keep Tyler from spiraling into incoherence.

Codex’s role is to ensure that all systems are:

* Modular
* Testable
* Consistent with Tyler's tone and mental state

---

## Codex Responsibilities

Codex must:

* Maintain and expand the core gameplay loop (**Prompt → Move → Narrate → Spiral → Render**).
* Port existing logic (sanity, spiral, enemies, map) into Pygame while preserving existing behaviors.
* Ensure Tyler's character remains internally consistent even as he degrades.
* Modularize code to support testing and future features (e.g., new characters, new hallucination effects).

---

## Project Structure (Pygame Edition - Suggested)

```
localspiral/
├── main.py              # Pygame main loop
├── assets/              # Sprites, sounds
├── characters/          # JSON profiles (Tyler, others)
├── game/                # Game logic (map, spiral, narration)
├── ui/                  # Rendering functions, overlays
├── tests/               # Unit tests
├── docs/                # Design docs
```

---

## Tyler Scienceman (Character Profile)

Each AI lives in a JSON file containing:

* `id`, `display_name`
* `starting_sanity`
* `spiral_triggers` & `recovery_anchors`
* `tone`
* `intro_prompt`

Codex must ensure Tyler:

* Responds in consistent tone
* References his internal state and surroundings
* Narrates with increasing distortion as spiral score climbs

---

## Spiral System

* Drift is calculated using embeddings (or placeholder functions for offline mode).
* Spiral score increases based on drift + trigger words.
* Visual effects and narration breakdowns must trigger at thresholds.
* All spiral logic must remain modular and testable.

---

## Mapping & Environment

* Procedural map (walkable `.`, blocked `#`, entities `@` `!` `?`)
* Tyler can only move into valid tiles.
* Map must update visually in Pygame.
* Narration should tie directly to map state and surroundings.

---

## Turn-Based Loop

1. **Chat Phase:**

   * Player issues prompt.
   * Tyler responds narratively.
   * Spiral updates.

2. **Decision Point:**

   * Player and Tyler "agree" on movement.
   * Map updates or Tyler hesitates.

3. **Enemy Turn:**

   * Enemies move or act.

4. **Loop:**

   * Return to Chat Phase.

---

## Enemies and Entities

* Entities have position, type, symbol, behavior.
* Hallucinations and real threats are indistinguishable visually but differ in effect.

Codex must ensure entities behave predictably in code, even if narratively unreliable.

---

## Pygame Visuals

* Map and entities rendered on grid.
* Narration box displays Tyler’s thoughts.
* Visual sanity effects: color changes, distortion, static overlays.

---

## Debug Mode

* Toggle to show real vs perceived map.
* Display spiral score, sanity, entity positions in text overlay.
* Easily removable for final release.

---

## Documentation and Observability

Codex should prioritize clarity of system behavior.
All non-trivial features must be accompanied by in-code comments or API-accessible diagnostics that explain their purpose and behavior.
When creating new systems, include a brief description of their logic and thresholds, especially if tied to gameplay feedback (e.g. hallucinations, spiral triggers, sanity modifiers), and create an accompanying doc file in /docs/.

---

## Final Principles

* **Narrative integrity over mechanical polish.**
* **All changes must reflect visually in Pygame.**
* **Tyler's tone is the heart of the game.**
* Codex commits should be **small, clear, and documented**.
