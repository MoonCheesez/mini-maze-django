from settings import maze_json_filename, players_json_filename

import json

def reset_players_json():
    players = {
        "player_positions": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "players_joined": 0,
        "move_number": 0,
        "moves": []
    }

    with open(players_json_filename, "w") as f:
        json.dump(players, f)


def reset_maze_json():
    maze = {
        "maze": [[1]*32]*32
    }

    with open(maze_json_filename, "w") as f:
        json.dump(maze, f)


if __name__ == '__main__':
    setup_players_json()
    setup_maze_json()