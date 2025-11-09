import random
import sys
from constants import *
from map_generation import  maze_generation
from wall import Wall
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


all_sprites = pygame.sprite.LayeredUpdates()
walls = pygame.sprite.Group()
inner_walls = pygame.sprite.Group()

class TestGame:
    pass
game = TestGame()
game.all_sprites = all_sprites
game.walls = walls
game.inner_walls = inner_walls

maze_data = maze_generation(MAZE_WIDTH, MAZE_HEIGHT)
game.maze_data = maze_data

inner_walls_list = []
empty_tiles = []
for row, tiles in enumerate(maze_data):
    for col, tile in enumerate(tiles):
        if tile == 1:
            is_inner = 0 < col < MAZE_WIDTH - 1 and 0 < row < MAZE_HEIGHT - 1

            wall = Wall(game, col, row, is_inner)
            if is_inner:
                inner_walls_list.append(wall)
        elif tile == 0 and (0 < col < MAZE_WIDTH - 1 and 0 < row < MAZE_HEIGHT -1):
            empty_tiles.append((col, row))

for wall in inner_walls_list:
        wall.draw_wall_segments()


if empty_tiles:
    start_pos = random.choice(empty_tiles)
    game.player = Player(game, start_pos[1], start_pos[1])




running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(SCREEN_COLOR)


    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()