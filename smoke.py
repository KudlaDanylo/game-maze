import pygame.time

from constants import  *
class Smoke(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.smokes
        super().__init__(self.groups)
        self.game = game
        self.frames = SMOKE_FRAMES
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect.copy()
        self.spawn_time = pygame.time.get_ticks()
        self.frame_duration = SMOKE_DURATION / len(self.frames) * 1000

    def update(self):
        now = pygame.time.get_ticks()
        age = now - self.spawn_time

        if age > SMOKE_DURATION * 1000:
            self.kill()
            return

        current_frame_index = int(age // self.frame_duration)
        if current_frame_index >= len(self.frames):
            current_frame_index = len(self.frames) - 1

        self.image = self.frames[current_frame_index]