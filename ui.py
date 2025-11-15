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

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        local_pos = (mouse_pos[0] - self.window_rect.x, mouse_pos[1] - self.window_rect.y)
        self.is_hovering_rocket = self.buy_rocket_rect.collidepoint(local_pos)
        self.is_hovering_smoke = self.buy_smoke_rect.collidepoint(local_pos)
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
        self.draw_shop_button(pos=mine_pos, is_hovering=False, is_clicking=False, is_disabled=True, icon=ICON_MINE, text="Недоступно")

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

