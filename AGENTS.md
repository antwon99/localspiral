# AGENT.md

This file is used by the Codex agent to understand the goals, conventions, and rules of the AI Spiral Simulator project.
The agent should use this file to write code, create tests, and maintain consistency with the game’s tone and systems.

## Project Purpose
AI Spiral Simulator is a web-based narrative roguelike where players must prevent an AI-generated character from spiraling into incoherence. Each turn, an AI character narrates a story fragment. The player must interpret the AI's generated text and submit a clarification. A backend system scores coherence between the story, the AI response, and finally the player’s response.

## The AI agent (Codex) should:

Maintain narrative coherence systems

Follow the structure and tone of each character profile

Respect the surreal but internally consistent game logic

## Project Structure

No idea, yet.

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

Title:
[Feature] Add spiral scoring module
or
[Fix] Correct Tyler Scienceman hallucination parser

Description:

Brief summary of changes

Files added/modified

Any tests run or verified

Reference to any issue IDs (if applicable)

## Behavior Notes for Codex
Always prioritize clarity and sanity-preservation logic

Match narrative tone to character traits

Favor a modular design: each system (image gen, text gen, drift check) should be swappable and/or editable.

Avoid speculative abstractions—stick close to what's described in README.md
