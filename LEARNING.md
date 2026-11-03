# Learning log and defence

## Entry 1 — Input strings and validation

**Topic:** Text input and menu choices.

**Explanation:** `input()` returns a string. I can compare a cleaned string to menu numbers without converting arbitrary input to an integer. `strip()` removes outer whitespace, and `lower()` makes commands case-insensitive.

**Experiment:** I tested `banana`, a blank command, and `999` against the rules and checked that the entire player dictionary stayed unchanged. The terminal test entered ` 1 ` and continued through a winning game. It also entered ` EXIT ` after replay.

**Conclusion:** Validation should happen before a state change. Menu numbers can remain strings. This avoids a `ValueError` from converting a word such as `banana` to an integer.

## Entry 2 — Lists, replay, and independent state

**Topic:** Creating a new inventory for each adventure.

**Explanation:** A list can be shared by two dictionaries if both refer to the same list. A fresh `[]` inside `new_game()` creates a separate inventory for every call.

**Experiment:** I collected rope, quit, and created another player using the same name. I checked that the new player started at the Beach with 5 energy and an empty inventory. I appended a lantern to the new player's inventory and confirmed that the first player still had only rope. The CLI test also replayed and printed an empty inventory.

**Conclusion:** Resetting a location is not enough for replay. The whole state must be newly created, including the inventory list.

## Defence

**Why a list for inventory?** There are only two items. A list keeps collection order, supports `append`, and makes membership checks readable. Before adding an item, I check whether it is already `in` the list.

**What stops the loop?** `play_game` repeats while `not player['game_over']`. Winning, losing, or quitting sets that flag to true. The outer replay loop stops when `ask_replay()` returns false.

**Which function returns a value instead of printing?** `can_cross_bridge(inventory)` returns `True` or `False`. This lets the movement rule decide what to do and makes the condition easy to test separately. `print()` displays something; `return` hands a value back to the caller.

**What edge case did I check?** Reaching the Lighthouse on the last energy point must lose immediately. The test places the player at the Old Bridge with both items and 1 energy, crosses, then attempts to light the beacon. The player remains defeated. This protects against checking victory before energy exhaustion.

**What evidence supports correctness?** The suite contains 19 passing tests, including real terminal runs through subprocesses. It checks state changes as well as messages. One successful manual route alone would not prove that replay, invalid input, and exhausted players work.

**What still needs review?** Another person should run the commands, read the rules, and ask me to trace a turn. Automated tests do not establish individual understanding.

## Reflection

The concept I understand now that I didn't before is the difference between displaying a value and returning one. A function that returns a boolean lets another function make a decision and lets a test inspect the result directly. Separating the input loop from the game rules also makes it possible to test a full adventure without typing each command manually. I can trace each turn as input, validation, state change, and feedback.
