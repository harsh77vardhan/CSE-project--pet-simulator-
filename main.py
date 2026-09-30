# CSE Project - Virtual Pet Simulator (College Edition)
# Shows: classes, inheritance, polymorphism, JSON save/load
# Run with: python3 main.py
import json, os
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"  # ANSI codes for terminal styling
RED, GREEN, YELLOW, CYAN, MAGENTA = "\033[91m", "\033[92m", "\033[93m", "\033[96m", "\033[95m"
def clear_screen(): os.system("cls" if os.name == "nt" else "clear")
def pause(msg="Press Enter to continue..."): input(f"\n{DIM}{msg}{RESET}")
def print_header(title): print(f"\n{CYAN}{BOLD}=== {title} ==={RESET}")
def print_success(msg): print(f"{GREEN}✔ {msg}{RESET}")
def print_warning(msg): print(f"{YELLOW}⚠ {msg}{RESET}")
def print_error(msg): print(f"{RED}✖ {msg}{RESET}")
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
    {"name": n, "category": c, "price": p, "boost": b, "description": d}
    for n, c, p, b, d in [
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
    def to_dict(self): return vars(self)  # needed for the JSON save
    @classmethod
    def from_dict(cls, d): return cls(**d)

class Inventory:
    def __init__(self): self.slots = []  # each slot is {"item": Item, "qty": int}
    def add_item(self, item, qty=1):
        slot = next((s for s in self.slots if s["item"].name.lower() == item.name.lower()), None)  # already own it?
        if slot: slot["qty"] += qty
        else: self.slots.append({"item": item, "qty": qty})
    def remove_item(self, name, qty=1):
        for i, s in enumerate(self.slots):
            if s["item"].name.lower() == name.lower():
                s["qty"] -= qty
                if s["qty"] <= 0: self.slots.pop(i)  # none left, drop the slot
                return True
        return False
    def get_items_by_category(self, cat):
        return [s for s in self.slots if s["item"].category.lower() == cat.lower()]
    def is_empty(self): return len(self.slots) == 0
    def use_item(self, name, pet):
        slot = next((s for s in self.slots if s["item"].name.lower() == name.lower()), None)
        if not slot: return {"success": False, "message": "Item not found in backpack!"}
        action = {"Food": pet.feed, "Toy": pet.play, "Medicine": pet.heal}.get(slot["item"].category)  # pick the right method
        if not action: return {"success": False, "message": "Cannot use this item."}
        res = action(slot["item"].boost)
        if res["success"]: self.remove_item(slot["item"].name, 1)  # only use up the item if it worked
        return res
    def to_dict(self): return [{"item": s["item"].to_dict(), "qty": s["qty"]} for s in self.slots]
    def load_from_list(self, lst):
        self.slots = [{"item": Item.from_dict(d["item"]), "qty": d["qty"]} for d in lst]

class Pet:
    def __init__(self, name, species="Pet"):
        self.name, self.species = name, species
        self.health, self.hunger, self.happiness, self.energy = 100, 80, 80, 80
        self.level, self.exp, self.coins = 1, 0, 50
        self.inventory = Inventory()
    def clamp(self, val): return max(0, min(100, val))  # stats stay between 0 and 100
    def is_alive(self): return self.health > 0 and self.hunger > 0
    def gain_exp(self, amt):
        self.exp += amt
        leveled = False
        while self.exp >= 100:  # 100 EXP per level, extra EXP carries over
            self.exp -= 100
            self.level += 1
            leveled = True
            self.health, self.energy = self.clamp(self.health + 10), self.clamp(self.energy + 10)
            self.coins += 25
        return leveled
    def feed(self, boost=25):
        if self.hunger >= 100: return {"success": False, "message": f"{self.name} is completely full!"}
        old = self.hunger; self.hunger = self.clamp(self.hunger + boost)
        return {"success": True, "leveled_up": self.gain_exp(10), "message": f"{self.name} ate food! (+{self.hunger - old} Hunger, +10 EXP)"}
    def play(self, boost=25):
        if self.energy < 15: return {"success": False, "message": f"{self.name} is too exhausted to play!"}
        old = self.happiness; self.happiness = self.clamp(self.happiness + boost)
        self.energy, self.hunger, self.coins = self.clamp(self.energy - 20), self.clamp(self.hunger - 10), self.coins + 15
        return {"success": True, "leveled_up": self.gain_exp(20), "message": f"{self.name} played happily! (+{self.happiness - old} Happiness, +15 Coins, +20 EXP)"}
    def sleep(self):
        if self.energy >= 100: return {"success": False, "message": f"{self.name} is already full of energy!"}
        old = self.energy; self.energy = self.clamp(self.energy + 40); self.hunger = self.clamp(self.hunger - 15)
        return {"success": True, "message": f"{self.name} had a refreshing sleep! (+{self.energy - old} Energy)"}
    def heal(self, boost=30):
        if self.health >= 100: return {"success": False, "message": f"{self.name} is already in perfect health!"}
        old = self.health; self.health = self.clamp(self.health + boost)
        return {"success": True, "message": f"{self.name} received medicine! (+{self.health - old} Health)"}
    def speak(self): return "..."  # each subclass overrides this
    def to_dict(self):
        return {"name": self.name, "species": self.species, "health": self.health, "hunger": self.hunger,
                "happiness": self.happiness, "energy": self.energy, "level": self.level, "exp": self.exp,
                "coins": self.coins, "inventory": self.inventory.to_dict()}

class Dog(Pet):
    def __init__(self, name): super().__init__(name, "Dog")
    def speak(self): return "Woof! Woof! 🐶"
    def play(self, boost=25):
        res = super().play(boost)
        if res["success"]:
            self.coins += 10  # dog perk
            res["message"] += "\n(Loyal Dog Bonus: +10 Coins!)"
        return res

class Cat(Pet):
    def __init__(self, name): super().__init__(name, "Cat")
    def speak(self): return "Meow~ Purrr... 🐱"
    def sleep(self):
        res = super().sleep()
        if res["success"]:
            old = self.energy; self.energy = self.clamp(self.energy + 20)  # cat perk: sleeps extra well
            res["message"] += f"\n(Cozy Catnap Perk: +{self.energy - old} Extra Energy!)" if self.energy > old else "\n(Cozy Catnap Perk: Energy fully restored!)"
        return res

class Dragon(Pet):
    def __init__(self, name): super().__init__(name, "Dragon")
    def speak(self): return "ROAAAR! 🔥🐉"
    def gain_exp(self, amt): return super().gain_exp(amt + 15)  # dragon perk: +15 EXP every time

class Shop:
    def __init__(self): self.catalog = [Item.from_dict(d) for d in ITEM_DATABASE]
    def buy_item(self, pet, name):
        target = next((i for i in self.catalog if i.name.lower() == name.lower()), None)
        if not target: return {"success": False, "message": "Item not found in store catalog!"}
        if pet.coins < target.price: return {"success": False, "message": f"Not enough coins! Costs {target.price} coins (You have: {pet.coins})."}
        pet.coins -= target.price; pet.inventory.add_item(target, 1)
        return {"success": True, "message": f"Successfully purchased {target.name} for {target.price} coins!\n(Remaining Balance: {pet.coins} coins)"}
SAVE_PATH, LEGACY_PATH = os.path.join("data", "pet_save.json"), os.path.join(".data", "pet_save.json")
def get_save_file(): return LEGACY_PATH if os.path.exists(LEGACY_PATH) else SAVE_PATH  # old saves still work
def has_save(): return os.path.exists(get_save_file())
def save_game(pet):
    try:
        path = get_save_file(); os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f: json.dump(pet.to_dict(), f, indent=4)
        return True
    except Exception as e: print_error(f"Failed to save: {e}"); return False
def load_game():
    path = get_save_file()
    if not os.path.exists(path): return None
    try:
        with open(path, "r", encoding="utf-8") as f: d = json.load(f)
        pet = {"Dog": Dog, "Cat": Cat, "Dragon": Dragon}.get(d.get("species"), Pet)(d.get("name", "Buddy"))
        for k in ("health", "hunger", "happiness", "energy", "level", "exp", "coins"):
            if k in d: setattr(pet, k, d[k])
        pet.inventory.load_from_list(d.get("inventory", []))
        return pet
    except Exception as e: print_error(f"Failed to load: {e}"); return None
def render_bar(label, val, max_val=100, length=15):
    r = max(0.0, min(1.0, val / max_val))
    bar = "█" * int(length * r) + "░" * (length - int(length * r))
    c = GREEN if r > 0.6 else (YELLOW if r > 0.3 else RED)  # green = good, red = low
    return f"{label + ':':<12} [{c}{bar}{RESET}]  {int(val):>3}/{max_val}"
def show_result(pet, res, fail=print_warning):  # prints an action's outcome, plus a level-up message if needed
    if res["success"]: print_success(res["message"])
    else: fail(res["message"])
    if res.get("leveled_up"): print_success(f"🎉 LEVEL UP! {pet.name} reached Level {pet.level}! (+10 Health, +10 Energy, +25 Coins)")
def show_status(pet):
    if pet.species in PET_ART: print(PET_ART[pet.species])
    c = PET_SPECIES_INFO.get(pet.species, {}).get("color", RESET)
    print(f"{c}{BOLD}🐾 {pet.name.upper()} THE {pet.species.upper()}{RESET} {DIM}({pet.speak()}){RESET}\n" + "─" * 46)
    for stat in ("Health", "Hunger", "Happiness", "Energy"):
        print(render_bar(stat, getattr(pet, stat.lower())))
    print("─" * 46 + f"\nLevel: {BOLD}{pet.level}{RESET}  |  EXP: {CYAN}{pet.exp}/100{RESET}  |  Coins: {YELLOW}{BOLD}{pet.coins} 🪙{RESET}\n" + "─" * 46 + "\n")
def use_backpack_item(pet, category):
    items = pet.inventory.get_items_by_category(category)
    if not items: return print_warning(f"No {category.lower()} items in backpack! Visit store.")
    print(f"\n{BOLD}Available {category}:{RESET}")
    for i, s in enumerate(items, 1): print(f"  [{i}] {s['item'].name} (x{s['qty']}) - {s['item'].description}")
    ch = input(f"\n{BOLD}Choose (0 to cancel): {RESET}").strip()
    if ch.isdigit() and 1 <= int(ch) <= len(items):
        show_result(pet, pet.inventory.use_item(items[int(ch) - 1]["item"].name, pet))
def handle_feed(pet):
    print_header(f"Feed {pet.name}")
    if pet.hunger >= 100: return print_warning(f"{pet.name} is completely full!")
    use_backpack_item(pet, "Food")
def handle_play(pet):
    print_header(f"Play with {pet.name}")
    toys = pet.inventory.get_items_by_category("Toy")
    print("  [1] Quick Free Play (costs 20 Energy)" + ("\n  [2] Play with a Toy from Backpack" if toys else "") + "\n  [0] Cancel")
    ch = input(f"\n{BOLD}Choose option: {RESET}").strip()
    if ch == "1": show_result(pet, pet.play())
    elif ch == "2" and toys: use_backpack_item(pet, "Toy")
def handle_sleep(pet):
    print_header(f"Nap Time for {pet.name}")
    show_result(pet, pet.sleep())
def handle_heal(pet):
    print_header(f"Heal {pet.name}")
    if pet.health >= 100: return print_warning(f"{pet.name} is already in perfect health!")
    use_backpack_item(pet, "Medicine")
def handle_shop(pet, shop):
    while True:
        clear_screen(); print_header("Pet Care Store")
        print(f"Your Coins: {YELLOW}{BOLD}{pet.coins} 🪙{RESET}\n\nNo.  Item             Type       Price    Effect\n" + "─" * 58)
        for i, it in enumerate(shop.catalog, 1):
            print(f"{i:<4}{it.name:<17}{it.category:<10}{str(it.price) + ' coins':<9}{it.description}")
        print("─" * 58 + "\n [0] Exit Store\n")
        ch = input(f"{BOLD}Enter item number to buy (0 to exit): {RESET}").strip()
        if ch == "0": break
        if ch.isdigit() and 1 <= int(ch) <= len(shop.catalog):
            res = shop.buy_item(pet, shop.catalog[int(ch) - 1].name)
            show_result(pet, res, print_error)
            if res["success"]: save_game(pet)
        else: print_error("Invalid selection.")
        pause()
def handle_inventory(pet):
    clear_screen(); print_header(f"{pet.name}'s Backpack")
    if pet.inventory.is_empty():
        print_warning("Backpack empty! Visit store to stock up.")
        return pause()
    print("No.  Item             Category   Qty   Description\n" + "─" * 58)
    for i, s in enumerate(pet.inventory.slots, 1):
        print(f"{i:<4}{s['item'].name:<17}{s['item'].category:<10}{str(s['qty']):<5}{s['item'].description}")
    print("─" * 58 + "\n [0] Return to Main Game\n")
    ch = input(f"{BOLD}Enter item number to use (or 0 to return): {RESET}").strip()
    if ch.isdigit() and 1 <= int(ch) <= len(pet.inventory.slots):
        res = pet.inventory.use_item(pet.inventory.slots[int(ch) - 1]["item"].name, pet)
        show_result(pet, res)
        save_game(pet); pause()
def create_pet():
    clear_screen(); print(BANNER); print_header("Adopt a New Pet\n\nAvailable Pet Companions:")
    keys = ["Dog", "Cat", "Dragon"]
    for i, k in enumerate(keys, 1):
        inf = PET_SPECIES_INFO[k]
        print(f"  {inf['color']}[{i}] {k:<7}{RESET} - {inf['title']:<16}: {inf['desc']}")
    ch = ""
    while ch not in ("1", "2", "3"): ch = input(f"\n{BOLD}Pick a species (1-3): {RESET}").strip()
    name = input(f"{BOLD}Name your pet (press Enter for 'Rex'): {RESET}").strip() or "Rex"
    pet = {"Dog": Dog, "Cat": Cat, "Dragon": Dragon}[keys[int(ch) - 1]](name)
    pet.inventory.add_item(Item.from_dict(ITEM_DATABASE[0]), 2)  # starter kit: 2 kibble...
    pet.inventory.add_item(Item.from_dict(ITEM_DATABASE[3]), 1)  # ...and a rubber ball
    print_success(f"You officially adopted {pet.name} the {pet.species}!")
    print(f"{CYAN}Starter Care Kit: 2x Dry Kibble, 1x Rubber Ball, 50 Coins.{RESET}")
    save_game(pet); pause()
    return pet
def game_loop(pet):
    shop = Shop()
    while True:
        clear_screen(); show_status(pet)
        if not pet.is_alive():
            print(PET_ART["RIP"])
            print_error(f"{pet.name} has fainted due to exhaustion or starvation!")
            print(f"  [1] Revive {pet.name} (restores 50 Health & Hunger)\n  [2] Adopt a brand new pet\n  [3] Exit to Main Menu")
            c = input(f"\n{BOLD}Choose option (1-3): {RESET}").strip()
            if c == "1":
                pet.health, pet.hunger = 50, 50
                save_game(pet); print_success(f"{pet.name} has been lovingly revived!"); pause(); continue
            elif c == "2": pet = create_pet(); continue
            break
        print(f"{BOLD}What would you like to do?{RESET}")
        menu = [f"[1] Feed {pet.name} 🍖", f"[5] Store 🏬", f"[2] Play {pet.name} 🎾", f"[6] Backpack 🎒",
                f"[3] Nap Time 💤", f"[7] Save Game 💾", f"[4] Heal {pet.name} 💊", f"[8] Save & Exit 🚪"]
        for i in range(0, 8, 2): print(f"  {CYAN}{menu[i]:<24}{menu[i+1]}{RESET}")  # two columns
        act = input(f"\n{BOLD}Enter choice (1-8): {RESET}").strip()
        if act in ("1", "2", "3", "4"):
            [handle_feed, handle_play, handle_sleep, handle_heal][int(act) - 1](pet); save_game(pet); pause()
        elif act == "5": handle_shop(pet, shop); save_game(pet)
        elif act == "6": handle_inventory(pet); save_game(pet)
        elif act == "7":
            (print_success if save_game(pet) else print_error)("Game progress saved to JSON database!"); pause()
        elif act == "8":
            save_game(pet); print_success(f"Game saved! Until next time, take care of {pet.name}! 👋")
            pause("Press Enter to return to Main Menu..."); break
        else: print_error("Invalid selection. Choose 1 through 8."); pause()
def main():
    try:
        while True:
            clear_screen(); print(BANNER); print_header("Main Menu")
            print(f"  {GREEN}[1] New Game{RESET}\n  {YELLOW if has_save() else DIM}[2] Continue {'Saved Game' if has_save() else '(no save file found)'}{RESET}\n  {RED}[3] Exit{RESET}")
            c = input(f"\n{BOLD}Choose option (1-3): {RESET}").strip()
            if c == "1": game_loop(create_pet())
            elif c == "2":
                pet = load_game()  # returns None if there is no save (or it is broken)
                if pet:
                    print_success(f"Loaded {pet.name} the {pet.species}!")
                    pause("Press Enter to begin playing..."); game_loop(pet)
                else: print_warning("No existing save file found. Please start a New Game!"); pause()
            elif c == "3": print(f"\n{GREEN}Thank you for playing CSE Pet Simulator! Goodbye! 👋{RESET}\n"); break
            else: print_error("Please enter a valid choice (1-3)."); pause()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{YELLOW}Game closed. Catch you later! 👋{RESET}\n")
if __name__ == "__main__":
    main()