"""Utility functions for scoring narrative coherence."""

def calculate_drift(reference: str, response: str) -> float:
    """Return a placeholder drift score between two text fragments.

    For now this simply measures difference by word count ratio.
    A real implementation would use embeddings and cosine similarity.
    """
    if not reference or not response:
        return 1.0
    ref_len = len(reference.split())
    resp_len = len(response.split())
    return abs(ref_len - resp_len) / max(ref_len, resp_len)
