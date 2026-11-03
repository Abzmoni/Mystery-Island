# Mystery Island — The Lost Lighthouse

A Python terminal adventure: wake up after a storm, collect supplies, secure an old bridge, and restore the lighthouse beacon before you run out of energy.

## Setup and running

Python 3.10 or newer is required. Tested with Python 3.13.5. There are no packages to install.

```sh
git clone https://github.com/Abzmoni/Mystery-Island.git
cd Mystery-Island
python main.py
```

If your system uses `python3`, substitute it for `python` in these commands.

## Map and rules

```text
Beach <-> Jungle <-> Cave <-> Old Bridge <-> Lighthouse
           rope     lantern       rope required ->
```

Going east moves right on the map; going west moves left. The player starts on the Beach with 5 energy and an empty inventory. Each successful move consumes exactly 1 energy, including backwards moves. Arriving with 0 energy ends the game immediately with a loss, even at the Lighthouse. Energy never becomes negative.

Collect rope in the Jungle and a lantern in the Cave. Each item can be collected only once. Pickups cost no energy. Crossing between the Old Bridge and Lighthouse requires rope. Lighting the beacon requires being at the Lighthouse, carrying the lantern, and having energy remaining. Rope is retained after crossing. There is no separate key puzzle: securing the broken bridge mechanism with rope unlocks the crossing.

Three decisions matter: collect or leave the rope, collect or leave the lantern, and advance or spend limited energy backtracking. Missing an item blocks progress; going back may cost the remaining energy. There are no random events, combat, or hidden energy costs.

Invalid commands, unavailable directions, blocked crossings, repeated pickups, inventory, and help do not change energy. The same state and action always produce the same result. After win, loss, or quit, no more actions change that game's state. Replay creates a fresh state and inventory, retaining only the player's name.

## Controls

Choose a displayed menu number or type its command. Numbers depend on the current room, so read the menu each time.

| Command | Meaning |
| --- | --- |
| `go east` / `go west` | Move along an available connection |
| `take rope` / `take lantern` | Collect an item in its room |
| `light beacon` | Signal rescue from the Lighthouse |
| `inventory` | Show collected items |
| `help` | Show the objective |
| `quit`, `exit`, `q` | End the current adventure |

Leading/trailing spaces and case are ignored: ` EXIT ` works. Blank or unrecognised commands show a retry message. A blank name becomes Explorer. Replay accepts `y`/`yes` or `n`/`no`; quit aliases also decline replay. End-of-input and Ctrl+C exit cleanly.

## Demonstrations

Winning inputs after entering your name:

```text
go east
take rope
go east
take lantern
go east
go east
light beacon
n
```

The player reaches Jungle at 4 energy, Cave at 3, Old Bridge at 2, and Lighthouse at 1. The final action prints `You win! The beacon shines and the rescue boat brings you home.`

Losing inputs after entering your name:

```text
go east
go west
go east
go west
go east
n
```

The fifth move prints `You lose: your energy ran out before rescue arrived.`

Invalid-input demonstration: enter `banana` at the Beach. The game prints a helpful error and still shows Beach with 5 energy. Then enter ` 1 ` to move to the Jungle with 4 energy. To demonstrate replay, quit, answer `y`, and inspect your inventory: it is empty at the Beach with 5 energy.

## Tests

```sh
python -m unittest discover -s tests -v
```

All 19 tests passed on Python 3.13.5. The tests cover T1–T10, duplicate lantern pickup, winning only at the lighthouse, losing on the final move, case/space handling, immutable finished games, free information commands, and actual CLI sessions for win/loss/replay/EOF. Full captured output is in [test-output.txt](evidence/test-output.txt).

## Function guide

The state dictionary groups name, location, integer energy, inventory list, and the boolean `game_over` and `won` flags. The CLI holds that state between input prompts. Rules have no terminal I/O, so tests can call them directly. Rule functions deliberately mutate the passed player dictionary; they are deterministic, not immutable transformations.

| Function | Responsibility |
| --- | --- |
| `new_game(name)` | Return a fresh state and independent inventory |
| `can_cross_bridge(inventory)` | Return a boolean indicating rope possession |
| `is_win(player)` | Return the win flag |
| `available_actions(player)` | Return current room commands |
| `move_player(player, direction)` | Validate a connection and gate, then charge one energy and check loss |
| `apply_action(player, action)` | Normalise and dispatch commands; return feedback |
| `choose_action(actions)` | Display the menu and read a number or command |
| `play_game(name)` | Repeat turns until `game_over` becomes true |
| `ask_replay()` | Validate the replay answer and return a boolean |
| `main()` | Display instructions, read the name, manage replay and terminal interruption |

## Limits and review

This is a small single-player terminal game without saves, random events, external services, or graphics. Command phrases use the documented spelling and internal spacing. Functions expect a state created by `new_game`; arbitrary corrupt dictionaries are not a supported interface. The game does not verify a learner's understanding. The [learning notes and defence](LEARNING.md) explain the main choices. Peer or mentor review is still pending; no independent review is claimed.
