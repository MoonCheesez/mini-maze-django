from django.shortcuts import render

from django.http import HttpResponse

from settings import players_json_filename
from setup import reset_all

import json

# Create your views here.
def join(request):
    with open(players_json_filename, "r") as f:
        players = json.load(f)

    try:
        i = players["players_joined"].index(False)
        players["players_joined"][i] = True

        with open(players_json_filename, "w") as f:
            json.dump(players, f)

        return HttpResponse(i+1)
    except ValueError:
        return HttpResponse("max")

def leave(request, player_id):
    with open(players_json_filename, "r") as f:
        players = json.load(f)

    players["players_joined"][player_id-1] = False

    with open(players_json_filename, "w") as f:
        json.dump(players, f)

def reset(request):
    reset_all()