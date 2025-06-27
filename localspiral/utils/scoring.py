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
from typing import Counter as CounterType


def _embed(text: str) -> CounterType[str]:
    """Embed text into a bag-of-words counter."""
    return Counter(text.lower().split())


def _cosine_similarity(vec1: CounterType[str], vec2: CounterType[str]) -> float:
    """Return cosine similarity between two sparse vectors."""
    keys = set(vec1) | set(vec2)
    dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in keys)
    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))
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

    ref_vec = _embed(reference)
    resp_vec = _embed(response)
    similarity = _cosine_similarity(ref_vec, resp_vec)
    return 1.0 - similarity
