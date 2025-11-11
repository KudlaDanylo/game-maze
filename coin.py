from constants import *
class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        super().__init__(self.groups)
        self.game = game
        self.image = COIN_TEXTURE
        self.rect = self.image.get_rect()
        self.rect.center = (MAP_OFFSET_X + (x * TILE_SIZE) + TILE_SIZE // 2, MAP_OFFSET_Y + (y * TILE_SIZE) + TILE_SIZE // 2)

    def update(self):
        pass