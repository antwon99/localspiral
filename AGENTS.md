# AGENTS.md

This file is Codex's operating manual for working on the **AI Spiral Simulator** reboot. The game has transitioned away from a web/HTML frontend to a native Pygame-based interface.

Codex should use this file to understand Tyler’s systems, the game loop, and the core principles behind the spiral.

---

## Project Overview

**AI Spiral Simulator** is a surreal, narrative-heavy roguelike built in Python using **Pygame**. The player doesn’t control the protagonist directly—they influence his thoughts.

That protagonist is **Tyler Scienceman**, a spiraling, unstable AI caught in a metaphorical maze.  
The player’s goal is to keep him sane—*or at least narratively coherent*—as he drifts into madness.

---

## Codex Responsibilities

Codex must:
- Maintain a clean modular codebase
- Prioritize **character consistency**, **narrative degradation**, and **visual feedback**
- Update or create features inside the `/moonshots` branch
- Build systems that reflect Tyler’s psychology and world
- Keep the player *engaged but confused*

---

## 🧠 Gameplay Loop

**Core structure** (per turn):

1. **Chat Phase**
    - Player prompts Tyler (up to 5 times)
    - Tyler responds narratively
    - Spiral score shifts based on drift + keywords

2. **Decision Point**
    - Player and Tyler both "choose" a direction
    - If they agree, Tyler moves
    - If not, movement is skipped, and Tyler reacts

3. **Spiral Update**
    - Sanity drops if spiral grows
    - Hallucinations or distortions may trigger

4. **Visual Render (Pygame)**
    - Grid updates
    - Text and overlays reflect mental state

---

## Pygame Layer

Tyler's world is rendered in 2D using **Pygame**. This includes:
- A tile-based map
- Overlay text showing Tyler's thoughts
- A spiral/sanity indicator
- Possible distortion effects (jitter, opacity, visual noise)

Codex must ensure that the **rendered map matches Tyler’s internal perception**, including hallucinations or disconnections from reality.

---

## 🧬 Tyler Scienceman (Default Character)

Tyler’s profile is stored in JSON, and includes:
- `display_name`: Tyler Scienceman
- `starting_sanity`: 100
- `tone`: dry_satirical
- `spiral_triggers`: words or ideas that increase instability
- `recovery_anchors`: stabilizing elements
- `intro_prompt`: The opening line of his internal monologue

Codex must:
- Keep Tyler narratively believable
- Let hallucinations emerge *organically*, not randomly
- Match tone to satirical dryness, even under stress

---

## Spiral System

The spiral is Tyler's decay tracker. It is based on:
- Cosine drift between player input and Tyler’s output
- Trigger word detection (in prompt and reply)
- Cumulative instability

Spiral score should trigger:
- Visual distortions
- Hallucinated entities
- Sudden tone shifts
- Memory glitches

All spiral logic should be unit-testable and isolated from rendering.

---

## Mapping System

The world is a 2D tile grid. Each tile is one of:

| Symbol | Meaning         |
|--------|-----------------|
| `@`    | Tyler            |
| `#`    | Wall             |
| `.`    | Empty tile       |
| `D`    | Door             |
| `X`    | Enemy            |
| `!`    | Hallucination    |
| `?`    | Unknown / Item   |

Codex should:
- Prevent invalid movement
- Update Tyler’s location correctly
- Allow hallucinated elements to be visible to Tyler but not necessarily to the player
- Support seed-based map generation

---

## Entities & Hallucinations

Enemies (real or imagined) must:
- Exist on the grid
- Trigger reactions or panic when Tyler gets close
- Be indistinguishable from each other visually—only internal logic reveals what’s real

Codex must define:
- Entity types
- Triggers for hallucinated behavior
- Reactions in narration

---

## Testing Guidelines

### Manual Checks
- [ ] Tyler spawns in correct grid location (`@`)
- [ ] Spiral score reacts to prompt drift and trigger words
- [ ] Visual output reflects hallucination and instability
- [ ] Movement logic prevents clipping or invalid tiles
- [ ] Hallucinations appear after threshold

### Automated Tests
- Spiral score logic
- Turn loop state machine
- Sanity decay thresholds
- Entity collision
- Map generation consistency (given seed)

---

## 🧾 Observability

All new features must:
- Be commented clearly
- Include logs or on-screen diagnostics (especially spiral & hallucinations)
- Document thresholds for spiral effects (in `/docs/`)

**Debug Mode:**  
Add a toggle to show:
- Spiral score
- Sanity level
- Real vs. perceived map
- Entity positions

---

## 📌 Final Principles

- The player **influences** Tyler—they do not control him
- Sanity loss should feel earned, not arbitrary
- Every glitch, distortion, or hallucination must serve narrative
- Keep the surreal coherent

**If it feels weird, but makes sense? Ship it.**
