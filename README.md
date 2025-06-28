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
├── scripts/               # Helper scripts
├── .gitignore
├── LICENSE
├── README.md              # This file
├── AGENTS.md              # Instructions for the Codex agent
├── requirements.txt       # Dependencies
└── pyproject.toml         # Package configuration
```
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
4. **Run the included helper script**:
```bash
./scripts/run_all.sh
```
   Or on Windows:
```bat
scripts\run.bat
```
5. Open `http://localhost:5000` in your browser. The root page now includes a
   basic interface for testing the API. Type a prompt and click **Send** to call
   the `/chat` route. Buttons are also provided to try the `/spiral` and `/map` endpoints. The `/map` output now renders as a small HTML grid styled like an old terminal so you can quickly inspect the generated layout.

## OpenAI API Key

Some features require an OpenAI API key. Set the variable `OPENAI_API_KEY` in your environment before running the server:
```bash
export OPENAI_API_KEY=sk-your-key
```
On Windows PowerShell use:
```powershell
$env:OPENAI_API_KEY="sk-your-key"
```
You can also create a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/). The application loads this file automatically.
Create a file named `.env` containing:
```
OPENAI_API_KEY=sk-your-key
```

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
