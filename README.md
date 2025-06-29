# AI Spiral Simulator

**A narrative roguelike where your only goal is to keep an AI protagonist—Tyler Scienceman—from spiraling into incoherent madness.**

Tyler narrates. You prompt. The Spiral responds.

This is a developer sandbox for exploring narrative integrity, drift mechanics, and AI-character coherence under pressure. Think terminal rogue-like meets psychological debugging.

---

## Project Status

**Current Phase:** Experimental core loop testing

**Core Features (In Progress):**

- Dynamic character system
- Spiral score & breakdown logic
- Turn-based narration engine
- Map rendering with movable AI (@)
- Enemies and hallucinations (WIP)

---

## Getting Started

This guide assumes you're running via VS Code or CLI with Python 3.11+

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key (required for narration & drift scoring)
export OPENAI_API_KEY=your-key-here

# 3. Run the local server
python -m localspiral.main
```

Then visit:

```
http://localhost:5000
```

You can test `/chat`, `/spiral`, `/map`, and `/reset` routes directly from the UI.

---

## Repository Layout

```bash
localspiral/
├── characters/        # Tyler and other profiles (JSON)
├── routes/            # Flask API endpoints
│   ├── chat/
│   └── spiral/
├── templates/         # Terminal-style frontend (basic HTML)
├── utils/             # Map gen, scoring, drift helpers
├── main.py            # Entry point (Flask app)
```

Other folders:

- `tests/` for unit tests
- `scripts/` for launch helpers
- `docs/` for design documents & systems info

---

## Agent Instructions

If you're using GitHub Copilot/Codex, refer to `AGENTS.md` for the in-depth ruleset. It contains behavior definitions, game logic expectations, and formatting requirements for automated fixes.

---

## License

[MIT](LICENSE)

---

For full vision, logic breakdowns, or to contribute: contact the project creator or explore the `main` and `old` branches for alternate timelines.

