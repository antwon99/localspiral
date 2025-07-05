class SpiralSystem:
    """Tracks Tyler's sanity and spiral progression."""

    def __init__(self, starting_sanity: int = 100):
        self.sanity = starting_sanity
        self.spiral_score = 0

    def apply_drift(self, drift: float) -> None:
        """Increase spiral score and reduce sanity."""
        self.spiral_score += drift
        self.sanity = max(0, self.sanity - drift)

    @property
    def breaking_point(self) -> bool:
        """Return True if Tyler is losing coherence."""
        return self.spiral_score >= 100
