# ─────────────────────────────────────────
# SCREEN
# ─────────────────────────────────────────
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 10 
STATS_PANEL_WIDTH = 250

# ─────────────────────────────────────────
# CREATURE BASE SETTINGS
# ─────────────────────────────────────────
POPULATION_SIZE = 100
MIN_SPEED = 1
MAX_SPEED = 5
MIN_VISION = 20
MAX_VISION = 100
MIN_SIZE = 3
MAX_SIZE = 10
STARTING_ENERGY = 100

# ─────────────────────────────────────────
# FOOD
# ─────────────────────────────────────────
FOOD_COUNT = 15
FOOD_RADIUS = 5

# ─────────────────────────────────────────
# EVOLUTION
# ─────────────────────────────────────────
MUTATION_RATE = 0.01
MUTATION_AMOUNT = 0.5
GENERATION_TIME = 120
MIN_SURVIVORS = 10

# ─────────────────────────────────────────
# ENERGY
# ─────────────────────────────────────────
STARTING_ENERGY   = 100
ENERGY_DRAIN_BASE = 0.15     # drains visibly fast
SPEED_ENERGY_COST = 0.04
SIZE_ENERGY_COST  = 0.015

# ─────────────────────────────────────────
# CREATURE TYPES
# ─────────────────────────────────────────
CREATURE_TYPES = {
    "runner": {
        "speed_bonus":  2.0, 
        "vision_bonus": -10,
        "size_bonus":   -2,
        "color":        (255, 100, 60),
        "label":        "Runner"
    }, 
    "watcher": {
        "speed_bonus":  0.0,
        "vision_bonus": 30,
        "size_bonus":   0,
        "color":        (60, 200, 255),
        "label":        "Watcher"
    },
    "tank": {
        "speed_bonus":  -1.0,
        "vision_bonus": -5,
        "size_bonus":   4,
        "color":        (160, 80, 255),
        "label":        "Tank"
    }
}

# ─────────────────────────────────────────
# ENVIRONMENTS
# ─────────────────────────────────────────
ENVIRONMENTS = {
    "forest": {
        "label":             "Forest",
        "bg_color":          (10, 20, 12),
        "grid_color":        (20, 35, 22),
        "food_color":        (0, 255, 100),
        "food_glow":         (0, 80,  40),
        "food_count_mult":   1.5,       # more food
        "energy_drain_mult": 0.7,       # easier survival
        "speed_mult":        1.0,
        "description":       "Lush forest — plenty of food, easy survival"
    },
    "desert": {
        "label":             "Desert",
        "bg_color":          (28, 18, 8),
        "grid_color":        (45, 32, 15),
        "food_color":        (255, 200, 50),
        "food_glow":         (120, 80, 10),
        "food_count_mult":   0.5,       # scarce food
        "energy_drain_mult": 1.8,       # harsh survival
        "speed_mult":        0.85,
        "description":       "Harsh desert — scarce food, fast energy drain"
    },
    "ocean": {
        "label":             "Ocean",
        "bg_color":          (5, 15, 35),
        "grid_color":        (10, 25, 55),
        "food_color":        (100, 220, 255),
        "food_glow":         (20, 80, 120),
        "food_count_mult":   1.0,
        "energy_drain_mult": 1.1,
        "speed_mult":        1.2,       # creatures move faster in water
        "description":       "Deep ocean — balanced but swift currents"
    }
}

# Active environment — changed at runtime
ACTIVE_ENV = "forest"

# ─────────────────────────────────────────
# COLORS (UI)
# ─────────────────────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
GREEN      = (0,   255, 120)
RED        = (255, 80,  80)
BLUE       = (80,  140, 255)
YELLOW     = (255, 220, 0)
GRAY       = (40,  40,  40)
LIGHT_GRAY = (200, 200, 200)
PANEL_COLOR = (15, 15, 25)
GRID_COLOR  = (25, 25, 40)
BG_COLOR    = (10, 10, 18)
FOOD_COLOR  = (0,  255, 120)
FOOD_GLOW_COLOR = (0, 100, 50) 