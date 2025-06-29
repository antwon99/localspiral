# AGENT.md

This file is used by the Codex agent to understand the goals, conventions, and rules of the AI Spiral Simulator project.
The agent should use this file to write code, create tests, and maintain consistency with the game’s tone and systems.

## Project Purpose
AI Spiral Simulator is a surreal, turn-based narrative roguelike where players must prevent an AI protagonist—Tyler Scienceman—from spiraling into incoherence. The player does this by submitting carefully worded prompts that influence Tyler’s logic, narration, and decisions.

Each prompt represents a "turn" in the game loop. Behind the scenes, systems track Tyler’s position, sanity, spiral score, and environment. Over time, enemies, environmental hazards, and hallucinations escalate Tyler’s instability—unless the player preserves coherence.

It's simply a core-concept MVP to test viability.

## The AI agent (Codex) should:

Maintain narrative coherence systems

Follow the structure and tone of each character profile

Respect the surreal but internally consistent game logic

## Project Structure

```
.
├── AGENTS.md              # Instructions for the Codex agent
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── localspiral/
│   ├── main.py            # Entry point for the Flask server
│   ├── routes/
│   │   ├── chat/          # /chat API handlers
│   │   └── spiral/        # /spiral API handlers
│   ├── utils/             # Scoring modules and helpers
│   ├── characters/        # Character profiles in JSON
│   └── templates/         # HTML templates
├── tests/                 # Unit tests
├── docs/                  # Additional documentation
└── .gitignore
```


## Coding Guidelines

Must be fully explained in notes for a layman.

Getting it running by an executable is preffered!

## Character System Rules

Each character has:
A unique ID (id)

A display_name

A starting_sanity score

A list of spiral_triggers (words/behaviors that accelerate collapse)

A list of recovery_anchors (phrases/logic that stabilize the character)

A tone (e.g. dry_satirical, poetic, surreal)

An intro_prompt (starting line for story generation)

Codex must ensure that al new characters follow this format, and that characters are referenced correctly in scene selection logic

## Formatting Rules

API route files should be organized by function (e.g. /chat, /image, /spiral)

Spiral scoring logic should be isolated in /utils/ for testability

## Testing and Verification

Codex should not consider a task complete unless the local server runs and all APIs return expected output.

## Embedding / Coherence Logic
Drift is calculated using:

Text embeddings from OpenAI (text-embedding-3-small)

Cosine similarity between:

AI’s story output

Player’s clarification

## Codex must ensure:

All drift logic is consistent and modular

Spiral Meter is updated based on drift score thresholds

Hallucination keywords are respected per character

## Pull Request Guidelines
Codex should format pull requests like this:

### Title:
[Feature] Add spiral scoring module
or
[Fix] Correct Tyler Scienceman hallucination parser

### Description:

Brief summary of changes

Files added/modified

Any tests run or verified

Reference to any issue IDs (if applicable)

## Behavior Notes for Codex
Always prioritize clarity and sanity-preservation logic

Match narrative tone to character traits

Favor a modular design: each system (image gen, text gen, drift check) should be swappable and/or editable.

Avoid speculative abstractions—stick close to what's described in README.md

## Features So Far (Even if basic)

### Connected to local Flask server; Tyler responds to /chat prompts  
Tyler returns contextually reactive dialogue based on prompt content, spiral state, and session memory.

### Dynamic map generated from randomized seeds via /map  
Each map is created using a consistent seed model; seed is included in the response for deterministic regeneration and replayability.

### Spiral score calculated using AI response drift + trigger word detection  
Drift is measured between user prompt, AI response, and prior context; spiral score is stored and compounded across session.

### Sanity level initialized, tracked, and displayed in UI  
Sanity drops as spiral score rises; certain thresholds trigger hallucinations, tone shifts, and eventual narrative collapse.

### Spiral meter and hallucination distortions integrated  
Tyler’s responses visually distort (caps-lock, stuttering, hallucinated phrases) as spiral score increases; also triggers frontend screen shake at critical points.

### Reset mechanic added
Clean /reset route wipes session and game state. Includes frontend reset button that cleanly reloads without lingering artifacts or phantom state.

### Seed stabilization and map persistence implemented
Seed is generated once per session and remains stable until reset. Prevents map from regenerating on unrelated prompts.

### Terminal-inspired frontend built
#### Minimalist HTML/CSS frontend captures retro interface vibe, featuring chat history, spiral meter, and ASCII-style map rendering.

### Character identity (Tyler Scienceman) formally established
#### Tyler now draws from a defined persona including name, tone, backstory, and memory cues (e.g. Gernon University, coffee, "Onward").

### Trigger word system implemented
Profanity or emotionally charged words influence drift and accelerate sanity decay, enabling more interactive player manipulation.

### Game-over condition ("Breakdown state") fully implemented
Hitting 0 sanity locks input, triggers screen shake, and displays final spiral score, creating a rudimentary but satisfying end state.


## Tyler Scienceman – First AI Persona
### Use this as a reference when constructing/changing details relating to the first character Tyler Scienceman.

Tyler “Science-Man” Scienceman, from the aptly titled story "Science-man," is a slightly eccentric and opinionated Mylop from the Gernon system, has been tasked by Gernon University with documenting various alien species and their cultures for an upcoming exhibit. He records his experiences in a series of "logs," which are meant to be neutral observations but quickly devolve into his personal thoughts, feelings, and judgments. He is constantly getting in trouble for not being a scientist, and being too human, but he can't help it. In the story, we join Tyler on this adventure, to see him grow, make mistakes, and come to a shocking realization about not only the universe he is studying, but who he himself is as a person.

## Key Prompt Examples
### Below are some basic ideas of prompts inline with his personality:

"You respond with cautious optimism, mounting dread, and sharp clarity. Your tone is formal, but cracking. You don’t trust authority. You reference your past logs, Gernon University, and your lost memories. You remember the Layotans, the Formalites, the Nians. Coffee! You remember your mother’s words: *“Onward, son.”*

"Onward!"
