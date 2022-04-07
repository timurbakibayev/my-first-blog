import pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Heli")
done = False
clock = pygame.time.Clock()
heli_left = pygame.image.load("heli_left.png")
heli_left = pygame.transform.scale(heli_left, (64, 64))
heli_right = pygame.image.load("heli_right.png")
heli_right = pygame.transform.scale(heli_right, (64, 64))
# Initialize some variables
x = 25
y = 25
dx = 0
dy = 0
up_key = False
looking = "right"
fire_x, fire_y, fire_dx = -100, -100, 0
while not done:
    # GAME UPDATE
    if up_key:
        dy = dy - 0.5
    else:
        dy = dy + 0.5
    if dy > 7:
        dy = 7
    if dy < -7:
        dy = -7
    last_x = x
    last_y = y
    fire_x = fire_x + fire_dx
    x = x + dx
    heli_rect = pygame.Rect(x, y, 64, 64)
    platform_rect = pygame.Rect(100, 300, 200, 30)
    if heli_rect.colliderect(platform_rect):
        x = last_x
        dx = 0
    y = y + dy
    heli_rect = pygame.Rect(x, y, 64, 64)
    platform_rect = pygame.Rect(100, 300, 200, 30)
    if heli_rect.colliderect(platform_rect):
        y = last_y
        dy = 0

    if y < 0:
        y = 0
        dy = 0

    if y > 480 - 64:
        y = 480 - 64
        dy = 0
    # KEYBOARD AND MOUSE HERE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = 5
                looking = "right"
            if event.key == pygame.K_LEFT:
                dx = -5
                looking = "left"
            if event.key == pygame.K_UP:
                up_key = True
            if event.key == pygame.K_SPACE:
                fire_x, fire_y = x+27, y+37
                if looking == "right":
                    fire_dx = 10
                else:
                    fire_dx = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                dx = 0
            if event.key == pygame.K_LEFT:
                dx = 0
            if event.key == pygame.K_UP:
                up_key = False
    screen.fill((255, 255, 255))
    # DRAWING HERE
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 639, 479), 2)
    pygame.draw.rect(screen, (0, 150, 0), (100, 300, 200, 30))
    if looking == "right":
        screen.blit(heli_right, (x, y))
    else:
        screen.blit(heli_left, (x, y))
    pygame.draw.circle(screen, (150, 0, 0), (fire_x, fire_y), 5)
    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
