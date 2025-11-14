import random

import pygame.draw

from constants import *

class BaseMonster(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.monsters
        super().__init__(self.groups)
        self.game = game
        self.rect = self.image.get_rect()
        hitbox_size = int(TILE_SIZE * 0.75)
        self.hit_rect = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.rect.topleft = (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(self.hit_rect.center)
        self.vel = pygame.math.Vector2(0, 0)
        self.damage = 0

    def collide_with_walls(self,dir):
        collided = False
        if dir == "x":
            for wall in self.game.walls:
                if self.hit_rect.colliderect(wall.hit_rect):
                    if self.vel.x > 0:
                        self.hit_rect.right = wall.hit_rect.left
                    if self.vel.x < 0:
                        self.hit_rect.left = wall.hit_rect.right
                    self.pos.x = self.hit_rect.centerx
                    collided = True
        if dir == "y":
            for wall in self.game.walls:
                if self.hit_rect.colliderect(wall.hit_rect):
                    if self.vel.y > 0:
                        self.hit_rect.bottom = wall.hit_rect.top
                    if self.vel.y < 0:
                        self.hit_rect.top = wall.hit_rect.bottom
                    self.pos.y = self.hit_rect.centery
                    collided = True
        return collided

    def base_update(self):
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls("x")
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls("y")
        self.rect.center = self.hit_rect.center

class Patrol(BaseMonster):
    def __init__(self, game, x, y):
        self.animation_frames = PACMAN_ANIMATION
        self.current_frame = 0
        self.last_update = 0
        self.direction = "idle"
        self.image = self.animation_frames[self.direction][self.current_frame]
        super().__init__(game, x, y)
        self.damage = PATROL_DAMAGE
        maze = self.game.maze_data

        x_len = 0
        for i in range(x - 1, 0, 1):
            if maze[y][i] == 1:
                break
            x_len += 1

        for i in range(x + 1, MAZE_WIDTH - 1):
            if maze[y][i] == 1:
                break
            x_len += 1

        y_len = 0
        for i in range(y - 1, 0, -1):
            if maze[i][x] == 1:
                break
            y_len += 1

        for i in range(y + 1, MAZE_HEIGHT - 1):
            if maze[i][x] == 1:
                break
            y_len += 1

        if x_len > y_len:
            self.vel = pygame.math.Vector2(MONSTER_SPEED, 0)
        else:
            self.vel = pygame.math.Vector2(0, MONSTER_SPEED)

        if random.choice([True, False]):
            self.vel *= -1
    def set_direction(self):
        if self.vel.x > 0:
            self.direction = "right"
        elif self.vel.x < 0:
            self.direction = "left"
        elif self.vel.y > 0:
            self.direction = "down"
        elif self.vel.y < 0:
            self.direction = "up"
        else:
            self.direction = "idle"

    def animate(self):
        now = pygame.time.get_ticks()
        if not self.animation_frames.get(self.direction):
            self.direction = "idle"

        if now - self.last_update > ANIMATION_SPEED * 1000:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.direction])
            self.image = self.animation_frames[self.direction][self.current_frame]

    def update(self):
        self.set_direction()
        self.pos += self.vel
        self.hit_rect.centerx = self.pos.x
        if self.collide_with_walls("x"):
            self.vel.x *= -1
        self.hit_rect.centery = self.pos.y
        if self.collide_with_walls("y"):
            self.vel.y *= -1
        self.rect.center = self.hit_rect.center

        self.rect.center = self.hit_rect.center
        self.animate()

class Hunter(BaseMonster):
    def __init__(self, game, x, y):
        self.image = HUNTER_TEXTURE
        super().__init__(game, x, y)
        self.damage = HUNTER_DAMAGE
        self.patrol_speed = MONSTER_SPEED
        self.chase_speed = HUNTER_SPEED
        self.state = "patrolling"
        self.path = []
        self.path_recalc_timer = 0
        self.path_recalc_interval = 0.5
        self.vel = pygame.math.Vector2(self.patrol_speed, 0)
        if random.choice([True, False]):
            self.vel = self.vel.rotate(90)
    def can_see_player(self):
        if not self.game.player:
            return False

        for smoke in self.game.smokes:
            if smoke.hit_rect.colliderect(self.game.player.hit_rect):
                return False
        p1 = self.pos
        p2 = self.game.player.pos

        for smoke in self.game.smokes:
            if smoke.hit_rect.clipline(p1, p2):
                vec_to_monster = self.pos - p2
                player_vel = self.game.player.vel
                if player_vel.length_squared() == 0:
                    return False
                dot_product = vec_to_monster.dot(player_vel)
                if dot_product > 0:
                    return True
                else:
                    return False
        return True


    def update(self):
        is_player_visible = False
        if self.game.player:
            dist = self.pos.distance_to(self.game.player.pos)
            if dist < HUNTER_VISION_RANGE and self.can_see_player():
                is_player_visible = True
        if is_player_visible:
            self.state = "chasing"
        else:
            self.state = "patrolling"

        if self.state == "chasing":
            self.chase(self.game.dt)
        else:
            self.patrol()
        super().base_update()

    def patrol(self):
        next_pos = self.pos + self.vel
        next_hit_rect = self.hit_rect.copy()
        next_hit_rect.center = next_pos

        hit_wall = False
        for wall in self.game.walls:
            if next_hit_rect.colliderect(wall.hit_rect):
                hit_wall = True
                break

        if hit_wall or self.vel.length_squared() == 0:
            self.chose_new_patrol_direction()

    def chose_new_patrol_direction(self):
        x = (self.hit_rect.centerx - MAP_OFFSET_X) // TILE_SIZE
        y = (self.hit_rect.centery - MAP_OFFSET_Y) // TILE_SIZE
        maze = self.game.maze_data

        possible_directions = []
        if maze[y-1][x] == 0:
            possible_directions.append(pygame.math.Vector2(0, -self.patrol_speed))
        if maze[y+1][x] == 0:
            possible_directions.append(pygame.math.Vector2(0, self.patrol_speed))
        if maze[y][x-1] == 0:
            possible_directions.append(pygame.math.Vector2(-self.patrol_speed, 0))
        if maze[y][x+1] == 0:
            possible_directions.append(pygame.math.Vector2(self.patrol_speed, 0))

        if possible_directions:
            self.vel = random.choice(possible_directions)
        else:
            self.vel *= -1

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

            if dist_vec.length_squared() > self.chase_speed**2:
                self.vel = dist_vec.normalize() * self.chase_speed
            else:
                self.pos = target_vec
                self.path.pop(0)