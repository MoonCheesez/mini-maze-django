from settings import *

import json
import random

def generate_maze(mx, my, pos, endpos):
    maze = [[0 for x in range(mx)] for y in range(my)]

    while maze[endpos[1]][endpos[0]] != 1:
        maze = [[0 for x in range(mx)] for y in range(my)]
        dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]

        cx, cy = pos
        maze[cy][cx] = 1; stack = [(cx, cy, 0)]

        while len(stack) > 0:
            (cx, cy, cd) = stack[-1]
            if len(stack) > 2:
                if cd != stack[-2][2]: dirRange = [cd]
                else: dirRange = range(4)
            else: dirRange = range(4)

            nlst = []
            for i in dirRange:
                nx = cx + dx[i]; ny = cy + dy[i]
                if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                    if maze[ny][nx] == 0:
                        ctr = 0
                        for j in range(4):
                            ex = nx + dx[j]; ey = ny + dy[j]
                            if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                                if maze[ey][ex] == 1: ctr += 1
                        if ctr == 1: nlst.append(i)

            if len(nlst) > 0:
                ir = nlst[random.randint(0, len(nlst) - 1)]
                cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 1
                stack.append((cx, cy, ir))
            else: stack.pop()

    return maze

def reset_players_json():
    player_positions = [
        (0, 0),
        (width-1, 0),
        (width-1, height-1),
        (0, height-1)
    ]

    players = {
        "player_positions": player_positions,
        "players_joined": [False]*max_players,
        "move_number": 0,
        "moves": []
    }

    with open(players_json_filename, "w") as f:
        json.dump(players, f)


def reset_maze_json():
    maze = {}

    submaze_height = int(height/2)
    submaze_width = int(width/2)

    submaze_dimension = (submaze_height-1, submaze_width-1)
    m1 = generate_maze(submaze_height, submaze_width, (0, 0), submaze_dimension)
    m2 = generate_maze(submaze_height, submaze_width, (submaze_width-1, 0), (0, submaze_height-1))
    m3 = generate_maze(submaze_height, submaze_width, (0, submaze_height-1), (submaze_width-1, 0))
    m4 = generate_maze(submaze_height, submaze_width, submaze_dimension, (0, 0))

    # Combine mazes
    m = m1
    for y in range(submaze_width):
        m[y].extend(m2[y])
        m3[y].extend(m4[y])
    m.extend(m3)

    maze["maze"] = m

    with open(maze_json_filename, "w") as f:
        json.dump(maze, f)

def reset_all():
    reset_players_json()
    reset_maze_json()