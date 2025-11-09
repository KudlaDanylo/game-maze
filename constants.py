import pygame
"""Вигляд фону гри"""
SCREEN_COLOR = (0, 0, 0)
INNER_WALL_GREY = (100, 100, 100)
PLAYER_COLOR = (255, 153, 102)
PLAYER_SPEED = 5



"""рівні спавну"""
WALL_LAYER = 1
PLAYER_LAYER = 2

"""Розміри"""
SCREEN_WIDTH = 1497
SCREEN_HEIGHT = 810

TILE_SIZE = 24
WALL_THICKNESS = 8


"""Відступ від країв екрану"""
MAP_OFFSET_X = 10
MAP_OFFSET_Y = 50

MAZE_WIDTH = (SCREEN_WIDTH - MAP_OFFSET_X) // TILE_SIZE
MAZE_HEIGHT = (SCREEN_HEIGHT - MAP_OFFSET_Y) // TILE_SIZE

"""Завантаження image"""
WALL_TEXTURE = pygame.transform.scale(pygame.image.load("image/Texture.jpg"),(TILE_SIZE, TILE_SIZE))