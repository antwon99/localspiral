class GameMap:
    """Simple grid-based map."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = [['.' for _ in range(width)] for _ in range(height)]
        # Block the borders
        for x in range(width):
            self.tiles[0][x] = '#'
            self.tiles[height - 1][x] = '#'
        for y in range(height):
            self.tiles[y][0] = '#'
            self.tiles[y][width - 1] = '#'

    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if the tile at (x, y) can be walked on."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] == '.'
        return False
