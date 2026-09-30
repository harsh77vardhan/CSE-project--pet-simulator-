# CSE Project - Virtual Pet Simulator (College Edition)
# Shows: classes, inheritance, polymorphism, JSON save/load
# Run with: python3 main.py
import json, os

RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"  # ANSI codes for terminal styling
RED, GREEN, YELLOW, CYAN, MAGENTA = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[95m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause(prompt_msg="Press Enter to continue..."):
    input(f"\n{DIM}{prompt_msg}{RESET}")

def print_header(title_text):
    print(f"\n{CYAN}{BOLD}=== {title_text} ==={RESET}")

def print_success(message):
    print(f"{GREEN}✔ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    print(f"{RED}✖ {message}{RESET}")

BANNER = f"{CYAN}{BOLD}╔═══════════════════════════════════════════════════════════════╗\n║          🐾  C S E   P E T   S I M U L A T O R  🐾           ║\n║              College Edition  •  OOP CLI Game                 ║\n╚═══════════════════════════════════════════════════════════════╝{RESET}"

PET_ART = {
    "Dog": f"{YELLOW}\n       / \\__\n      (    @\\___\n      /         O\n     /   (_____/\n    /_____/   U{RESET}",
    "Cat": f"{MAGENTA}\n      |\\__/,|   (`\\\n    _.|o o  |_   ) )\n  -(((---(((--------{RESET}",
    "Dragon": f"{RED}\n       __  /\\_\n      /  \\/   \\\n     / /\\_/\\   \\\n    / /      \\  |\n    \\/  \\  /  \\/\n     \\   \\/   /\n      \\      /\n       '----'{RESET}",
    "RIP": f"{RED}\n       ______\n    .-\"      \"-.\n   /            \\\n  |   R.I.P.    |\n  |  Your pet   |\n  |  fainted!   |\n  |_____________|{RESET}"}

PET_SPECIES_INFO = {
    "Dog":    {"title": "Loyal Companion", "desc": "Earns +10 bonus coins during playtime.",        "color": YELLOW},
    "Cat":    {"title": "Cozy Napper",     "desc": "Recovers +20 extra Energy from sleeping.",      "color": MAGENTA},
    "Dragon": {"title": "Mythical Power",  "desc": "Earns +15 bonus EXP on every leveling action.", "color": RED}}

ITEM_DATABASE = [  # shop items: (name, category, price, boost, description)
    {"name": item_name, "category": item_cat, "price": item_price, "boost": item_boost, "description": item_desc}
    for item_name, item_cat, item_price, item_boost, item_desc in [
        ("Dry Kibble",     "Food",     10, 20, "Crunchy pet food (+20 Hunger)"),
        ("Gourmet Meat",   "Food",     25, 45, "Juicy steak (+45 Hunger)"),
        ("Golden Apple",   "Food",     50, 80, "Rare fruit (+80 Hunger)"),
        ("Rubber Ball",    "Toy",      15, 25, "Bouncy ball (+25 Happy)"),
        ("Feather Wand",   "Toy",      30, 45, "Play wand (+45 Happy)"),
        ("Laser Pointer",  "Toy",      55, 75, "Beam toy (+75 Happy)"),
        ("Bandage Roll",   "Medicine", 15, 25, "First-aid (+25 Health)"),
        ("Health Elixir",  "Medicine", 35, 50, "Fast tonic (+50 Health)"),
        ("Miracle Potion", "Medicine", 70, 90, "Cure-all (+90 Health)")]]

class Item:
    def __init__(self, name, category, price, boost, description):
        self.name, self.category, self.price, self.boost, self.description = name, category, price, boost, description

    def to_dict(self):
        return vars(self)  # needed for the JSON save

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

class Inventory:
    def __init__(self):
        self.slots = []  # each slot is {"item": Item, "qty": int}

    def add_item(self, item, qty=1):
        existing_slot = next((slot for slot in self.slots if slot["item"].name.lower() == item.name.lower()), None)  # already own it?
        if existing_slot:
            existing_slot["qty"] += qty
        else:
            self.slots.append({"item": item, "qty": qty})

    def remove_item(self, item_name, qty=1):
        for idx, slot in enumerate(self.slots):
            if slot["item"].name.lower() == item_name.lower():
                slot["qty"] -= qty
                if slot["qty"] <= 0:
                    self.slots.pop(idx)  # none left, drop the slot
                return True
        return False

    def get_items_by_category(self, target_cat):
        return [slot for slot in self.slots if slot["item"].category.lower() == target_cat.lower()]

    def is_empty(self):
        return len(self.slots) == 0

    def use_item(self, item_name, pet):
        target_slot = next((slot for slot in self.slots if slot["item"].name.lower() == item_name.lower()), None)
        if not target_slot:
            return {"success": False, "message": "Item not found in backpack!"}
        action_map = {"Food": pet.feed, "Toy": pet.play, "Medicine": pet.heal}
        action_handler = action_map.get(target_slot["item"].category)  # pick the right method
        if not action_handler:
            return {"success": False, "message": "Cannot use this item."}
        action_res = action_handler(target_slot["item"].boost)
        if action_res["success"]:
            self.remove_item(target_slot["item"].name, 1)  # only use up the item if it worked
        return action_res

    def to_dict(self):
        return [{"item": slot["item"].to_dict(), "qty": slot["qty"]} for slot in self.slots]

    def load_from_list(self, slot_list):
        self.slots = [{"item": Item.from_dict(entry["item"]), "qty": entry["qty"]} for entry in slot_list]

class Pet:
    def __init__(self, name, species="Pet"):
        self.name, self.species = name, species
        self.health, self.hunger, self.happiness, self.energy = 100, 80, 80, 80
        self.level, self.exp, self.coins = 1, 0, 50
        self.inventory = Inventory()

    def clamp(self, stat_val):
        return max(0, min(100, stat_val))  # stats stay between 0 and 100

    def is_alive(self):
        return self.health > 0 and self.hunger > 0

    def gain_exp(self, exp_pts):
        self.exp += exp_pts
        leveled_up = False
        while self.exp >= 100:  # 100 EXP per level, extra EXP carries over
            self.exp -= 100
            self.level += 1
            leveled_up = True
            self.health, self.energy = self.clamp(self.health + 10), self.clamp(self.energy + 10)
            self.coins += 25
        return leveled_up

    def feed(self, boost=25):
        if self.hunger >= 100:
            return {"success": False, "message": f"{self.name} is completely full!"}
        prev_hunger = self.hunger
        self.hunger = self.clamp(self.hunger + boost)
        return {"success": True, "leveled_up": self.gain_exp(10), "message": f"{self.name} ate food! (+{self.hunger - prev_hunger} Hunger, +10 EXP)"}

    def play(self, boost=25):
        if self.energy < 15:
            return {"success": False, "message": f"{self.name} is too exhausted to play!"}
        prev_happiness = self.happiness
        self.happiness = self.clamp(self.happiness + boost)
        self.energy, self.hunger, self.coins = self.clamp(self.energy - 20), self.clamp(self.hunger - 10), self.coins + 15
        return {"success": True, "leveled_up": self.gain_exp(20), "message": f"{self.name} played happily! (+{self.happiness - prev_happiness} Happiness, +15 Coins, +20 EXP)"}

    def sleep(self):
        if self.energy >= 100:
            return {"success": False, "message": f"{self.name} is already full of energy!"}
        prev_energy = self.energy
        self.energy = self.clamp(self.energy + 40)
        self.hunger = self.clamp(self.hunger - 15)
        return {"success": True, "message": f"{self.name} had a refreshing sleep! (+{self.energy - prev_energy} Energy)"}

    def heal(self, boost=30):
        if self.health >= 100:
            return {"success": False, "message": f"{self.name} is already in perfect health!"}
        prev_health = self.health
        self.health = self.clamp(self.health + boost)
        return {"success": True, "message": f"{self.name} received medicine! (+{self.health - prev_health} Health)"}

    def speak(self):
        return "..."  # each subclass overrides this

    def to_dict(self):
        return {
            "name": self.name, "species": self.species, "health": self.health, "hunger": self.hunger,
            "happiness": self.happiness, "energy": self.energy, "level": self.level, "exp": self.exp,
            "coins": self.coins, "inventory": self.inventory.to_dict()
        }

class Dog(Pet):
    def __init__(self, name):
        super().__init__(name, "Dog")

    def speak(self):
        return "Woof! Woof! 🐶"

    def play(self, boost=25):
        play_res = super().play(boost)
        if play_res["success"]:
            self.coins += 10  # dog perk
            play_res["message"] += "\n(Loyal Dog Bonus: +10 Coins!)"
        return play_res

class Cat(Pet):
    def __init__(self, name):
        super().__init__(name, "Cat")

    def speak(self):
        return "Meow~ Purrr... 🐱"

    def sleep(self):
        sleep_res = super().sleep()
        if sleep_res["success"]:
            prev_energy = self.energy
            self.energy = self.clamp(self.energy + 20)  # cat perk: sleeps extra well
            sleep_res["message"] += f"\n(Cozy Catnap Perk: +{self.energy - prev_energy} Extra Energy!)" if self.energy > prev_energy else "\n(Cozy Catnap Perk: Energy fully restored!)"
        return sleep_res

class Dragon(Pet):
    def __init__(self, name):
        super().__init__(name, "Dragon")

    def speak(self):
        return "ROAAAR! 🔥🐉"

    def gain_exp(self, exp_pts):
        return super().gain_exp(exp_pts + 15)  # dragon perk: +15 EXP every time

class Shop:
    def __init__(self):
        self.catalog = [Item.from_dict(item_data) for item_data in ITEM_DATABASE]

    def buy_item(self, pet, item_name):
        target_item = next((item for item in self.catalog if item.name.lower() == item_name.lower()), None)
        if not target_item:
            return {"success": False, "message": "Item not found in store catalog!"}
        if pet.coins < target_item.price:
            return {"success": False, "message": f"Not enough coins! Costs {target_item.price} coins (You have: {pet.coins})."}
        pet.coins -= target_item.price
        pet.inventory.add_item(target_item, 1)
        return {"success": True, "message": f"Successfully purchased {target_item.name} for {target_item.price} coins!\n(Remaining Balance: {pet.coins} coins)"}

SAVE_PATH, LEGACY_PATH = os.path.join("data", "pet_save.json"), os.path.join(".data", "pet_save.json")

def get_save_file():
    return LEGACY_PATH if os.path.exists(LEGACY_PATH) else SAVE_PATH  # old saves still work

def has_save():
    return os.path.exists(get_save_file())

def save_game(pet):
    try:
        target_path = get_save_file()
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as save_file:
            json.dump(pet.to_dict(), save_file, indent=4)
        return True
    except Exception as exc:
        print_error(f"Failed to save: {exc}")
        return False

def load_game():
    target_path = get_save_file()
    if not os.path.exists(target_path):
        return None
    try:
        with open(target_path, "r", encoding="utf-8") as save_file:
            saved_data = json.load(save_file)
        species_map = {"Dog": Dog, "Cat": Cat, "Dragon": Dragon}
        pet_class = species_map.get(saved_data.get("species"), Pet)
        loaded_pet = pet_class(saved_data.get("name", "Buddy"))
        for stat_key in ("health", "hunger", "happiness", "energy", "level", "exp", "coins"):
            if stat_key in saved_data:
                setattr(loaded_pet, stat_key, saved_data[stat_key])
        loaded_pet.inventory.load_from_list(saved_data.get("inventory", []))
        return loaded_pet
    except Exception as exc:
        print_error(f"Failed to load: {exc}")
        return None

def render_bar(label_name, current_val, max_val=100, bar_length=15):
    fill_ratio = max(0.0, min(1.0, current_val / max_val))
    bar_chars = "█" * int(bar_length * fill_ratio) + "░" * (bar_length - int(bar_length * fill_ratio))
    bar_color = GREEN if fill_ratio > 0.6 else (YELLOW if fill_ratio > 0.3 else RED)  # green = good, red = low
    return f"{label_name + ':':<12} [{bar_color}{bar_chars}{RESET}]  {int(current_val):>3}/{max_val}"

def show_result(pet, action_result, error_printer=print_warning):  # prints an action's outcome, plus a level-up message if needed
    if action_result["success"]:
        print_success(action_result["message"])
    else:
        error_printer(action_result["message"])
    if action_result.get("leveled_up"):
        print_success(f"🎉 LEVEL UP! {pet.name} reached Level {pet.level}! (+10 Health, +10 Energy, +25 Coins)")

def show_status(pet):
    if pet.species in PET_ART:
        print(PET_ART[pet.species])
    theme_color = PET_SPECIES_INFO.get(pet.species, {}).get("color", RESET)
    print(f"{theme_color}{BOLD}🐾 {pet.name.upper()} THE {pet.species.upper()}{RESET} {DIM}({pet.speak()}){RESET}\n" + "─" * 46)
    for stat_name in ("Health", "Hunger", "Happiness", "Energy"):
        print(render_bar(stat_name, getattr(pet, stat_name.lower())))
    print("─" * 46 + f"\nLevel: {BOLD}{pet.level}{RESET}  |  EXP: {CYAN}{pet.exp}/100{RESET}  |  Coins: {YELLOW}{BOLD}{pet.coins} 🪙{RESET}\n" + "─" * 46 + "\n")

def use_backpack_item(pet, category_name):
    matching_items = pet.inventory.get_items_by_category(category_name)
    if not matching_items:
        return print_warning(f"No {category_name.lower()} items in backpack! Visit store.")
    print(f"\n{BOLD}Available {category_name}:{RESET}")
    for idx, slot_data in enumerate(matching_items, 1):
        print(f"  [{idx}] {slot_data['item'].name} (x{slot_data['qty']}) - {slot_data['item'].description}")
    user_choice = input(f"\n{BOLD}Choose (0 to cancel): {RESET}").strip()
    if user_choice.isdigit() and 1 <= int(user_choice) <= len(matching_items):
        show_result(pet, pet.inventory.use_item(matching_items[int(user_choice) - 1]["item"].name, pet))

def handle_feed(pet):
    print_header(f"Feed {pet.name}")
    if pet.hunger >= 100:
        return print_warning(f"{pet.name} is completely full!")
    use_backpack_item(pet, "Food")

def handle_play(pet):
    print_header(f"Play with {pet.name}")
    toy_items = pet.inventory.get_items_by_category("Toy")
    print("  [1] Quick Free Play (costs 20 Energy)" + ("\n  [2] Play with a Toy from Backpack" if toy_items else "") + "\n  [0] Cancel")
    user_choice = input(f"\n{BOLD}Choose option: {RESET}").strip()
    if user_choice == "1":
        show_result(pet, pet.play())
    elif user_choice == "2" and toy_items:
        use_backpack_item(pet, "Toy")

def handle_sleep(pet):
    print_header(f"Nap Time for {pet.name}")
    show_result(pet, pet.sleep())

def handle_heal(pet):
    print_header(f"Heal {pet.name}")
    if pet.health >= 100:
        return print_warning(f"{pet.name} is already in perfect health!")
    use_backpack_item(pet, "Medicine")

def handle_shop(pet, current_shop):
    while True:
        clear_screen()
        print_header("Pet Care Store")
        print(f"Your Coins: {YELLOW}{BOLD}{pet.coins} 🪙{RESET}\n\nNo.  Item             Type       Price    Effect\n" + "─" * 58)
        for idx, shop_item in enumerate(current_shop.catalog, 1):
            print(f"{idx:<4}{shop_item.name:<17}{shop_item.category:<10}{str(shop_item.price) + ' coins':<9}{shop_item.description}")
        print("─" * 58 + "\n [0] Exit Store\n")
        user_choice = input(f"{BOLD}Enter item number to buy (0 to exit): {RESET}").strip()
        if user_choice == "0":
            break
        if user_choice.isdigit() and 1 <= int(user_choice) <= len(current_shop.catalog):
            purchase_res = current_shop.buy_item(pet, current_shop.catalog[int(user_choice) - 1].name)
            show_result(pet, purchase_res, print_error)
            if purchase_res["success"]:
                save_game(pet)
        else:
            print_error("Invalid selection.")
        pause()

def handle_inventory(pet):
    clear_screen()
    print_header(f"{pet.name}'s Backpack")
    if pet.inventory.is_empty():
        print_warning("Backpack empty! Visit store to stock up.")
        return pause()
    print("No.  Item             Category   Qty   Description\n" + "─" * 58)
    for idx, slot_data in enumerate(pet.inventory.slots, 1):
        print(f"{idx:<4}{slot_data['item'].name:<17}{slot_data['item'].category:<10}{str(slot_data['qty']):<5}{slot_data['item'].description}")
    print("─" * 58 + "\n [0] Return to Main Game\n")
    user_choice = input(f"{BOLD}Enter item number to use (or 0 to return): {RESET}").strip()
    if user_choice.isdigit() and 1 <= int(user_choice) <= len(pet.inventory.slots):
        use_res = pet.inventory.use_item(pet.inventory.slots[int(user_choice) - 1]["item"].name, pet)
        show_result(pet, use_res)
        save_game(pet)
        pause()

def create_pet():
    clear_screen()
    print(BANNER)
    print_header("Adopt a New Pet\n\nAvailable Pet Companions:")
    species_options = ["Dog", "Cat", "Dragon"]
    for idx, species_key in enumerate(species_options, 1):
        species_data = PET_SPECIES_INFO[species_key]
        print(f"  {species_data['color']}[{idx}] {species_key:<7}{RESET} - {species_data['title']:<16}: {species_data['desc']}")
    species_choice = ""
    while species_choice not in ("1", "2", "3"):
        species_choice = input(f"\n{BOLD}Pick a species (1-3): {RESET}").strip()
    chosen_name = input(f"{BOLD}Name your pet (press Enter for 'Rex'): {RESET}").strip() or "Rex"
    species_map = {"Dog": Dog, "Cat": Cat, "Dragon": Dragon}
    pet = species_map[species_options[int(species_choice) - 1]](chosen_name)
    pet.inventory.add_item(Item.from_dict(ITEM_DATABASE[0]), 2)  # starter kit: 2 kibble...
    pet.inventory.add_item(Item.from_dict(ITEM_DATABASE[3]), 1)  # ...and a rubber ball
    print_success(f"You officially adopted {pet.name} the {pet.species}!")
    print(f"{CYAN}Starter Care Kit: 2x Dry Kibble, 1x Rubber Ball, 50 Coins.{RESET}")
    save_game(pet)
    pause()
    return pet

def game_loop(pet):
    store = Shop()
    while True:
        clear_screen()
        show_status(pet)
        if not pet.is_alive():
            print(PET_ART["RIP"])
            print_error(f"{pet.name} has fainted due to exhaustion or starvation!")
            print(f"  [1] Revive {pet.name} (restores 50 Health & Hunger)\n  [2] Adopt a brand new pet\n  [3] Exit to Main Menu")
            revive_choice = input(f"\n{BOLD}Choose option (1-3): {RESET}").strip()
            if revive_choice == "1":
                pet.health, pet.hunger = 50, 50
                save_game(pet)
                print_success(f"{pet.name} has been lovingly revived!")
                pause()
                continue
            elif revive_choice == "2":
                pet = create_pet()
                continue
            break
        print(f"{BOLD}What would you like to do?{RESET}")
        menu_items = [
            f"[1] Feed {pet.name} 🍖", f"[5] Store 🏬",
            f"[2] Play {pet.name} 🎾", f"[6] Backpack 🎒",
            f"[3] Nap Time 💤",         f"[7] Save Game 💾",
            f"[4] Heal {pet.name} 💊", f"[8] Save & Exit 🚪"
        ]
        for idx in range(0, 8, 2):
            print(f"  {CYAN}{menu_items[idx]:<24}{menu_items[idx+1]}{RESET}")  # two columns
        menu_selection = input(f"\n{BOLD}Enter choice (1-8): {RESET}").strip()
        if menu_selection in ("1", "2", "3", "4"):
            pet_actions = [handle_feed, handle_play, handle_sleep, handle_heal]
            pet_actions[int(menu_selection) - 1](pet)
            save_game(pet)
            pause()
        elif menu_selection == "5":
            handle_shop(pet, store)
            save_game(pet)
        elif menu_selection == "6":
            handle_inventory(pet)
            save_game(pet)
        elif menu_selection == "7":
            save_successful = save_game(pet)
            (print_success if save_successful else print_error)("Game progress saved to JSON database!")
            pause()
        elif menu_selection == "8":
            save_game(pet)
            print_success(f"Game saved! Until next time, take care of {pet.name}! 👋")
            pause("Press Enter to return to Main Menu...")
            break
        else:
            print_error("Invalid selection. Choose 1 through 8.")
            pause()

def main():
    try:
        while True:
            clear_screen()
            print(BANNER)
            print_header("Main Menu")
            save_exists = has_save()
            save_label = 'Saved Game' if save_exists else '(no save file found)'
            save_style = YELLOW if save_exists else DIM
            print(f"  {GREEN}[1] New Game{RESET}\n  {save_style}[2] Continue {save_label}{RESET}\n  {RED}[3] Exit{RESET}")
            nav_choice = input(f"\n{BOLD}Choose option (1-3): {RESET}").strip()
            if nav_choice == "1":
                game_loop(create_pet())
            elif nav_choice == "2":
                loaded_pet = load_game()  # returns None if there is no save (or it is broken)
                if loaded_pet:
                    print_success(f"Loaded {loaded_pet.name} the {loaded_pet.species}!")
                    pause("Press Enter to begin playing...")
                    game_loop(loaded_pet)
                else:
                    print_warning("No existing save file found. Please start a New Game!")
                    pause()
            elif nav_choice == "3":
                print(f"\n{GREEN}Thank you for playing CSE Pet Simulator! Goodbye! 👋{RESET}\n")
                break
            else:
                print_error("Please enter a valid choice (1-3).")
                pause()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{YELLOW}Game closed. Catch you later! 👋{RESET}\n")

if __name__ == "__main__":
    main()
