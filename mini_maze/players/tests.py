from django.test import TestCase
from django.http import HttpRequest

from players.views import join, leave, reset

from settings import players_json_filename, max_players
from setup import reset_all

import json

def fetch_players_joined():
    with open(players_json_filename) as f:
        players_json = json.load(f)
    return players_json["players_joined"]

def setup_players_joined_json(players_joined):
    with open(players_json_filename) as f:
        players_json = json.load(f)

    players_json["players_joined"] = players_joined
    
    with open(players_json_filename, "w") as f:
        json.dump(players_json, f)

class PlayersJoinAndLeaveTest(TestCase):
    def setUp(self):
        reset_all()

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

        response = join(HttpRequest()).content.decode('utf8')

        self.assertEqual(response, "1")

        # [True, False, True, False] to [True, True, True, False]
        setup_players_joined_json([True, False, True, False])

        response = join(HttpRequest()).content.decode('utf8')

        self.assertEqual(response, "2")

    def test_disallow_player_join_after_maximum_players_reached(self):
        setup_players_joined_json([True]*4)

        response = join(HttpRequest()).content.decode('utf8')

        self.assertEqual(response, "max")
        self.assertEqual(fetch_players_joined(), [True]*4)

    def test_player_with_correct_id_leaves(self):
        setup_players_joined_json([True]*4)

        leave(HttpRequest(), 2)
        self.assertEqual(fetch_players_joined(), [True, False, True, True])

        leave(HttpRequest(), 3)
        self.assertEqual(fetch_players_joined(), [True, False, False, True])

        leave(HttpRequest(), 1)
        self.assertEqual(fetch_players_joined(), [False, False, False, True])
