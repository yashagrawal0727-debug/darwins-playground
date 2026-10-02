import random
import config
from creature import Creature

def select_survivors(population):  
    return [c for c in population if c.alive]

def get_surviving_types(survivors):
    return list(set(c.creature_type for c in survivors)) 

def reproduce_population(survivors):
    new_population = [] 
    for creature in survivors:
        new_population.append(creature.reproduce())
        new_population.append(creature.reproduce())
    return new_population  

def next_generation(population):
    survivors       = select_survivors(population) 
    surviving_types = get_surviving_types(survivors)  

    print(f"Surviving types: {surviving_types}")

    if len(survivors) < config.MIN_SURVIVORS:
        print("Too few survivors — fresh population!")
        return [Creature() for _ in range(config.POPULATION_SIZE)]

    new_population = reproduce_population(survivors)

    # Trim if too many
    while len(new_population) > config.POPULATION_SIZE:
        new_population.pop()

    # Pad ONLY with surviving types
    while len(new_population) < config.POPULATION_SIZE:
        t = random.choice(surviving_types)
        new_population.append(Creature(creature_type=t))

    return new_population  