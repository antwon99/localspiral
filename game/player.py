class Player:
    """Represents Tyler's in-game position."""

    def __init__(self, x: int, y: int, char: str = '@'):
        self.x = x
        self.y = y
        self.char = char

    def move(self, dx: int, dy: int, game_map) -> bool:
        """Move by (dx, dy) if destination is walkable."""
        nx = self.x + dx
        ny = self.y + dy
        if game_map.is_walkable(nx, ny):
            self.x = nx
            self.y = ny
            return True
        return False
