from django.test import TestCase
from django.http import HttpRequest

from django.core.urlresolvers import resolve

from players.views import join, leave, reset, serve, receive

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

    def test_join_resolves_to_join_view(self):
        r = resolve('/join/')
        self.assertEqual(r.func, join)

    def test_leave_resolves_to_leave_view(self):
        r = resolve('/leave/1')
        self.assertEqual(r.func, leave)

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

class PlayersJSONServedTest(TestCase):
    def setUp(self):
        reset_all()

    def test_players_resolves_to_players_view(self):
        r = resolve('/players')
        self.assertEqual(r.func, serve)

    def test_json_served_same(self):
        # Very basic test that covers a small case
        raw = serve(HttpRequest()).content.decode('utf8')
        players = json.loads(raw)

        with open(players_json_filename, "r") as f:
            self.assertEqual(players, json.load(f))


        setup_players_joined_json([True, False, False, False])
        raw = serve(HttpRequest()).content.decode('utf8')
        players = json.loads(raw)

        with open(players_json_filename, "r") as f:
            self.assertEqual(players, json.load(f))

def move_player(player_id, moves):
    request = HttpRequest()
    request.method = "POST"
    request.POST = {
        "player_no": player_id,
        "moves": moves
    }

    receive(request)

class PlayersMoveReceivedTest(TestCase):
    def setUp(self):
        reset_all()

    def test_maze_resolves_to_receive_view(self):
        r = resolve('/maze/')
        self.assertEqual(r.func, receive)

    def test_player_move_reflected_on_response(self):
        valid_tests_data = [
            (1, [0, 1, 2, 3]),
            (2, [2, 3, 1, 0]),
            (3, [0, 0, 1, 3, 2]),
            (4, [1])
        ]

        for test in valid_tests_data:
            player_id = test[0]
            moves = test[1]

            move_player(player_id, moves)

            with open(players_json_filename, "r") as f:
                players = json.load(f)

            self.assertEqual(players["moves"], moves)
            self.assertEqual(players["move_number"]%4, player_id%4)

        reset_all()

        invalid_test_data = [
            (2, [0]),
            (4, [1]),
            (3, [2]),
            (-1, [3]),
            (1, [10]),
        ]

        with open(players_json_filename, "r") as f:
            players_default = json.load(f)

        for test in invalid_test_data:
            player_id = test[0]
            moves = test[1]

            move_player(player_id, moves)

            with open(players_json_filename, "r") as f:
                players_after = json.load(f)

            self.assertEqual(players_default, players_after)
