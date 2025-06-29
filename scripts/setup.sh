#!/bin/bash
# Setup a Python virtual environment for the AI Spiral Simulator.
# Usage: source scripts/setup.sh
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
