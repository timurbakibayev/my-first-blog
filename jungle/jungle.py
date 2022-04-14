import pygame
pygame.init()
screen_size = (800, 400)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Jungle")
playing = True
clock = pygame.time.Clock()
hero_size = (40, 70)
hero_idle = pygame.image.load("sprites/idle.gif")
hero_idle_right = pygame.transform.scale(hero_idle, hero_size)
hero_idle_left = pygame.transform.flip(hero_idle_right, flip_x=True, flip_y=False)

hero_run = pygame.image.load("sprites/run.gif")
hero_run_right = pygame.transform.scale(hero_run, hero_size)
hero_run_left = pygame.transform.flip(hero_run_right, flip_x=True, flip_y=False)

x = 10
y = 10
dx = 0
dy = 0
horizontal_speed = 10
look_right = True
jumping = 1

while playing:  # Game loop
    x += dx
    y += dy
    if y > screen_size[1] - hero_size[1]:
        y = screen_size[1] - hero_size[1]
        jumping = 0
    dy += 1
    if dy > 10:
        dy = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
            if event.key == pygame.K_LEFT:
                dx = -horizontal_speed
                look_right = False
            if event.key == pygame.K_RIGHT:
                dx = horizontal_speed
                look_right = True
            if event.key == pygame.K_UP:
                if jumping == 0:
                    dy = -15
                    jumping = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dx = 0
            if event.key == pygame.K_RIGHT:
                dx = 0

    # clear screen
    screen.fill((255, 255, 255))
    if look_right:
        icon = hero_idle_right
        if dx != 0:
            icon = hero_run_right
    else:
        icon = hero_idle_left
        if dx != 0:
            icon = hero_run_left

    screen.blit(icon, (x, y))
    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
