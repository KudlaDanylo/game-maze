from constants import *
class Mine(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.mines_group
        super().__init__(self.groups)
        self.game = game
        self.image = MINE_TEXTURE
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect.copy().inflate(-4, -4)

    def update(self):
        if self.game.player and self.hit_rect.colliderect(self.game.player.hit_rect):
            self.game.player.die()
            self.kill()
            return

        monster_hits = pygame.sprite.spritecollide(self, self.game.monsters, False)
        detonated = False
        for monster in monster_hits:
            if self.hit_rect.colliderect(monster.hit_rect):
                if monster.type == "hunter":
                    monster.kill()
                    detonated = True
                elif monster.type == "patrol":
                    detonated = True

        if detonated:
            self.kill()