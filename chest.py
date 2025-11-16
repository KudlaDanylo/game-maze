from constants import *
class Chest(pygame.sprite.Sprite):
    def __init__(self, game, x, y, chest_type):
        self.groups = game.all_sprites, game.chests_group
        super().__init__(self.groups)
        self.game = game
        self.type = chest_type
        self.x = x
        self.y = y

        if self.type == "yellow":
            self.image = CHEST_SMALL_TEXTURE
        else:
            self.image = CHEST_GREAT_TEXTURE

        self.rect = self.image.get_rect()
        self.rect.topleft = (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE)
        self.hit_rect = self.rect.copy().inflate(-4, -4)