# This bot looks one move ahead, and if possible it will make a move to
# block its opponent winning.  Otherwise, it picks a move at random.

import copy
import random
from botany_connectfour import game
from collections import defaultdict

def cut_fn(x):
    return (x[0])

def remaining_to_win(board,line):
    line_string = "".join([board[l][r] for l,r in line])
    if 'X' in line_string and 'O' in line_string:
        return 5
    else:
        return line_string.count('.') or 5

def get_next_move(board, token):
    available_moves = game.available_moves(board)
    available_position = [(a,board[a].index('.')) for a in available_moves]
    available_play = available_position


    if token == 'X':
        other_token = 'O'
    else:
        other_token = 'X'

    possible = [line for line in game.LINES_OF_4 if not set(available_position).isdisjoint(line)]
    outcome = dict()

    best = 5

    for line in possible:
        # line_string = "".join([board[l][r] for l,r in line])
        # if 'X' in line_string and 'O' in line_string:
        #     continue
        # remaining = line_string.count('.')
        remaining = remaining_to_win(board,line)

        if best > remaining:
            outcome = defaultdict(int)
            best = remaining
        if best == remaining and remaining < 5:
            the_moves = list(set(line) & set(available_play))
            for move in the_moves:
                outcome[move[0]] += 1

    proposal = list((j,board[i].index('.'),i) for i,j in outcome.items())


    try:
        outputs = [e[2] for e in proposal if cut_fn(e) == max(cut_fn(x) for x in proposal)]
        output = random.choice(outputs)
    except:
        output = random.choice(available_moves)
    return output
