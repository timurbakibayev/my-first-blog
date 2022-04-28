from dataclasses import dataclass
from typing import Tuple
from load_sprites import load_sprites, Sprites

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
    sprites: Sprites
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
            game=self,
        )

        if self.hero.dead:
            self.hero.dead = False
            self.position_hero_start()

        if self.hero.x + self.background < self.screen_size[0] * 0.1:
            self.background += (self.screen_size[0] * 0.1 - self.hero.x - self.background) / 2
        if self.hero.x + self.background > self.screen_size[0] * 0.7:
            self.background += (self.screen_size[0] * 0.7 - self.hero.x - self.background) / 2

    def next_level(self):
        self.current_level = (self.current_level + 1) % len(self.levels)
        self.position_hero_start()

    def position_hero_start(self):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 8:
                    self.hero.x = j*self.mrp
                    self.hero.y = i*self.mrp-self.hero_size[1]

    @classmethod
    def load(cls, clock: Clock, screen_size: Tuple[int, int]) -> "Game":
        mrp: int = screen_size[1] // 15
        hero_size = (screen_size[1] // 80 * 4, screen_size[1] // 80 * 7)
        brick_size = (mrp, mrp)
        game = cls(
            levels=levels,
            clock=clock,
            hero=Hero.from_mrp(mrp),
            mrp=mrp,
            screen_size=screen_size,
            brick_size=brick_size,
            hero_size=hero_size,
            sprites=load_sprites(
                screen_size=screen_size,
                hero_size=hero_size,
                brick_size=brick_size,
            ),
        )
        game.position_hero_start()
        return game

    def draw(self, screen):
        for i in [0, 4]:
            bg_image = self.sprites.bg_images[i]
            background_position = (self.background / (6 - i)) % self.screen_size[0]
            screen.blit(bg_image, (background_position, 0))
            screen.blit(bg_image, (background_position - self.screen_size[0], 0))
            screen.blit(bg_image, (background_position + self.screen_size[0], 0))

        if self.hero.look_right:
            icon = self.sprites.hero_idle_right
            if self.hero.dx != 0:
                icon = self.sprites.hero_run_right
            if self.hero.jumping > 0:
                icon = self.sprites.hero_jumping_right
            if self.hero.dy > 1:
                icon = self.sprites.hero_landing_right
            if self.hero.holding_wall:
                icon = self.sprites.hero_holding_right
        else:
            icon = self.sprites.hero_idle_left
            if self.hero.dx != 0:
                icon = self.sprites.hero_run_left
            if self.hero.jumping > 0:
                icon = self.sprites.hero_jumping_left
            if self.hero.dy > 1:
                icon = self.sprites.hero_landing_left
            if self.hero.holding_wall:
                icon = self.sprites.hero_holding_left
        screen.blit(icon, (self.hero.x + self.background, self.hero.y))

        # draw level
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                brick_x = j * self.brick_size[0]
                brick_y = i * self.brick_size[1]
                if 7 > self.level[i][j] > 0:
                    screen.blit(self.sprites.grounds[self.level[i][j]], (brick_x + self.background, brick_y))
                if self.level[i][j] == 7:
                    screen.blit(self.sprites.apple, (brick_x + self.background, brick_y))

