# 🧬 Darwin's Playground

A Python-based evolutionary simulation that demonstrates the concepts of **natural selection, survival, mutation, reproduction, and adaptation** through an interactive visual environment.

In Darwin's Playground, a population of creatures lives in different environments, searches for food, consumes energy, reproduces, and evolves across generations. Creatures with different characteristics have different survival strategies, allowing the simulation to demonstrate how populations can adapt over time.

---

## 🎯 Project Overview

Darwin's Playground is an interactive simulation built using **Python and Pygame**.

Each creature has characteristics such as:

- Speed
- Vision
- Size
- Energy
- Creature type
- Evolution level

Creatures must find food to maintain their energy. Their movement, vision, size, and environment affect their energy consumption and survival.

As generations progress, surviving creatures reproduce and their offspring can inherit modified characteristics through mutation.

---

## ✨ Features

### 🧬 Evolution System

The simulation supports multiple generations of creatures.

Surviving creatures can reproduce and pass their characteristics to their offspring. Small random mutations can occur during reproduction, allowing new traits to appear.

---

### 🐾 Three Creature Types

The simulation contains three different creature types:

| Type | Characteristics |
|------|-----------------|
| 🏃 Runner | Higher speed but lower vision and smaller size |
| 👁️ Watcher | Higher vision and balanced characteristics |
| 🛡️ Tank | Larger size but lower movement speed |

Each type has different advantages and disadvantages.

---

### 🌍 Multiple Environments

The simulation supports different environments that affect creature survival.

#### 🌲 Forest

- More available food
- Lower energy consumption
- Normal movement speed
- Easier survival conditions

#### 🏜️ Desert

- Less available food
- Higher energy consumption
- Reduced movement speed
- Harsh survival conditions

#### 🌊 Ocean

- Balanced food availability
- Slightly higher energy consumption
- Increased movement speed

The environment affects how creatures survive and adapt.

---

## 🍎 Food and Energy System

Creatures continuously lose energy while moving and surviving.

Energy consumption depends on:

- Base energy drain
- Movement speed
- Creature size
- Environment

When a creature finds food, it gains energy.

If a creature's energy reaches zero, it dies.

This creates survival pressure that influences the population.

---

## 🧬 Mutation

During reproduction, creature characteristics can undergo small random mutations.

Mutation can affect:

- Speed
- Vision
- Size

The mutation rate and mutation amount can be configured in `config.py`.

Example:

```python
MUTATION_RATE = 0.01
MUTATION_AMOUNT = 0.5
```

Mutation introduces variation into the population and allows new characteristics to appear across generations.

---

## 📈 Evolution Levels

Creatures can progress through different evolution levels as they survive and reproduce.

### Level 1

Newly created creatures begin at Level 1.

### Level 2

Surviving creatures can receive improvements to characteristics such as:

- Speed
- Vision

### Level 3

Higher-level creatures can receive additional improvements such as:

- Speed
- Vision
- Size

Evolution levels allow the simulation to represent progressive adaptation across generations.

---

## 📊 Real-Time Statistics

The simulation provides real-time statistics to observe changes in the population.

The statistics can include:

- Current generation
- Population
- Remaining time
- Average speed
- Average vision
- Average size
- Average energy
- Number of runners
- Number of watchers
- Number of tanks
- Number of Level 1 creatures
- Number of Level 2 creatures
- Number of Level 3 creatures
- Total food eaten
- Number of extinctions

These statistics make it easier to analyze how the population changes over time.

---

## 🎮 Interactive Simulation

The project provides an interactive graphical simulation using Pygame.

Users can configure simulation parameters before starting the evolutionary process.

Configurable parameters may include:

- Population size
- Food count
- Generation duration
- Energy drain
- Mutation rate

The simulation then runs continuously and displays the evolving population.

---

## 🛠️ Technologies Used

- **Python**
- **Pygame**
- **Object-Oriented Programming**
- **Evolutionary Algorithms**
- **Randomized Simulation**
- **Mutation and Reproduction**
- **Mathematical Distance Calculations**
- **Real-Time Statistics**

---

## 📁 Project Structure

```text
darwins-playground/
│
├── .vscode/
│   └── settings.json
│
├── .gitignore
├── config.py
├── creature.py
├── evolution.py
├── main.py
├── stats.py
├── world.py
└── README.md
```

---

## 📄 File Description

### `main.py`

The main entry point of the application.

It handles:

- Starting the simulation
- Pygame window
- User interaction
- Main simulation loop
- Rendering

### `creature.py`

Handles creature-related functionality including:

- Creature creation
- Movement
- Food detection
- Eating
- Energy consumption
- Reproduction
- Mutation
- Evolution levels

### `evolution.py`

Handles the evolutionary process and generation transitions.

It manages the population as generations progress.

### `world.py`

Handles the simulation world and food-related functionality.

It manages:

- Food creation
- Food positioning
- Food spawning
- Food replenishment
- Environment conditions

### `stats.py`

Handles simulation statistics and the statistics display.

It calculates information such as:

- Population
- Average speed
- Average vision
- Average size
- Average energy
- Creature type distribution
- Evolution level distribution
- Food consumed
- Extinctions

### `config.py`

Contains the main configuration parameters used by the simulation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yashagrawal0727-debug/darwins-playground.git
```

### 2. Enter the project directory

```bash
cd darwins-playground
```

### 3. Install Pygame

```bash
pip install pygame
```

---

## ▶️ Running the Project

Run the main Python file:

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

The Pygame simulation window should open.

---

## 🔬 How the Simulation Works

```text
              START
                │
                ▼
        Create Population
                │
                ▼
           Spawn Food
                │
                ▼
        Start Simulation
                │
                ▼
       Creatures Search
            for Food
                │
                ▼
           Eat Food
                │
                ▼
          Gain Energy
                │
                ▼
        Energy Decreases
                │
                ▼
       Creature Alive?
          /          \
        Yes           No
         │             │
         ▼             ▼
    Reproduction   Creature Dies
         │
         ▼
      Mutation
         │
         ▼
  Next Generation
         │
         ▼
    Repeat Cycle
```

---

## 🧠 Core Concepts Demonstrated

### Object-Oriented Programming

The project uses classes to represent different components of the simulation.

Examples include:

- `Creature`
- `World`
- `Food`

### Natural Selection

Creatures that successfully survive and reproduce contribute to future generations.

### Trait Inheritance

Offspring inherit characteristics from their parent creatures.

These characteristics can include:

- Speed
- Vision
- Size
- Creature type

### Mutation

Small random changes can occur during reproduction.

Mutation introduces variation into the population and can produce different characteristics in future generations.

### Reproduction

Surviving creatures can reproduce and create new members of the population.

### Simulation

The program models a dynamic environment through repeated simulation steps.

---

## 🎛️ Configuration

Most simulation parameters can be modified in:

`config.py`

For example:

```python
POPULATION_SIZE = 100
MIN_SPEED = 1
MAX_SPEED = 5
MIN_VISION = 20
MAX_VISION = 100
FOOD_COUNT = 15
MUTATION_RATE = 0.01
MUTATION_AMOUNT = 0.5
GENERATION_TIME = 120
```

Changing these parameters allows different evolutionary scenarios to be tested.

---

## 🚀 Future Improvements

Possible future improvements include:

- More creature types
- More environments
- Predator-prey interactions
- Advanced genetic inheritance
- Population graphs
- Historical generation data
- Save and load simulation states
- Machine learning-based evolutionary analysis
- Interactive environment selection
- Improved creature animations
- Sound effects and background music
- Advanced visualization of evolutionary trends

---

## 🎓 Educational Purpose

Darwin's Playground was developed as an educational simulation to demonstrate how computational models can be used to represent evolutionary concepts.

The project combines:

**Programming + Simulation + Evolutionary Computing + Artificial Intelligence Concepts**

to create an interactive environment where users can observe population behavior, survival, reproduction, mutation, and adaptation.

---

## 👨‍💻 Author

**Yash Agrawal**

Computer Science Engineering Student

**Vishwakarma Institute of Technology (VIT Pune)**

---

## 📜 License

This project is currently available for educational and learning purposes.


