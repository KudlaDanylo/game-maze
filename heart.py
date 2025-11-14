from constants import  *
class Heart(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.ui_sprites
        super().__init__(self.groups)
        self.game = game
        self.image = HEART_TEXTURE
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def set_empty(self):
        self.image = HEART_LOST_TEXTURE

    def set_full(self):
        self.image = HEART_TEXTURE

