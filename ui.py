import pygame.mouse

from constants import *

class Shop:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.is_hovering_rocket = False
        self.is_hovering_smoke = False
        self.is_clicking_rocket = False
        self.is_clicking_smoke = False
        self.font_title = pygame.font.Font(None, SHOP_TITLE_FONT_SIZE)
        self.font_item = pygame.font.Font(None, SHOP_ITEM_FONT_SIZE)
        self.font_close = pygame.font.Font(None, 18)

        shop_w = 400
        shop_h = 400
        self.window_rect = pygame.Rect((SCREEN_WIDTH - shop_w) // 2, (SCREEN_HEIGHT - shop_h) // 2, shop_w, shop_h)
        btn_x = (shop_w - SHOP_BUTTON_WIDTH) // 2
        self.buy_rocket_rect = pygame.Rect(btn_x, 70, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        self.buy_smoke_rect = pygame.Rect(btn_x, self.buy_rocket_rect.bottom + 15, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        self.buy_mine_rect = pygame.Rect(btn_x, self.buy_smoke_rect.bottom + 15, SHOP_BUTTON_WIDTH, SHOP_BUTTON_HEIGHT)
        self.close_button_rect = pygame.Rect((shop_w - CLOSE_BUTTON_WIDTH) // 2, shop_h - CLOSE_BUTTON_HEIGHT - 20, CLOSE_BUTTON_WIDTH, CLOSE_BUTTON_HEIGHT)
        self.bg_surface = pygame.Surface((shop_w, shop_h), pygame.SRCALPHA)
        self.bg_surface.fill(COLOR_SHOP_BG)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        local_pos = (mouse_pos[0] - self.window_rect.x, mouse_pos[1] - self.window_rect.y)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buy_rocket_rect.collidepoint(local_pos):
                self.game.buy_item("rocket")
            elif self.buy_smoke_rect.collidepoint(local_pos):
                self.game.buy_item("smoke")
            elif self.buy_mine_rect.collidepoint(local_pos):
                self.game.buy_item("mine")
            elif self.close_button_rect.collidepoint(local_pos):
                self.game.game_state = "playing"
            elif not self.window_rect.collidepoint(mouse_pos):
                self.game.game_state = "playing"
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_clicking_rocket = False
            self.is_clicking_smoke = False
            self.is_clicking_mine = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        local_pos = (mouse_pos[0] - self.window_rect.x, mouse_pos[1] - self.window_rect.y)
        self.is_hovering_rocket = self.buy_rocket_rect.collidepoint(local_pos)
        self.is_hovering_smoke = self.buy_smoke_rect.collidepoint(local_pos)
        self.is_hovering_mine = self.buy_mine_rect.collidepoint(local_pos)
        self.is_hovering_close = self.close_button_rect.collidepoint(local_pos)

    def draw(self):
        self.screen.blit(self.bg_surface, self.window_rect.topleft)

        title_surf = self.font_title.render("Магазин", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.window_rect.centerx, self.window_rect.y + 30))
        self.screen.blit(title_surf, title_rect)

        rocked_pos = self.buy_rocket_rect.move(self.window_rect.topleft)
        self.draw_shop_button(pos=rocked_pos, is_hovering=self.is_hovering_rocket, is_clicking=self.is_clicking_rocket, is_disabled=False, icon=ICON_ROCKET, text=f"Ракета {COINS_FOR_ROCKET} монет")


        smoke_pos = self.buy_smoke_rect.move(self.window_rect.topleft)
        self.draw_shop_button(pos=smoke_pos, is_hovering=self.is_hovering_smoke, is_clicking=self.is_clicking_smoke, is_disabled=False, icon=ICON_SMOKE, text=f"Дим {COINS_FOR_SMOKE} монет")

        mine_pos = self.buy_mine_rect.move(self.window_rect.topleft)
        self.draw_shop_button(pos=mine_pos, is_hovering=self.is_hovering_mine, is_clicking=False, is_disabled=False, icon=ICON_MINE, text=f"Міна {COINS_FOR_MINE} монет")

        close_pos = self.close_button_rect.move(self.window_rect.topleft)
        if self.is_hovering_close:
            bg_img = BUTTON_SHOP_EXIT_HOVER
        else:
            bg_img = BUTTON_SHOP_EXIT_NORMAL
        self.screen.blit(bg_img, close_pos.topleft)
        text_surf = self.font_close.render("Вихід", True, WHITE)
        text_rect = text_surf.get_rect(center=close_pos.center)
        self.screen.blit(text_surf, text_rect)

    def draw_shop_button(self, pos, is_hovering, is_clicking, is_disabled, icon, text):
        if is_disabled:
            bg_img = BUTTON_SHOP_BUY_NORMAL
        if is_clicking:
            bg_img = BUTTON_SHOP_BUY_NORMAL
        elif is_hovering:
            bg_img = BUTTON_SHOP_BUY_HOVER
        else:
            bg_img = BUTTON_SHOP_BUY_NORMAL

        self.screen.blit(bg_img, pos.topleft)
        icon_rect = icon.get_rect(centery = pos.centery, left = pos.x + 20)
        self.screen.blit(icon, icon_rect)

        text_color = (110, 110, 110) if is_disabled else WHITE
        text_surf = self.font_item.render(text, True, text_color)
        text_rect = text_surf.get_rect(centery = pos.centery, left = icon_rect.right + 20)
        self.screen.blit(text_surf, text_rect)


class GameOver:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.is_hovering_restart = False
        self.is_hovering_exit = False
        self.font_title = pygame.font.Font(None, GAME_OVER_FRONT_SIZE)
        self.font_button = pygame.font.Font(None, SHOP_ITEM_FONT_SIZE)
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 100))

        center_x = SCREEN_WIDTH // 2
        self.restart_rect = pygame.Rect(center_x - (GAME_OVER_BUTTON_WIDTH // 2), 350, GAME_OVER_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT)
        self.exit_rect = pygame.Rect(center_x - (GAME_OVER_BUTTON_WIDTH // 2), self.restart_rect.bottom + 20, GAME_OVER_BUTTON_WIDTH, GAME_OVER_BUTTON_HEIGHT)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_rect.collidepoint(mouse_pos):
                self.game.start_new_game()
            elif self.exit_rect.collidepoint(mouse_pos):
                self.game.quit_game()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering_restart = self.restart_rect.collidepoint(mouse_pos)
        self.is_hovering_exit = self.exit_rect.collidepoint(mouse_pos)

    def draw(self):
        self.screen.blit(self.overlay, (0, 0))
        title_surf = self.font_title.render("ГРА ПРОГРАНА", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(title_surf, title_rect)

        if self.is_hovering_restart:
            self.screen.blit(BUTTON_GAME_RESTART_HOVER, self.restart_rect.topleft)
        else:
            self.screen.blit(BUTTON_GAME_RESTART_NORMAL, self.restart_rect.topleft)
        text_surf = self.font_button.render("Рестарт", True, WHITE)
        text_rect = text_surf.get_rect(center=self.restart_rect.center)
        self.screen.blit(text_surf, text_rect)

        if self.is_hovering_exit:
            self.screen.blit(BUTTON_GAME_EXIT_HOVER, self.exit_rect.topleft)
        else:
            self.screen.blit(BUTTON_GAME_EXIT_NORMAL, self.exit_rect.topleft)
        text_surf = self.font_button.render("Вийти з гри", True, WHITE)
        text_rect = text_surf.get_rect(center=self.exit_rect.center)
        self.screen.blit(text_surf, text_rect)


class ChestUI:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.state = "idle"
        self.current_chest = None
        self.loot_amount = 0

        self.font_title = pygame.font.Font(None, SHOP_TITLE_FONT_SIZE)
        self.font_item = pygame.font.Font(None, SHOP_ITEM_FONT_SIZE)
        self.font_congrats = pygame.font.Font(None, GAME_OVER_FRONT_SIZE)

        self.window_rect = pygame.Rect((SCREEN_WIDTH - CHEST_UI_WIDTH) // 2, (SCREEN_HEIGHT - CHEST_UI_HEIGHT) // 2, CHEST_UI_WIDTH, CHEST_UI_HEIGHT)
        self.image_pos = (self.window_rect.x + (CHEST_UI_WIDTH - CHEST_IMAGE_SILE[0]) // 2, self.window_rect.y + 60)
        btn_y = self.window_rect.y + CHEST_IMAGE_SILE[1] + 80
        btn_padding = (CHEST_UI_WIDTH - (CHEST_BUTTON_SIZE[0] * 2)) // 3

        self.button_accept_rect = pygame.Rect(self.window_rect.x + btn_padding, btn_y, CHEST_BUTTON_SIZE[0], CHEST_BUTTON_SIZE[1])
        self.button_cancel_rect = pygame.Rect(self.button_accept_rect.right + btn_padding, btn_y, CHEST_BUTTON_SIZE[0], CHEST_BUTTON_SIZE[1])
        self.button_continue_rect = pygame.Rect(self.window_rect.centerx - (CHEST_BUTTON_SIZE_CONTINUE[0] // 2), btn_y, CHEST_BUTTON_SIZE_CONTINUE[0], CHEST_BUTTON_SIZE_CONTINUE[1])

        self.is_hovering_accept = False
        self.is_hovering_cancel = False
        self.is_hovering_continue = False

    def open(self, chest_sprite):
        self.current_chest = chest_sprite
        self.state = "opening"
        self.game.game_state = "chest_open"

    def close(self):
        self.game.game_state = "playing"
        self.current_chest = None
        self.state = "idle"
        self.loot_amount = 0

    def show_loot(self, amount):
        self.loot_amount = amount
        self.state = "showing_loot"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if self.state == "opening":
                    if self.button_accept_rect.collidepoint(mouse_pos):
                        self.game.accept_chest(self.current_chest)
                    elif self.button_cancel_rect.collidepoint(mouse_pos):
                        self.close()
                    elif not self.window_rect.collidepoint(mouse_pos):
                        self.close()

                elif self.state == "showing_loot":
                    if self.button_continue_rect.collidepoint(mouse_pos):
                        self.game.collect_loot(self.current_chest)
                        self.close()
                    elif not self.window_rect.collidepoint(mouse_pos):
                        self.close()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == "opening":
            self.is_hovering_accept = self.button_accept_rect.collidepoint(mouse_pos)
            self.is_hovering_cancel = self.button_cancel_rect.collidepoint(mouse_pos)
            self.is_hovering_continue = False
        elif self.state == "showing_loot":
            self.is_hovering_accept = False
            self.is_hovering_cancel = False
            self.is_hovering_continue = self.button_continue_rect.collidepoint(mouse_pos)
        else:
            self.is_hovering_accept = False
            self.is_hovering_cancel = False
            self.is_hovering_continue = False

    def draw(self):
        s = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(self.screen, COLOR_SHOP_BG, self.window_rect, border_radius=10)
        if self.state == "opening":
            self.draw_opening_window()
        elif self.state == "showing_loot":
            self.draw_loot_window()

    def draw_opening_window(self):
        if self.current_chest.type == "yellow":
            title_surf = self.font_title.render("Жовта скриня", True, WHITE)
            self.screen.blit(IMAGE_CHEST_SMALL, self.image_pos)
            accept_text = "Забрати"
        else:
            title_surf = self.font_title.render("Синя скриня", True, WHITE)
            self.screen.blit(IMAGE_CHEST_GREAT, self.image_pos)
            accept_text = f"-{BLUE_CHEST_COST} монет"
        title_rect = title_surf.get_rect(center=(self.window_rect.centerx, self.window_rect.y + 30))
        self.screen.blit(title_surf, title_rect)

        bg_accept = BUTTON_CHEST_ACCENT_HOVER if self.is_hovering_accept else BUTTON_CHEST_ACCENT_NORMAL
        self.screen.blit(bg_accept, self.button_accept_rect.topleft)
        text_surf = self.font_item.render(accept_text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.button_accept_rect.center)
        self.screen.blit(text_surf, text_rect)

        bg_cancel = BUTTON_CHEST_CANCEL_HOVER if self.is_hovering_cancel else BUTTON_CHEST_CANCEL_NORMAL
        self.screen.blit(bg_cancel, self.button_cancel_rect.topleft)
        text_surf = self.font_item.render("Залишити", True, WHITE)
        text_rect = text_surf.get_rect(center=self.button_cancel_rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_loot_window(self):
        title_surf = self.font_congrats.render("вітаю", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.window_rect.centerx, self.window_rect.y + 100))
        self.screen.blit(title_surf, title_rect)

        loot_text = f"Ви отримали {self.loot_amount} монет"
        loot_surf = self.font_title.render(loot_text, True, WHITE)
        loot_rect = loot_surf.get_rect(center=(self.window_rect.centerx, self.window_rect.y + 160))
        self.screen.blit(loot_surf, loot_rect)

        bg_continue = BUTTON_CHEST_CONTINUE_HOVER if self.is_hovering_continue else BUTTON_CHEST_CONTINUE_NORMAL
        self.screen.blit(bg_continue, self.button_continue_rect.topleft)
        text_surf = self.font_item.render("Продовжити", True, WHITE)
        text_rect = text_surf.get_rect(center=self.button_continue_rect.center)
        self.screen.blit(text_surf, text_rect)


