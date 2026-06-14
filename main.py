import pygame
import config
from maze        import Maze
from player      import Player
from npc         import NPC
from hud         import draw_hud, HUD_X

def show_end_screen(screen, font, big_font, moves, result):
    screen.fill(config.DARK_BG)

    cx = HUD_X // 2

    if result == "win":
        title = big_font.render("ESCAPED!", True, config.TEAL)
        sub   = font.render("You outsmarted the neuromorphic NPC!", True, config.WHITE)
    else:
        title = big_font.render("CAUGHT!", True, config.CORAL)
        sub   = font.render("The NPC learned and predicted your moves.", True, config.WHITE)

    screen.blit(title, (cx - title.get_width() // 2, 100))
    screen.blit(sub,   (cx - sub.get_width()   // 2, 175))

    pygame.draw.line(screen, config.PURPLE, (cx - 200, 215), (cx + 200, 215), 1)

    stats = [
        (f"Moves survived : {moves}",   config.AMBER),
        (f"Score          : {moves * 5}", config.TEAL),
    ]
    for i, (text, color) in enumerate(stats):
        label = font.render(text, True, color)
        screen.blit(label, (cx - label.get_width() // 2, 230 + i * 28))

    pygame.draw.line(screen, config.PURPLE, (cx - 200, 300), (cx + 200, 300), 1)

    screen.blit(font.render("NPC Brain Summary:",              True, config.PURPLE), (cx - 140, 315))
    screen.blit(font.render("Stage 1 — Random movement",       True, config.GRAY),  (cx - 140, 340))
    screen.blit(font.render("Stage 2 — BFS pathfinding chase", True, config.AMBER), (cx - 140, 363))
    screen.blit(font.render("Stage 3 — Neuromorphic prediction",True, config.CORAL),(cx - 140, 386))

    pygame.draw.line(screen, config.PURPLE, (cx - 200, 420), (cx + 200, 420), 1)

    hint = font.render("Press R to restart   ESC to quit", True, config.GRAY)
    screen.blit(hint, (cx - hint.get_width() // 2, 440))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    return True

def run_game():
    pygame.init()
    screen     = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont("consolas", 16)
    small_font = pygame.font.SysFont("consolas", 13)
    big_font   = pygame.font.SysFont("consolas", 52, bold=True)

    maze         = Maze()
    player       = Player(maze)
    npc          = NPC(maze)
    move_cooldown = 1

    # Find exit position
    exit_col, exit_row = 13, 11
    for r in range(maze.rows):
        for c in range(maze.cols):
            if maze.layout[r][c] == 'E':
                exit_col, exit_row = c, r

    # Draw exit marker
    def draw_exit(screen):
        ex = config.MAZE_OFFSET_X + exit_col * config.CELL_SIZE
        ey = config.MAZE_OFFSET_Y + exit_row * config.CELL_SIZE
        pygame.draw.rect(screen, config.TEAL,
                         (ex + 4, ey + 4, config.CELL_SIZE - 8, config.CELL_SIZE - 8), 2)
        efont = pygame.font.SysFont("consolas", 14, bold=True)
        elabel = efont.render("EXIT", True, config.TEAL)
        screen.blit(elabel, (ex + 2, ey + 12))

    print("NeuroNex Maze — WASD/Arrows to move. Reach EXIT before NPC catches you!")

    running = True
    while running:
        clock.tick(config.FPS)
        move_cooldown = max(0, move_cooldown - 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if move_cooldown == 0:
            keys  = pygame.key.get_pressed()
            moved = player.handle_input(keys)
            if moved:
                move_cooldown = 4
                last = player.logger.get_recent(1)
                if last:
                    npc.brain.record_move(last[0]["direction"])

        player.update()
        npc.update(player.col, player.row, player.logger)

        # Draw
        screen.fill(config.DARK_BG)
        maze.draw(screen)
        draw_exit(screen)
        player.draw(screen)
        npc.draw(screen)

        # Stage message
        if npc.stage == 2:
            msg = font.render("NPC LEARNING YOUR PATTERNS...", True, config.AMBER)
            screen.blit(msg, (HUD_X // 2 - msg.get_width() // 2, 5))
        elif npc.stage == 3:
            msg = font.render("NPC NOW PREDICTING YOUR MOVES!", True, config.CORAL)
            screen.blit(msg, (HUD_X // 2 - msg.get_width() // 2, 5))

        draw_hud(screen, font, small_font, player, npc)
        pygame.display.flip()

        # Check win — player reached exit
        if player.col == exit_col and player.row == exit_row:
            restart = show_end_screen(screen, font, big_font,
                                      player.logger.total(), "win")
            if restart:
                run_game()
            return

        # Check caught
        if npc.caught_player(player.col, player.row):
            restart = show_end_screen(screen, font, big_font,
                                      player.logger.total(), "caught")
            if restart:
                run_game()
            return

    pygame.quit()

if __name__ == "__main__":
    run_game()