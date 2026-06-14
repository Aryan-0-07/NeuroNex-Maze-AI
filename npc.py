import pygame
import math
import random
from collections import deque
import config
from npc_brain import NPCBrain

DIRS = ["UP", "DOWN", "LEFT", "RIGHT"]
DIR_VECTORS = {
    "UP":    (0, -1),
    "DOWN":  (0,  1),
    "LEFT":  (-1, 0),
    "RIGHT": (1,  0),
}

class NPC:
    def __init__(self, maze):
        self.maze        = maze
        self.brain       = NPCBrain()
        self.col         = 7
        self.row         = 6
        self.x           = float(config.MAZE_OFFSET_X + self.col * config.CELL_SIZE + config.CELL_SIZE // 2)
        self.y           = float(config.MAZE_OFFSET_Y + self.row * config.CELL_SIZE + config.CELL_SIZE // 2)
        self.move_timer  = 0
        self.move_interval = 6

    @property
    def stage(self):
        return self.brain.get_stage()

    def _bfs(self, target_col, target_row):
        start  = (self.col, self.row)
        target = (target_col, target_row)
        if start == target:
            return None

        queue   = deque()
        queue.append((start, []))
        visited = {start}

        while queue:
            (col, row), path = queue.popleft()
            for dc, dr in DIR_VECTORS.values():
                nc, nr = col + dc, row + dr
                if (nc, nr) in visited:
                    continue
                if self.maze.is_wall(nc, nr):
                    continue
                new_path = path + [(nc, nr)]
                if (nc, nr) == target:
                    return new_path[0] if new_path else None
                visited.add((nc, nr))
                queue.append(((nc, nr), new_path))
        return None

    def update(self, player_col, player_row, player_logger):
        self.move_timer += 1
        if self.move_timer < self.move_interval:
            self._smooth_move()
            return
        self.move_timer = 0

        if self.brain.stage == 1:
            self._random_move()
        elif self.brain.stage == 2:
            self._bfs_chase(player_col, player_row)
        elif self.brain.stage == 3:
            self._predictive_move(player_col, player_row)

        self._smooth_move()

    def _random_move(self):
        options = []
        for dc, dr in DIR_VECTORS.values():
            if not self.maze.is_wall(self.col + dc, self.row + dr):
                options.append((dc, dr))
        if options:
            dc, dr = random.choice(options)
            self.col += dc
            self.row += dr

    def _bfs_chase(self, target_col, target_row):
        next_step = self._bfs(target_col, target_row)
        if next_step:
            self.col, self.row = next_step

    def _predictive_move(self, player_col, player_row):
        predicted = self.brain.predict_player_move()
        if predicted and predicted in DIR_VECTORS:
            dc, dr = DIR_VECTORS[predicted]
            target_col = player_col + dc * 2
            target_row = player_row + dr * 2
            target_col = max(0, min(self.maze.cols - 1, target_col))
            target_row = max(0, min(self.maze.rows - 1, target_row))
            if self.maze.is_wall(target_col, target_row):
                self._bfs_chase(player_col, player_row)
            else:
                next_step = self._bfs(target_col, target_row)
                if next_step:
                    self.col, self.row = next_step
                else:
                    self._bfs_chase(player_col, player_row)
        else:
            self._bfs_chase(player_col, player_row)

    def _smooth_move(self):
        target_x = config.MAZE_OFFSET_X + self.col * config.CELL_SIZE + config.CELL_SIZE // 2
        target_y = config.MAZE_OFFSET_Y + self.row * config.CELL_SIZE + config.CELL_SIZE // 2
        self.x += (target_x - self.x) * 0.5
        self.y += (target_y - self.y) * 0.5

    def caught_player(self, player_col, player_row):
        return self.col == player_col and self.row == player_row

    def draw(self, screen):
        stage_colors = {1: config.CORAL, 2: config.AMBER, 3: (220, 50, 50)}
        color = stage_colors.get(self.stage, config.CORAL)
        pygame.draw.circle(screen, color,
                           (int(self.x), int(self.y)),
                           config.NPC_SIZE // 2)
        pygame.draw.circle(screen, (255, 255, 255),
                           (int(self.x), int(self.y)),
                           config.NPC_SIZE // 2, 2)

        font = pygame.font.SysFont("consolas", 11)
        label = font.render(f"S{self.stage}", True, color)
        screen.blit(label, (int(self.x) - 8, int(self.y) - config.NPC_SIZE // 2 - 14))