# TURNBOUND

## Python ASCII Turn-Based Survival Roguelike

A highly stylized turn-based ASCII survival roguelike built with Python, Textual, and Rich.

---

## Features

- **Tactical Turn-Based Combat**: Every action advances the world state
- **Procedural Arenas**: Unique battlefields each run
- **Wave Survival**: Face increasingly difficult enemy waves
- **Boss Duels**: Epic encounters every 5 waves
- **Deep Build Crafting**: Tag-driven upgrade system with synergies
- **4 Unique Characters**: Each with distinct mechanics
- **Rich ASCII Graphics**: Atmospheric terminal rendering with colors and effects

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the Game

```bash
python main.py
```

---

## Controls

### Movement
- **Arrow Keys**: Move in directions
- **Space**: Wait/Skip turn

### Skills
- **Q**: Primary Skill
- **W**: Secondary Skill
- **E**: Utility Skill
- **R**: Ultimate Skill

### Other
- **ESC**: Pause menu
- **↑↓**: Navigate menus
- **ENTER**: Select option

---

## Characters

### The Executioner
Brutal blood-fueled melee fighter. Rage generation mechanic.

### The Astromancer
Temporal and spatial manipulation. Echo system for repeating abilities.

### The Plague Saint
Infection and arena corruption. Spread infection to enemies.

### The Mirror Duelist
Precision, counters, and prediction. Focus system for perfect timing.

---

## Architecture

The game uses an ECS-Lite architecture:
- **Entities**: Simple integer IDs
- **Components**: Data-only containers
- **Systems**: Logic processors

### Core Systems
- Combat System: Damage, crits, status interactions
- Movement System: Collision detection, pathfinding
- AI System: Utility-based decision making
- Wave System: Enemy spawning, difficulty scaling
- Render System: Terminal buffer, dirty tile rendering

---

## Project Structure

```
turnbound/
├── assets/          # ASCII art, palettes, themes
├── data/            # JSON game content
├── saves/           # Save files
├── src/
│   ├── core/        # Engine core
│   ├── ecs/         # Entity system
│   ├── components/  # Component definitions
│   ├── systems/     # Game systems
│   ├── render/      # Rendering engine
│   ├── animation/   # Visual effects
│   ├── ai/          # AI behaviors
│   ├── generation/  # Procedural generation
│   └── ui/          # User interface
├── tests/           # Automated tests
└── main.py          # Entry point
```

---

## Development

Run tests:
```bash
pytest tests/ -v
```

---

## Requirements

- Python 3.12+
- Textual >= 0.47.0
- Rich >= 13.0.0
- pytest >= 7.0.0

---

## License

MIT License
