"""Utility functions for scoring narrative coherence.

By default a simple bag-of-words embedding is used so tests can run offline.
When ``OPENAI_API_KEY`` is present, the OpenAI embedding API
(``text-embedding-3-small``) is attempted and the bag-of-words approach is used
as a fallback if the request fails. Drift is computed as ``1 -`` the cosine
similarity between embeddings.
"""

from __future__ import annotations

from collections import Counter
import json
import math
import os
from typing import Any, Counter as CounterType
from urllib import request
from ..config import get_openai_api_key

_EMBED_URL = "https://api.openai.com/v1/embeddings"


def _bow_embed(text: str) -> CounterType[str]:
    """Embed text into a bag-of-words counter."""
    return Counter(text.lower().split())


def _openai_embed(
    text: str, model: str = "text-embedding-3-small"
) -> list[float]:
    """Return embedding from OpenAI's API."""
    api_key = get_openai_api_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {"model": model, "input": text}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        _EMBED_URL, data=data, headers=headers, method="POST"
    )
    with request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
    parsed: Any = json.loads(body)
    return parsed["data"][0]["embedding"]


def _cosine_similarity_sparse(
    vec1: CounterType[str], vec2: CounterType[str]
) -> float:
    """Return cosine similarity between two sparse vectors."""
    keys = set(vec1) | set(vec2)
    dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in keys)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def _cosine_similarity_dense(vec1: list[float], vec2: list[float]) -> float:
    """Return cosine similarity between two dense vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def calculate_drift(reference: str, response: str) -> float:
    """Return a drift score between two text fragments.

    The score ranges from ``0`` (identical) to ``1`` (completely dissimilar)
    based on cosine similarity of their embeddings.
    """
    if not reference or not response:
        return 1.0

    use_openai = os.getenv("OPENAI_API_KEY")

    if use_openai:
        try:
            ref_vec = _openai_embed(reference)
            resp_vec = _openai_embed(response)
            similarity = _cosine_similarity_dense(ref_vec, resp_vec)
            return 1.0 - similarity
        except Exception:
            # Fall back to bag-of-words on any failure
            pass

    ref_vec = _bow_embed(reference)
    resp_vec = _bow_embed(response)
    similarity = _cosine_similarity_sparse(ref_vec, resp_vec)
    return 1.0 - similarity
