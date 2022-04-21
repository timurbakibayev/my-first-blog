from load_sprites import *
import pygame
from maps import levels
from hero import Hero
pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Jungle")
playing = True
clock = pygame.time.Clock()


background = 0

hero1 = Hero.from_mrp(mrp=mrp)
hero2 = Hero.from_mrp(mrp=mrp)
hero2.x = 10*mrp
heroes = [hero1, hero2]

horizontal_speed = mrp//4
current_level = 0
level = levels[current_level]


def next_level():
    global current_level, level, levels, heroes
    current_level = (current_level + 1) % len(levels)
    level = levels[current_level]
    heroes[0].x = 2 * mrp
    heroes[0].y = 5 * mrp
    heroes[1].x = 10 * mrp
    heroes[1].y = 5 * mrp


while playing:  # Game loop
    for hero in heroes:
        hero.update(
            level,
            hero_size,
            brick_size,
            screen_size,
            horizontal_speed,
            mrp,
            next_level,
        )

    for hero in heroes:
        if hero.x + background < screen_size[0]*0.1:
            background += (screen_size[0] * 0.1 - hero.x - background) / 2
        if hero.x + background > screen_size[0]*0.7:
            background += (screen_size[0]*0.7 - hero.x - background)/2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
            for hero in heroes:
                if event.key == pygame.K_SPACE:
                    hero.pressing_spacebar = True
                if event.key == pygame.K_LEFT:
                    hero.dx = -horizontal_speed
                    hero.look_right = False
                if event.key == pygame.K_RIGHT:
                    hero.dx = horizontal_speed
                    hero.look_right = True
                if event.key == pygame.K_UP:
                    if hero.jumping < 1:
                        hero.dy = -horizontal_speed*1.4
                        if hero.jumping == 1:
                            hero.dy = -horizontal_speed
                        hero.jumping += 1
        if event.type == pygame.KEYUP:
            for hero in heroes:
                if event.key == pygame.K_LEFT:
                    hero.dx = 0
                if event.key == pygame.K_RIGHT:
                    hero.dx = 0
                if event.key == pygame.K_SPACE:
                    hero.pressing_spacebar = False

    # clear screen
    screen.fill((255, 255, 255))
    for i in [0, 4]:
        bg_image = bg_images[i]
        background_position = (background/(6-i)) % screen_size[0]
        screen.blit(bg_image, (background_position, 0))
        screen.blit(bg_image, (background_position-screen_size[0], 0))
        screen.blit(bg_image, (background_position+screen_size[0], 0))

    for hero in heroes:
        if hero.look_right:
            icon = hero_idle_right
            if hero.dx != 0:
                icon = hero_run_right
            if hero.jumping > 0:
                icon = hero_jumping_right
            if hero.dy > 1:
                icon = hero_landing_right
            if hero.holding_wall:
                icon = hero_holding_right
        else:
            icon = hero_idle_left
            if hero.dx != 0:
                icon = hero_run_left
            if hero.jumping > 0:
                icon = hero_jumping_left
            if hero.dy > 1:
                icon = hero_landing_left
            if hero.holding_wall:
                icon = hero_holding_left
        screen.blit(icon, (hero.x + background, hero.y))

    # draw level
    for i in range(len(level)):
        for j in range(len(level[i])):
            brick_x = j*brick_size[0]
            brick_y = i*brick_size[1]
            if 7 > level[i][j] > 0:
                screen.blit(grounds[level[i][j]], (brick_x + background, brick_y))
            if level[i][j] == 7:
                screen.blit(apple, (brick_x + background, brick_y))

    # Display what we have drawn before
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
