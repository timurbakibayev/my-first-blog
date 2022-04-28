from dataclasses import dataclass
import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game


@dataclass
class Hero:
    x: int
    y: int
    dx: float
    dy: float
    look_right: bool
    jumping: int
    pressing_spacebar: bool
    holding_wall: bool
    horizontal_speed: int
    dead: bool = False

    @classmethod
    def from_mrp(cls, mrp: int) -> "Hero":
        return cls(
            x=2 * mrp,
            y=5 * mrp,
            dx=0,
            dy=0,
            pressing_spacebar=False,
            jumping=1,
            look_right=True,
            holding_wall=False,
            horizontal_speed=mrp // 4,
        )

    def key_pressed(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.pressing_spacebar = True
            if event.key == pygame.K_LEFT:
                self.dx = -self.horizontal_speed
                self.look_right = False
            if event.key == pygame.K_RIGHT:
                self.dx = self.horizontal_speed
                self.look_right = True
            if event.key == pygame.K_UP:
                if self.jumping < 1:
                    self.dy = -self.horizontal_speed*1.4
                    if self.jumping == 1:
                        self.dy = -self.horizontal_speed
                    self.jumping += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.dx = 0
            if event.key == pygame.K_RIGHT:
                self.dx = 0
            if event.key == pygame.K_SPACE:
                self.pressing_spacebar = False

    def update(
            self,
            game: "Game",
    ):
        was_x = self.x
        self.x += self.dx
        hero_rect = pygame.Rect(self.x, self.y, game.hero_size[0], game.hero_size[1])
        horizontal_collision = False
        for i in range(len(game.level)):
            for j in range(len(game.level[i])):
                if game.level[i][j] != 0:
                    brick_rect = pygame.Rect(
                        j * game.brick_size[0],
                        i * game.brick_size[1],
                        game.brick_size[0],
                        game.brick_size[1],
                    )
                    if hero_rect.colliderect(brick_rect):
                        if game.level[i][j] < 7:
                            self.x = was_x
                            horizontal_collision = True
                        if game.level[i][j] == 7:
                            game.next_level()

        was_y = self.y

        if self.pressing_spacebar and horizontal_collision:
            self.jumping = 0
        else:
            self.y += self.dy

        self.dy += 1
        if self.dy > self.horizontal_speed:
            self.dy = self.horizontal_speed

        hero_rect = pygame.Rect(self.x, self.y, game.hero_size[0], game.hero_size[1])
        for i in range(len(game.level)):
            for j in range(len(game.level[i])):
                if game.level[i][j] != 0:
                    brick_rect = pygame.Rect(
                        j * game.brick_size[0],
                        i * game.brick_size[1],
                        game.brick_size[0],
                        game.brick_size[1],
                    )
                    if hero_rect.colliderect(brick_rect):
                        if game.level[i][j] < 7:
                            self.y = was_y
                            self.jumping = 0
                            self.dy = 0
                        if game.level[i][j] == 7:
                            game.next_level()

        if self.y > game.screen_size[1]:
            self.dead = True
            return

        self.holding_wall = horizontal_collision and self.pressing_spacebar

        hero_rect = pygame.Rect(self.x, self.y, game.hero_size[0], game.hero_size[1])
        for coin_x, coin_y in game.coins:
            coin_rect = pygame.Rect(coin_x, coin_y, game.brick_size[0], game.brick_size[1])
            if hero_rect.colliderect(coin_rect):
                game.eat_coin((coin_x, coin_y))
