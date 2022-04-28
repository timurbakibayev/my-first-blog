from game import Game

import pygame
pygame.init()

screen_size = (1000, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Jungle")

clock = pygame.time.Clock()

game = Game.load(
    clock=clock,
    screen_size=screen_size,
)


while game.playing:  # Game loop
    game.update()

    for event in pygame.event.get():
        game.key_pressed(event)

    screen.fill((255, 255, 255))

    game.draw(screen)

    pygame.display.flip()
    clock.tick(20)

pygame.quit()
