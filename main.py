import random
import sys

import pygame.constants

from constants import *
from map_generation import  maze_generation
from wall import Wall
from player import Player
from exit import Exit
from monster import Patrol, Hunter
from coin import Coin
from heart import Heart
from smoke import Smoke

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("game")
        self.dt = 0

        self.font_hud =pygame.font.Font(None, HUD_FONT_SIZE)
        self.font_shop_title = pygame.font.Font(None, SHOP_TITLE_FONT_SIZE)
        self.font_shop_item = pygame.font.Font(None, SHOP_ITEM_FONT_SIZE)
        self.font = pygame.font.Font(None, 40)

        self.game_state = "playing"
        self.fog_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.coins_collected = 0
        self.rockets = 0
        self.smoke_grenades = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.inner_walls = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.smokes = pygame.sprite.Group()

        self.heart_sprites = []
        self.maze_data = []
        self.player = None
        self.player_start_pos = None
        self.level = 1
        self.lives = PLAYER_LIVES


        shop_btn_rect_size = SHOP_ICON_SIZE[0]
        self.shop_button_rect = pygame.Rect(SCREEN_WIDTH - 400 - shop_btn_rect_size - 10, 8, shop_btn_rect_size, shop_btn_rect_size)
        shop_w = 400
        shop_h = 300
        self.shop_window_rect = pygame.Rect((SCREEN_WIDTH - shop_w) // 2, (SCREEN_HEIGHT - shop_h) // 2, shop_w, shop_h)
        self.buy_rocket_rect = pygame.Rect(50, 80, shop_w - 100, 60)
        self.buy_smoke_rect = pygame.Rect(50, 160, shop_w - 100, 60)

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

             if event.type == pygame.MOUSEBUTTONDOWN:
                 mouse_pos = pygame.mouse.get_pos()

                 if self.game_state == "playing":
                     if event.button == 3:
                         if self.smoke_grenades > 0:
                             distance = self.player.pos.distance_to(mouse_pos)
                             if distance <= VISION_RADIUS_OUTER:
                                 Smoke(self, mouse_pos)
                                 self.smoke_grenades -= 1

                     elif event.button == 1:
                         if self.shop_button_rect.collidepoint(mouse_pos):
                             self.game_state = "shop"

                 elif self.game_state == "shop":
                     if event.button == 1:
                         local_pos = (mouse_pos[0] - self.shop_window_rect.x, mouse_pos[1] - self.shop_window_rect.y)
                         if self.buy_rocket_rect.collidepoint(local_pos):
                             self.buy_item("rocket")
                         elif self.buy_smoke_rect.collidepoint(local_pos):
                             self.buy_item("smoke")
                         elif not self.shop_window_rect.collidepoint(mouse_pos):
                             self.game_state = "playing"


             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and self.rockets > 0:
                     self.use_rocket()

    def buy_item(self, item_type):
        if item_type == "rocket":
            if self.coins_collected >= COINS_FOR_ROCKET:
                self.coins_collected -= COINS_FOR_ROCKET
                self.rockets += 1

        elif item_type == "smoke":
            if self.coins_collected >= COINS_FOR_SMOKE:
                self.coins_collected -= COINS_FOR_SMOKE
                self.smoke_grenades += 1


    def update(self):
        if self.game_state == "playing":
            self.all_sprites.update()

            if self.player:
                self.check_coin_hits()
                self.check_exit_hits()
                self.check_monster_hits()


    def check_coin_hits(self):
        if not self.player:
            return
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coin_hits:
            self.coins_collected += 1

    def check_exit_hits(self):
        if not self.player:
            return
        exit_hits = pygame.sprite.spritecollide(self.player, self.exit_group, False)
        if exit_hits:
            self.running = False

    def check_monster_hits(self):
        if not self.player:
            return
        is_player_in_smoke = False
        for smoke in self.smokes:
            if smoke.hit_rect.colliderect(self.player.hit_rect):
                is_player_in_smoke = True
                break
        if is_player_in_smoke:
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
        rocket_text = f" {self.rockets}"
        self.draw_text(rocket_text, 1325, 10, WHITE)
        smoke_text = f"{self.smoke_grenades}"
        self.draw_text(smoke_text, 1425, 10, WHITE)

        #if self.player:
            #self.draw_text(f"HP :{self.player.health}", 10, 70, WHITE)
        self.screen.blit(ICON_SHOP, self.shop_button_rect)
        if self.game_state == "shop":
            self.draw_shop_window()
        self.screen.blit(pygame.image.load("image/rocket.png"), (1300, 8))
        self.screen.blit(pygame.image.load("image/money.png"), (1200, 8))
        self.screen.blit(pygame.image.load("image/smoke_grenade.png"), (1400, 8))
        #self.screen.blit(pygame.image.load("image/s1.png"), (1100, 8))
        pygame.display.flip()

    def draw_shop_window(self):
        wind_back = pygame.Surface((self.shop_window_rect.width, self.shop_window_rect.height), pygame.SRCALPHA)
        wind_back.fill(COLOR_SHOP_BG)
        self.screen.blit(wind_back, self.shop_window_rect.topleft)

        title_surf = self.font_shop_title.render("Магазин", True, WHITE)
        title_rect = title_surf.get_rect(center = (self.shop_window_rect.centerx, self.shop_window_rect.y + 30))
        self.screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        local_pos = (mouse_pos[0] - self.shop_window_rect.x, mouse_pos[1] - self.shop_window_rect.y)

        color_rocket = COLOR_BUTTON_HOVER if self.buy_rocket_rect.collidepoint(local_pos) else COLOR_BUTTON
        rocket_full_rect = self.buy_rocket_rect.move(self.shop_window_rect.topleft)
        pygame.draw.rect(self.screen, color_rocket, rocket_full_rect)
        self.screen.blit(ICON_ROCKET, (rocket_full_rect.x + 6, rocket_full_rect.centery - ICON_SIZE[1] // 2))
        self.draw_text(f"Ракета - {COINS_FOR_ROCKET} монет", rocket_full_rect.x + 70, rocket_full_rect.centery - 10, WHITE)

        color_smoke = COLOR_BUTTON_HOVER if self.buy_smoke_rect.collidepoint(local_pos) else COLOR_BUTTON
        smoke_full_rect = self.buy_smoke_rect.move(self.shop_window_rect.topleft)
        pygame.draw.rect(self.screen, color_smoke, smoke_full_rect)
        self.screen.blit(ICON_SMOKE, (smoke_full_rect.x + 6, smoke_full_rect.centery - ICON_SIZE[1] // 2))
        self.draw_text(f"Димова гранат - {COINS_FOR_SMOKE} монет", smoke_full_rect.x + 70, smoke_full_rect.centery - 10, WHITE)

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