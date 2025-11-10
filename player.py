import pygame.key

from constants import *
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)

        self.game = game
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (TILE_SIZE // 2, TILE_SIZE //2), TILE_SIZE // 4)
        self.rect = self.image.get_rect()
        self.hit_rect = pygame.Rect(0, 0, TILE_SIZE * 0.75, TILE_SIZE * 0.75)
        self.rect.topleft = (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE)
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(self.hit_rect.center)
        self.vel = pygame.math.Vector2(0,0)

    def get_keys(self):
        self.vel = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vel.y = PLAYER_SPEED
        if keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED

    def update(self):
        self.get_keys()
        self.pos += self.vel

        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls("x")

        self.hit_rect.centery = self.pos.y
        self.collide_with_walls("y")
        self.rect.center = self.hit_rect.center

    def collide_with_walls(self, dir):
        if dir == "x":
            for wall in self.game.walls:
                if self.hit_rect.colliderect(wall.hit_rect):
                    if self.vel.x > 0:
                        self.hit_rect.right = wall.hit_rect.left
                    if self.vel.x < 0:
                        self.hit_rect.left = wall.hit_rect.right
                    self.pos.x = self.hit_rect.centerx

        if dir == "y":
            for wall in self.game.walls:
                if self.hit_rect.colliderect(wall.hit_rect):
                    if self.vel.y > 0:
                        self.hit_rect.bottom = wall.hit_rect.top
                    if self.vel.y < 0:
                        self.hit_rect.top = wall.hit_rect.bottom
                    self.pos.y = self.hit_rect.centery