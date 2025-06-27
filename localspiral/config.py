"""Configuration helpers for API access."""

import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

if load_dotenv:
    load_dotenv()


def get_openai_api_key() -> str:
    """Return the OpenAI API key from the environment.

    The key is read from the ``OPENAI_API_KEY`` environment variable.
    If the variable is missing or empty, ``RuntimeError`` is raised.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    return key
