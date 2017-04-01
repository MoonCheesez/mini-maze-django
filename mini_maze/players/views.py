from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from settings import players_json_filename, maze_json_filename, height, width
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
        
        player_id = int(data["player_no"])-1
        moves = [int(x) for x in data["moves"]]

        with open(players_json_filename, "r") as f:
            players = json.load(f)
        with open(maze_json_filename, "r") as f:
            maze = json.load(f)["maze"]

        if False in players["players_joined"]:
            return HttpResponse("")

        if players["move_number"]%4 != player_id%4:
            return HttpResponse("")

        # Check if there are move values other than 0, 1, 2, 3, 4
        if list(filter(lambda x: x not in range(4), moves)):
            return HttpResponse("")

        """
        0 - up
        1 - left
        2 - right
        3 - down
        """
        player_pos = players["player_positions"][player_id]

        dx = [0, -1, 1, 0]
        dy = [-1, 0, 0, 1]

        for i in range(len(moves)):
            move = moves[i]

            nx = player_pos[0] + dx[move]
            ny = player_pos[1] + dy[move]

            if (nx >= 0 and nx < width and ny >= 0 and ny < height and
                    maze[ny][nx] != 0):
                player_pos[0] = nx
                player_pos[1] = ny
            else:
                moves[i] *= -1

        players["moves"] = moves
        players["move_number"] += 1

        with open(players_json_filename, "w") as f:
            json.dump(players, f)

        return HttpResponse("")
