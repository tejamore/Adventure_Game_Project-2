# adventure_game.py
# A text-based adventure game (Course-End Project)
# Purpose: Interactive CLI where the player searches for legendary treasure.

import time
import sys
import random
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except Exception:
    # Fallback colors if colorama is not installed
    class Fore:
        RED = ""
        GREEN = ""
        YELLOW = ""
        CYAN = ""
        MAGENTA = ""
        BLUE = ""
        RESET = ""

    class Style:
        BRIGHT = ""
        RESET_ALL = ""

# Optional sound support (playsound)
try:
    from playsound import playsound
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# Utility: cinematic slow print

def slow_print(text, delay=0.02):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def title_art():
    return (
        f"{Fore.CYAN}{Style.BRIGHT}"
        "\n" 
        "  /\\\\\\\\\\\\   _    _  _   _  ____   ____  _   _  _____  \n"
        " /  _____  \\ | |  | || | | ||  _ \ |  _ \| \ | ||  ___| \n"
        "|  /     \  || |  | || | | || | | || |_) |  \| || |_     \n"
        "| |       | || |  | || | | || | | ||  _ <| . ` ||  _|    \n"
        "|  \_____/  || |__| || |_| || |_| || |_) | |\  || |___   \n"
        " \_________/  \____/  \___/ |____/ |____/|_| \_||____/   \n"
        "\n"
        f"{Style.RESET_ALL}"
    )


def forest_art():
    return (
        f"{Fore.GREEN}{Style.BRIGHT}"
        "   &&& &&  & &&\n"
        "  && &\\\|//& &&\n"
        "   &&  |||  &&\n"
        "      |||\n"
        "      |||     \n"
        f"{Style.RESET_ALL}"
    )


def cave_art():
    return (
        f"{Fore.MAGENTA}{Style.BRIGHT}"
        "      _________\n"
        "     / ======= \\\n        "    / __________\\\n"
        "   | ___________ |\n"
        "   ||  _  _    ||\n"
        "   || |_|/ \___||\n"
        "   ||  _    _  ||\n"
        "   ||_| \__/ |_|\n"
        "   |  _______  |\n"
        f"{Style.RESET_ALL}"
    )


def treasure_art():
    return (
        f"{Fore.YELLOW}{Style.BRIGHT}"
        "       _.--.    .--._\n"
        "     ."      \\" """"/      ".\n"
        "    /  .-.-.  \\  /  .-.-.  \\\n"
        "   |  /  _  \  ||  /  _  \  ||\n"
        "   | |  (_)  | || |  (_)  | ||\n"
        "    \ \_____/ /  \ \_____/ / /\n"
        "     `-.____.'    `-.____.-'\n"
        f"{Style.RESET_ALL}"
    )


def play_sound(filename):
    """Play a sound if playsound is installed and the file exists."""
    if not SOUND_AVAILABLE:
        return
    path = os.path.join(SOUNDS_DIR, filename)
    if os.path.exists(path):
        try:
            playsound(path)
        except Exception:
            pass


def prompt_choice(prompt, choices):
    """Prompt until the user provides a valid choice from choices (list of lowercase strings)."""
    choices_display = "/".join(choices)
    while True:
        choice = input(f"{Fore.BLUE}{prompt} [{choices_display}]: {Fore.RESET}").strip().lower()
        if choice in choices:
            return choice
        else:
            print(f"Please choose one of: {choices_display}")


# Game logic functions

def forest_path(player_name):
    print(forest_art())
    slow_print("You step into the dense forest. The canopy filters the light into emerald shards.")
    slow_print("You hear a river nearby and see a tall tree whose branches look climbable.")
    choice = prompt_choice("Do you follow the river or climb the tree?", ["river", "climb"])

    if choice == "river":
        slow_print("You follow the river downstream. The water is swift — and you spot a rickety bridge.")
        sub = prompt_choice("Cross the bridge or look for another path?", ["cross", "search"])
        if sub == "cross":
            slow_print("The bridge groans but holds. Halfway across, a hidden trapdoor opens beneath you!")
            if random.random() < 0.5:
                slow_print(Fore.RED + "You fall into a pit of thorns. Your quest ends here.")
                return "lose"
            else:
                slow_print(Fore.YELLOW + "You manage to grab the edge and pull yourself up, bruised but alive.")
                slow_print("Across the bridge you find a mossy stone with strange runes — a clue to the treasure.")
                return "clue"
        else:
            slow_print("You find a hidden glade with ancient markings pointing to a cave entrance.")
            return "cave"

    else:  # climb
        slow_print("You climb the tree and from the top you see smoke rising to the north.")
        find = random.choice(["a hawk", "an old watchtower", "nothing"])
        slow_print(f"Up high you notice {find}.")
        if find == "a hawk":
            slow_print("The hawk drops a small shiny key that falls near your feet when you descend.")
            slow_print("This key might open something important later.")
            return "key"
        elif find == "an old watchtower":
            slow_print("You spot an abandoned watchtower — perhaps someone has been here before.")
            return "tower"
        else:
            slow_print("The view gives you confidence and you climb back down, ready to decide your next move.")
            return "continue"


def cave_path(player_name, inventory):
    print(cave_art())
    slow_print("You approach the mouth of a cave. A chill breeze carries distant echoes.")
    choice = prompt_choice("Do you light a torch or proceed in the dark?", ["torch", "dark"])

    if choice == "torch":
        slow_print("You light a torch. Shadows cast ominous shapes on the walls — and you spot ancient paintings.")
        play_sound("torch.wav")
        slow_print("One of the paintings shows a chest and a symbol that matches the mossy stone clue.")
        if "key" in inventory:
            slow_print(Fore.GREEN + "With the key you found, you locate a small locked chest behind a rock.")
            slow_print(treasure_art())
            slow_print(Fore.YELLOW + f"Congratulations, {player_name}! You found the legendary treasure!")
            play_sound("treasure.wav")
            return "win"
        else:
            slow_print("You find a small locked chest but you don't have a key. Perhaps explore elsewhere.")
            return "no_key"

    else:  # dark
        slow_print("You step into the dark relying on your senses. Suddenly the ground gives way.")
        if random.random() < 0.4:
            slow_print(Fore.RED + "You fall into an underground stream and are swept away. The adventure ends.")
            return "lose"
        else:
            slow_print("You feel along the wall and discover a narrow passage leading to a subterranean chamber.")
            slow_print("In the chamber you find a rusted key half-buried in dirt.")
            inventory.add("key")
            return "key_found"


def start_game():
    print(title_art())
    slow_print("Welcome to the Ancient Lands — a text-based adventure.")
    player_name = input("Brave explorer, what is your name? ").strip() or "Explorer"
    slow_print(f"Greetings, {player_name}. Your quest: find the legendary treasure hidden in these lands.")

    # cinematic intro sound (optional)
    play_sound("intro.wav")

    inventory = set()
    state = None

    while True:
        slow_print("You stand at a crossroad: a dark forest to your left and a mysterious cave to your right.")
        choice = prompt_choice("Which do you choose?", ["forest", "cave", "status"])

        if choice == "forest":
            outcome = forest_path(player_name)
            if outcome == "lose":
                slow_print(Fore.RED + "You have perished in the forest.")
                if not restart_prompt():
                    break
                else:
                    inventory.clear()
                    continue
            elif outcome == "cave":
                slow_print("The forest points you toward the cave. You head there now.")
                outcome = cave_path(player_name, inventory)
            elif outcome == "key":
                inventory.add("key")
                slow_print(Fore.GREEN + "You picked up a small key and put it in your pack.")
            elif outcome == "clue":
                slow_print(Fore.YELLOW + "You made a note of the runes — they might match symbols in the cave.")
            # other outcomes lead back to the loop

        elif choice == "cave":
            outcome = cave_path(player_name, inventory)

        else:  # status
            slow_print(f"Player: {player_name}")
            slow_print(f"Inventory: {', '.join(sorted(inventory)) if inventory else 'empty'}")
            continue

        # Evaluate cave outcomes
        if outcome == "win":
            slow_print(Fore.GREEN + "You won the adventure!")
            if not restart_prompt():
                break
            else:
                inventory.clear()
                continue
        elif outcome == "lose":
            slow_print(Fore.RED + "You lost your life on this quest.")
            if not restart_prompt():
                break
            else:
                inventory.clear()
                continue
        elif outcome in ("key_found", "no_key", "continue", "tower"):
            slow_print("You continue your journey, wiser for the experience.")
            continue


def restart_prompt():
    choice = prompt_choice("Would you like to play again?", ["yes", "no"]) 
    return choice == "yes"


if __name__ == "__main__":
    try:
        start_game()
    except KeyboardInterrupt:
        print("\nThanks for playing. Farewell, explorer!")
