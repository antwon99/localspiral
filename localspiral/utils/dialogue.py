"""Simple wrapper around the OpenAI chat completion API."""

from __future__ import annotations

import json
from typing import Any
from urllib import request, error

from ..config import get_openai_api_key


_API_URL = "https://api.openai.com/v1/chat/completions"


def _post_json(
    url: str, payload: dict[str, Any], headers: dict[str, str]
) -> str:
    """Send JSON data via POST and return the response body as a string."""
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers=headers, method="POST")
    with request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


def generate_reply(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    *,
    system_prompt: str | None = None,
) -> str:
    """Return the assistant reply for ``prompt`` using OpenAI's API.

    Parameters
    ----------
    prompt:
        The user's message.
    model:
        The OpenAI chat model to use.
    system_prompt:
        Optional system prompt that will be prepended to the conversation.
    """
    api_key = get_openai_api_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        body = _post_json(_API_URL, payload, headers)
    except error.HTTPError as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

    data: Any = json.loads(body)
    return data["choices"][0]["message"]["content"]
