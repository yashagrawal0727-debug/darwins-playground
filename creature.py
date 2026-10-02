import random
import math
import config

class Creature:
    def __init__(self, speed=None, vision=None, size=None, creature_type=None, level=1):
        self.x = random.randint(10, config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH - 10)
        self.y = random.randint(10, config.SCREEN_HEIGHT - 10)

        self.creature_type = creature_type or random.choice(list(config.CREATURE_TYPES.keys()))
        type_data = config.CREATURE_TYPES[self.creature_type]

        base_speed  = speed  if speed  is not None else random.uniform(config.MIN_SPEED,  config.MAX_SPEED)
        base_vision = vision if vision is not None else random.uniform(config.MIN_VISION, config.MAX_VISION)
        base_size   = size   if size   is not None else random.uniform(config.MIN_SIZE,   config.MAX_SIZE)

        self.speed  = max(config.MIN_SPEED,  min(config.MAX_SPEED,  base_speed  + type_data["speed_bonus"]))
        self.vision = max(config.MIN_VISION, min(config.MAX_VISION, base_vision + type_data["vision_bonus"]))
        self.size   = max(config.MIN_SIZE,   min(config.MAX_SIZE,   base_size   + type_data["size_bonus"]))

        self.level = level 
        self.generations_survived = level - 1
        self.energy      = config.STARTING_ENERGY
        self.alive       = True
        self.target_food = None
        self.direction   = random.uniform(0, 2 * math.pi) 

        self._apply_level_bonus() #This line is calling a method (function) inside the same class/object.

    def _apply_level_bonus(self): #Applies survival bonuses.
        if self.level == 2:#Checks if creature survived enough.
            self.speed  = min(config.MAX_SPEED,  self.speed  * 1.08) #8% increase.
            self.vision = min(config.MAX_VISION, self.vision * 1.08)
        elif self.level >= 3:#Higher-level evolution. 
            self.speed  = min(config.MAX_SPEED,  self.speed  * 1.18) 
            self.vision = min(config.MAX_VISION, self.vision * 1.18)
            self.size   = min(config.MAX_SIZE,   self.size   * 1.10) 

    def get_color(self): #Returns display color. This defines a method named get_color
        base = config.CREATURE_TYPES[self.creature_type]["color"] 
        if self.level == 2:
            return tuple(min(255, c + 40) for c in base) #colours stored as tuples .RGB values cannot exceed 255.
        elif self.level >= 3:
            return tuple(min(255, c + 80) for c in base) #Loop through each color component,Converts the generated values into a color tuple.
        return base #If the creature is level 1 (or anything not matching above conditions):
                    #Use original color unchanged. generator expression = It creates new values from existing ones efficiently.

    def find_food(self, food_list): #This function searches through a list of food objects and finds the closest visible food.This defines a method called find_food.
        closest_food     = None #None means empty/no value.
        closest_distance = float('inf') #Start with very large distance
        for food in food_list:
            d = self.distance_to(food.x, food.y) #This calculates how far the creature is from the food.
            if d < self.vision and d < closest_distance: #Food must be close enough to see.Food must be closer than the currently saved closest food.
                closest_food     = food 
                closest_distance = d # method call = distance_to() calculates distance
        self.target_food = closest_food 

    def move(self):
        env        = config.ENVIRONMENTS[config.ACTIVE_ENV] #Loads active environment.
        speed_mult = env["speed_mult"] #This changes movement speed depending on environment.

        if self.target_food:
            dx = self.target_food.x - self.x #Difference in x-direction. 
            dy = self.target_food.y - self.y
            d  = self.distance_to(self.target_food.x, self.target_food.y) #Distance between creature and food. using dist formula 
            if d > 0:
                self.x += (dx / d) * self.speed * speed_mult #This moves creature toward food horizontally.
                self.y += (dy / d) * self.speed * speed_mult
        else:
            self.direction += random.uniform(-0.3, 0.3)   
            self.x += math.cos(self.direction) * self.speed * speed_mult * 0.5 #Random wandering is intentionally slower than food chasing.
            self.y += math.sin(self.direction) * self.speed * speed_mult * 0.5

        self.x = max(5, min(config.SCREEN_WIDTH - config.STATS_PANEL_WIDTH - 5, self.x)) #This prevents leaving screen horizontally.
        self.y = max(5, min(config.SCREEN_HEIGHT - 5, self.y))  

    def drain_energy(self):
            env_mult = config.ENVIRONMENTS[config.ACTIVE_ENV]["energy_drain_mult"]
            self.energy -= config.ENERGY_DRAIN_BASE    * env_mult #Subtracts base energy cost.
            self.energy -= self.speed * config.SPEED_ENERGY_COST * env_mult
            self.energy -= self.size  * config.SIZE_ENERGY_COST  * env_mult

            # Remove overeating death completely — only starvation kills
            if self.energy <= 0:
                self.alive = False

    def eat(self, food_list):
            for food in food_list:
                if self.distance_to(food.x, food.y) < self.size + config.FOOD_RADIUS: #Checks whether creature is close enough to touch/eat the food.to calculate distance between creature and food.
                    self.energy      = min(config.STARTING_ENERGY, self.energy + 12) #Creature gains 12 energy
                    self.target_food = None
                    return food
            return None 

    def distance_to(self, x, y): #"How far is this creature from another point?"
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def reproduce(self):
        child_speed  = self.speed
        child_vision = self.vision
        child_size   = self.size

        if random.random() < config.MUTATION_RATE:
            child_speed  += random.uniform(-config.MUTATION_AMOUNT, config.MUTATION_AMOUNT)
        if random.random() < config.MUTATION_RATE:
            child_vision += random.uniform(-5, 5) #Vision mutation range is fixed separately from speed mutation.
        if random.random() < config.MUTATION_RATE:
            child_size   += random.uniform(-config.MUTATION_AMOUNT, config.MUTATION_AMOUNT)

        child_speed  = max(config.MIN_SPEED,  min(config.MAX_SPEED,  child_speed))
        child_vision = max(config.MIN_VISION, min(config.MAX_VISION, child_vision))
        child_size   = max(config.MIN_SIZE,   min(config.MAX_SIZE,   child_size))

        new_level = min(3, self.level + (1 if self.generations_survived >= (self.level * 2) else 0))

        return Creature(child_speed, child_vision, child_size,
                        creature_type=self.creature_type,
                        level=new_level)       