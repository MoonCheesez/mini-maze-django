from django.shortcuts import render

from settings import players_json_filename, max_players, height, width

def player_control(request):
    context = {
        "height": "0"*height,
        "width": "0"*width,
    }
    return render(request, 'player_control/player_control.html', context)