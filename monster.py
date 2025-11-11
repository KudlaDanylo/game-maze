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
        self.damage = 0

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

    def base_update(self):
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
        self.damage = PATROL_DAMAGE
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

class Hunter(BaseMonster):
    def __init__(self, game, x, y):
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, HUNTER_COLOR, (TILE_SIZE // 2, TILE_SIZE // 2), int(TILE_SIZE * (1/3) * 2))
        super().__init__(game, x, y)
        self.damage = HUNTER_DAMAGE
        self.speed = HUNTER_SPEED
        self.state = "patrolling"
        self.path = []
        self.path_recalc_timer = 0
        self.path_recalc_interval = 0.5
        self.vel = pygame.math.Vector2(MONSTER_SPEED, 0)
        if random.choice([True, False]):
            self.vel = self.vel.rotate(90)

    def update(self):
        if not self.game.player:
            self.state = "patrolling"
        else:
            dist = self.pos.distance_to(self.game.player.pos)
            if dist < HUNTER_VISION_RANGE:
                self.state = "chasing"
            else:
                self.state = "patrolling"

        if self.state == "chasing":
            self.chase(self.game.dt)
        else:
            self.patrol()
        super().base_update()

    def patrol(self):
        old_pos = self.pos.copy()
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        hit_x = self.collide_with_walls("x")
        self.hit_rect.centery = self.pos.y
        hit_y = self.collide_with_walls("y")
        if hit_x or hit_y:
            self.pos = old_pos
            self.hit_rect.center = self.pos
            self.chose_new_patrol_direction()

    def chose_new_patrol_direction(self):
        x = (self.hit_rect.centerx - MAP_OFFSET_X) // TILE_SIZE
        y = (self.hit_rect.centery - MAP_OFFSET_Y) // TILE_SIZE
        maze = self.game.maze_data

        possible_directions = []
        if maze[y-1][x] == 0 and self.vel.y == 0:
            possible_directions.append(pygame.math.Vector2(0, -self.speed))
        if maze[y+1][x] == 0 and self.vel.y == 0:
            possible_directions.append(pygame.math.Vector2(0, self.speed))
        if maze[y][x-1] == 0 and self.vel.x == 0:
            possible_directions.append(pygame.math.Vector2(-self.speed, 0))
        if maze[y][x+1] == 0 and self.vel.x == 0:
            possible_directions.append(pygame.math.Vector2(self.speed, 0))

        if possible_directions:
            self.vel = random.choice(possible_directions)
        else:
            self.vel *= 1

    def chase(self, dt):
        self.path_recalc_timer += dt
        if self.path_recalc_timer >= self.path_recalc_interval:
            self.path_recalc_timer = 0
            if self.game.player:
                monster_tile_x = (self.hit_rect.centerx - MAP_OFFSET_X) // TILE_SIZE
                monster_tile_y = (self.hit_rect.centery - MAP_OFFSET_Y) // TILE_SIZE
                player_tile_x = (self.game.player.hit_rect.centerx - MAP_OFFSET_X) // TILE_SIZE
                player_tile_y = (self.game.player.hit_rect.centery - MAP_OFFSET_Y) // TILE_SIZE
                self.path = self.game.find_path((monster_tile_x, monster_tile_y), (player_tile_x, player_tile_y))
                if self.path:
                    self.path.pop(0)
            else:
                self.path = []
        self.vel = pygame.math.Vector2(0 , 0)
        if self.path:
            next_tile_pos = self.path[0]
            target_pixel_pos = (MAP_OFFSET_X + next_tile_pos[0] * TILE_SIZE + TILE_SIZE // 2, MAP_OFFSET_Y + next_tile_pos[1] * TILE_SIZE + TILE_SIZE // 2)
            target_vec = pygame.math.Vector2(target_pixel_pos)
            dist_vec = target_vec - self.pos

            if dist_vec.length_squared() > self.speed**2:
                self.vel = dist_vec.normalize() * self.speed
            else:
                self.pos = target_vec
                self.path.pop(0)