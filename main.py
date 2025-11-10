import random
import sys
import pygame
from constants import *
from map_generation import  maze_generation
from wall import Wall
from player import Player
from exit import Exit
from monster import Patrol

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("game")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.inner_walls = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

    def new_level(self):

        for sprite in self.all_sprites:
            self.kill()

        self.maze_data = maze_generation(MAZE_WIDTH, MAZE_HEIGHT)
    #Стіни
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
    #Вихід
        # exit_pos = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
        # if exit_pos in empty_tiles:
        #     empty_tiles.remove(exit_pos)

        # Exit(self, exit_pos[0], exit_pos[1])
    #Гравець
        self.player_start_pos = None
        if empty_tiles:
            self.player_start_pos = random.choice(empty_tiles)
            empty_tiles.remove(self.player_start_pos)
            self.player = Player(self, self.player_start_pos[0], self.player_start_pos[1])

    #Вихід
        furthest_pos = None
        max_distance = - 1
        for pos in empty_tiles:
            distance = abs(pos[0] - self.player_start_pos[0]) + abs(pos[1] - self.player_start_pos[1])

        if distance > max_distance:
            max_distance = distance
            furthest_pos = pos

        if furthest_pos:
            Exit(self, furthest_pos[0], furthest_pos[1])
            empty_tiles.remove(furthest_pos)

    #Монстри
        safe_spawn_points = []
        if self.player_start_pos:
            for pos in empty_tiles:
                distance = abs(pos[0] - self.player_start_pos[0]) + abs(pos[1] - self.player_start_pos[1])

                if distance > 5:
                    safe_spawn_points.append(pos)

        num_monsters = 1
        # if len(safe_spawn_points) < num_monsters:
        #     for pos in empty_tiles:
        #         if pos not in safe_spawn_points:
        #             safe_spawn_points.append(pos)

        for _ in range(num_monsters):
            if safe_spawn_points:
                pos = random.choice(safe_spawn_points)
                safe_spawn_points.remove(pos)
                Patrol(self, pos[0], pos[1])


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
        if self.player:
            exit_hits = pygame.sprite.spritecollide(self.player, self.exit_group, False)
            if exit_hits:
                self.running = False

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