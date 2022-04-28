from dataclasses import dataclass
from typing import Tuple
from load_sprites import *

import pygame
from pygame.time import Clock

from hero import Hero
from maps import levels


@dataclass
class Game:
    levels: list[list[list[int]]]
    clock: Clock
    hero: Hero
    mrp: int
    hero_size: Tuple[int, int]
    brick_size: Tuple[int, int]
    screen_size: Tuple[int, int]
    playing: bool = True
    current_level: int = 0
    background: int = 0

    def key_pressed(self, event):
        if event.type == pygame.QUIT:
            self.playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.playing = False
        self.hero.key_pressed(event)

    @property
    def level(self) -> list[list[int]]:
        return self.levels[self.current_level]

    def update(self) -> None:
        self.hero.update(
            mrp=self.mrp,
            level=self.level,
            hero_size=self.hero_size,
            brick_size=self.brick_size,
            screen_size=self.screen_size,
            next_level=self.next_level,
        )
        if self.hero.x + self.background < self.screen_size[0] * 0.1:
            self.background += (self.screen_size[0] * 0.1 - self.hero.x - self.background) / 2
        if self.hero.x + self.background > self.screen_size[0] * 0.7:
            self.background += (self.screen_size[0] * 0.7 - self.hero.x - self.background) / 2

    def next_level(self):
        self.current_level = (self.current_level + 1) % len(self.levels)

    @classmethod
    def load(cls, clock: Clock, screen_size: Tuple[int, int]) -> "Game":
        mrp: int = screen_size[1] // 15
        return cls(
            levels=levels,
            clock=clock,
            hero=Hero.from_mrp(mrp),
            mrp=mrp,
            screen_size=screen_size,
            brick_size=(mrp, mrp),
            hero_size=(mrp, mrp*2),
        )

    def draw(self, screen):
        for i in [0, 4]:
            bg_image = bg_images[i]
            background_position = (self.background / (6 - i)) % self.screen_size[0]
            screen.blit(bg_image, (background_position, 0))
            screen.blit(bg_image, (background_position - self.screen_size[0], 0))
            screen.blit(bg_image, (background_position + self.screen_size[0], 0))

        if self.hero.look_right:
            icon = hero_idle_right
            if self.hero.dx != 0:
                icon = hero_run_right
            if self.hero.jumping > 0:
                icon = hero_jumping_right
            if self.hero.dy > 1:
                icon = hero_landing_right
            if self.hero.holding_wall:
                icon = hero_holding_right
        else:
            icon = hero_idle_left
            if self.hero.dx != 0:
                icon = hero_run_left
            if self.hero.jumping > 0:
                icon = hero_jumping_left
            if self.hero.dy > 1:
                icon = hero_landing_left
            if self.hero.holding_wall:
                icon = hero_holding_left
        screen.blit(icon, (self.hero.x + self.background, self.hero.y))

        # draw level
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                brick_x = j * self.brick_size[0]
                brick_y = i * self.brick_size[1]
                if 7 > self.level[i][j] > 0:
                    screen.blit(grounds[self.level[i][j]], (brick_x + self.background, brick_y))
                if self.level[i][j] == 7:
                    screen.blit(apple, (brick_x + self.background, brick_y))

