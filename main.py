import random
import sys
import pygame


from constants import *
from map_generation import  maze_generation
from wall import Wall
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.inner_walls = pygame.sprite.Group()

    def new_level(self):
        self.maze_data = maze_generation(MAZE_WIDTH, MAZE_HEIGHT)

        inner_walls_list = []
        empty_tiles = []
        for row, tiles in enumerate(self.maze_data):
            for col, tile in enumerate(tiles):
                is_inner = 0 < col < MAZE_WIDTH - 1 and 0 < row < MAZE_HEIGHT - 1
                if tile == 1:
                    wall = Wall(self, col, row, is_inner)

                    if is_inner:
                        inner_walls_list.append(wall)

                elif tile == 0 and is_inner:
                    empty_tiles.append((col, row))

        for wall in inner_walls_list:
                wall.draw_wall_segments()


        if empty_tiles:
            start_pos = random.choice(empty_tiles)
            self.player = Player(self, start_pos[0], start_pos[1])

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                self.running = False
                self.quit_game()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    g = Game()
    g.new_level()
    g.run()