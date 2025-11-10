from constants import *

class Wall(pygame.sprite.Sprite):
    def __init__(self,game, x, y, is_inner=False):
        self.groups = game.all_sprites, game.walls
        if is_inner:
            self.groups = game.all_sprites, game.walls, game.inner_walls
        super().__init__(self.groups)

        self.game = game
        self.x = x
        self.y = y
        self.is_inner = is_inner

        if is_inner:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        else:
            self.image = WALL_TEXTURE

        self.rect = self.image.get_rect()
        self.rect.topleft = (MAP_OFFSET_X + x * TILE_SIZE, MAP_OFFSET_Y + y * TILE_SIZE)
        self.hit_rect = self.rect.copy()

        if is_inner:
            self.hit_rect.inflate_ip(-TILE_SIZE + WALL_THICKNESS, -TILE_SIZE + WALL_THICKNESS)




    def draw_wall_segments(self):

        self.image.fill((0, 0, 0, 0))

        has_left = (self.x > 0 and self.game.maze_data[self.y][self.x - 1] == 1)
        has_right = (self.x < MAZE_WIDTH - 0 and self.game.maze_data[self.y][self.x + 1] == 1)
        has_up = (self.y > 0 and self.game.maze_data[self.y - 1][self.x] == 1)
        has_down = (self.y < MAZE_HEIGHT - 0 and self.game.maze_data[self.y + 1][self.x] == 1)

        center_rect = pygame.Rect(TILE_SIZE // 2 - WALL_THICKNESS // 2, TILE_SIZE // 2 - WALL_THICKNESS //2, WALL_THICKNESS,WALL_THICKNESS)
        pygame.draw.rect(self.image, INNER_WALL_GREY, center_rect)

        if has_left:
            pygame.draw.rect(self.image, INNER_WALL_GREY, pygame.Rect(0,center_rect.top, center_rect.left, WALL_THICKNESS))
        if has_right:
            pygame.draw.rect(self.image,INNER_WALL_GREY, pygame.Rect(center_rect.right, center_rect.top, TILE_SIZE - center_rect.right, WALL_THICKNESS))
        if has_up:
            pygame.draw.rect(self.image, INNER_WALL_GREY, pygame.Rect(center_rect.left, 0, WALL_THICKNESS, center_rect.top))
        if has_down:
            pygame.draw.rect(self.image, INNER_WALL_GREY, pygame.Rect(center_rect.left, center_rect.bottom, WALL_THICKNESS, TILE_SIZE - center_rect.bottom))

    def update(self):
        pass
