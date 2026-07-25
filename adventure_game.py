"""
adventure_game.py

A text-based adventure game built with Python.
The player takes on the role of an explorer searching for a legendary
treasure hidden in an ancient land. The player navigates through a
dark forest or a mysterious cave, making choices along the way that
lead to winning (finding the treasure), losing (a poor decision ends
the quest), or restarting the adventure.

This script was scaffolded and refined with the help of GitHub Copilot
inside VS Code -- see the accompanying project report for details on
how Copilot was used.
"""

import sys
import time

# Small pause used between print statements to give the game a more
# "narrated" feel. Kept short so automated/non-interactive runs are fast.
TYPE_DELAY = 0.0


def slow_print(text, delay=TYPE_DELAY):
    """Print text, optionally with a small delay to simulate narration."""
    print(text)
    if delay:
        time.sleep(delay)


def get_choice(prompt, valid_choices):
    """
    Ask the player for input and keep asking until a valid choice
    (case-insensitive) is entered. Returns the choice in lowercase.
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please choose one of: {', '.join(valid_choices)}")


def start_game():
    """
    Display the game introduction, ask the player for their name,
    and present the initial choice of path (forest or cave).
    """
    slow_print("=" * 55)
    slow_print("       WELCOME TO THE QUEST FOR THE LOST TREASURE")
    slow_print("=" * 55)
    player_name = input("\nBefore we begin, what is your name, explorer? ").strip()
    if not player_name:
        player_name = "Explorer"

    slow_print(f"\nWelcome, {player_name}!")
    slow_print(
        "Legend speaks of a legendary treasure hidden deep within an "
        "ancient land, guarded by trials of courage and wit."
    )
    slow_print(
        "Many have searched for it, but few have returned. "
        "Today, you set out to find it.\n"
    )
    slow_print("Ahead of you lie two paths:")
    slow_print("  1) A dark, whispering forest")
    slow_print("  2) A mysterious, echoing cave")

    path_choice = get_choice(
        "\nWhich path do you choose? (forest/cave): ", ["forest", "cave"]
    )

    if path_choice == "forest":
        return forest_path(player_name)
    else:
        return cave_path(player_name)


def forest_path(player_name):
    """
    Describe the forest scenario and let the player choose between
    following a river or climbing a tree. Returns True if the player
    wins, False if the player loses.
    """
    slow_print(f"\n{player_name} steps into the dark forest.")
    slow_print(
        "Tall trees block out the sunlight, and strange sounds echo "
        "all around. Soon you come across a fork in the path."
    )
    slow_print("\nDo you:")
    slow_print("  1) Follow the river, hoping it leads somewhere useful")
    slow_print("  2) Climb a tall tree to get a better view of the land")

    choice = get_choice(
        "\nEnter your choice (river/tree): ", ["river", "tree"]
    )

    if choice == "river":
        slow_print(
            "\nYou follow the gentle sound of flowing water. The river "
            "leads you to a hidden clearing where an old stone map is "
            "carved into a rock, pointing toward a hidden cave entrance."
        )
        slow_print("You have found a clue that brings you closer to the treasure!")
        return cave_path(player_name, has_clue=True)
    else:
        slow_print(
            "\nYou climb the tallest tree you can find. From the top, "
            "you spot a glint of gold near a rocky outcrop in the "
            "distance -- and, unfortunately, you also spot a pack of "
            "wolves patrolling the forest floor below."
        )
        outcome = get_choice(
            "\nDo you climb down carefully or jump down quickly? "
            "(careful/quick): ",
            ["careful", "quick"],
        )
        if outcome == "careful":
            slow_print(
                "\nYou climb down slowly and quietly, avoiding the "
                "wolves entirely. You continue toward the rocky outcrop "
                "and discover the entrance to a cave!"
            )
            return cave_path(player_name, has_clue=True)
        else:
            slow_print(
                "\nYou jump down quickly to save time, but you land "
                "awkwardly and twist your ankle. The wolves hear the "
                "noise and begin to close in. Unable to run, your "
                "journey ends here."
            )
            return False


def cave_path(player_name, has_clue=False):
    """
    Describe the cave scenario and let the player choose between
    lighting a torch or proceeding in the dark. Returns True if the
    player wins, False if the player loses.
    """
    slow_print(f"\n{player_name} approaches the mouth of a mysterious cave.")
    if has_clue:
        slow_print(
            "Thanks to the clue you found earlier, you know the "
            "treasure lies somewhere deep within these tunnels."
        )
    slow_print(
        "Cold air drifts out from the darkness within. You must decide "
        "how to proceed."
    )
    slow_print("\nDo you:")
    slow_print("  1) Light a torch before entering")
    slow_print("  2) Proceed in the dark to avoid attracting attention")

    choice = get_choice(
        "\nEnter your choice (torch/dark): ", ["torch", "dark"]
    )

    if choice == "torch":
        slow_print(
            "\nYou light a torch. Its warm glow reveals ancient "
            "carvings on the walls, guiding you safely through the "
            "twisting tunnels."
        )
        if has_clue:
            slow_print(
                "Following the map's clue and the carvings on the "
                "walls, you arrive at a hidden chamber. In the center, "
                "resting on a stone pedestal, lies the LEGENDARY "
                "TREASURE!"
            )
            slow_print(
                f"\nCongratulations, {player_name}! You have won the "
                "game and claimed the treasure!"
            )
            return True
        else:
            slow_print(
                "\nWithout the earlier clue, the tunnels branch "
                "endlessly. You wander for hours before finding your "
                "way back out, empty-handed but alive."
            )
            return False
    else:
        slow_print(
            "\nYou creep forward in total darkness. Without light, you "
            "misjudge a step and fall into a hidden pit. Your torchless "
            "gamble has cost you the quest."
        )
        return False


def play_again():
    """Ask the player if they would like to restart the game."""
    choice = get_choice(
        "\nWould you like to play again? (yes/no): ", ["yes", "no"]
    )
    return choice == "yes"


def main():
    """Main game loop: runs the game and offers a restart option."""
    keep_playing = True
    while keep_playing:
        won = start_game()
        print("\n" + "-" * 55)
        if won:
            slow_print("RESULT: You found the treasure. Victory is yours!")
        else:
            slow_print("RESULT: Your quest has ended without the treasure.")
        print("-" * 55)
        keep_playing = play_again()

    slow_print("\nThanks for playing the Quest for the Lost Treasure. Farewell!")
    sys.exit(0)


if __name__ == "__main__":
    main()
