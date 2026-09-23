# ==============================================================================
# 🐾 CSE PROJECT - VIRTUAL PET SIMULATOR (COLLEGE EDITION)
# ==============================================================================
# Course: B.Tech Computer Science & Engineering
# Topic : Object-Oriented Programming (OOP) & CLI Simulation
# File  : main.py (Standalone Game Executable & Database Engine)
# Run   : python3 main.py
# ==============================================================================

import json
import os
import sys
import time

# ==============================================================================
# SECTION 1: ANSI COLOR PALETTE & UI FORMATTING CONSTANTS
# ==============================================================================
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

def clear_screen():
    """Clears the terminal screen across Linux, macOS, and Windows."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def pause(prompt_msg="Press Enter to continue..."):
    """Pauses execution until user presses Enter."""
    input("\n" + DIM + prompt_msg + RESET)

def print_header(title):
    """Prints a styled section header."""
    print("\n" + CYAN + BOLD + "=== " + title + " ===" + RESET)

def print_success(msg):
    """Prints a green success message."""
    print(GREEN + "✔ " + msg + RESET)

def print_warning(msg):
    """Prints a yellow warning message."""
    print(YELLOW + "⚠ " + msg + RESET)

def print_error(msg):
    """Prints a red error message."""
    print(RED + "✖ " + msg + RESET)


# ==============================================================================
# SECTION 2: ASCII ART REPOSITORY
# ==============================================================================
BANNER = CYAN + BOLD + """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          🐾  C S E   P E T   S I M U L A T O R  🐾           ║
║              College Edition  •  OOP CLI Game                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""" + RESET

DOG_ART = YELLOW + """
       / \\__
      (    @\\___
      /         O
     /   (_____/
    /_____/   U
""" + RESET

CAT_ART = MAGENTA + """
      |\\__/,|   (`\\
    _.|o o  |_   ) )
  -(((---(((--------
""" + RESET

DRAGON_ART = RED + """
       __  /\\_
      /  \\/   \\
     / /\\_/\\   \\
    / /      \\  |
    \\/  \\  /  \\/
     \\   \\/   /
      \\      /
       '----'
""" + RESET

RIP_ART = RED + """
       ______
    .-"      "-.
   /            \\
  |   R.I.P.    |
  |  Your pet   |
  |  fainted!   |
  |_____________|
""" + RESET

def get_pet_art(species):
    """Returns the ASCII art illustration corresponding to the pet species."""
    if species == "Dog":
        return DOG_ART
    elif species == "Cat":
        return CAT_ART
    elif species == "Dragon":
        return DRAGON_ART
    return ""


# ==============================================================================
# SECTION 3: MAIN PROJECT DATABASE
# ==============================================================================
# Centralized game database containing item catalog, pet species traits,
# and shop inventories.

ITEM_DATABASE = [
    # --- Category: Food (Restores Hunger, grants modest EXP) ---
    {
        "id": "dry_kibble",
        "name": "Dry Kibble",
        "category": "Food",
        "price": 10,
        "boost": 20,
        "description": "Crunchy standard pet food (+20 Hunger)"
    },
    {
        "id": "gourmet_meat",
        "name": "Gourmet Meat",
        "category": "Food",
        "price": 25,
        "boost": 45,
        "description": "Juicy tender steak slice (+45 Hunger)"
    },
    {
        "id": "golden_apple",
        "name": "Golden Apple",
        "category": "Food",
        "price": 50,
        "boost": 80,
        "description": "Rare mystical fruit (+80 Hunger)"
    },

    # --- Category: Toy (Restores Happiness, costs Energy) ---
    {
        "id": "rubber_ball",
        "name": "Rubber Ball",
        "category": "Toy",
        "price": 15,
        "boost": 25,
        "description": "Bouncy colorful ball (+25 Happiness)"
    },
    {
        "id": "feather_wand",
        "name": "Feather Wand",
        "category": "Toy",
        "price": 30,
        "boost": 45,
        "description": "Interactive play wand (+45 Happiness)"
    },
    {
        "id": "laser_pointer",
        "name": "Laser Pointer",
        "category": "Toy",
        "price": 55,
        "boost": 75,
        "description": "High-tech beam chase toy (+75 Happiness)"
    },

    # --- Category: Medicine (Restores Health when injured or sick) ---
    {
        "id": "bandage_roll",
        "name": "Bandage Roll",
        "category": "Medicine",
        "price": 15,
        "boost": 25,
        "description": "Basic first-aid bandage (+25 Health)"
    },
    {
        "id": "health_elixir",
        "name": "Health Elixir",
        "category": "Medicine",
        "price": 35,
        "boost": 50,
        "description": "Fast-acting healing tonic (+50 Health)"
    },
    {
        "id": "miracle_potion",
        "name": "Miracle Potion",
        "category": "Medicine",
        "price": 70,
        "boost": 90,
        "description": "Legendary cure-all potion (+90 Health)"
    }
]

PET_SPECIES_DATABASE = {
    "Dog": {
        "species": "Dog",
        "perk_title": "Loyal Companion",
        "perk_description": "Earns +10 bonus coins during playtime.",
        "sound": "Woof! Woof! 🐶",
        "color": YELLOW
    },
    "Cat": {
        "species": "Cat",
        "perk_title": "Cozy Napper",
        "perk_description": "Recovers +20 extra Energy from sleeping.",
        "sound": "Meow~ Purrr... 🐱",
        "color": MAGENTA
    },
    "Dragon": {
        "species": "Dragon",
        "perk_title": "Mythical Power",
        "perk_description": "Earns +15 bonus EXP on every leveling action.",
        "sound": "ROAAAR! 🔥🐉",
        "color": RED
    }
}


# ==============================================================================
# SECTION 4: OBJECT-ORIENTED PROGRAMMING CORE CLASSES
# ==============================================================================

class Item:
    """
    Represents an in-game consumable or usable item.
    Encapsulates name, category, price, stat boost value, and description.
    """
    def __init__(self, name, category, price, boost, description):
        self.name = name
        self.category = category   # "Food", "Toy", or "Medicine"
        self.price = price
        self.boost = boost         # Value added to the respective stat
        self.description = description

    def to_dict(self):
        """Serializes the item instance into a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "boost": self.boost,
            "description": self.description
        }

    @staticmethod
    def from_dict(data):
        """Factory method to reconstruct an Item instance from a dictionary."""
        return Item(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            boost=data["boost"],
            description=data["description"]
        )


class Inventory:
    """
    Manages the pet's backpack and item storage.
    Supports item stacking, item removal, category filtering, and serialization.
    """
    def __init__(self):
        # Stored as a list of dicts: [{"item": Item, "qty": int}]
        self.slots = []

    def add_item(self, item, qty=1):
        """Adds an item to the inventory. Stacks quantity if item already exists."""
        for slot in self.slots:
            if slot["item"].name.lower() == item.name.lower():
                slot["qty"] += qty
                return
        self.slots.append({"item": item, "qty": qty})

    def remove_item(self, item_name):
        """Removes 1 unit of an item. Pops slot when quantity hits 0."""
        for i, slot in enumerate(self.slots):
            if slot["item"].name.lower() == item_name.lower():
                slot["qty"] -= 1
                if slot["qty"] <= 0:
                    self.slots.pop(i)
                return True
        return False

    def get_items_by_category(self, category):
        """Returns all inventory slots matching the given category."""
        return [slot for slot in self.slots if slot["item"].category.lower() == category.lower()]

    def is_empty(self):
        """Returns True if the inventory contains no items."""
        return len(self.slots) == 0

    def use_item(self, item_name, pet):
        """Applies an item's stat boost to the pet and decrements inventory quantity."""
        found_item = None
        for slot in self.slots:
            if slot["item"].name.lower() == item_name.lower():
                found_item = slot["item"]
                break

        if found_item is None:
            return {"success": False, "message": "Item not found in inventory!"}

        if found_item.category == "Food":
            result = pet.feed(boost=found_item.boost)
        elif found_item.category == "Toy":
            result = pet.play(boost=found_item.boost)
        elif found_item.category == "Medicine":
            result = pet.heal(boost=found_item.boost)
        else:
            return {"success": False, "message": "Unknown item category!"}

        if result["success"]:
            self.remove_item(found_item.name)
            result["item_used"] = found_item.name

        return result

    def to_dict(self):
        """Serializes inventory slots into a list of dictionaries for JSON saving."""
        return [{"item": slot["item"].to_dict(), "qty": slot["qty"]} for slot in self.slots]

    def load_from_list(self, data_list):
        """Restores inventory slots from a serialized list."""
        self.slots = []
        for entry in data_list:
            item = Item.from_dict(entry["item"])
            self.slots.append({"item": item, "qty": entry["qty"]})


class Pet:
    """
    Base Class for all virtual pets.
    Demonstrates Encapsulation (stat clamping) and provides baseline behaviors.
    """
    def __init__(self, name, species="Pet"):
        self.name = name
        self.species = species

        # Primary Stats (bounded 0 to 100)
        self.health = 100
        self.hunger = 80
        self.happiness = 80
        self.energy = 80

        # Progression & Economy
        self.level = 1
        self.exp = 0
        self.coins = 50

        # Dedicated Inventory
        self.inventory = Inventory()

    def clamp(self, value):
        """Encapsulation: guarantees stat attributes remain in [0, 100] range."""
        return max(0, min(100, value))

    def is_alive(self):
        """Checks if the pet has remaining health and hunger."""
        return self.health > 0 and self.hunger > 0

    def gain_exp(self, amount):
        """Awards experience points and handles level-up thresholds."""
        self.exp += amount
        leveled_up = False
        while self.exp >= 100:
            self.exp -= 100
            self.level += 1
            leveled_up = True
            # Level-up rewards
            self.health = self.clamp(self.health + 10)
            self.energy = self.clamp(self.energy + 10)
            self.coins += 25
        return leveled_up

    def feed(self, boost=25):
        """Feeds the pet to reduce hunger."""
        if self.hunger >= 100:
            return {"success": False, "message": self.name + " is completely full!"}
        old_val = self.hunger
        self.hunger = self.clamp(self.hunger + boost)
        gained = self.hunger - old_val
        leveled_up = self.gain_exp(10)
        return {
            "success": True,
            "leveled_up": leveled_up,
            "message": self.name + " enjoyed the food! (+" + str(gained) + " Hunger, +10 EXP)"
        }

    def play(self, boost=25):
        """Plays with the pet, trading energy for happiness and coins."""
        if self.energy < 15:
            return {"success": False, "message": self.name + " is too exhausted to play!"}
        old_val = self.happiness
        self.happiness = self.clamp(self.happiness + boost)
        self.energy = self.clamp(self.energy - 20)
        self.hunger = self.clamp(self.hunger - 10)
        self.coins += 15
        leveled_up = self.gain_exp(20)
        gained = self.happiness - old_val
        return {
            "success": True,
            "leveled_up": leveled_up,
            "message": self.name + " played happily! (+" + str(gained) + " Happiness, +15 Coins, +20 EXP)"
        }

    def sleep(self):
        """Puts the pet to sleep to recover energy."""
        if self.energy >= 100:
            return {"success": False, "message": self.name + " is already fully energetic!"}
        old_val = self.energy
        self.energy = self.clamp(self.energy + 40)
        self.hunger = self.clamp(self.hunger - 15)
        gained = self.energy - old_val
        return {
            "success": True,
            "message": self.name + " had a refreshing sleep! (+" + str(gained) + " Energy)"
        }

    def heal(self, boost=30):
        """Treats the pet with medicine to restore health."""
        if self.health >= 100:
            return {"success": False, "message": self.name + " is in peak health!"}
        old_val = self.health
        self.health = self.clamp(self.health + boost)
        gained = self.health - old_val
        return {
            "success": True,
            "message": self.name + " took medicine and recovered! (+" + str(gained) + " Health)"
        }

    def speak(self):
        """Polymorphism placeholder: overridden in child classes."""
        return "..."

    def to_dict(self):
        """Converts complete pet state to a serializable dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "health": self.health,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "level": self.level,
            "exp": self.exp,
            "coins": self.coins,
            "inventory": self.inventory.to_dict()
        }


# ==============================================================================
# SECTION 5: INHERITANCE & POLYMORPHISM (CHILD PET CLASSES)
# ==============================================================================

class Dog(Pet):
    """
    Child class inheriting from Pet.
    Polymorphic override of speak() and play() with canine loyalty perk.
    """
    def __init__(self, name):
        super().__init__(name, species="Dog")

    def speak(self):
        return "Woof! Woof! 🐶"

    def play(self, boost=25):
        result = super().play(boost=boost)
        if result["success"]:
            # Dog Perk: +10 bonus coins for loyal companionship
            self.coins += 10
            result["message"] += " (Loyal Dog Bonus: +10 Coins!)"
        return result


class Cat(Pet):
    """
    Child class inheriting from Pet.
    Polymorphic override of speak() and sleep() with feline cozy napper perk.
    """
    def __init__(self, name):
        super().__init__(name, species="Cat")

    def speak(self):
        return "Meow~ Purrr... 🐱"

    def sleep(self):
        result = super().sleep()
        if result["success"]:
            # Cat Perk: +20 extra energy from deep catnaps
            old_energy = self.energy
            self.energy = self.clamp(self.energy + 20)
            gained = self.energy - old_energy
            result["message"] += " (Catnap Perk: +" + str(gained) + " Extra Energy!)"
        return result


class Dragon(Pet):
    """
    Child class inheriting from Pet.
    Polymorphic override of speak() and gain_exp() with mythical power perk.
    """
    def __init__(self, name):
        super().__init__(name, species="Dragon")

    def speak(self):
        return "ROAAAR! 🔥🐉"

    def gain_exp(self, amount):
        # Dragon Perk: +15 bonus EXP on every progression gain
        return super().gain_exp(amount + 15)


# ==============================================================================
# SECTION 6: IN-GAME SHOP SYSTEM
# ==============================================================================

class Shop:
    """
    In-game store engine populated directly from the main ITEM_DATABASE.
    Handles purchasing transactions, currency deduction, and inventory delivery.
    """
    def __init__(self):
        self.catalog = [Item.from_dict(item_data) for item_data in ITEM_DATABASE]

    def get_item_by_number(self, number):
        """Retrieves an item from catalog by 1-indexed number."""
        index = number - 1
        if 0 <= index < len(self.catalog):
            return self.catalog[index]
        return None

    def buy_item(self, pet, item_name):
        """Attempts to purchase an item for the pet."""
        selected = None
        for item in self.catalog:
            if item.name.lower() == item_name.lower():
                selected = item
                break

        if selected is None:
            return {"success": False, "message": "Item not found in store catalog!"}

        if pet.coins < selected.price:
            return {
                "success": False,
                "message": "Not enough coins! " + selected.name + " costs " + str(selected.price) + " coins (You have: " + str(pet.coins) + ")."
            }

        pet.coins -= selected.price
        pet.inventory.add_item(selected, 1)
        return {
            "success": True,
            "message": "Successfully purchased " + selected.name + " for " + str(selected.price) + " coins! (Balance: " + str(pet.coins) + " coins)"
        }


# ==============================================================================
# SECTION 7: DATABASE PERSISTENCE & SAVE MANAGER
# ==============================================================================

SAVE_DIR = ".data"
SAVE_FILE = os.path.join(SAVE_DIR, "pet_save.json")
FALLBACK_SAVE_FILE = os.path.join("data", "pet_save.json")

def get_active_save_file():
    """Returns the active save file path (.data or data)."""
    if os.path.exists(SAVE_FILE):
        return SAVE_FILE
    if os.path.exists(FALLBACK_SAVE_FILE):
        return FALLBACK_SAVE_FILE
    return SAVE_FILE

def save_game(pet):
    """Saves the pet's full state to the JSON database."""
    try:
        active_file = get_active_save_file()
        save_dir = os.path.dirname(active_file)
        os.makedirs(save_dir, exist_ok=True)
        with open(active_file, "w", encoding="utf-8") as f:
            json.dump(pet.to_dict(), f, indent=4)
        return True
    except Exception as e:
        print_error("Failed to save game data: " + str(e))
        return False

def load_game():
    """Loads pet state from JSON database and reconstructs the correct subclass."""
    try:
        active_file = get_active_save_file()
        if not os.path.exists(active_file):
            return None
        with open(active_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        name = data["name"]
        species = data["species"]

        # Polymorphic instantiation based on saved species tag
        if species == "Dog":
            pet = Dog(name)
        elif species == "Cat":
            pet = Cat(name)
        elif species == "Dragon":
            pet = Dragon(name)
        else:
            pet = Pet(name, species)

        # Restore vital stats
        pet.health = data.get("health", 100)
        pet.hunger = data.get("hunger", 80)
        pet.happiness = data.get("happiness", 80)
        pet.energy = data.get("energy", 80)
        pet.level = data.get("level", 1)
        pet.exp = data.get("exp", 0)
        pet.coins = data.get("coins", 50)

        # Restore inventory backpack
        pet.inventory.load_from_list(data.get("inventory", []))
        return pet
    except Exception as e:
        print_error("Failed to load game data: " + str(e))
        return None

def has_save():
    """Returns True if a valid save database file exists on disk."""
    active_file = get_active_save_file()
    return os.path.exists(active_file)

def delete_save():
    """Deletes existing save game data file."""
    active_file = get_active_save_file()
    if os.path.exists(active_file):
        os.remove(active_file)
        return True
    return False
    return os.path.exists(SAVE_FILE)

def delete_save():
    """Deletes existing save game data file."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        return True
    return False


# ==============================================================================
# SECTION 8: STATUS DISPLAY & PROGRESS BAR ENGINE
# ==============================================================================

def render_bar(label, value, max_val=100, bar_length=15):
    """Renders a colorful visual progress bar."""
    ratio = max(0.0, min(1.0, value / max_val))
    filled_len = int(bar_length * ratio)
    empty_len = bar_length - filled_len
    bar_str = "█" * filled_len + "░" * empty_len

    if ratio > 0.6:
        color = GREEN
    elif ratio > 0.3:
        color = YELLOW
    else:
        color = RED

    label_str = (label + ":").ljust(12)
    val_str = (str(int(value)) + "/" + str(max_val)).rjust(8)
    return label_str + " [" + color + bar_str + RESET + "] " + val_str

def show_status(pet):
    """Displays the comprehensive pet status card."""
    art = get_pet_art(pet.species)
    if art:
        print(art)

    species_info = PET_SPECIES_DATABASE.get(pet.species, {})
    color = species_info.get("color", WHITE)

    print(color + BOLD + "🐾 " + pet.name.upper() + " THE " + pet.species.upper() + RESET +
          DIM + " (" + pet.speak() + ")" + RESET)
    print("─" * 46)
    print(render_bar("Health", pet.health))
    print(render_bar("Hunger", pet.hunger))
    print(render_bar("Happiness", pet.happiness))
    print(render_bar("Energy", pet.energy))
    print("─" * 46)
    print("Level: " + BOLD + str(pet.level) + RESET + "  |  " +
          "EXP: " + CYAN + str(pet.exp) + "/100" + RESET + "  |  " +
          "Coins: " + YELLOW + BOLD + str(pet.coins) + " 🪙" + RESET)
    print("─" * 46 + "\n")


# ==============================================================================
# SECTION 9: USER ACTION HANDLERS & MENUS
# ==============================================================================

def create_pet():
    """Guides the user through adopting and naming a new pet."""
    clear_screen()
    print(BANNER)
    print_header("Adopt a New Pet")

    print("\n" + BOLD + "Available Pet Companions:" + RESET)
    for key, info in PET_SPECIES_DATABASE.items():
        print("  " + info["color"] + "[" + str(list(PET_SPECIES_DATABASE.keys()).index(key) + 1) + "] " +
              info["species"].ljust(7) + RESET + " - " + info["perk_title"] + ": " + info["perk_description"])

    choice = ""
    species_list = list(PET_SPECIES_DATABASE.keys())
    while choice not in ["1", "2", "3"]:
        choice = input("\n" + BOLD + "Pick a species (1-3): " + RESET).strip()
        if choice not in ["1", "2", "3"]:
            print_error("Please enter 1, 2, or 3.")

    name = ""
    while not name:
        name = input(BOLD + "Name your pet: " + RESET).strip()
        if not name:
            print_error("Name cannot be empty!")

    selected_species = species_list[int(choice) - 1]
    if selected_species == "Dog":
        pet = Dog(name)
    elif selected_species == "Cat":
        pet = Cat(name)
    else:
        pet = Dragon(name)

    # Starter Kit from Database
    kibble = Item.from_dict(ITEM_DATABASE[0])
    ball = Item.from_dict(ITEM_DATABASE[3])
    pet.inventory.add_item(kibble, 2)
    pet.inventory.add_item(ball, 1)

    print_success("You officially adopted " + pet.name + " the " + pet.species + "!")
    print(CYAN + "Starter Care Kit: 2x Dry Kibble, 1x Rubber Ball, and 50 Coins granted." + RESET)
    save_game(pet)
    pause()
    return pet

def handle_feed(pet):
    """Feeds the pet using food from the inventory."""
    print_header("Feed " + pet.name)
    if pet.hunger >= 100:
        print_warning(pet.name + " is completely full!")
        return

    food_items = pet.inventory.get_items_by_category("Food")
    if not food_items:
        print_warning("No food items in your backpack!")
        print(CYAN + "Tip: Visit the Pet Care Store to buy tasty meals." + RESET)
        return

    print("\n" + BOLD + "Available Food:" + RESET)
    for i, slot in enumerate(food_items):
        item = slot["item"]
        qty = slot["qty"]
        print("  [" + str(i + 1) + "] " + item.name + " (x" + str(qty) + ") - " + item.description)
    print("  [0] Cancel")

    choice = input("\n" + BOLD + "Choose food (0-" + str(len(food_items)) + "): " + RESET).strip()
    if choice == "0" or not choice.isdigit():
        return

    index = int(choice) - 1
    if 0 <= index < len(food_items):
        item_name = food_items[index]["item"].name
        result = pet.inventory.use_item(item_name, pet)
        if result["success"]:
            print_success(result["message"])
            if result.get("leveled_up"):
                print_success("🎉 LEVEL UP! " + pet.name + " advanced to Level " + str(pet.level) + "!")
        else:
            print_warning(result["message"])
    else:
        print_error("Invalid selection.")

def handle_play(pet):
    """Engages the pet in play activities with or without toys."""
    print_header("Play with " + pet.name)
    toy_items = pet.inventory.get_items_by_category("Toy")

    print("  [1] Quick Free Play (costs 20 Energy)")
    if toy_items:
        print("  [2] Play with a Toy from Backpack")
    print("  [0] Cancel")

    choice = input("\n" + BOLD + "Choose option: " + RESET).strip()
    if choice == "1":
        result = pet.play()
        if result["success"]:
            print_success(result["message"])
            if result.get("leveled_up"):
                print_success("🎉 LEVEL UP! " + pet.name + " reached Level " + str(pet.level) + "!")
        else:
            print_warning(result["message"])
    elif choice == "2" and toy_items:
        print("\n" + BOLD + "Your Toys:" + RESET)
        for i, slot in enumerate(toy_items):
            item = slot["item"]
            qty = slot["qty"]
            print("  [" + str(i + 1) + "] " + item.name + " (x" + str(qty) + ") - " + item.description)

        pick = input("\n" + BOLD + "Choose toy (1-" + str(len(toy_items)) + "): " + RESET).strip()
        if pick.isdigit() and 1 <= int(pick) <= len(toy_items):
            item_name = toy_items[int(pick) - 1]["item"].name
            result = pet.inventory.use_item(item_name, pet)
            if result["success"]:
                print_success(result["message"])
                if result.get("leveled_up"):
                    print_success("🎉 LEVEL UP! " + pet.name + " reached Level " + str(pet.level) + "!")
            else:
                print_warning(result["message"])
        else:
            print_error("Invalid selection.")

def handle_sleep(pet):
    """Puts pet to sleep to regenerate energy."""
    print_header("Nap Time for " + pet.name)
    result = pet.sleep()
    if result["success"]:
        print_success(result["message"])
    else:
        print_warning(result["message"])

def handle_heal(pet):
    """Treats pet injuries and restores health using medicine."""
    print_header("Heal " + pet.name)
    if pet.health >= 100:
        print_warning(pet.name + " is already in perfect health!")
        return

    med_items = pet.inventory.get_items_by_category("Medicine")
    if not med_items:
        print_warning("No medicine available in your backpack!")
        print(CYAN + "Tip: Visit the Pet Care Store to purchase Bandages or Potions." + RESET)
        return

    print("\n" + BOLD + "Available Medicine:" + RESET)
    for i, slot in enumerate(med_items):
        item = slot["item"]
        qty = slot["qty"]
        print("  [" + str(i + 1) + "] " + item.name + " (x" + str(qty) + ") - " + item.description)
    print("  [0] Cancel")

    choice = input("\n" + BOLD + "Choose medicine (0-" + str(len(med_items)) + "): " + RESET).strip()
    if choice == "0" or not choice.isdigit():
        return

    index = int(choice) - 1
    if 0 <= index < len(med_items):
        item_name = med_items[index]["item"].name
        result = pet.inventory.use_item(item_name, pet)
        if result["success"]:
            print_success(result["message"])
        else:
            print_warning(result["message"])
    else:
        print_error("Invalid selection.")

def handle_shop(pet, shop):
    """Interactive shopping interface for buying catalog items."""
    while True:
        clear_screen()
        print_header("Pet Care Store")
        print("Your Coins: " + YELLOW + BOLD + str(pet.coins) + " 🪙" + RESET + "\n")

        print("No.  Item             Type       Price    Effect")
        print("─" * 58)
        for i, item in enumerate(shop.catalog):
            num = str(i + 1).ljust(4)
            name = item.name.ljust(17)
            cat = item.category.ljust(10)
            price = (str(item.price) + " coins").ljust(9)
            print(num + name + cat + price + item.description)
        print("─" * 58)
        print(" [0] Exit Store\n")

        choice = input(BOLD + "Enter item number to buy (0-" + str(len(shop.catalog)) + "): " + RESET).strip()
        if choice == "0":
            break

        if choice.isdigit() and 1 <= int(choice) <= len(shop.catalog):
            item = shop.catalog[int(choice) - 1]
            result = shop.buy_item(pet, item.name)
            if result["success"]:
                print_success(result["message"])
            else:
                print_error(result["message"])
            pause()
        else:
            print_error("Invalid selection.")
            pause()

def handle_inventory(pet):
    """Displays the pet's backpack and allows using items directly."""
    clear_screen()
    print_header(pet.name + "'s Backpack")

    if pet.inventory.is_empty():
        print_warning("Your backpack is completely empty! Visit the store to stock up.")
        pause()
        return

    print("\nNo.  Item             Category   Qty   Description")
    print("─" * 58)
    for i, slot in enumerate(pet.inventory.slots):
        item = slot["item"]
        qty = slot["qty"]
        num = str(i + 1).ljust(4)
        name = item.name.ljust(17)
        cat = item.category.ljust(10)
        q = str(qty).ljust(5)
        print(num + name + cat + q + item.description)
    print("─" * 58)
    print(" [0] Return to Main Game\n")

    choice = input(BOLD + "Enter item number to use (or 0 to return): " + RESET).strip()
    if choice == "0" or not choice.isdigit():
        return

    index = int(choice) - 1
    if 0 <= index < len(pet.inventory.slots):
        item_name = pet.inventory.slots[index]["item"].name
        result = pet.inventory.use_item(item_name, pet)
        if result["success"]:
            print_success(result["message"])
            if result.get("leveled_up"):
                print_success("🎉 LEVEL UP! " + pet.name + " advanced to Level " + str(pet.level) + "!")
        else:
            print_warning(result["message"])
        pause()
    else:
        print_error("Invalid selection.")
        pause()


# ==============================================================================
# SECTION 10: MAIN GAME LOOP & ENTRY POINT
# ==============================================================================

def game_loop(pet):
    """Core interactive loop processing player choices."""
    shop = Shop()

    while True:
        clear_screen()
        show_status(pet)

        # Faint state evaluation
        if not pet.is_alive():
            print(RIP_ART)
            print_error(pet.name + " has fainted due to exhaustion or starvation!")
            print("  [1] Revive " + pet.name + " (restores 50 Health & Hunger)")
            print("  [2] Adopt a brand new pet")
            print("  [3] Exit to Main Menu")

            choice = input("\n" + BOLD + "Choose option (1-3): " + RESET).strip()
            if choice == "1":
                pet.health = 50
                pet.hunger = 50
                save_game(pet)
                print_success(pet.name + " has been lovingly revived!")
                pause()
                continue
            elif choice == "2":
                pet = create_pet()
                continue
            else:
                break

        print(BOLD + "What would you like to do?" + RESET)
        print("  " + CYAN + "[1]" + RESET + " Feed " + pet.name + " 🍖")
        print("  " + CYAN + "[2]" + RESET + " Play with " + pet.name + " 🎾")
        print("  " + CYAN + "[3]" + RESET + " Put " + pet.name + " to Sleep 💤")
        print("  " + CYAN + "[4]" + RESET + " Heal " + pet.name + " 💊")
        print("  " + CYAN + "[5]" + RESET + " Visit Pet Care Store 🏬")
        print("  " + CYAN + "[6]" + RESET + " Open Backpack 🎒")
        print("  " + CYAN + "[7]" + RESET + " Save Game 💾")
        print("  " + CYAN + "[8]" + RESET + " Save & Exit 🚪")

        action = input("\n" + BOLD + "Enter choice (1-8): " + RESET).strip()

        if action == "1":
            handle_feed(pet)
            save_game(pet)
            pause()
        elif action == "2":
            handle_play(pet)
            save_game(pet)
            pause()
        elif action == "3":
            handle_sleep(pet)
            save_game(pet)
            pause()
        elif action == "4":
            handle_heal(pet)
            save_game(pet)
            pause()
        elif action == "5":
            handle_shop(pet, shop)
            save_game(pet)
        elif action == "6":
            handle_inventory(pet)
            save_game(pet)
        elif action == "7":
            if save_game(pet):
                print_success("Game progress successfully saved!")
            else:
                print_error("Failed to save progress.")
            pause()
        elif action == "8":
            save_game(pet)
            print_success("Game saved! Until next time, take care of " + pet.name + "! 👋")
            break
        else:
            print_error("Invalid selection. Please choose 1 through 8.")
            pause()

def main():
    """Application starting point rendering main menu."""
    try:
        while True:
            clear_screen()
            print(BANNER)
            print_header("Main Menu")
            print("  " + GREEN + "[1] New Game" + RESET)
            if has_save():
                print("  " + YELLOW + "[2] Continue Saved Game" + RESET)
            else:
                print("  " + DIM + "[2] Continue (no save file found)" + RESET)
            print("  " + RED + "[3] Exit" + RESET)

            choice = input("\n" + BOLD + "Choose option (1-3): " + RESET).strip()

            if choice == "1":
                pet = create_pet()
                game_loop(pet)
            elif choice == "2":
                if has_save():
                    pet = load_game()
                    if pet is not None:
                        print_success("Loaded " + pet.name + " the " + pet.species + "!")
                        pause("Press Enter to begin playing...")
                        game_loop(pet)
                    else:
                        print_error("Unable to read saved game data.")
                        pause()
                else:
                    print_warning("No existing save file found. Please start a New Game!")
                    pause()
            elif choice == "3":
                print("\n" + GREEN + "Thank you for playing CSE Pet Simulator! Goodbye! 👋" + RESET + "\n")
                sys.exit(0)
            else:
                print_error("Please enter a valid choice (1-3).")
                pause()

    except KeyboardInterrupt:
        print("\n\n" + YELLOW + "Game terminated gracefully. Goodbye!" + RESET + "\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
