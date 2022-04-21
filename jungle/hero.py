from dataclasses import dataclass
import pygame


@dataclass
class Hero:
    x: int
    y: int
    dx: int
    dy: int
    look_right: bool
    jumping: int
    pressing_spacebar: bool
    holding_wall: bool

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
        )

    def update(
            self,
            level,
            hero_size,
            brick_size,
            screen_size,
            horizontal_speed,
            mrp,
            next_level,
    ):
        was_x = self.x
        self.x += self.dx
        hero_rect = pygame.Rect(self.x, self.y, hero_size[0], hero_size[1])
        horizontal_collision = False
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] != 0:
                    brick_rect = pygame.Rect(j * brick_size[0], i * brick_size[1], brick_size[0], brick_size[1])
                    if hero_rect.colliderect(brick_rect):
                        if level[i][j] != 7:
                            self.x = was_x
                            horizontal_collision = True
                        if level[i][j] == 7:
                            next_level()

        was_y = self.y

        if self.pressing_spacebar and horizontal_collision:
            self.jumping = 0
        else:
            self.y += self.dy

        self.dy += 1
        if self.dy > horizontal_speed:
            self.dy = horizontal_speed

        hero_rect = pygame.Rect(self.x, self.y, hero_size[0], hero_size[1])
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] != 0:
                    brick_rect = pygame.Rect(j * brick_size[0], i * brick_size[1], brick_size[0], brick_size[1])
                    if hero_rect.colliderect(brick_rect):
                        if level[i][j] != 7:
                            self.y = was_y
                            self.jumping = 0
                            self.dy = 0
                        if level[i][j] == 7:
                            next_level()

        if self.y > screen_size[1]:
            self.x = 2 * mrp
            self.y = 5 * mrp

        self.holding_wall = horizontal_collision and self.pressing_spacebar
