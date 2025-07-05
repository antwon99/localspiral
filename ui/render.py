import pygame

TILE_SIZE = 32

class Renderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.font = pygame.font.SysFont("monospace", 16)

    def draw_map(self, game_map, player=None):
        self.surface.fill((0, 0, 0))
        for y, row in enumerate(game_map.tiles):
            for x, char in enumerate(row):
                color = (200, 200, 200)
                if char == '#':
                    color = (100, 100, 100)
                self._draw_tile(x, y, char, color)
        if player:
            self._draw_tile(player.x, player.y, player.char, (255, 200, 0))

    def _draw_tile(self, x, y, char, color):
        text = self.font.render(char, True, color)
        self.surface.blit(text, (x * TILE_SIZE, y * TILE_SIZE))
