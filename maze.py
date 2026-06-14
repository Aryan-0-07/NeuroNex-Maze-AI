import pygame
import config

MAZE_LAYOUT = [
    "###############",
    "#P..#.....#...#",
    "#.#.#.###.#.#.#",
    "#.#...#.#...#.#",
    "#.#####.#####.#",
    "#.............#",
    "#.###.#.#.###.#",
    "#...#.#.#.#...#",
    "###.#.###.#.###",
    "#...#.....#...#",
    "#.#########.#.#",
    "#...........#E#",
    "###############",
]

class Maze:
    def __init__(self):
        self.layout = MAZE_LAYOUT
        self.rows   = len(self.layout)
        self.cols   = len(self.layout[0])

    def is_wall(self, col, row):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return True
        return self.layout[row][col] == '#'

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                x = config.MAZE_OFFSET_X + col * config.CELL_SIZE
                y = config.MAZE_OFFSET_Y + row * config.CELL_SIZE
                cell = self.layout[row][col]
                if cell == '#':
                    pygame.draw.rect(screen, config.MID_BG,
                                     (x, y, config.CELL_SIZE, config.CELL_SIZE))
                    pygame.draw.rect(screen, config.PURPLE,
                                     (x, y, config.CELL_SIZE, config.CELL_SIZE), 1)
                else:
                    pygame.draw.rect(screen, config.GRAY,
                                     (x, y, config.CELL_SIZE, config.CELL_SIZE))

    def get_start_pos(self, char):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.layout[row][col] == char:
                    return (
                        config.MAZE_OFFSET_X + col * config.CELL_SIZE + config.CELL_SIZE // 2,
                        config.MAZE_OFFSET_Y + row * config.CELL_SIZE + config.CELL_SIZE // 2
                    )
        return (80, 60)