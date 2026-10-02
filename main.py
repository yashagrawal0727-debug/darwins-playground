import pygame
import sys
import time
import math
import config
from creature import Creature
from world import World, Food
from evolution import next_generation
from stats import Stats 


class Slider:
    def __init__(self, x, y, w, min_val, max_val, default, label, is_float=False):
        self.x = x; self.y = y; self.w = w
        self.min_val = min_val; self.max_val = max_val
        self.value = default; self.label = label
        self.is_float = is_float; self.dragging = False
        self.h = 6; self.knob_radius = 10

    def get_knob_x(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return int(self.x + ratio * self.w)

    def draw(self, surface, font):
        pygame.draw.rect(surface, (50, 50, 70),
            (self.x, self.y + self.knob_radius - self.h//2, self.w, self.h), border_radius=4)
        fw = self.get_knob_x() - self.x
        if fw > 0:
            pygame.draw.rect(surface, (80, 160, 255),
                (self.x, self.y + self.knob_radius - self.h//2, fw, self.h), border_radius=4)
        kx = self.get_knob_x()
        pygame.draw.circle(surface, (255,255,255), (kx, self.y + self.knob_radius), self.knob_radius)
        pygame.draw.circle(surface, (80,160,255),  (kx, self.y + self.knob_radius), self.knob_radius-3)
        val = f"{self.value:.2f}" if self.is_float else str(int(self.value))
        surface.blit(font.render(f"{self.label}: {val}", True, (200,200,220)),
                     (self.x, self.y - 26))

    def handle_event(self, event):
        kx = self.get_knob_x(); ky = self.y + self.knob_radius
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.sqrt((event.pos[0]-kx)**2 + (event.pos[1]-ky)**2) <= self.knob_radius+4:
                self.dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            ratio = max(0, min(1, (event.pos[0]-self.x)/self.w))
            raw = self.min_val + ratio*(self.max_val-self.min_val)
            self.value = raw if self.is_float else round(raw)


def environment_screen(screen):
    clock = pygame.time.Clock()
    ft = pygame.font.SysFont("Arial", 34, bold=True)
    fm = pygame.font.SysFont("Arial", 18)
    fs = pygame.font.SysFont("Arial", 14)
    cx = config.SCREEN_WIDTH // 2
    selected = "forest"
    env_keys = list(config.ENVIRONMENTS.keys())
    card_w, card_h = 200, 160
    spacing = 40
    total_w = len(env_keys)*card_w + (len(env_keys)-1)*spacing
    start_x = cx - total_w//2
    btn_rect = pygame.Rect(cx-110, 460, 220, 50)

    while True:
        screen.fill(config.BG_COLOR)
        for x in range(0, config.SCREEN_WIDTH, 50):
            pygame.draw.line(screen, config.GRID_COLOR, (x,0),(x,config.SCREEN_HEIGHT))
        for y in range(0, config.SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, config.GRID_COLOR, (0,y),(config.SCREEN_WIDTH,y))

        title = ft.render("Choose Your Environment", True, config.YELLOW)
        screen.blit(title, title.get_rect(center=(cx,55)))
        sub = fm.render("Each environment affects food, energy and speed", True, (160,160,190))
        screen.blit(sub, sub.get_rect(center=(cx,95)))

        mx, my = pygame.mouse.get_pos()
        for i, key in enumerate(env_keys):
            env = config.ENVIRONMENTS[key]
            cx_ = start_x + i*(card_w+spacing) + card_w//2
            cy_ = 280
            rect = pygame.Rect(cx_-card_w//2, cy_-card_h//2, card_w, card_h)
            is_sel   = (key == selected)
            is_hover = rect.collidepoint(mx,my)
            border_col = (80,255,120) if is_sel else ((200,200,200) if is_hover else (60,60,80))
            fill_col = (env["bg_color"][0]+15, env["bg_color"][1]+15, env["bg_color"][2]+15) \
                       if is_sel else env["bg_color"]
            pygame.draw.rect(screen, fill_col, rect, border_radius=12)
            pygame.draw.rect(screen, border_col, rect, 2, border_radius=12)
            label = fm.render(env["label"], True, config.YELLOW)
            screen.blit(label, label.get_rect(center=(cx_,cy_-40)))
            for j in range(int(env["food_count_mult"]*6)):
                fx = rect.x+20+(j%6)*28
                fy = cy_-5+(j//6)*18
                pygame.draw.circle(screen, env["food_color"], (fx,fy), 5)
            words = env["description"].split(" — ")
            for wi, w in enumerate(words):
                desc = fs.render(w, True, (180,180,180))
                screen.blit(desc, desc.get_rect(center=(cx_,cy_+38+wi*18)))
            if is_sel:
                sel = fm.render("Selected", True, (80,255,120))
                screen.blit(sel, sel.get_rect(center=(cx_,cy_+78)))

        bc = (40,120,60) if btn_rect.collidepoint(mx,my) else (30,90,45)
        pygame.draw.rect(screen, bc, btn_rect, border_radius=10)
        pygame.draw.rect(screen, (80,255,120), btn_rect, 2, border_radius=10)
        bt = pygame.font.SysFont("Arial",20,bold=True).render("NEXT: Settings",True,(200,255,210))
        screen.blit(bt, bt.get_rect(center=btn_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, key in enumerate(env_keys):
                    cx_ = start_x+i*(card_w+spacing)+card_w//2
                    rect = pygame.Rect(cx_-card_w//2, 280-card_h//2, card_w, card_h)
                    if rect.collidepoint(event.pos): selected = key
                if btn_rect.collidepoint(event.pos):
                    config.ACTIVE_ENV = selected; return
        pygame.display.flip()
        clock.tick(60)


def settings_screen(screen):
    clock = pygame.time.Clock()
    ft = pygame.font.SysFont("Arial", 32, bold=True)
    fs = pygame.font.SysFont("Arial", 17)
    fb = pygame.font.SysFont("Arial", 20, bold=True)
    cx = config.SCREEN_WIDTH//2
    sw = 400
    sliders = [
        Slider(cx-sw//2,165,sw,20,  200,config.POPULATION_SIZE,   "Population",          False),
        Slider(cx-sw//2,245,sw,10,  100,config.FOOD_COUNT,         "Food Count",           False),
        Slider(cx-sw//2,325,sw,5,   120,config.GENERATION_TIME,    "Generation Time (s)",  False),
        Slider(cx-sw//2,405,sw,0.01,0.20,config.ENERGY_DRAIN_BASE, "Energy Drain",         True),
        Slider(cx-sw//2,485,sw,0.01,0.10,config.MUTATION_RATE,     "Mutation Rate",        True),
    ]
    btn_rect = pygame.Rect(cx-110, 545, 220, 50)

    while True:
        screen.fill(config.BG_COLOR)
        for x in range(0, config.SCREEN_WIDTH, 50):
            pygame.draw.line(screen, config.GRID_COLOR,(x,0),(x,config.SCREEN_HEIGHT))
        for y in range(0, config.SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, config.GRID_COLOR,(0,y),(config.SCREEN_WIDTH,y))
        title = ft.render("Simulation Settings", True, config.YELLOW)
        screen.blit(title, title.get_rect(center=(cx,55)))
        env_text = fs.render(
            f"Environment: {config.ENVIRONMENTS[config.ACTIVE_ENV]['label']}",
            True, config.GREEN)
        screen.blit(env_text, env_text.get_rect(center=(cx,95)))
        for s in sliders: s.draw(screen, fs)
        mx, my = pygame.mouse.get_pos()
        bc = (40,120,60) if btn_rect.collidepoint((mx,my)) else (30,90,45)
        pygame.draw.rect(screen, bc, btn_rect, border_radius=10)
        pygame.draw.rect(screen, (80,255,120), btn_rect, 2, border_radius=10)
        bl = fb.render("START SIMULATION", True, (200,255,210))
        screen.blit(bl, bl.get_rect(center=btn_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            for s in sliders: s.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                config.POPULATION_SIZE   = int(sliders[0].value)
                config.FOOD_COUNT        = int(sliders[1].value)
                config.GENERATION_TIME   = int(sliders[2].value)
                config.ENERGY_DRAIN_BASE = sliders[3].value
                config.MUTATION_RATE     = sliders[4].value
                return
        pygame.display.flip()
        clock.tick(60)


def draw_grid(surface):
    env = config.ENVIRONMENTS[config.ACTIVE_ENV]
    for x in range(0, config.SCREEN_WIDTH-config.STATS_PANEL_WIDTH, 50):
        pygame.draw.line(surface, env["grid_color"],(x,0),(x,config.SCREEN_HEIGHT))
    for y in range(0, config.SCREEN_HEIGHT, 50):
        pygame.draw.line(surface, env["grid_color"],(0,y),
            (config.SCREEN_WIDTH-config.STATS_PANEL_WIDTH,y))


def draw_food(surface, food_list, tick):
    for food in food_list:
        fx, fy = int(food.x), int(food.y) 
        r = 7
        pygame.draw.circle(surface, (40, 10, 10),   (fx, fy+1), r+2)
        pygame.draw.circle(surface, (210, 40, 40),  (fx, fy+1), r)
        pygame.draw.circle(surface, (240, 70, 60),  (fx, fy),   r)
        pygame.draw.circle(surface, (255, 200, 200),(fx-2, fy-2), 2)
        pygame.draw.circle(surface, (255, 240, 240),(fx-2, fy-2), 1)
        pygame.draw.line(surface, (100, 60, 20),(fx, fy-r+1),(fx+2, fy-r-4), 2)
        leaf_pts = [(fx+2,fy-r-2),(fx+7,fy-r-5),(fx+6,fy-r)]
        pygame.draw.polygon(surface, (50, 180, 50), leaf_pts)
        pygame.draw.polygon(surface, (30, 140, 30), leaf_pts, 1)
        pygame.draw.circle(surface, (170, 30, 30),(fx, fy-r+2), 2)  


def draw_creature(surface, creature, tick):
    if not creature.alive:
        return

    color        = creature.get_color()
    cx, cy       = int(creature.x), int(creature.y)
    r            = max(14, int(creature.size) + 8)
    energy_ratio = creature.energy / config.STARTING_ENERGY

    # Low energy red warning glow
    if energy_ratio < 0.2:
        pygame.draw.circle(surface, (160, 20, 20), (cx, cy), r + 8)

    # Level 3 gold pulsing ring
    if creature.level >= 3:
        pulse = r + 9 + int(4 * math.sin(tick * 0.1))
        pygame.draw.circle(surface, (255, 215, 0), (cx, cy), pulse, 2)

    # Level 2 bright ring
    if creature.level >= 2:
        pygame.draw.circle(surface,
                           tuple(min(255, c+80) for c in color),
                           (cx, cy), r+5, 2)

    # Facing direction
    if creature.target_food:
        dx = creature.target_food.x - creature.x
        dy = creature.target_food.y - creature.y
        angle_deg = math.degrees(math.atan2(dy, dx))
    else:
        angle_deg = math.degrees(creature.direction)

    angle_rad = math.radians(angle_deg)

    # Antennae
    wiggle = int(2 * math.sin(tick * 0.15))
    ant_base_left  = (cx - r//3, cy - r + 2)
    ant_base_right = (cx + r//3, cy - r + 2)
    ant_tip_left   = (cx - r//2 - 2 + wiggle, cy - r - 14)
    ant_tip_right  = (cx + r//2 + 2 + wiggle, cy - r - 14)
    pygame.draw.line(surface, (20,20,20), ant_base_left,  ant_tip_left,  2)
    pygame.draw.line(surface, (20,20,20), ant_base_right, ant_tip_right, 2)
    sq = 5
    tip_color = tuple(min(255, c+60) for c in color)
    for tip in [ant_tip_left, ant_tip_right]:
        pygame.draw.rect(surface, (20,20,20),
                         (tip[0]-sq//2-1, tip[1]-sq//2-1, sq+2, sq+2))
        pygame.draw.rect(surface, tip_color,
                         (tip[0]-sq//2, tip[1]-sq//2, sq, sq))

    # Pac-Man mouth
    if creature.target_food:
        mouth_open = 35 + int(18 * abs(math.sin(tick * 0.15)))
    else:
        mouth_open = 5

    # Draw full colored circle
    pygame.draw.circle(surface, (20,20,20), (cx, cy), r+2)
    pygame.draw.circle(surface, color,      (cx, cy), r)

    # Cut black wedge for mouth
    wedge_dist = r + 4
    wedge = [
        (cx, cy),
        (cx + int(wedge_dist * math.cos(math.radians(angle_deg + mouth_open))),
         cy + int(wedge_dist * math.sin(math.radians(angle_deg + mouth_open)))),
        (cx + int(wedge_dist * math.cos(math.radians(angle_deg + mouth_open*0.5))),
         cy + int(wedge_dist * math.sin(math.radians(angle_deg + mouth_open*0.5)))),
        (cx + int(wedge_dist * math.cos(math.radians(angle_deg))),
         cy + int(wedge_dist * math.sin(math.radians(angle_deg)))),
        (cx + int(wedge_dist * math.cos(math.radians(angle_deg - mouth_open*0.5))),
         cy + int(wedge_dist * math.sin(math.radians(angle_deg - mouth_open*0.5)))),
        (cx + int(wedge_dist * math.cos(math.radians(angle_deg - mouth_open))),
         cy + int(wedge_dist * math.sin(math.radians(angle_deg - mouth_open)))),
    ]
    pygame.draw.polygon(surface, (0,0,0), wedge)
    pygame.draw.circle(surface, (20,20,20), (cx,cy), r, 2)

    # Shine
    shine = tuple(min(255, c+70) for c in color)
    pygame.draw.circle(surface, shine, (cx-r//3, cy-r//3), r//4)

    # Legs
    leg_wiggle = int(3 * math.sin(tick * 0.2))
    legs = [
        ((cx-r+2, cy+4),  (cx-r-8, cy+9  + leg_wiggle)),
        ((cx-r+2, cy+10), (cx-r-8, cy+16 - leg_wiggle)),
        ((cx+r-2, cy+4),  (cx+r+8, cy+9  + leg_wiggle)),
        ((cx+r-2, cy+10), (cx+r+8, cy+16 - leg_wiggle)),
    ]
    for start, end in legs:
        pygame.draw.line(surface, (20,20,20), start, end, 2)

    # Eye
    eye_angle = math.radians(angle_deg - 70)
    eye_x = cx + int(r * 0.52 * math.cos(eye_angle))
    eye_y = cy + int(r * 0.52 * math.sin(eye_angle))
    eye_r = max(3, r//4)
    pygame.draw.circle(surface, (20,20,20),    (eye_x, eye_y), eye_r+1)
    pygame.draw.circle(surface, (255,255,255), (eye_x, eye_y), eye_r)
    pygame.draw.circle(surface, (10,10,10),    (eye_x, eye_y), max(2, eye_r-2))

    # Level 3 crown
    if creature.level >= 3:
        pygame.draw.circle(surface, (255,215,0), (cx, cy-r-18), 5)

    # ── ENERGY BAR ───────────────────────────────────────────
    bar_w = r * 2
    bar_h = 5
    bar_x = cx - r
    bar_y = cy + r + 8

    # Dark background
    pygame.draw.rect(surface, (30,30,30),
                     (bar_x-1, bar_y-1, bar_w+2, bar_h+2), border_radius=2)

    # Fill ratio — 100 energy = full bar
    fill_ratio = max(0.0, min(1.0, creature.energy / config.STARTING_ENERGY))
    fill_w     = int(bar_w * fill_ratio)

    # Color based on energy level
    if fill_ratio > 0.6:
        bar_color = (50, 220, 50)      # green
    elif fill_ratio > 0.3:
        bar_color = (255, 180, 0)      # yellow
    else:
        bar_color = (220, 40, 40)      # red

    if fill_w > 0:
        pygame.draw.rect(surface, bar_color,
                         (bar_x, bar_y, fill_w, bar_h), border_radius=2)

    # Border
    pygame.draw.rect(surface, (80,80,80),
                     (bar_x, bar_y, bar_w, bar_h), 1, border_radius=2)

    # Vision arc — every 3rd tick only
    if tick % 3 == 0:
        vision_color = (color[0]//5, color[1]//5, color[2]//5)
        for i in range(7):
            arc_a = angle_rad - math.radians(60) + math.radians(120*i/6)
            vx = cx + int(creature.vision * math.cos(arc_a))
            vy = cy + int(creature.vision * math.sin(arc_a))
            pygame.draw.circle(surface, vision_color, (vx, vy), 1)


def draw_world(surface, population, world, tick):
    env = config.ENVIRONMENTS[config.ACTIVE_ENV]
    pygame.draw.rect(surface, env["bg_color"],
        (0, 0, config.SCREEN_WIDTH-config.STATS_PANEL_WIDTH, config.SCREEN_HEIGHT))
    draw_grid(surface)
    draw_food(surface, world.food_list, tick)
    for creature in population:
        draw_creature(surface, creature, tick)


def draw_legend(surface):
    font      = pygame.font.SysFont("Arial", 13)
    font_bold = pygame.font.SysFont("Arial", 13, bold=True)
    box_x = 5
    box_y = config.SCREEN_HEIGHT - 140
    box_w = 215
    box_h = 135
    bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 200))
    surface.blit(bg, (box_x, box_y))
    pygame.draw.rect(surface, (60,60,80), (box_x,box_y,box_w,box_h), 1, border_radius=6)
    surface.blit(font_bold.render("CREATURES", True, (220,220,220)),
                 (box_x+8, box_y+6))
    items = [
        ("Runner  - Fast & aggressive",  config.CREATURE_TYPES["runner"]["color"]),
        ("Watcher - Wide vision arc",    config.CREATURE_TYPES["watcher"]["color"]),
        ("Tank    - Large & slow",       config.CREATURE_TYPES["tank"]["color"]),
        ("Level 2 - Evolved",            (100, 200, 255)),
        ("Level 3 - Elite",              (255, 215,   0)),
    ]
    y = box_y + 24
    for text, color in items:
        surface.blit(font.render(text, True, color), (box_x+8, y))
        y += 20


def draw_speed_indicator(surface, slow_mode):
    font  = pygame.font.SysFont("Arial", 13, bold=True)
    label = "SLOW MODE ON - press S to speed up" if slow_mode else "press S for slow mode"
    color = (255, 220, 0) if slow_mode else (150, 150, 150)
    surface.blit(font.render(label, True, color), (10, config.SCREEN_HEIGHT - 148))


def draw_birth_animations(surface, birth_events, tick):
    for event in birth_events[:]:
        x, y, color, age, event_type = event
        if age > 25:
            birth_events.remove(event)
            continue
        if event_type == "birth":
            radius = age * 3
            bright = tuple(min(255, c+100) for c in color)
            pygame.draw.circle(surface, bright, (int(x), int(y)), radius, 2)
        event[3] += 1 


def draw_generation_banner(surface, generation, survivors, total):
    font_big   = pygame.font.SysFont("Arial", 36, bold=True)
    font_med   = pygame.font.SysFont("Arial", 20)
    font_small = pygame.font.SysFont("Arial", 16)
    overlay = pygame.Surface(
        (config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH, config.SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    cx = (config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH) // 2
    cy = config.SCREEN_HEIGHT // 2
    box_rect = pygame.Rect(cx-220, cy-90, 440, 180)
    pygame.draw.rect(surface, (20,40,20), box_rect, border_radius=16)
    pygame.draw.rect(surface, config.YELLOW, box_rect, 2, border_radius=16)
    t1 = font_big.render(f"Generation {generation} Complete!", True, config.YELLOW)
    t2 = font_med.render(f"{survivors} survived out of {total} creatures", True, config.GREEN)
    t3 = font_med.render("Reproducing next generation...", True, (200,200,200))
    t4 = font_small.render("Watch for new births", True, (150,150,150))
    surface.blit(t1, t1.get_rect(center=(cx, cy-50)))
    surface.blit(t2, t2.get_rect(center=(cx, cy-5)))
    surface.blit(t3, t3.get_rect(center=(cx, cy+35)))
    surface.blit(t4, t4.get_rect(center=(cx, cy+70)))


def run_simulation(screen): 
    clock = pygame.time.Clock() #Creates a clock object that controls how fast the game loop runs (FPS limiter).
    population = [Creature() for _ in range(config.POPULATION_SIZE)] # _ is used cus its a dummy variable it doesn't any use after population function 
    world      = World()
    stats      = Stats()
    generation_start = time.time() #Records the current time in seconds. Used later to track how long a generation has been running.
    paused    = False
    slow_mode = False
    tick      = 0
    birth_events     = []
    show_banner      = False
    banner_timer     = 0
    banner_survivors = 0   #All just variable initialization before the loop starts
    banner_total     = 0  # all this to intialise this class

    back_rect = pygame.Rect(
        config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH + 10,
        config.SCREEN_HEIGHT - 45, 230, 36) # defines a rectangle for the back button. Used for click detection later.
    fb = pygame.font.SysFont("Arial", 14, bold=True) #Loads Arial font at size 14, bold. Stored in fb to render text later.
    print("SPACE=Pause | S=Slow | R=Reset | B=Back | Q=Quit") 

    while True: # loop runs forever until broken by return 
        for event in pygame.event.get():#pygame.event.get() returns a list of everything that happened since the last frame — clicks, keypresses, window close.
            if event.type == pygame.QUIT: # If user clicks the Q button on the window, shut everything down. pygame.quit() closes pygame, sys.exit() exits Python entirely.
                pygame.quit(); sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:#not paused flips the boolean — if it was True it becomes False and vice versa. This is the toggle pattern.
                    paused = not paused
                    print("Paused" if paused else "Resumed")
                if event.key == pygame.K_s:
                    slow_mode = not slow_mode #Same toggle pattern. Slow mode drops FPS from 60 to 8 AND reduces energy drain so creatures don't die too fast in slow motion.
                    if slow_mode:
                        config.FPS = 8
                        config.ENERGY_DRAIN_BASE = 0.02
                        print("SLOW MODE ON")
                    else:
                        config.FPS = 60
                        config.ENERGY_DRAIN_BASE = 0.08
                        print("Normal speed")
                if event.key == pygame.K_r: #Reset — just recreates everything from scratch.
                    population = [Creature() for _ in range(config.POPULATION_SIZE)]
                    world = World(); stats = Stats()
                    generation_start = time.time(); tick = 0
                    birth_events = []; show_banner = False
                    print("Reset!")
                if event.key == pygame.K_b: return
                if event.key == pygame.K_q: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos): #collidepoint(x, y) checks if a point is inside the rectangle. event.pos is a tuple (x, y) of where the mouse clicked. If click is inside the back button, return.
                return 

        if not paused: # indentation used 
            tick += 1 #tick is a frame counter. Increments every frame.
            for creature in population:
                if creature.alive:
                    creature.find_food(world.food_list)
                    creature.move()
                    creature.drain_energy()
                    eaten = creature.eat(world.food_list)
                    if eaten:
                        world.remove_food(eaten)
                        world.food_list.append(Food())
                        stats.total_food_eaten += 1 

            world.replenish_food()
            elapsed   = time.time() - generation_start #time.time() returns current time. Subtracting the start time gives seconds elapsed. Then subtract from total generation time to get countdown
            time_left = config.GENERATION_TIME - elapsed

            if time_left <= 0:
                alive_count      = sum(1 for c in population if c.alive)
                banner_survivors = alive_count
                banner_total     = len(population)
                print(f"Gen {stats.generation} ended — {alive_count} survivors")
                if alive_count < config.MIN_SURVIVORS:
                    stats.extinctions += 1
                for c in population:
                    if c.alive:
                        c.generations_survived += 1
                new_population = next_generation(population)
                for creature in new_population:
                    birth_events.append(
                        [creature.x, creature.y, creature.get_color(), 0, "birth"])
                population       = new_population  #Swap in new population, reset the world, increment generation counter, restart the timer, trigger the banner display
                world            = World()
                stats.generation += 1
                generation_start = time.time()
                show_banner      = True
                banner_timer     = tick
                print(f"Gen {stats.generation} started!")

            draw_world(screen, population, world, tick)
            stats.draw(screen, population, time_left)
            draw_legend(surface=screen)
            draw_speed_indicator(screen, slow_mode)
            draw_birth_animations(screen, birth_events, tick)

            if show_banner: #Show the banner for 120 ticks (2 seconds at 60fps), then hide it. tick - banner_timer is how many frames have passed since banner appeared.
                draw_generation_banner(screen, stats.generation-1,
                                       banner_survivors, banner_total)
                if tick - banner_timer > 120:
                    show_banner = False  

            mx, my = pygame.mouse.get_pos()
            bc = (60,40,40) if back_rect.collidepoint((mx,my)) else (40,30,30)
            pygame.draw.rect(screen, bc, back_rect, border_radius=8)
            pygame.draw.rect(screen, (180,80,80), back_rect, 2, border_radius=8)
            screen.blit(fb.render("Back to Settings", True, (255,160,160)),
                        (back_rect.x+12, back_rect.y+9))
            pygame.display.flip() # actually pushes everything drawn to the visible screen. Without this nothing appears. pygame draws to a back buffer, flip() swaps it to front.

        clock.tick(config.FPS) 

 
def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Darwin's Playground")
    while True:
        environment_screen(screen) #pygame.init() starts all pygame modules. set_mode() creates the window taking a tuple (width, height). set_caption() sets the title bar text. 
        settings_screen(screen)
        run_simulation(screen)
                                    #The while True loop means after simulation ends you go back to environment screen — the whole app loops.


if __name__ == "__main__":
    main() 