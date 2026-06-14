# config.py — all constants in one place

# Window
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 650
FPS           = 60
TITLE         = "NeuroNex — Neuromorphic NPC AI"

# Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (40,  40,  40)
TEAL       = (0,   212, 170)
CORAL      = (255, 107, 107)
AMBER      = (239, 159,  39)
PURPLE     = (83,  74,  183)
DARK_BG    = (13,  27,  42)
MID_BG     = (27,  43,  62)

# Maze
CELL_SIZE   = 40
MAZE_COLS   = 15
MAZE_ROWS   = 13
MAZE_OFFSET_X = 20
MAZE_OFFSET_Y = 20

# Player
PLAYER_SPEED   = 10
PLAYER_SIZE    = 20
PLAYER_COLOR   = TEAL

# NPC
NPC_SPEED      = 2
NPC_SIZE       = 20
NPC_COLOR      = CORAL

# SNN / NPC brain
SPIKE_WINDOW   = 3     
LIF_TAU        = 10.0
LIF_THRESHOLD  = 3.0

# HUD
HUD_WIDTH      = 220

YELLOW = (255, 230, 50)