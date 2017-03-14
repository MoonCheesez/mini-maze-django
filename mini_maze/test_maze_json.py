from django.test import TestCase

from settings import height, width, maze_json_filename
from setup import reset_maze_json

import json

class MazeJSONTest(TestCase):
    def setUp(self):
        reset_maze_json()

        with open(maze_json_filename, "r") as f:
            self.maze_json = json.load(f)

    def test_have_fields(self):
        self.assertIsNotNone(self.maze_json["maze"])

    def test_maze_values(self):
        for y in self.maze_json["maze"]:
            for x in y:
                self.assertIn(x, [0, 1])

    def test_dimensions(self):
        self.assertEqual(len(self.maze_json["maze"]), height)
        for row in self.maze_json["maze"]:
            self.assertEqual(len(row), width)