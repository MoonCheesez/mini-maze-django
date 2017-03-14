from django.test import TestCase

from settings import *
from setup import reset_all

import json

class PlayersJSONTest(TestCase):
    def setUp(self):
        reset_all()

        with open(players_json_filename, "r") as f:
            self.players_json = json.load(f)

        with open(maze_json_filename, "r") as f:
            self.maze_json = json.load(f)

    def test_have_fields(self):
        fields = [
            "player_positions",
            "players_joined",
            "move_number",
            "moves"
        ]

        for field in fields:
            self.assertIsNotNone(self.players_json[field])

        self.assertEqual(len(self.players_json["player_positions"]), max_players)

    def test_fields_correct_type(self):
        # This only checks the top layer
        self.assertIsInstance(self.players_json["player_positions"], list)
        self.assertIsInstance(self.players_json["players_joined"], list)
        self.assertIsInstance(self.players_json["move_number"], int)
        self.assertIsInstance(self.players_json["moves"], list)

    def test_players_have_x_and_y_position(self):
        for player in self.players_json["player_positions"]:
            self.assertEqual(len(player), 2)

    def test_players_in_maze(self):
        for position in self.players_json["player_positions"]:
            x = position[0]
            y = position[1]

            self.assertLess(x, width)
            self.assertLess(y, height)

    def test_players_not_in_walls(self):
        for position in self.players_json["player_positions"]:
            x = position[0]
            y = position[1]

            # 0 is a wall
            self.assertNotEqual(self.maze_json["maze"][y][x], 0)

    def test_players_unique_positions(self):
        positions = [tuple(x) for x in self.players_json["player_positions"]]
        self.assertEqual(len(set(positions)),
            len(self.players_json["player_positions"]))

    def test_players_joined_within_settings_limits(self):
        self.assertEqual(len(self.players_json["players_joined"]), max_players)
