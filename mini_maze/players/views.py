from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from settings import players_json_filename
from setup import reset_all

import json

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

    players["players_joined"][int(player_id)-1] = False

    with open(players_json_filename, "w") as f:
        json.dump(players, f)

    return HttpResponse("")

def reset(request):
    reset_all()

    return HttpResponse("")

def serve(request):
    with open(players_json_filename, "r") as f:
        players = json.load(f)

    return JsonResponse(players)

@csrf_exempt
def receive(request):
    if request.method == "POST":
        data = request.POST
        
        player_id = data["player_no"]-1
        moves = data["moves"]

        with open(players_json_filename, "r") as f:
            players = json.load(f)

        if players["move_number"]%4 != player_id%4:
            return

        # Check if there are move values other than 0, 1, 2, 3, 4
        if list(filter(lambda x: x not in range(4), moves)):
            return


        players["moves"] = moves
        players["move_number"] += 1

        with open(players_json_filename, "w") as f:
            json.dump(players, f)
