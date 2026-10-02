import random 
import config

class Food:
    def __init__(self):
        self.x = random.randint(10, config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH - 10)
        self.y = random.randint(10, config.SCREEN_HEIGHT - 10)

class World:
    def __init__(self):
        self.food_list = []
        env = config.ENVIRONMENTS[config.ACTIVE_ENV]
        self.food_count = int(config.FOOD_COUNT * env["food_count_mult"])
        self.spawn_food(self.food_count)

    def spawn_food(self, count):
        for _ in range(count):
            self.food_list.append(Food())

    def replenish_food(self):
        # Only replenish up to food_count slowly
        if len(self.food_list) < self.food_count:
            # Add one food every 10 frames not instantly
            if random.random() < 0.1: 
                self.food_list.append(Food())  

    def remove_food(self, food):
        if food in self.food_list: 
            self.food_list.remove(food)  