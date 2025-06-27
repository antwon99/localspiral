# AI Spiral Simulator

**A narrative roguelike where your only goal is to keep an AI protagonist from spiraling into incoherent madness.**

Inspired by DougDoug’s chaotic AI experiments, this game transforms LLM instability into a gameplay mechanic. You, the **Narrative Handler**, must interpret AI-generated story scenes and prevent narrative collapse—measured by how far the AI drifts from the generated context.


## Concept

Each run begins with:
- A chosen AI character (e.g., Tyler Scienceman)
- An initial GPT-generated narrative prompt
- Seed based logic for the characters route home.

The player must:
- Analyze the scene and AI output
- Submit a corrected or clarified description
- Prevent divergence between scene ↔ AI text ↔ player text

Behind the scenes, some sort of **coherence engine** scores the drift and adjusts a **Spiral Meter**. When it hits zero? Sanity fails. Game over.


## Tech Stack

No idea! :)

## Project Structure

No idea! :)

## Getting Started

No idea! :)

## Features (In Progress)

Main Focus (prioritize first):

Basic character selection
GPT-based scene generation
Core gameplay loop
Spiral scoring via embeddings
Spiral Meter UI

After the basics are in place:

Leaderboards: “Longest sanity run"
Chaos modifiers and unlockables
Multiplayer? (stretch goal)


## How to Add New Characters

No idea! :)

## Codex & Agent Instructions

The AGENTS.md file contains detailed instructions for GitHub Copilot/Codex, including:

- Style rules (naming conventions, formatting, etc.)

- Coding preferences (e.g., avoid console.log, use custom logger)

- How to run tests or check correctness

- Pull request formatting

- This helps the AI contribute consistent code aligned with the game’s narrative tone and technical goals.

