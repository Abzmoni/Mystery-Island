"""Terminal interface for Mystery Island. Run with python main.py."""

from game import SCENES, apply_action, available_actions, new_game


def choose_action(actions):
    """Display numbered commands and translate a valid number to a command."""
    for number, action in enumerate(actions, start=1):
        print(f"  {number}. {action}")
    choice = input("> ").strip().lower()
    # Compare strings: arbitrary text and huge numbers need no int conversion.
    for number, action in enumerate(actions, start=1):
        if choice == str(number):
            return action
    return choice


def play_game(name):
    """Run a fresh adventure until the player wins, loses, or quits."""
    player = new_game(name)
    print(f"\nWelcome, {player['name']}! You wake up after a storm.")
    while not player["game_over"]:
        print(f"\n{player['location']} | Energy: {player['energy']}/5")
        print(SCENES[player["location"]])
        print(apply_action(player, choose_action(available_actions(player))))
    return player


def ask_replay():
    """Repeat the replay prompt until a yes or no answer is supplied."""
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no", "q", "quit", "exit"):
            return False
        print("Please enter y or n.")


def main():
    """Show instructions, ask for a name, and offer replay after each game."""
    print("MYSTERY ISLAND — The Lost Lighthouse")
    print("Restore the beacon before your energy runs out.")
    print("Choose a menu number or type its command. Type quit or exit to stop.")
    print("Every legal move costs 1 energy; at 0 you lose immediately.")
    print("Pickups, inventory, help, and rejected commands cost no energy.")
    try:
        name = input("What is your name? ")
        while True:
            play_game(name)
            if not ask_replay():
                break
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed. Adventure ended.")
    print("Thanks for exploring Mystery Island!")


if __name__ == "__main__":
    main()
