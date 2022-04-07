import pygame
pygame.init()
screen = pygame.display.set_mode((600, 480), pygame.NOFRAME)
pygame.display.set_caption("Mario")
playing = True
clock = pygame.time.Clock()
mario = pygame.image.load("mario.png")
mario = pygame.transform.scale(mario, (64, 64))
# FPS - frames per second
x = 25
y = 25
dx = 0
dy = 0
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (150, 0, 0), (50,50), 5)

    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
