# AI Spiral Simulator

**A narrative roguelike where your only goal is to keep an AI protagonist from spiraling into incoherent madness.**

This repository contains the barebones implementation so you can start experimenting quickly. It uses Python with [Flask](https://flask.palletsprojects.com/) for a lightweight API server.

## Project Structure

```
.
├── AGENTS.md              # Instructions for the Codex agent
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/
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

## Getting Started

1. **Install Python 3.11 or later.**
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the server**:
   ```bash
   python src/main.py
   ```
5. Open `http://localhost:5000` in your browser to see the placeholder homepage. The `/chat` and `/spiral` routes will return simple JSON messages.

## How to Add New Characters

Place a JSON file in `src/characters/` following the format described in `docs/character_format.md`. The example `sample_character.json` shows all required fields.

## Tests

Run tests with:
```bash
pytest
```
They cover basic utility functions and ensure the project imports correctly.

## Why `.gitignore`?

The `.gitignore` file prevents temporary or local files (like virtual environments and compiled Python bytecode) from cluttering your repository. This keeps version control clean and focused on source code.
