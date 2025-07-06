"""Main entry point for the Pygame spiral simulator."""

import json
import os
import pygame
from game.map import GameMap
from game.player import Player
from game.spiral import SpiralSystem
from ui.render import Renderer, STATUS_BAR_HEIGHT, NARRATION_HEIGHT, TILE_SIZE


def load_character(path: str) -> dict:
    """Return character data from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    pygame.init()
    map_width = 20
    map_height = 15
    screen_height = STATUS_BAR_HEIGHT + map_height * TILE_SIZE + NARRATION_HEIGHT
    screen = pygame.display.set_mode((map_width * TILE_SIZE, screen_height))
    pygame.display.set_caption("AI Spiral Simulator")
    clock = pygame.time.Clock()

    # Load Tyler's profile to seed initial sanity and future behaviors
    character = load_character(os.path.join("characters", "tyler.json"))

    game_map = GameMap(width=map_width, height=map_height)
    player = Player(1, 1)
    spiral = SpiralSystem(starting_sanity=character.get("starting_sanity", 100))
    renderer = Renderer(screen)
    narration = character.get("intro_prompt", "")

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
                elif event.key == pygame.K_RETURN:
                    narration = "Tyler ponders your words..."

        spiral.apply_drift(0.1)
        status = "Spiraling" if spiral.breaking_point else "Stable"
        renderer.render(game_map, player, spiral, status, narration)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
