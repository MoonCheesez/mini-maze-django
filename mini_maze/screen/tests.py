from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from settings import height, width, max_players, players_json_filename
from setup import reset_all

from screen.views import screen

import json

def setup_players_joined_json(players_joined):
    with open(players_json_filename) as f:
        players_json = json.load(f)

    players_json["players_joined"] = players_joined
    
    with open(players_json_filename, "w") as f:
        json.dump(players_json, f)

class ScreenTest(TestCase):
    def setUp(self):
        reset_all()

    def test_root_url_resolves_to_screen_page_view(self):
        root = resolve('/')
        self.assertEqual(root.func, screen)

    def test_returns_correct_skeleton_html(self):
        response = screen(HttpRequest())
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<!DOCTYPE html>\n<html>'))
        self.assertIn('<title>Mini Maze</title>', html)

        self.assertTrue(html.endswith('</html>'))

    def test_returns_correct_html_for_different_number_of_players(self):
        # Tesf 0 to before maximum number of players
        for no_of_players in range(max_players):
            players_joined = [True]*no_of_players
            players_joined.extend([False]*(max_players-no_of_players))

            setup_players_joined_json(players_joined)

            response = screen(HttpRequest())
            html = response.content.decode('utf8')

            self.assertIn('<h1>Waiting for {0} more players to join...</h1>'
                .format(max_players-no_of_players), html)

            self.assertIn('<section id="waiting">', html)

            self.assertNotIn('<section id="maze>', html)
            self.assertNotIn('<tr>', html)
            self.assertNotIn('<td>', html)

        # Test maximum number of players
        setup_players_joined_json([True]*max_players)
        response = screen(HttpRequest())
        html = response.content.decode('utf8')

        self.assertIn('<section id="maze">', html)
        
        self.assertEqual(html.count('<tr>'), height+max_players)
        self.assertEqual(html.count('<td'), width*height + max_players*2)

        self.assertNotIn('<h1>Waiting for ', html)
        self.assertNotIn(' more players to join...</h1>', html)
        self.assertNotIn('<section id="waiting">', html)