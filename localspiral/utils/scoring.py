"""Utility functions for scoring narrative coherence.

This module provides a small, self-contained embedding solution so unit tests can
run without network access. Each piece of text is converted into a simple bag-of-
words vector. Cosine similarity between these vectors yields a measure of how
similar two passages are. The drift score is then ``1 - similarity`` so that
identical text returns ``0`` and completely unrelated text approaches ``1``.
"""

from __future__ import annotations

from collections import Counter
import math
from typing import Iterable, Counter as CounterType

try:  # optional dependency
    import openai  # type: ignore
except Exception:  # pragma: no cover - openai may not be installed
    openai = None

from ..config import OPENAI_API_KEY


def _embed(text: str) -> CounterType[str]:
    """Embed text into a bag-of-words counter."""
    return Counter(text.lower().split())


def _openai_embed(text: str) -> Iterable[float]:
    """Return an embedding using the OpenAI API."""
    if openai is None or not OPENAI_API_KEY:
        raise RuntimeError("OpenAI support is not available")

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        result = client.embeddings.create(
            input=[text],
            model="text-embedding-3-small",
        )
        return result.data[0].embedding
    except AttributeError:  # fallback for legacy package
        openai.api_key = OPENAI_API_KEY
        result = openai.Embedding.create(input=[text], model="text-embedding-3-small")
        return result["data"][0]["embedding"]


def _cosine_similarity(vec1: Iterable[float] | CounterType[str], vec2: Iterable[float] | CounterType[str]) -> float:
    """Return cosine similarity between dense or sparse vectors."""
    if isinstance(vec1, (list, tuple)) and isinstance(vec2, (list, tuple)):
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    keys = set(vec1) | set(vec2)  # type: ignore[arg-type]
    dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in keys)  # type: ignore[index]
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))  # type: ignore[call-arg]
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))  # type: ignore[call-arg]
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def calculate_drift(reference: str, response: str, *, use_openai: bool = False) -> float:
    """Return a drift score between two text fragments.

    The score ranges from ``0`` (identical) to ``1`` (completely dissimilar)
    based on cosine similarity of their embeddings.
    """
    if not reference or not response:
        return 1.0

    if use_openai:
        ref_vec = list(_openai_embed(reference))
        resp_vec = list(_openai_embed(response))
    else:
        ref_vec = _embed(reference)
        resp_vec = _embed(response)
    similarity = _cosine_similarity(ref_vec, resp_vec)
    return 1.0 - similarity
