from django.shortcuts import render

from settings import players_json_filename, max_players, height, width

def player_control(request, player_no):
    context = {
        "height": "0"*int(height/2),
        "width": "0"*int(width/2),
        "player_no": player_no
    }
    return render(request, 'player_control/player_control.html', context)