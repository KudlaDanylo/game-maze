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
from mine import Mine
from heart import Heart
from smoke import Smoke
from ui import Shop, GameOver, ChestUI
from chest import Chest

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("game")
        self.dt = 0

        self.font = pygame.font.Font(None, HUD_FONT_SIZE)


        self.game_state = "playing"
        self.is_paused = False
        self.fog_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.coins_collected = 30
        self.rockets = 10
        self.smoke_grenades = 0
        self.mines = 0

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.inner_walls = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.smokes = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.LayeredUpdates()
        self.mines_group = pygame.sprite.Group()
        self.chests_group = pygame.sprite.Group()

        self.heart_sprites = []
        self.maze_data = []
        self.player = None
        self.player_start_pos = None
        self.level = 1
        self.lives = PLAYER_LIVES
        self.shop = Shop(self)
        self.game_over = GameOver(self)
        self.chest_ui = ChestUI(self)

        shop_btn_rect_size_tuple = (SHOP_ICON_SIZE[0], SHOP_ICON_SIZE[1])
        self.shop_button_rect = pygame.Rect(SCREEN_WIDTH - 400 - shop_btn_rect_size_tuple[0] - 10, 8, shop_btn_rect_size_tuple[0], shop_btn_rect_size_tuple[1])
        self.pause_button_rect = pygame.Rect(self.shop_button_rect.left - CONTROL_ICON_SIZE[0] - 10, 10, CONTROL_ICON_SIZE[0], CONTROL_ICON_SIZE[1])


    def start_new_game(self):
        self.lives = PLAYER_LIVES
        self.level = 1
        self.coins_collected = 0
        self.rockets = 0
        self.smoke_grenades = 0
        self.mines = 0
        self.game_state = "playing"
        self.is_paused = False
        self.new_level()

    def find_dead_emds(self):
        dead_ends = []
        if not self.maze_data:
            return []
        for y in range(1, MAZE_HEIGHT - 1):
            for x in range(1, MAZE_WIDTH - 1):
                if self.maze_data[y][x] == 0:
                    wall_count = 0
                    if self.maze_data[y-1][x] == 1:
                        wall_count += 1
                    if self.maze_data[y+1][x] == 1:
                        wall_count += 1
                    if self.maze_data[y][x-1] == 1:
                        wall_count += 1
                    if self.maze_data[y][x+1] == 1:
                        wall_count += 1
                    if wall_count == 3:
                        dead_ends.append((x, y))
        return dead_ends

    def new_level(self):

        for sprite in self.all_sprites:
            sprite.kill()
        self.heart_sprites = []
        self.maze_data = maze_generation(MAZE_WIDTH, MAZE_HEIGHT)
    #Життя
        for i, heart in enumerate(self.heart_sprites):
            if i < self.lives:
                heart.set_full()
            else:
                heart.set_empty()

        if not self.heart_sprites and self.lives > 0:
            for i in range(self.lives):
                x_pos = 0 + ((36 + HEART_PADDING) * (self.lives - i))
                y_pos = HEART_PADDING
                heart = Heart(self, x_pos, y_pos)
                self.heart_sprites.append(heart)
            self.heart_sprites.sort(key=lambda sprite: sprite.rect.x)
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

        dead_ends = self.find_dead_emds()
        spawnable_dead_ends = [pos for pos in dead_ends if pos in empty_tiles]

        yellow_chance = YELLOW_CHEST_SPAWN_CHANCE * self.level
        blue_chance = BLUE_CHEST_SPAWN_CHANCE * self.level

        for pos in spawnable_dead_ends:
            empty_tiles.remove(pos)
            if random.random() < blue_chance:
                Chest(self, pos[0], pos[1], "blue")
            elif random.random() < yellow_chance:
                Chest(self, pos[0], pos[1], "yellow")


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

             if self.game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.pause_button_rect.collidepoint(mouse_pos):
                        self.is_paused = not self.is_paused
                        self.game_state = 'playing'
                        continue

                    if self.shop_button_rect.collidepoint(mouse_pos):
                        self.game_state = "shop"
                        self.is_paused = False
                        continue

                    if not self.is_paused and self.player:
                        clicked_chests = [s for s in self.chests_group if s.rect.collidepoint(mouse_pos)]
                        if clicked_chests:
                            chest = clicked_chests[0]
                            dist = self.player.pos.distance_to(chest.rect.center)
                            if dist <= VISION_RADIUS_INNER:
                                self.chest_ui.open(chest)
                                continue

                        if self.smoke_grenades > 0:
                            if self.player.pos.distance_to(mouse_pos) <= VISION_RADIUS_OUTER:
                                Smoke(self, mouse_pos)
                                self.smoke_grenades -= 1

                if event.type == pygame.KEYDOWN:
                    if self.game_state == "playing" and not self.is_paused:
                        if event.key == pygame.K_SPACE and self.rockets > 0:
                            self.use_rocket()
                        if event.key == pygame.K_q and self.mines > 0:
                            self.place_mine()
             elif self.game_state == "shop":
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                     self.shop.handle_event(event)

             elif self.game_state == 'chest_open':
                 self.chest_ui.handle_event(event)


             elif self.game_state == "game_over":
                 self.game_over.handle_event(event)


    def buy_item(self, item_type):
        if item_type == "rocket":
            if self.coins_collected >= COINS_FOR_ROCKET:
                self.coins_collected -= COINS_FOR_ROCKET
                self.rockets += 1

        elif item_type == "smoke":
            if self.coins_collected >= COINS_FOR_SMOKE:
                self.coins_collected -= COINS_FOR_SMOKE
                self.smoke_grenades += 1

        elif item_type == "mine":
            if self.coins_collected >= COINS_FOR_MINE:
                self.coins_collected -= COINS_FOR_MINE
                self.mines += 1


    def update(self):
        if self.game_state == "shop":
            self.shop.update()
        elif self.game_state == "game_over":
            self.game_over.update()
        elif self.game_state == "chest_open":
            self.chest_ui.update()

        elif self.game_state == "playing" and not self.is_paused:
            self.all_sprites.update()

            if  self.player:
                self.check_coin_hits()
                self.check_exit_hits()
                self.check_monster_hits()

    def place_mine(self):
        if self.mines <= 0 or not self.player:
            return
        mouse_pos = pygame.mouse.get_pos()
        distance = self.player.pos.distance_to(mouse_pos)

        if distance <= VISION_RADIUS_INNER:
            self.mines -= 1
            Mine(self, mouse_pos)

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
                    break

    def player_is_dead(self):
        self.lives -= 1
        if self.lives < len(self.heart_sprites) and self.lives >= 0:
            self.heart_sprites[self.lives].set_empty()

        if self.lives > 0:
            self.player = Player(self, self.player_start_pos[0], self.player_start_pos[1])
        else:
            self.game_state = 'game_over'
            self.player = None

    def roll_loot(self, chest_type):
        if chest_type == "yellow":
            population = list(range(1, 8))
            weight = [40, 25, 15, 10, 5, 3, 2]
            return random.choices(population, weight, k=1)[0]
        elif chest_type == "blue":
            return random.randint(5,20)
        return 0

    def accept_chest(self, chest_sprite):
        if chest_sprite.type == "blue":
            if self.coins_collected >= BLUE_CHEST_COST:
                self.coins_collected -= BLUE_CHEST_COST
            else:
                self.chest_ui.close()
                return

        loot_amount = self.roll_loot(chest_sprite.type)
        self.chest_ui.show_loot(loot_amount)

    def collect_loot(self, chest_sprite):
        loot_amount = self.chest_ui.loot_amount
        self.coins_collected += loot_amount
        chest_sprite.kill()

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
        self.draw_text(smoke_text, 1400, 10, WHITE)
        self.draw_text(f" {self.mines}", 10, 100, WHITE)

        #if self.player:
            #self.draw_text(f"HP :{self.player.health}", 10, 70, WHITE)
        self.screen.blit(ICON_SHOP, self.shop_button_rect)
        if self.is_paused:
            self.screen.blit(ICON_PLAY, self.pause_button_rect)
        else:
            self.screen.blit(ICON_PAUSE, self.pause_button_rect)

        if self.game_state == "shop":
            self.shop.draw()
        elif self.game_state == 'game_over':
            self.game_over.draw()
        elif self.game_state == "chest_open":
            self.chest_ui.draw()
        elif self.is_paused:
            s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            self.screen.blit(s,(0, 0))
        self.screen.blit(pygame.image.load("image/icon/rocket.png"), (1300, 8))
        self.screen.blit(pygame.image.load("image/texture/mine_1.png"), (1200, 8))
        self.screen.blit(pygame.image.load("image/icon/smoke_grenade.png"), (1400, 8))
        #self.screen.blit(pygame.image.load("image/r1.png"), (660, 300))
        #self.screen.blit(pygame.image.load("image/t1.png"), (760, 500))
        #self.screen.blit(pygame.image.load("image/t1.png"), (630, 500))
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