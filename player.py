import pygame
import config
from event_logger import EventLogger

DIR_MAP = {
    pygame.K_UP:    (0, -1, "UP"),
    pygame.K_DOWN:  (0,  1, "DOWN"),
    pygame.K_LEFT:  (-1, 0, "LEFT"),
    pygame.K_RIGHT: (1,  0, "RIGHT"),
    pygame.K_w:     (0, -1, "UP"),
    pygame.K_s:     (0,  1, "DOWN"),
    pygame.K_a:     (-1, 0, "LEFT"),
    pygame.K_d:     (1,  0, "RIGHT"),
}

class Player:
    def __init__(self, maze):
        self.maze   = maze
        self.logger = EventLogger()
        px, py      = maze.get_start_pos('P')
        self.x      = float(px)
        self.y      = float(py)
        self.col    = 1
        self.row    = 1

    def handle_input(self, keys):
        for key, (dc, dr, label) in DIR_MAP.items():
            if keys[key]:
                new_col = self.col + dc
                new_row = self.row + dr
                if not self.maze.is_wall(new_col, new_row):
                    self.col = new_col
                    self.row = new_row
                    self.logger.log(self.col, self.row, label)
                    return True
        return False

    def update(self):
        target_x = config.MAZE_OFFSET_X + self.col * config.CELL_SIZE + config.CELL_SIZE // 2
        target_y = config.MAZE_OFFSET_Y + self.row * config.CELL_SIZE + config.CELL_SIZE // 2
        self.x += (target_x - self.x) * 0.2
        self.y += (target_y - self.y) * 0.2

    def draw(self, screen):
        pygame.draw.circle(screen, config.PLAYER_COLOR,
                           (int(self.x), int(self.y)),
                           config.PLAYER_SIZE // 2)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.x), int(self.y)),
                           config.PLAYER_SIZE // 2, 2)