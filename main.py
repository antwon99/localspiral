"""Main entry point for the Pygame spiral simulator."""

import json
import os
import pygame
from game.map import GameMap
from game.player import Player
from game.spiral import SpiralSystem
from ui.render import Renderer


def load_character(path: str) -> dict:
    """Return character data from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("AI Spiral Simulator")
    clock = pygame.time.Clock()

    # Load Tyler's profile to seed initial sanity and future behaviors
    character = load_character(os.path.join("characters", "tyler.json"))

    game_map = GameMap(width=20, height=15)
    player = Player(1, 1)
    spiral = SpiralSystem(starting_sanity=character.get("starting_sanity", 100))
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(0, -1, game_map)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, game_map)
                elif event.key == pygame.K_LEFT:
                    player.move(-1, 0, game_map)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, game_map)

        spiral.apply_drift(0.1)
        renderer.draw_map(game_map, player)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
