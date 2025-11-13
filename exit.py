from constants import *
class Exit(pygame.sprite.Sprite):
    def __init__(self, game, x, y, texture_to_use):
        self.groups = game.all_sprites, game.exit_group
        super().__init__(self.groups)
        self.game = game
        self.image = texture_to_use
        self.rect = self.image.get_rect()
        tile_center_x = MAP_OFFSET_X + (x * TILE_SIZE) + (TILE_SIZE // 2)
        tile_center_y = MAP_OFFSET_Y + (y * TILE_SIZE) + (TILE_SIZE // 2)
        self.rect.center = (tile_center_x, tile_center_y)
