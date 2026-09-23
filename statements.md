# 📋 Problem Statement, Uses & Features Specification

**Project Title:** CLI Virtual Pet Simulator (College Edition)  
**Academic Program:** B.Tech Computer Science & Engineering  
**Core Subject:** Object-Oriented Programming (OOP) in Python  

---

## 1. 🎯 Problem Statement

### 1.1 Academic Context & Motivation
Object-Oriented Programming (OOP) is one of the most fundamental paradigms taught in Computer Science & Engineering. However, introductory coursework often relies on overly abstract, dry examples (such as generic `Vehicle -> Car` or `Shape -> Circle` hierarchies) that do not adequately showcase:
1. **Real-world State Management:** How an object's internal state evolves over time in response to external events.
2. **Data Persistence:** How runtime objects can be serialized, saved to disk, and accurately reconstructed across different application sessions.
3. **User Interaction & Error Handling:** How a system gracefully handles invalid inputs, state transitions, and edge cases.

### 1.2 The Core Problem
To bridge this gap between theory and practical software engineering, there was a need to design and implement a **lightweight, dependency-free, interactive terminal simulation** that models a living entity. The system needed to:
- Model multiple pet species with shared behaviors and distinctive traits using **Inheritance** and **Polymorphism**.
- Enforce strict state invariants (e.g., stats never exceeding 100 or falling below 0) through **Encapsulation**.
- Maintain an in-game economy with shop catalogs, inventory management, and leveling progression.
- Provide a clean, robust **JSON-based database persistence layer** without requiring bulky database servers (such as MySQL or PostgreSQL).
- Present an intuitive, visually appealing Command-Line Interface (CLI) utilizing dynamic ANSI progress bars and ASCII art.

---

## 2. 💡 Practical Uses & Applications

This project serves several educational and practical functions:

### 2.1 Educational Tool for OOP Paradigms
- **Visualizing Inheritance:** Students see how subclasses (`Dog`, `Cat`, `Dragon`) inherit foundational properties from the base `Pet` class while adding specialized perks.
- **Hands-on Polymorphism:** Demonstrates method overriding in practice (`speak()`, `play()`, `sleep()`, and `gain_exp()`), showing how identical method calls produce distinct behaviors depending on object type.
- **Enforcing Encapsulation:** Illustrates data hiding and boundary validation using helper methods like `clamp()`.

### 2.2 Academic Evaluation & Viva Demonstration
- Perfect for laboratory practical exams, semester viva evaluations, and portfolio presentations.
- Demonstrates clean code organization, PEP 8 compliance, and comprehensive inline documentation.

### 2.3 Game Development Foundations
- Explains core gameplay loops, tick-based stat consumption, resource economies, and backpack/inventory systems.
- Demonstrates modular database catalogs for items (foods, toys, medicines) and species configurations.

### 2.4 Zero-Dependency Distribution
- Runs anywhere Python 3 is installed across Linux, Windows, and macOS without requiring `pip install` or external internet connectivity.

---

## 3. 🚀 Comprehensive Features Offered

### 🐾 3.1 Diverse Pet Companions & Species Perks
Players can adopt from three distinct companion archetypes, each with custom ASCII artwork, dialogue sounds, and mechanical gameplay perks:
- **🐶 Dog (The Loyal Companion):** Overrides `speak()` with *"Woof! Woof!"* and provides a **+10 bonus coin reward** during playtime.
- **🐱 Cat (The Cozy Napper):** Overrides `speak()` with *"Meow~ Purrr..."* and gains **+20 extra Energy** whenever taking a nap.
- **🐉 Dragon (The Mythical Powerhouse):** Overrides `speak()` with *"ROAAAR! 🔥"* and earns **+15 bonus EXP** on all developmental activities.

### 📊 3.2 Dynamic Vital Stat Engine & Encapsulation
- **Health (0 - 100):** Depleted by neglect or sickness; restored using medical supplies.
- **Hunger (0 - 100):** Depleted by activities; replenished with food from the inventory.
- **Happiness (0 - 100):** Increased by playing and using toys; drained over time.
- **Energy (0 - 100):** Spent on playtime and training; regenerated through sleep.
- **Clamping Safety:** All stats are automatically clamped between `0` and `100`, eliminating overflow or underflow bugs.

### 🌟 3.3 Experience, Leveling & Virtual Economy
- **Leveling System:** Actions generate Experience Points (EXP). Reaching 100 EXP triggers a **Level Up**, boosting max stats, restoring health/energy, and awarding bonus coins.
- **Virtual Coin Currency:** Earn coins by playing and leveling up. Coins are spent in the Pet Care Store.

### 🏬 3.4 In-Game Pet Care Store & Database Catalog
Centralized item catalog structured across three essential categories:
1. **Food Items:** *Dry Kibble* (+20 Hunger), *Gourmet Meat* (+45 Hunger), *Golden Apple* (+80 Hunger).
2. **Toy Items:** *Rubber Ball* (+25 Happiness), *Feather Wand* (+45 Happiness), *Laser Pointer* (+75 Happiness).
3. **Medical Supplies:** *Bandage Roll* (+25 Health), *Health Elixir* (+50 Health), *Miracle Potion* (+90 Health).

### 🎒 3.5 Backpack & Inventory Management System
- **Slot-Based Stacking:** Identical items automatically stack quantities rather than consuming multiple inventory slots.
- **Category Filtering:** Easily filter and browse items by "Food", "Toy", or "Medicine".
- **Direct Consumption:** Players can use items directly from the backpack menu or via context-sensitive action menus.

### 💾 3.6 JSON Database Persistence & Save Engine
- Complete game state serialization to `data/pet_save.json`.
- Automatic directory creation and atomic file writes.
- Polymorphic deserialization: accurately reconstructs the exact subclass (`Dog`, `Cat`, or `Dragon`) with full inventory state restored.
- Resume capability directly from the Main Menu.

### 🎨 3.7 Terminal User Interface (TUI)
- **ASCII Art Gallery:** Custom banner and pet illustrations for all three species, plus a revival/faint screen.
- **Dynamic Progress Bars:** Color-coded status bars (Green for healthy `>60%`, Yellow for caution `>30%`, Red for critical `<30%`).
- **Cross-Platform Clear Screen:** Flawless terminal clearing on Windows (`cls`) and Linux/macOS (`clear`).

### 🛡️ 3.8 Robust Error Handling & Graceful Exit
- Sanitized input validation on all numbered menus.
- Keyboard interrupt (`Ctrl+C`) intercepted gracefully without unhandled tracebacks.

---

## 4. ⚙️ Technical Specifications

| Specification | Detail |
|---|---|
| **Programming Language** | Python 3 (3.6+) |
| **Dependencies** | None (100% Python Standard Library: `json`, `os`, `sys`, `time`) |
| **Persistence Format** | JSON (JavaScript Object Notation) |
| **Supported Operating Systems** | Linux, macOS, Windows |
| **Architecture** | Object-Oriented Programming (OOP) with MVC-inspired separation |
| **Executable Entry Point** | `python3 main.py` |
