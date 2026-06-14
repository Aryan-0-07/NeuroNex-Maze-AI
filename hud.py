import pygame
import config

HUD_X = config.MAZE_OFFSET_X + config.MAZE_COLS * config.CELL_SIZE + 10

def draw_hud(screen, font, small_font, player, npc):
    pygame.draw.rect(screen, config.MID_BG,
                     (HUD_X, 0, config.SCREEN_WIDTH - HUD_X, config.SCREEN_HEIGHT))
    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X, 0), (HUD_X, config.SCREEN_HEIGHT), 2)

    stage_colors = {1: config.GRAY, 2: config.AMBER, 3: config.CORAL}
    stage_names  = {1: "1 - Random", 2: "2 - Chasing", 3: "3 - Predictive"}

    screen.blit(font.render("NEURONEX", True, config.TEAL),        (HUD_X + 10, 20))
    screen.blit(font.render("NPC Maze AI", True, config.WHITE),    (HUD_X + 10, 42))

    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X + 8, 65), (config.SCREEN_WIDTH - 8, 65), 1)

    screen.blit(font.render(f"Moves: {player.logger.total()}", True, config.AMBER),  (HUD_X + 10, 75))
    screen.blit(font.render(f"Survived: {player.logger.total()}s", True, config.TEAL), (HUD_X + 10, 98))

    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X + 8, 125), (config.SCREEN_WIDTH - 8, 125), 1)

    screen.blit(font.render("-- NPC BRAIN --", True, config.PURPLE), (HUD_X + 10, 135))
    col = stage_colors.get(npc.stage, config.WHITE)
    screen.blit(font.render(f"Stage: {npc.stage}", True, col),                         (HUD_X + 10, 158))
    screen.blit(font.render(f"Spikes: {npc.brain.get_spike_rate()}", True, config.TEAL),   (HUD_X + 10, 181))
    screen.blit(font.render(f"Conf:  {npc.brain.get_confidence()}%", True, config.AMBER),  (HUD_X + 10, 204))

    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X + 8, 228), (config.SCREEN_WIDTH - 8, 228), 1)

    screen.blit(small_font.render("Stages:", True, config.WHITE), (HUD_X + 10, 238))
    for s in [1, 2, 3]:
        c = stage_colors[s] if s == npc.stage else config.GRAY
        screen.blit(small_font.render(stage_names[s], True, c),
                    (HUD_X + 10, 255 + (s - 1) * 20))

    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X + 8, 320), (config.SCREEN_WIDTH - 8, 320), 1)

    # Neuron activity bars
    screen.blit(small_font.render("Neuron activity:", True, config.WHITE), (HUD_X + 10, 330))
    dirs     = ["UP", "DN", "LT", "RT"]
    membrane = npc.brain.get_membrane()
    weights  = npc.brain.get_weights()
    for i, d in enumerate(dirs):
        by  = 350 + i * 36
        val = min(1.0, float(membrane[i]) / config.LIF_THRESHOLD)
        w   = min(1.0, float(weights[i]))
        bar_w = config.SCREEN_WIDTH - HUD_X - 40
        pygame.draw.rect(screen, config.GRAY,   (HUD_X + 10, by, bar_w, 14))
        pygame.draw.rect(screen, config.PURPLE, (HUD_X + 10, by, int(bar_w * val), 14))
        screen.blit(small_font.render(f"{d} w:{w:.2f}", True, config.WHITE),
                    (HUD_X + 10, by + 16))

    pygame.draw.line(screen, config.PURPLE,
                     (HUD_X + 8, 500), (config.SCREEN_WIDTH - 8, 500), 1)

    screen.blit(small_font.render("Controls:", True, config.WHITE),       (HUD_X + 10, 510))
    screen.blit(small_font.render("WASD/Arrows", True, config.GRAY),     (HUD_X + 10, 528))
    screen.blit(small_font.render("ESC - Quit", True, config.GRAY),      (HUD_X + 10, 546))