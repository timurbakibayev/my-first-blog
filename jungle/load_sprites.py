from dataclasses import dataclass
from typing import Tuple

import pygame
from pygame import Surface


@dataclass
class Sprites:
    hero_idle_right: Surface
    hero_run_right: Surface
    hero_jumping_right: Surface
    hero_landing_right: Surface
    hero_holding_right: Surface
    hero_idle_left: Surface
    hero_run_left: Surface
    hero_jumping_left: Surface
    hero_landing_left: Surface
    hero_holding_left: Surface
    apple: Surface
    grounds: list[Surface]
    bg_images: list[Surface]
    coin: Surface


def crop(big_image, rect, size):
    cropped = pygame.Surface((rect[2], rect[3]))
    cropped.blit(big_image, (0, 0), rect)
    return pygame.transform.scale(cropped, size)


def load_sprites(
        screen_size: Tuple[int, int],
        brick_size: Tuple[int, int],
        hero_size: Tuple[int, int],
) -> Sprites:
    bg_images = list()
    for i in range(1, 6):
        bg_image = pygame.image.load(f"sprites/plx-{i}.png")
        bg_image = pygame.transform.scale(bg_image, screen_size)
        bg_images.append(bg_image)

    apple = pygame.image.load("sprites/apple.png")
    apple = pygame.transform.scale(apple, brick_size)

    coin = pygame.image.load("sprites/coin.png")
    coin = pygame.transform.scale(coin, brick_size)

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

    return Sprites(
        hero_idle_right=hero_idle_right,
        hero_run_right=hero_run_right,
        hero_jumping_right=hero_jumping_right,
        hero_landing_right=hero_landing_right,
        hero_holding_right=hero_holding_right,
        hero_idle_left=hero_idle_left,
        hero_run_left=hero_run_left,
        hero_jumping_left=hero_jumping_left,
        hero_landing_left=hero_landing_left,
        hero_holding_left=hero_holding_left,
        apple=apple,
        grounds=grounds,
        bg_images=bg_images,
        coin=coin,
    )
