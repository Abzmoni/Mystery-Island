"""Rule acceptance tests and complete terminal journeys."""

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest

from game import apply_action, available_actions, can_cross_bridge, is_win, new_game


class GameTests(unittest.TestCase):
    def setUp(self):
        self.player = new_game("Ada")

    def act(self, *commands):
        for command in commands:
            apply_action(self.player, command)

    def assert_rejected(self, command):
        before = deepcopy(self.player)
        apply_action(self.player, command)
        self.assertEqual(self.player, before)

    def test_t1_new_game(self):
        self.assertEqual(self.player, {"name": "Ada", "location": "Beach",
                         "energy": 5, "inventory": [], "game_over": False, "won": False})

    def test_t2_invalid_commands_do_not_mutate_state(self):
        for command in ("", "banana", "999", "take gold", "go", "go east west"):
            with self.subTest(command=command):
                self.assert_rejected(command)

    def test_t3_move_costs_exactly_one(self):
        self.act("go east")
        self.assertEqual(self.player["location"], "Jungle")
        self.assertEqual(self.player["energy"], 4)

    def test_t4_wrong_direction_is_free(self):
        self.assert_rejected("go west")

    def test_t5_rope_collected_once(self):
        self.act("go east", "take rope")
        self.assertEqual(self.player["inventory"], ["rope"])
        self.assertEqual(self.player["energy"], 4)
        self.assert_rejected("take rope")

    def test_t6_bridge_requires_rope(self):
        self.act("go east", "go east", "go east")
        self.assert_rejected("go east")
        self.assertFalse(can_cross_bridge(self.player["inventory"]))

    def test_t7_beacon_requires_lantern(self):
        self.act("go east", "take rope", "go east", "go east", "go east")
        self.assertEqual(self.player["location"], "Lighthouse")
        self.assert_rejected("light beacon")
        self.assertFalse(is_win(self.player))

    def test_t8_complete_winning_path(self):
        self.act("go east", "take rope", "go east", "take lantern",
                 "go east", "go east", "light beacon")
        self.assertTrue(is_win(self.player))
        self.assertTrue(self.player["game_over"])
        self.assertEqual(self.player["energy"], 1)

    def test_t9_exhaustion_and_no_negative_energy(self):
        self.act("go east", "go west", "go east", "go west", "go east")
        self.assertEqual(self.player["energy"], 0)
        self.assertTrue(self.player["game_over"])
        self.assertFalse(is_win(self.player))
        self.assert_rejected("go west")

    def test_t10_new_game_resets_independent_inventory(self):
        self.act("go east", "take rope", "quit")
        replay = new_game(self.player["name"])
        self.assertEqual(replay["energy"], 5)
        self.assertEqual(replay["location"], "Beach")
        self.assertEqual(replay["inventory"], [])
        self.assertFalse(replay["game_over"])
        replay["inventory"].append("lantern")
        self.assertEqual(self.player["inventory"], ["rope"])

    def test_lantern_collected_once(self):
        self.act("go east", "go east", "take lantern")
        self.assertEqual(self.player["inventory"], ["lantern"])
        self.assert_rejected("take lantern")

    def test_cannot_win_outside_lighthouse(self):
        self.act("go east", "take rope", "go east", "take lantern")
        self.assert_rejected("light beacon")

    def test_final_move_loses_even_on_arrival_at_lighthouse(self):
        self.player.update(location="Old Bridge", energy=1, inventory=["rope", "lantern"])
        self.act("go east")
        self.assertEqual(self.player["location"], "Lighthouse")
        self.assertTrue(self.player["game_over"])
        self.assertFalse(is_win(self.player))
        self.assert_rejected("light beacon")

    def test_normalization_and_exit(self):
        self.act("  GO EAST  ", " TAKE ROPE ", " EXIT ")
        self.assertEqual(self.player["inventory"], ["rope"])
        self.assertTrue(self.player["game_over"])
        self.assertFalse(is_win(self.player))

    def test_finished_game_rejects_every_action(self):
        self.act("quit")
        for command in ("go east", "take rope", "light beacon", "quit"):
            self.assert_rejected(command)
        self.assertEqual(available_actions(self.player), [])

    def test_information_is_free(self):
        self.assert_rejected("inventory")
        self.assert_rejected("help")


class TerminalTests(unittest.TestCase):
    def run_cli(self, commands):
        result = subprocess.run([sys.executable, "main.py"],
                                input="\n".join(commands) + "\n", text=True,
                                capture_output=True, timeout=10,
                                cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_win_with_invalid_input_and_replay_reset(self):
        output = self.run_cli(["Ada", "banana", " 1 ", "take rope", "go east",
                               "take lantern", "go east", "go east", "light beacon",
                               "maybe", " YES ", "inventory", " EXIT ", "n"])
        self.assertIn("Invalid command", output)
        self.assertIn("You win!", output)
        self.assertIn("Please enter y or n", output)
        self.assertIn("Inventory: empty", output)
        self.assertIn("You quit", output)
        self.assertEqual(output.count("Welcome, Ada!"), 2)
        self.assertIn("Beach | Energy: 5/5", output.split("You win!")[1])

    def test_losing_terminal_path(self):
        output = self.run_cli(["Ada", "go east", "go west", "go east",
                               "go west", "go east", "n"])
        self.assertIn("You lose:", output)
        self.assertIn("Play again?", output)

    def test_blank_name_and_end_of_input(self):
        output = self.run_cli([""])
        self.assertIn("Welcome, Explorer!", output)
        self.assertIn("Input closed", output)


if __name__ == "__main__":
    unittest.main()
