from django.test import TestCase

from settings import players_json_filename, maze_json_filename, max_players
import json

class PlayersJSONTest(TestCase):
    def setUp(self):
        self.players_json = json.load(players_json_filename)
        self.maze_json = json.load(maze_json_filename)

    def test_have_fields(self):
        self.assertIsNotNone(self.players_json["player_positions"])
        self.assertIsNotNone(self.players_json["players_joined"])
        self.assertIsNotNone(self.players_json["move_number"])
        self.assertIsNotNone(self.players_json["moves"])

    def test_players_have_x_and_y_position(self):
        for player in self.players_json["player_positions"]:
            self.assertEqual(len(player), 2)

    def test_players_not_in_walls(self):
        for player in self.players_json["player_positions"]:
            x = player[0]
            y = player[1]

            # 0 is a wall
            self.assertNotEqual(self.maze_json["maze"][y][x], 0)

    def test_players_joined_within_settings_limits(self):
        self.assertTrue(self.players_json["players_joined"] <= max_players)

