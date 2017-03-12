from settings import height, width, joined_players, max_players

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from screen.views import screen

class ScreenTest(TestCase):
    def test_root_url_resolves_to_screen_page_view(self):
        root = resolve('/')
        self.assertEqual(root.func, screen)

    def test_screen_page_returns_correct_html(self):
        request = HttpRequest()
        response = screen(request)
        html = response.content.decode('utf8')

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Mini Maze</title>', html)

        if joined_players() == max_players:
            self.assertIn('<section id="maze">', html)
            
            self.assertEqual(html.count('<tr>'), height)
            self.assertEqual(html.count('<td>'), width)
        else:
            self.assertIn('<h1>Waiting for {0} more players to join...</h1>'
                .format(max_players-joined_players()), html)

            self.assertIn('<section id="waiting">', html)

        self.assertTrue(html.endswith('</html>'))