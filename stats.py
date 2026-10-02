import config

class Stats:
    def __init__(self):
        self.generation      = 1
        self.total_food_eaten = 0
        self.extinctions     = 0

    def get_averages(self, population):
        alive = [c for c in population if c.alive]
        if not alive: 
            return 0, 0, 0, 0 
        return (
            round(sum(c.speed  for c in alive) / len(alive), 2),
            round(sum(c.vision for c in alive) / len(alive), 2),
            round(sum(c.size   for c in alive) / len(alive), 2), 
            round(sum(c.energy for c in alive) / len(alive), 2), 
        ) 

    def get_type_counts(self, population):
        alive = [c for c in population if c.alive]
        counts = {"runner": 0, "watcher": 0, "tank": 0}
        for c in alive:
            counts[c.creature_type] += 1
        return counts

    def get_level_counts(self, population):
        alive = [c for c in population if c.alive]
        counts = {1: 0, 2: 0, 3: 0}
        for c in alive:
            counts[c.level] += 1
        return counts

    def draw(self, surface, population, time_left):
        import pygame
        alive_count  = sum(1 for c in population if c.alive)
        avg_sp, avg_vi, avg_sz, avg_en = self.get_averages(population)
        type_counts  = self.get_type_counts(population)
        level_counts = self.get_level_counts(population)
        env          = config.ENVIRONMENTS[config.ACTIVE_ENV]

        panel_rect = pygame.Rect(
            config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH, 0,
            config.STATS_PANEL_WIDTH, config.SCREEN_HEIGHT)
        pygame.draw.rect(surface, config.PANEL_COLOR, panel_rect)

        fl = pygame.font.SysFont("Arial", 18, bold=True)
        fs = pygame.font.SysFont("Arial", 14)

        def txt(text, color, font, y):
            surface.blit(font.render(text, True, color),
                         (config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH + 10, y))

        y = 14
        txt("DARWIN'S PLAYGROUND", config.YELLOW, fl, y);  y += 26
        txt(f"Environment : {env['label']}", config.GREEN, fs, y); y += 22
        txt("", config.WHITE, fs, y); y += 10

        txt(f"Generation  : {self.generation}", config.WHITE, fs, y);  y += 20
        txt(f"Population  : {alive_count}",     config.GREEN, fs, y);  y += 20
        txt(f"Time Left   : {int(time_left)}s", config.LIGHT_GRAY, fs, y); y += 24

        txt("--- Averages ---", config.YELLOW, fs, y); y += 20
        txt(f"Avg Speed   : {avg_sp}", config.WHITE, fs, y); y += 18
        txt(f"Avg Vision  : {avg_vi}", config.WHITE, fs, y); y += 18
        txt(f"Avg Size    : {avg_sz}", config.WHITE, fs, y); y += 18
        txt(f"Avg Energy  : {avg_en}", config.WHITE, fs, y); y += 24

        txt("--- Creature Types ---", config.YELLOW, fs, y); y += 20
        txt(f"Runners     : {type_counts['runner']}",
            config.CREATURE_TYPES['runner']['color'],  fs, y); y += 18
        txt(f"Watchers    : {type_counts['watcher']}",
            config.CREATURE_TYPES['watcher']['color'], fs, y); y += 18
        txt(f"Tanks       : {type_counts['tank']}",
            config.CREATURE_TYPES['tank']['color'],    fs, y); y += 24

        txt("--- Levels ---", config.YELLOW, fs, y); y += 20
        txt(f"Level 1     : {level_counts[1]}", config.LIGHT_GRAY, fs, y); y += 18
        txt(f"Level 2     : {level_counts[2]}", (100, 200, 255),   fs, y); y += 18
        txt(f"Level 3     : {level_counts[3]}", (255, 215, 0),     fs, y); y += 24

        txt("--- Total ---", config.YELLOW, fs, y); y += 20
        txt(f"Food Eaten  : {self.total_food_eaten}", config.GREEN, fs, y); y += 18
        txt(f"Extinctions : {self.extinctions}",      config.RED,   fs, y)  