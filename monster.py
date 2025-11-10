import random

import pygame.draw

from constants import *

class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.monsters
        super().__init__(self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect.copy().inflate(-10, -10)
        self.rect.topleft = (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(self.hit_rect.center)
        self.vel = pygame.math.Vector2(0, 0)

    def collide_with_walls(self,dir):
        collided_walls = []
        for wall in self.game.walls:
            if self.hit_rect.colliderect(wall.hit_rect):
                collided_walls.append(wall)

        if not collided_walls:
            return False

        if dir == "x":
            if self.vel.x > 0:
                self.hit_rect.right = collided_walls[0].hit_rect.left
            if self.vel.x < 0:
                self.hit_rect.left = collided_walls[0].hit_rect.right
            #self.vel.x = 0
            self.pos.x = self.hit_rect.centerx
        if dir == "y":
            if self.vel.y > 0:
                self.hit_rect.bottom = collided_walls[0].hit_rect.top
            if self.vel.y < 0:
                self.hit_rect.top = collided_walls[0].hit_rect.bottom
            #self.vel.y = 0
            self.pos.y = self.hit_rect.centery
        return True
    def update(self):
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls("x")
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls("y")
        self.rect.center = self.hit_rect.center

class Patrol(BaseMonster):
    def __init__(self, game, x, y):
        self.image =pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PATROL_COLOR, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 3)
        super().__init__(game, x, y)
        maze = self.game.maze_data
        start_x, start_y = x, y

        x_len = 0
        for i in range(start_x - 1, 0, 1):
            if maze[start_y][i] == 1:
                break
            x_len += 1

        for i in range(start_x + 1, MAZE_WIDTH - 1):
            if maze[start_y][i] == 1:
                break
            x_len += 1

        y_len = 0
        for i in range(start_y - 1, 0, -1):
            if maze[i][start_x] == 1:
                break
            y_len += 1

        for i in range(start_y + 1, MAZE_HEIGHT - 1):
            if maze[i][start_x] == 1:
                break
            y_len += 1

        if x_len > y_len:
            self.vel = pygame.math.Vector2(MONSTER_SPEED, 0)
        else:
            self.vel = pygame.math.Vector2(0, MONSTER_SPEED)

        if random.choice([True, False]):
            self.vel *= -1

    def update(self):
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        if self.collide_with_walls("x"):
            self.vel.x *= -1
        self.hit_rect.centery = self.pos.y
        if self.collide_with_walls("y"):
            self.vel.y *= -1
        self.rect.center = self.hit_rect.center