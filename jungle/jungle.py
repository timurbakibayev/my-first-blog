import pygame
from maps import levels
pygame.init()
screen_size = (1200, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Jungle")
playing = True
clock = pygame.time.Clock()
hero_size = (screen_size[1]//80*4, screen_size[1]//80*7)
map_height = len(levels[0])
brick_size = (screen_size[1] // map_height, screen_size[1] // map_height)

bg_image = pygame.image.load("sprites/plx-5.png")
bg_image = pygame.transform.scale(bg_image, screen_size)

hero_idle = pygame.image.load("sprites/idle.gif")
hero_idle_right = pygame.transform.scale(hero_idle, hero_size)
hero_idle_left = pygame.transform.flip(hero_idle_right, flip_x=True, flip_y=False)

hero_run = pygame.image.load("sprites/run.gif")
hero_run_right = pygame.transform.scale(hero_run, hero_size)
hero_run_left = pygame.transform.flip(hero_run_right, flip_x=True, flip_y=False)

hero_landing = pygame.image.load("sprites/landing.png")
hero_landing_right = pygame.transform.scale(hero_landing, hero_size)
hero_landing_left = pygame.transform.flip(hero_landing_right, flip_x=True, flip_y=False)


def crop(big_image, rect):
    cropped = pygame.Surface((rect[2], rect[3]))
    cropped.blit(big_image, (0, 0), rect)
    return cropped


jungle = pygame.image.load("sprites/jungle.png")
ground_with_gras = crop(jungle, (16, 224, 32, 32))
ground_with_gras = pygame.transform.scale(ground_with_gras, brick_size)
ground = crop(jungle, (305, 209, 32, 32))
ground = pygame.transform.scale(ground, brick_size)

background = 0
x = 10
y = 10
dx = 0
dy = 0
horizontal_speed = 10
look_right = True
jumping = 1
level = levels[0]

while playing:  # Game loop
    was_x = x
    x += dx
    hero_rect = pygame.Rect(x, y, hero_size[0], hero_size[1])
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] != 0:
                brick_rect = pygame.Rect(j*brick_size[0], i*brick_size[1], brick_size[0], brick_size[1])
                if hero_rect.colliderect(brick_rect):
                    x = was_x

    was_y = y
    y += dy

    dy += 1
    if dy > 10:
        dy = 10

    hero_rect = pygame.Rect(x, y, hero_size[0], hero_size[1])
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] != 0:
                brick_rect = pygame.Rect(j*brick_size[0], i*brick_size[1], brick_size[0], brick_size[1])
                if hero_rect.colliderect(brick_rect):
                    y = was_y
                    jumping = 0
                    dy = 0

    if x + background < screen_size[0]*0.1:
        background += horizontal_speed
    if x + background > screen_size[0]*0.8:
        background -= horizontal_speed

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
                if jumping < 2:
                    dy = -14
                    if jumping == 1:
                        dy = -10
                    jumping += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dx = 0
            if event.key == pygame.K_RIGHT:
                dx = 0

    # clear screen
    screen.fill((255, 255, 255))
    background_position = background/2 % screen_size[0]
    screen.blit(bg_image, (background_position, 0))
    screen.blit(bg_image, (background_position-screen_size[0], 0))
    screen.blit(bg_image, (background_position+screen_size[0], 0))

    if look_right:
        icon = hero_idle_right
        if dx != 0:
            icon = hero_run_right
        if dy > 1:
            icon = hero_landing_right
    else:
        icon = hero_idle_left
        if dx != 0:
            icon = hero_run_left
        if dy > 1:
            icon = hero_landing_left

    # draw level
    for i in range(len(level)):
        for j in range(len(level[i])):
            brick_x = j*brick_size[0]
            brick_y = i*brick_size[1]
            if level[i][j] == 1:
                screen.blit(ground_with_gras, (brick_x + background, brick_y))
            if level[i][j] == 2:
                screen.blit(ground, (brick_x + background, brick_y))

    screen.blit(icon, (x + background, y))

    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
