import pygame
from graph import LineGraph
from random import randint
from ui import Pane
import math
pygame.init()


def main():
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    f = lambda x: 2*x + 1

    g = LineGraph(width, height, [
        [i/10, f(i/10)] for i in range(-100, 101) if i !=0
    ])
    # g = LineGraph(width, height, [[1.5, 0.2], [5.1, 3.8]])

    pane = Pane(300, 400)

    running = True
    prev_mouse_pos = None
    mouse_down = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    g.incr_offset(incr_y=-10)
                elif event.key == pygame.K_s:
                    g.incr_offset(incr_y=10)
                elif event.key == pygame.K_a:
                    g.incr_offset(incr_x=10)
                elif event.key == pygame.K_d:
                    g.incr_offset(incr_x=-10)
                elif event.key == pygame.K_UP:
                    g.change_res(10)
                elif event.key == pygame.K_DOWN:
                    g.change_res(-10)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    prev_mouse_pos = None

        if prev_mouse_pos is not None and mouse_down:
            cur = pygame.mouse.get_pos()
            g.incr_offset(incr_x=cur[0] - prev_mouse_pos[0], incr_y=prev_mouse_pos[1] - cur[1])
        if mouse_down:
            prev_mouse_pos = pygame.mouse.get_pos()

        window.fill((255, 255, 255))

        g.draw()
        window.blit(g, (0, 0))

        pane.draw()
        window.blit(pane, (200, 200))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
