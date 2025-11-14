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
PLAYER_SPEED = 3
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
FOG_ALPHA_GRADIENT = 250




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

"""Димова завіса"""
SMOKE_DURATION = 6.0

"""інтерфейс магазину"""
HUD_FONT_SIZE = 30
SHOP_TITLE_FONT_SIZE = 40
SHOP_ITEM_FONT_SIZE = 28

"""icon image"""
ICON_SHOP = pygame.image.load("image/icon_shop.png")
ICON_ROCKET = pygame.image.load("image/rocket.png")
ICON_SMOKE = pygame.image.load("image/smoke_grenade.png")

"""Завантаження image"""
WALL_TEXTURE = pygame.transform.scale(pygame.image.load("image/Texture.jpg"),(TILE_SIZE, TILE_SIZE))
COIN_TEXTURE = pygame.image.load("image/coin.png")
HUNTER_TEXTURE = pygame.image.load("image/soldier2.png")
EXIT_TEXTURE_RIGHT = pygame.image.load("image/door_right.png")
EXIT_TEXTURE_LEFT = pygame.image.load("image/door_left.png")
HEART_TEXTURE = pygame.image.load("image/HP.png")
HEART_LOST_TEXTURE = pygame.image.load("image/lostHP.png")

"""Завантаження image smoke"""
SMOKE_FRAMES = [
    pygame.image.load("smoke/smoke1.png"),
    pygame.image.load("smoke/smoke2.png"),
    pygame.image.load("smoke/smoke3.png"),
]

"""Завантаження image pacman"""
PACMAN_RIGHT = [
    pygame.image.load("pacman/pacman_right/pacman_right1.png"),
    pygame.image.load("pacman/pacman_right/pacman_right2.png"),
    pygame.image.load("pacman/pacman_right/pacman_right3.png"),
]
PACMAN_LEFT = [
    pygame.image.load("pacman/pacman_left/pacman_left1.png"),
    pygame.image.load("pacman/pacman_left/pacman_left2.png"),
    pygame.image.load("pacman/pacman_left/pacman_left3.png"),
]
PACMAN_UP = [
    pygame.image.load("pacman/pacman_up/pacman_up1.png"),
    pygame.image.load("pacman/pacman_up/pacman_up2.png"),
    pygame.image.load("pacman/pacman_up/pacman_up3.png"),
]
PACMAN_DOWN = [
    pygame.image.load("pacman/pacman_down/pacman_down1.png"),
    pygame.image.load("pacman/pacman_down/pacman_down2.png"),
    pygame.image.load("pacman/pacman_down/pacman_down3.png"),
]
PACMAN_IDLE = [pygame.image.load("pacman/pacman_idle.png")]

PACMAN_ANIMATION = {
    "right": PACMAN_RIGHT,
    "left": PACMAN_LEFT,
    "up": PACMAN_UP,
    "down": PACMAN_DOWN,
    "idle": PACMAN_IDLE
}