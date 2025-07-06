import pygame

TILE_SIZE = 32
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
STATUS_BAR_HEIGHT = 32
NARRATION_HEIGHT = 64


class Renderer:
    """Collection of rendering helpers for the Pygame UI."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 16)

    def render(self, game_map, player, spiral, status_text, narration):
        """Composite draw call for the entire UI."""
        self.surface.fill(BLACK)
        self.draw_status_bar(spiral, status_text)
        self.draw_map(game_map, player, STATUS_BAR_HEIGHT)
        map_height_px = len(game_map.tiles) * TILE_SIZE
        self.draw_narration(narration, STATUS_BAR_HEIGHT + map_height_px)

    def draw_map(self, game_map, player=None, offset_y: int = 0):
        for y, row in enumerate(game_map.tiles):
            for x, char in enumerate(row):
                self._draw_tile(x, y, char, GREEN, offset_y)
        if player:
            self._draw_tile(player.x, player.y, player.char, GREEN, offset_y)

    def draw_status_bar(self, spiral, status_text: str):
        text = self.font.render(
            f"Spiral Score: {spiral.spiral_score:.1f}  Sanity Level: {spiral.sanity:.1f}  Status: {status_text}",
            True,
            GREEN,
        )
        self.surface.blit(text, (0, 0))

    def draw_narration(self, text: str, y: int):
        narration_surface = self.font.render(text, True, GREEN)
        self.surface.blit(narration_surface, (0, y))

    def _draw_tile(self, x, y, char, color, offset_y: int = 0):
        text = self.font.render(char, True, color)
        self.surface.blit(text, (x * TILE_SIZE, offset_y + y * TILE_SIZE))
