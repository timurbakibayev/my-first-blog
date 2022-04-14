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
mrp = screen_size[1] // map_height
brick_size = (mrp, mrp)

bg_images = list()
for i in range(1, 6):
    bg_image = pygame.image.load(f"sprites/plx-{i}.png")
    bg_image = pygame.transform.scale(bg_image, screen_size)
    bg_images.append(bg_image)

hero_idle = pygame.image.load("sprites/idle.gif")
hero_idle_right = pygame.transform.scale(hero_idle, hero_size)
hero_idle_left = pygame.transform.flip(hero_idle_right, flip_x=True, flip_y=False)

hero_run = pygame.image.load("sprites/run.gif")
hero_run_right = pygame.transform.scale(hero_run, hero_size)
hero_run_left = pygame.transform.flip(hero_run_right, flip_x=True, flip_y=False)

hero_landing = pygame.image.load("sprites/landing.png")
hero_landing_right = pygame.transform.scale(hero_landing, hero_size)
hero_landing_left = pygame.transform.flip(hero_landing_right, flip_x=True, flip_y=False)

hero_jumping = pygame.image.load("sprites/jump.png")
hero_jumping_right = pygame.transform.scale(hero_jumping, hero_size)
hero_jumping_left = pygame.transform.flip(hero_jumping_right, flip_x=True, flip_y=False)


def crop(big_image, rect, brick_size):
    cropped = pygame.Surface((rect[2], rect[3]))
    cropped.blit(big_image, (0, 0), rect)
    return pygame.transform.scale(cropped, brick_size)


jungle = pygame.image.load("sprites/jungle.png")

"""
1 - grass top
2 - no grass
3 - grass left and right
4 - grass right
5 - grass left
"""
grounds = [
    None,
    crop(jungle, (16, 224, 32, 32), brick_size),
    crop(jungle, (305, 209, 32, 32), brick_size),
    crop(jungle, (656, 136, 32, 32), brick_size),
    crop(jungle, (193, 241, 32, 32), brick_size),
    crop(jungle, (257, 241, 32, 32), brick_size)
]

background = 0
x = 2*mrp
y = 5*mrp
dx = 0
dy = 0
horizontal_speed = mrp//4
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
    if dy > horizontal_speed:
        dy = horizontal_speed

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
                    dy = -horizontal_speed*1.4
                    if jumping == 1:
                        dy = -horizontal_speed
                    jumping += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dx = 0
            if event.key == pygame.K_RIGHT:
                dx = 0

    # clear screen
    screen.fill((255, 255, 255))
    for i in [0, 1, 2, 3, 4]:
        bg_image = bg_images[i]
        background_position = (background/(6-i)) % screen_size[0]
        screen.blit(bg_image, (background_position, 0))
        screen.blit(bg_image, (background_position-screen_size[0], 0))
        screen.blit(bg_image, (background_position+screen_size[0], 0))

    if look_right:
        icon = hero_idle_right
        if dx != 0:
            icon = hero_run_right
        if jumping > 0:
            icon = hero_jumping_right
        if dy > 1:
            icon = hero_landing_right
    else:
        icon = hero_idle_left
        if dx != 0:
            icon = hero_run_left
        if jumping > 0:
            icon = hero_jumping_left
        if dy > 1:
            icon = hero_landing_left

    # draw level
    for i in range(len(level)):
        for j in range(len(level[i])):
            brick_x = j*brick_size[0]
            brick_y = i*brick_size[1]
            if level[i][j] > 0:
                screen.blit(grounds[level[i][j]], (brick_x + background, brick_y))

    screen.blit(icon, (x + background, y))

    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
