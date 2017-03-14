from django.shortcuts import render

from settings import players_json_filename, max_players, height, width

import json

def screen(request):
    with open(players_json_filename) as f:
        players = json.load(f)

    context = {
        "height": "0"*height,
        "width": "0"*width,
        "players_left": max_players-players["players_joined"].count(True),
    }
    return render(request, 'screen/screen.html', context)