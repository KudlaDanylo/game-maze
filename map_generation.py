import random
def maze_generation(width, height):

    maze = [[1 for _ in range(width)] for _ in range(height)]

    start_x = random.randrange(1, width - 1, 2)
    start_y = random.randrange(1, height - 1, 2)

    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]

    while stack:
        current_x, current_y = stack[-1]

        boxs = []
        for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nx , ny = current_x + dx, current_y + dy

            if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                    if maze[ny][nx] == 1:
                        boxs.append((nx, ny))

        if boxs:
            next_x, next_y = random.choice(boxs)
            wall_x = current_x + (next_x - current_x) // 2
            wall_y = current_y + (next_y - current_y) // 2
            maze[wall_y][wall_x] = 0
            maze[next_y][next_x] = 0
            stack.append((next_x, next_y))
        else:
            stack.pop()


    return maze