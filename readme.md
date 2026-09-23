# 🐾 CSE Project — Virtual Pet Simulator (College Edition)

[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![OOP Concepts](https://img.shields.io/badge/Architecture-Object--Oriented-brightgreen.svg)](#-object-oriented-programming-concepts)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-None%20(Pure%20Standard%20Library)-success.svg)](#-how-to-run)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A feature-rich, text-based **Virtual Pet Simulator** built in Python using **Object-Oriented Programming (OOP)** principles. Designed as a college demonstration project for **B.Tech Computer Science & Engineering**.

---

## 📸 Gameplay & Terminal Outputs

The image below shows real gameplay outputs captured from the terminal, including the Welcome & Adoption menu, Pet Status Dashboard with colorful progress bars, the In-Game Store, and the Dragon Level-Up action:

![CSE Pet Simulator Gameplay Outputs](screenshots.png)

---

## ⚡ Quick Start & How to Run

### System Requirements
- Python 3.6 or newer installed on your computer.
- Compatible with **Linux**, **macOS**, and **Windows**.
- **No external pip packages needed!** This project utilizes only Python's built-in standard library (`json`, `os`, `sys`, `time`).

### Execution Command
Open your terminal or command prompt in this directory and run:

```bash
python3 main.py
```

*(On Windows, you can also run `python main.py`)*

---

## 📁 Clean Project Architecture

The entire project has been consolidated into a clean, unified architecture containing four core files:

```text
CSE project (pet simulator)/
├── main.py            - Complete standalone game executable, OOP classes & database
├── readme.md          - Comprehensive project documentation, viva guide & screenshots
├── statements.md      - Detailed Problem Statement, practical uses & features
└── screenshots.png    - High-resolution visual showcase of gameplay terminal screens
```

> 📄 For the formal Problem Statement, Practical Uses, and Educational Objectives, see [statements.md](file:///home/harsh/Documents/CSE%20project%20%28pet%20simulator%29/statements.md).

---

## 🎮 Core Gameplay & Features

1. **Choose Your Companion:**
   - 🐶 **Dog (Loyal Companion):** Earns **+10 bonus coins** during play sessions. Overrides `speak()` with *"Woof! Woof!"*.
   - 🐱 **Cat (Cozy Napper):** Recovers **+20 extra Energy** from sleeping. Overrides `speak()` with *"Meow~ Purrr..."*.
   - 🐉 **Dragon (Mythical Power):** Earns **+15 bonus EXP** on all developmental activities. Overrides `speak()` with *"ROAAAR! 🔥"*.

2. **Vital Stats Simulation:**
   - **Health, Hunger, Happiness, and Energy** are visually rendered with dynamic, color-coded progress bars.
   - Internal values are safely bounded between `0` and `100` via encapsulation.

3. **In-Game Store & Economy:**
   - Earn coins by playing and leveling up.
   - Buy **Foods** (*Dry Kibble*, *Gourmet Meat*, *Golden Apple*), **Toys** (*Rubber Ball*, *Feather Wand*, *Laser Pointer*), and **Medicines** (*Bandage Roll*, *Health Elixir*, *Miracle Potion*).

4. **Backpack & Item Management:**
   - Stacking inventory system with category-based filtering and instant consumption.

5. **JSON Database Persistence:**
   - Game progress is automatically serialized to `data/pet_save.json`.
   - Players can save, quit, and resume anytime from the Main Menu.

---

## 🧠 Object-Oriented Programming (OOP) Concepts

This project was built to illustrate real-world application of the four pillars of OOP:

| OOP Concept | How & Where It Is Implemented |
|---|---|
| **Classes & Objects** | Defined in `Item`, `Inventory`, `Pet`, `Dog`, `Cat`, `Dragon`, and `Shop`. Objects are instantiated dynamically at runtime. |
| **Inheritance** | `Dog`, `Cat`, and `Dragon` inherit foundational attributes and behavior from the base `Pet` class (`class Dog(Pet)`). |
| **Polymorphism** | Subclasses override `speak()`, `play()`, `sleep()`, and `gain_exp()` to execute species-specific mechanics through unified method signatures. |
| **Encapsulation** | Protected state updates through methods like `clamp()`, ensuring stat boundaries (`0` to `100`) cannot be corrupted. |
| **Data Abstraction** | The `Shop` and `Inventory` classes abstract away underlying data structures, exposing clean, intuitive APIs like `buy_item()` and `use_item()`. |

---

## 🎓 College Viva / Lab Questions & Model Answers

### Q1: Where and why is Inheritance used in this project?
> **Answer:** `Dog`, `Cat`, and `Dragon` inherit from the parent class `Pet` (`class Dog(Pet)`). This eliminates code duplication because common logic (health clamping, hunger decay, inventory association, leveling) is written once in `Pet` and automatically shared by all species.

### Q2: How is Polymorphism demonstrated?
> **Answer:** Polymorphism is demonstrated through method overriding. When `pet.speak()` is invoked, Python dynamically determines the object's class at runtime:
> - A `Dog` object outputs *"Woof! Woof!"*
> - A `Cat` object outputs *"Meow~ Purrr..."*
> - A `Dragon` object outputs *"ROAAAR! 🔥"*
> Similarly, `Dog` overrides `play()` to grant bonus currency, and `Cat` overrides `sleep()` for energy buffs.

### Q3: How does the game save and restore state without an external SQL server?
> **Answer:** State serialization is achieved using Python's built-in `json` module. The `to_dict()` methods convert pet and inventory objects into JSON-compatible dictionaries, which are saved to `data/pet_save.json`. Upon loading, the saved species tag is read to reconstruct the exact subclass (`Dog`, `Cat`, or `Dragon`) with restored stats and backpack items.

### Q4: How is Encapsulation enforced?
> **Answer:** The `clamp()` method bounds stats strictly within `0` and `100`. State modifications (eating, playing, sleeping, healing) pass through clamped calculation methods rather than arbitrary unchecked assignments.

---

## 📜 Author & Project Metadata

- **Course:** B.Tech Computer Science & Engineering
- **Project:** Virtual Pet Simulator
- **Language:** Python 3 (Pure Standard Library)
- **Files Maintained:** [main.py](file:///home/harsh/Documents/CSE%20project%20%28pet%20simulator%29/main.py), [readme.md](file:///home/harsh/Documents/CSE%20project%20%28pet%20simulator%29/readme.md), [statements.md](file:///home/harsh/Documents/CSE%20project%20%28pet%20simulator%29/statements.md), [screenshots.png](file:///home/harsh/Documents/CSE%20project%20%28pet%20simulator%29/screenshots.png)
