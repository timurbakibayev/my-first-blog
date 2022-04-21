import pygame
screen_size = (1200, 600)
hero_size = (screen_size[1]//80*4, screen_size[1]//80*7)

map_height = 15
mrp = screen_size[1] // map_height
brick_size = (mrp, mrp)

bg_images = list()
for i in range(1, 6):
    bg_image = pygame.image.load(f"sprites/plx-{i}.png")
    bg_image = pygame.transform.scale(bg_image, screen_size)
    bg_images.append(bg_image)

apple = pygame.image.load("sprites/apple.png")
apple = pygame.transform.scale(apple, brick_size)


hero_idle = pygame.image.load("sprites/idle.gif")
hero_idle_right = pygame.transform.scale(hero_idle, hero_size)
hero_idle_left = pygame.transform.flip(hero_idle_right, flip_x=True, flip_y=False)

hero_holding = pygame.image.load("sprites/holding.gif")
hero_holding_right = pygame.transform.scale(hero_holding, hero_size)
hero_holding_left = pygame.transform.flip(hero_holding_right, flip_x=True, flip_y=False)

hero_run = pygame.image.load("sprites/run.gif")
hero_run_right = pygame.transform.scale(hero_run, hero_size)
hero_run_left = pygame.transform.flip(hero_run_right, flip_x=True, flip_y=False)

hero_landing = pygame.image.load("sprites/landing.png")
hero_landing_right = pygame.transform.scale(hero_landing, hero_size)
hero_landing_left = pygame.transform.flip(hero_landing_right, flip_x=True, flip_y=False)

hero_jumping = pygame.image.load("sprites/jump.png")
hero_jumping_right = pygame.transform.scale(hero_jumping, hero_size)
hero_jumping_left = pygame.transform.flip(hero_jumping_right, flip_x=True, flip_y=False)


def crop(big_image, rect, size):
    cropped = pygame.Surface((rect[2], rect[3]))
    cropped.blit(big_image, (0, 0), rect)
    return pygame.transform.scale(cropped, size)


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