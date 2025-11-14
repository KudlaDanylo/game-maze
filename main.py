import random
import sys

from constants import *
from map_generation import  maze_generation
from wall import Wall
from player import Player
from exit import Exit
from monster import Patrol, Hunter
from coin import Coin
from heart import Heart

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("game")
        self.dt = 0
        self.font = pygame.font.Font(None, 40)
        self.fog_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.coins_collected = 0
        self.rockets = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.inner_walls = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()

        self.heart_sprites = []
        self.maze_data = []
        self.player = None
        self.player_start_pos = None
        self.level = 1
        self.lives = PLAYER_LIVES


    def new_level(self):

        for sprite in self.all_sprites:
            self.kill()
        self.heart_sprites = []
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

    #Гравець
        self.player_start_pos = None
        if empty_tiles:
            self.player_start_pos = random.choice(empty_tiles)
            empty_tiles.remove(self.player_start_pos)
            self.player = Player(self, self.player_start_pos[0], self.player_start_pos[1])
    #Вихід
        corners = {
            "top_left": (1,1),
            "top_right": (MAZE_WIDTH - 2, 1),
            "bottom_left": (1, MAZE_HEIGHT - 2),
            "bottom_right": (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
        }
        furthest_corner_pos = None
        max_distance = -1
        px, py = self.player_start_pos

        for corner_name, (cx, cy) in corners.items():
            distance = abs(cx - px) + abs(cy - py)
            if distance > max_distance:
                max_distance = distance
                furthest_corner_pos = (cx, cy)

        exit_pos = furthest_corner_pos
        if exit_pos[0]< MAZE_WIDTH / 2:
            texture_to_use = EXIT_TEXTURE_LEFT
        else:
            texture_to_use = EXIT_TEXTURE_RIGHT

        Exit(self, exit_pos[0], exit_pos[1], texture_to_use)

        if exit_pos in empty_tiles:
            empty_tiles.remove(exit_pos)

    #Монстри
        safe_spawn_points = []
        if self.player_start_pos:
            for pos in empty_tiles:
                distance = abs(pos[0] - self.player_start_pos[0]) + abs(pos[1] - self.player_start_pos[1])

                if distance > 5:
                    safe_spawn_points.append(pos)

        num_monsters = 5
        for i in range(num_monsters):
            if safe_spawn_points:
                pos = random.choice(safe_spawn_points)
                safe_spawn_points.remove(pos)
                if i < 2:
                    Hunter(self, pos[0], pos[1])
                else:
                    Patrol(self, pos[0], pos[1])
            else:
                break

        num_coins = 7
        for _ in range(num_coins):
            if empty_tiles:
                pos = random.choice(empty_tiles)
                empty_tiles.remove(pos)
                Coin(self, pos[0], pos[1])

    #Життя
        for i in range(PLAYER_LIVES):
            x_pos = 0 + ((36 + HEART_PADDING) * (PLAYER_LIVES - i))
            y_pos = HEART_PADDING
            heart = Heart(self, x_pos, y_pos)
            self.heart_sprites.append(heart)
        self.heart_sprites.sort(key=lambda sprite: sprite.rect.x)


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

             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and self.rockets > 0:
                     self.use_rocket()

    def update(self):
        self.all_sprites.update()
        if self.player:
            coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            for hit in coin_hits:
                self.coins_collected += 1
                if self.coins_collected >= COINS_FOR_ROCKET:
                    self.coins_collected -= COINS_FOR_ROCKET
                    self.rockets += 1

            self.check_monster_hits()

            exit_hits = pygame.sprite.spritecollide(self.player, self.exit_group, False)
            if exit_hits:
                self.running = False

    def check_monster_hits(self):
        if not self.player:
            return
        now = pygame.time.get_ticks() / 500
        if now - self.player.last_damage_time > DAMAGE_COOLDOWN:
            for monster in self.monsters:
                if self.player.hit_rect.colliderect(monster.hit_rect):
                    self.player.take_damage(monster.damage)

    def player_is_dead(self):
        self.lives -= 1
        if self.lives < len(self.heart_sprites):
            self.heart_sprites[self.lives].set_empty()

        if self.lives > 0:
            self.player = Player(self, self.player_start_pos[0], self.player_start_pos[1])
        else:
            self.running = False

    def use_rocket(self):
        if self.rockets <= 0 or not self.player:
            return
        closest_wall = None
        min_dist = float("inf")
        for wall in self.inner_walls:
            dist = self.player.pos.distance_to(wall.hit_rect.center)
            if dist < min_dist:
                min_dist = dist
                closest_wall = wall

        if closest_wall and min_dist < TILE_SIZE * 2:
            self.rockets -= 1
            closest_wall.kill()
            self.maze_data[closest_wall.y][closest_wall.x] = 0

    def find_path(self, start_pos, end_pos):
        grid = self.maze_data
        queue = [(start_pos, [start_pos])]
        visited = {start_pos}

        while queue:
            current_pos, path = queue.pop(0)
            if current_pos == end_pos:
                return path

            x, y = current_pos
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)

                if (0 <= next_x < MAZE_WIDTH and 0 <= next_y < MAZE_HEIGHT and grid[next_y][next_x] == 0 and next_pos not in visited):
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append((next_pos, new_path))

        return

    def draw(self):
        self.screen.fill(SCREEN_COLOR)
        self.all_sprites.draw(self.screen)
        self.fog_surface.fill((*FOG_COLOR, FOG_ALPHA))
        if self.player:
            pygame.draw.circle(self.fog_surface,(*FOG_COLOR, FOG_ALPHA_GRADIENT), self.player.hit_rect.center, VISION_RADIUS_OUTER)
            pygame.draw.circle(self.fog_surface,(0,0,0,0), self.player.hit_rect.center, VISION_RADIUS_INNER)
        self.screen.blit(self.fog_surface, (0, 0))

        self.ui_sprites.draw(self.screen)
        coin_text = f" {self.coins_collected}"
        self.draw_text(coin_text, 1230, 12, WHITE)
        rocket_text = f"Ракети: {self.rockets}"
        self.draw_text(rocket_text, 200, 10, WHITE)

        #if self.player:
            #self.draw_text(f"HP :{self.player.health}", 10, 70, WHITE)

        self.screen.blit(pygame.image.load("image/money.png"), (1200, 8))
        pygame.display.flip()

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    g = Game()
    g.new_level()
    g.run()