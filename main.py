import pygame
from game.map import GameMap
from ui.render import Renderer


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("AI Spiral Simulator")
    clock = pygame.time.Clock()

    game_map = GameMap(width=20, height=15)
    renderer = Renderer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        renderer.draw_map(game_map)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
