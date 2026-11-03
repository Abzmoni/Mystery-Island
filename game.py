"""Deterministic game rules; no terminal input or output."""

LOCATIONS = {
    "Beach": {"east": "Jungle"},
    "Jungle": {"west": "Beach", "east": "Cave"},
    "Cave": {"west": "Jungle", "east": "Old Bridge"},
    "Old Bridge": {"west": "Cave", "east": "Lighthouse"},
    "Lighthouse": {"west": "Old Bridge"},
}

SCENES = {
    "Beach": "Storm wreckage covers the sand. A trail leads east into the jungle.",
    "Jungle": "A sturdy rope hangs from a branch. The cave lies east.",
    "Cave": "A working lantern rests on a ledge. The old bridge lies east.",
    "Old Bridge": "The crossing is locked by a broken safety mechanism. Rope can secure it.",
    "Lighthouse": "The beacon is dark. Use your lantern to light it and signal rescue.",
}

ITEMS = {"Jungle": "rope", "Cave": "lantern"}


def new_game(name):
    """Create an independent player state, including a fresh inventory."""
    return {"name": name.strip() or "Explorer", "location": "Beach",
            "energy": 5, "inventory": [], "game_over": False, "won": False}


def can_cross_bridge(inventory):
    """Return whether the player has the rope needed for the crossing."""
    return "rope" in inventory


def is_win(player):
    """Return whether this player has rescued themselves."""
    return player["won"]


def available_actions(player):
    """Return commands for this room, including attempts at blocked puzzles."""
    if player["game_over"]:
        return []
    actions = ["go " + direction for direction in LOCATIONS[player["location"]]]
    item = ITEMS.get(player["location"])
    if item and item not in player["inventory"]:
        actions.append("take " + item)
    if player["location"] == "Lighthouse":
        actions.append("light beacon")
    return actions + ["inventory", "help", "quit"]


def move_player(player, direction):
    """Apply a valid move once; rejected moves leave state unchanged."""
    if player["game_over"]:
        return "This adventure has ended. Start a new game to move again."
    destination = LOCATIONS[player["location"]].get(direction)
    if destination is None:
        return "You cannot go that way. Choose a direction from the menu."
    crossing = {player["location"], destination} == {"Old Bridge", "Lighthouse"}
    if crossing and not can_cross_bridge(player["inventory"]):
        return "The bridge is blocked. You need rope to secure the crossing."
    player["location"] = destination
    player["energy"] = max(0, player["energy"] - 1)
    if player["energy"] == 0:
        player["game_over"] = True
        return "You lose: your energy ran out before rescue arrived."
    return "You arrive at " + destination + "."


def apply_action(player, action):
    """Apply one command and return feedback; never read or print input."""
    if player["game_over"]:
        return "This adventure has ended. Start a new game to play again."
    action = action.strip().lower()
    if action in ("quit", "exit", "q"):
        player["game_over"] = True
        return "You quit the adventure. The lighthouse remains dark."
    if action == "inventory":
        return "Inventory: " + (", ".join(player["inventory"]) or "empty")
    if action == "help":
        return "Collect rope and lantern, cross the bridge, then light beacon. Moves cost 1 energy."
    if action.startswith("go "):
        return move_player(player, action[3:])
    if action.startswith("take "):
        item = action[5:]
        if item in player["inventory"]:
            return "You already collected that item."
        if ITEMS.get(player["location"]) != item:
            return "That item is not here."
        player["inventory"].append(item)
        return "You collected the " + item + "."
    if action == "light beacon":
        if player["location"] != "Lighthouse":
            return "You must reach the Lighthouse first."
        if "lantern" not in player["inventory"]:
            return "You need a lantern to light the beacon."
        if player["energy"] <= 0:
            return "You have no energy left to light the beacon."
        player["won"] = True
        player["game_over"] = True
        return "You win! The beacon shines and the rescue boat brings you home."
    return "Invalid command. Enter a menu number or one of the listed commands."
