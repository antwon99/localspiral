# AI Spiral Simulator

**A narrative roguelike where your only goal is to keep an AI protagonist from spiraling into incoherent madness.**

This repository contains the barebones implementation so you can start experimenting quickly. It uses Python with [Flask](https://flask.palletsprojects.com/) for a lightweight API server.

## Project Structure

```
localspiral/
├── docs/                  # Additional documentation
├── localspiral/
│   ├── characters/        # Character profiles in JSON
│   ├── routes/            # Anything incoming and outgoing
│   │   ├── chat/          # /chat API handlers
│   │   └── spiral/        # /spiral API handlers
│   ├── templates/         # HTML templates (future)
│   ├── utils/             # Scoring modules and helpers
│   └── main.py            # Entry point for the Flask server
├── tests/                 # Unit tests
├── .gitignore
├── LICENSE
├── README.md              # This file
└── requirements.txt       # Dependencies
```
AGENTS.md              # Instructions for the Codex agent
## Getting Started

1. **Install Python 3.11 or later.**
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install the package in editable mode**:
   ```bash
   pip install -e .
   ```
4. **Run the server**:
   ```bash
   localspiral
   ```
5. Open `http://localhost:5000` in your browser to see the placeholder homepage. The `/chat` and `/spiral` routes will return simple JSON messages.

## OpenAI API Key

Some features require an OpenAI API key. Set the variable `OPENAI_API_KEY` in your environment before running the server:
```bash
export OPENAI_API_KEY=sk-your-key
```
If you prefer a `.env` file, install [python-dotenv](https://pypi.org/project/python-dotenv/) and create a file containing:
```
OPENAI_API_KEY=sk-your-key
```
Then call `dotenv.load_dotenv()` early in your application to load the variable.

## How to Add New Characters

Place a JSON file in `localspiral/characters/` following the format described in `docs/character_format.md`. The example `sample_character.json` shows all required fields.

## Map Generation

The `localspiral.utils` package includes a tiny map generator for experiments.
Use `generate_map(seed)` to produce a deterministic grid of ``'.'`` and ``'#'``
tiles. Calling the function with the same seed always returns the same layout.

Example:

```python
from localspiral.utils.map import generate_map

grid = generate_map(123)
for row in grid:
    print("".join(row))
```

## Tests

Run tests with:
```bash
pytest
```
They cover basic utility functions and ensure the project imports correctly.

## Why `.gitignore`?

The `.gitignore` file prevents temporary or local files (like virtual environments and compiled Python bytecode) from cluttering your repository. This keeps version control clean and focused on source code.
