import pygame
"""Вигляд фону гри"""
SCREEN_COLOR = (0, 0, 0)
INNER_WALL_GREY = (100, 100, 100)
PLAYER_COLOR = (255, 153, 102)
EXIT_COLOR = (186, 173, 169)
PATROL_COLOR = (255, 47, 47)
HUNTER_COLOR = (200, 0, 100)
WHITE = (255, 255, 255)

COLOR_SHOP_BG = (10, 20, 30, 220)
COLOR_BUTTON = (80, 80, 80)
COLOR_BUTTON_HOVER = (110, 110, 110)

ANIMATION_SPEED = 0.15
PLAYER_SPEED = 2.2
MONSTER_SPEED = 2
HUNTER_SPEED = 2
HUNTER_VISION_RANGE = 500
PLAYER_LIVES = 3

PLAYER_HEALTH = 100
DAMAGE_COOLDOWN = 1
PATROL_DAMAGE = 50
HUNTER_DAMAGE = 10

"""рівні спавну"""
WALL_LAYER = 1
PLAYER_LAYER = 2

FOG_COLOR = (0, 0, 0)
FOG_ALPHA = 252
VISION_RADIUS_INNER = 50
VISION_RADIUS_OUTER = 140
FOG_ALPHA_GRADIENT = 245


CONTROL_ICON_SIZE = (32, 32)

"""Розміри"""
SCREEN_WIDTH = 1497
SCREEN_HEIGHT = 810

TILE_SIZE = 24
WALL_THICKNESS = 8
ICON_SIZE = (TILE_SIZE * 2, TILE_SIZE * 2)
SHOP_ICON_SIZE = (TILE_SIZE * 3, TILE_SIZE * 3)

"""Відступ від країв екрану"""
MAP_OFFSET_X = 10
MAP_OFFSET_Y = 50
HEART_PADDING = 8

MAZE_WIDTH = (SCREEN_WIDTH - MAP_OFFSET_X) // TILE_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - MAP_OFFSET_Y) // TILE_SIZE

"""Ціни на товари"""
COINS_FOR_ROCKET = 5
COINS_FOR_SMOKE = 5
COINS_FOR_MINE = 7
BLUE_CHEST_COST = 10

"""Димова завіса"""
SMOKE_DURATION = 6.0

"""інтерфейс магазину"""
HUD_FONT_SIZE = 30
SHOP_TITLE_FONT_SIZE = 40
SHOP_ITEM_FONT_SIZE = 28
GAME_OVER_FRONT_SIZE = 80

SHOP_BUTTON_WIDTH = 300
SHOP_BUTTON_HEIGHT = 60
CLOSE_BUTTON_WIDTH = 80
CLOSE_BUTTON_HEIGHT = 30
GAME_OVER_BUTTON_WIDTH = 250
GAME_OVER_BUTTON_HEIGHT = 50

CHEST_UI_WIDTH = 300
CHEST_UI_HEIGHT = 300
CHEST_IMAGE_SILE = (200, 170)
CHEST_BUTTON_SIZE = (120, 35)
CHEST_BUTTON_SIZE_CONTINUE = (130, 35)

MAX_LEVEL = 10
LEVEL_TEXT_SIZE = 40

"""Налаштування рівнів"""
LEVEL_CONFIGS = [
    {"vision": 3000, "patrol": 2, "hunters": 0, "hunters_vis": 100, "hunter_dmg": 10, "speed": 2, "prices": (5,5,7), "chest_y": (1, 0.7), "chest_b": (0.1, 0.03), "timer": None},
    {"vision": 3000, "patrol": 2, "hunters": 1, "hunters_vis": 100, "hunter_dmg": 10, "speed": 2, "prices": (5,5,7), "chest_y": (6, 4), "chest_b": (0.7, 0.25), "timer": None},
    {"vision": 170, "patrol": 3, "hunters": 1, "hunters_vis": 150, "hunter_dmg": 10, "speed": 2, "prices": (5,5,7), "chest_y": (10, 7), "chest_b": (2, 1), "timer": None},
    {"vision": 170, "patrol": 2, "hunters": 2, "hunters_vis": 175, "hunter_dmg": 10, "speed": 2, "prices": (5,5,7), "chest_y": (15, 10), "chest_b": (5, 2), "timer": None},
    {"vision": 150, "patrol": 2, "hunters": 3, "hunters_vis": 230, "hunter_dmg": 10, "speed": 2, "prices": (5,5,7), "chest_y": (20, 13), "chest_b": (7, 4), "timer": None},
    {"vision": 120, "patrol": 3, "hunters": 3, "hunters_vis": 300, "hunter_dmg": 10, "speed": 2, "prices": (6,6,8), "chest_y": (23, 18), "chest_b": (12, 6), "timer": None},
    {"vision": 90, "patrol": 4, "hunters": 3, "hunters_vis": 380, "hunter_dmg": 15, "speed": 2, "pries": (6,6,8), "chest_y": (30, 23), "chest_b": (18, 10), "timer": None},
    {"vision": 70, "patrol": 2, "hunters": 5, "hunters_vis": 450, "hunter_dmg": 15, "speed": 2, "prices": (6,7,10), "chest_y": (40, 30), "chest_b": (35, 18), "timer": None},
    {"vision": 50, "patrol": 4, "hunters": 7, "hunters_vis": 3000, "hunter_dmg": 15, "speed": 3, "prices": (6,7,10), "chest_y": (70, 60), "chest_b": (50, 50), "timer": 80},
]


BUTTON_SHOP_BUY_NORMAL = pygame.image.load("image/button/shop_normal.png")
BUTTON_SHOP_BUY_HOVER = pygame.image.load("image/button/shop_hover.png")
BUTTON_SHOP_EXIT_NORMAL = pygame.image.load("image/button/shop_exit_norm.png")
BUTTON_SHOP_EXIT_HOVER = pygame.image.load("image/button/shop_exit_hover.png")

BUTTON_GAME_RESTART_NORMAL = pygame.image.load("image/button/game_restart_norm.png")
BUTTON_GAME_RESTART_HOVER = pygame.image.load("image/button/game_restart_hover.png")
BUTTON_GAME_EXIT_NORMAL = pygame.image.load("image/button/game_exit_norm.png")
BUTTON_GAME_EXIT_HOVER = pygame.image.load("image/button/game_exit_hover.png")

BUTTON_CHEST_CANCEL_NORMAL = pygame.image.load("image/button/chest_norm.png")
BUTTON_CHEST_CANCEL_HOVER = pygame.image.load("image/button/chest_hover.png")
BUTTON_CHEST_ACCENT_NORMAL = pygame.image.load("image/button/chest_norm.png")
BUTTON_CHEST_ACCENT_HOVER = pygame.image.load("image/button/chest_hover.png")
BUTTON_CHEST_CONTINUE_NORMAL = pygame.image.load("image/button/chest_exit_norm.png")
BUTTON_CHEST_CONTINUE_HOVER = pygame.image.load("image/button/chest_exit_hover.png")
IMAGE_CHEST_SMALL = pygame.image.load("image/chest_small.png")
IMAGE_CHEST_GREAT = pygame.image.load("image/chest_big.png")

"""icon image"""
ICON_SHOP = pygame.image.load("image/icon/icon_shop.png")
ICON_COIN = pygame.image.load("image/icon/money.png")
ICON_ROCKET = pygame.image.load("image/icon/rocket.png")
ICON_SMOKE = pygame.image.load("image/icon/smoke_grenade.png")
ICON_MINE = pygame.image.load("image/icon/mine.png")
ICON_PLAY = pygame.image.load("image/icon/play.png")
ICON_PAUSE = pygame.image.load("image/icon/pause.png")
ICON_HEART = pygame.image.load("image/icon/HP.png")
ICON_HEART_LOST = pygame.image.load("image/icon/lostHP.png")


"""Завантаження image текстур"""
WALL_TEXTURE = pygame.transform.scale(pygame.image.load("image/texture/Texture.jpg"),(TILE_SIZE, TILE_SIZE))
COIN_TEXTURE = pygame.image.load("image/texture/coin.png")
HUNTER_TEXTURE = pygame.image.load("image/texture/soldier2.png")
EXIT_TEXTURE_RIGHT = pygame.image.load("image/texture/door_right.png")
EXIT_TEXTURE_LEFT = pygame.image.load("image/texture/door_left.png")
MINE_TEXTURE = pygame.image.load("image/texture/mine_1.png")
CHEST_SMALL_TEXTURE = pygame.image.load("image/texture/chest.png")
CHEST_GREAT_TEXTURE = pygame.image.load("image/texture/chest_diamond.png")

"""Завантаження image smoke"""
SMOKE_FRAMES = [
    pygame.image.load("image/smoke/smoke1.png"),
    pygame.image.load("image/smoke/smoke2.png"),
    pygame.image.load("image/smoke/smoke3.png"),
]

"""Завантаження image pacman"""
PACMAN_RIGHT = [
    pygame.image.load("image/pacman/pacman_right/pacman_right1.png"),
    pygame.image.load("image/pacman/pacman_right/pacman_right2.png"),
    pygame.image.load("image/pacman/pacman_right/pacman_right3.png"),
]
PACMAN_LEFT = [
    pygame.image.load("image/pacman/pacman_left/pacman_left1.png"),
    pygame.image.load("image/pacman/pacman_left/pacman_left2.png"),
    pygame.image.load("image/pacman/pacman_left/pacman_left3.png"),
]
PACMAN_UP = [
    pygame.image.load("image/pacman/pacman_up/pacman_up1.png"),
    pygame.image.load("image/pacman/pacman_up/pacman_up2.png"),
    pygame.image.load("image/pacman/pacman_up/pacman_up3.png"),
]
PACMAN_DOWN = [
    pygame.image.load("image/pacman/pacman_down/pacman_down1.png"),
    pygame.image.load("image/pacman/pacman_down/pacman_down2.png"),
    pygame.image.load("image/pacman/pacman_down/pacman_down3.png"),
]
PACMAN_IDLE = [pygame.image.load("image/pacman/pacman_idle.png")]

PACMAN_ANIMATION = {
    "right": PACMAN_RIGHT,
    "left": PACMAN_LEFT,
    "up": PACMAN_UP,
    "down": PACMAN_DOWN,
    "idle": PACMAN_IDLE
}