from django.test import TestCase
from django.http import HttpRequest

from views import join, leave, reset

from settings import players_json_filename, max_players
import json

class PlayersJoinTest(TestCase):
    def fetch_players_joined(self):
        players_json = json.load(players_json_filename)
        return players_json["players_joined"]

    def setup_players_joined_json(self, players_joined):
        players_json = json.load(players_json_filename)
        players_json["players_joined"] = players_joined
        json.dump(players_json, open(players_json_filename, "w"))

    def test_reset_players(self):
        join(HttpRequest())

        before = fetch_players_joined()
        reset(HttpRequest())
        after = fetch_players_joined()
        
        self.assertNotEqual(before, after)

    def test_player_joins_and_gets_id(self):
        # List of players joined from
        # [False, False, False, False] to [True, False, False, False]
        setup_players_joined_json([False]*4)

        response = join(HttpRequest())

        self.assertEqual(response, "1")

        # [True, False, True, False] to [True, True, True, False]
        setup_players_joined_json([True, False, True, False])

        response = join(HttpRequest())

        self.assertEqual(response, "2")

    def test_disallow_player_join_after_maximum_players_reached(self):
        setup_players_joined_json([True]*4)

        response = join(HttpRequest())

        self.assertEqual(response, "max")
        self.assertEqual(fetch_players_joined(), [True]*4)
