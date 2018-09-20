# This bot looks one move ahead, and if possible it will make a move to
# block its opponent winning.  Otherwise, it picks a move at random.

import copy
import random
from botany_connectfour import game
from collections import defaultdict

def cut_fn(x):
    return (x[0])

def remaining_to_win(board,line,token):
    line_string = "".join([board[l][r] for l,r in line])
    if 'X' in line_string and 'O' in line_string:
        return (5,token)
    else:
        letters = line_string.replace('.','')
        letter = token
        if len(letters)> 0:
            letter = letters[0]
        return (line_string.count('.') or 5,letter)

def get_traps(board,the_lines,best,token):
    dict_traps = defaultdict(list)
    for line in the_lines:
        dict_traps[remaining_to_win(board,line,token)[0]].append(line)
    if min(dict_traps.keys()) == 1:
        return dict_traps[1]
    output = list()
    for i in [key for key in dict_traps.keys() if key<best]:
        output += dict_traps[i]
    return output

def get_his_deadly_traps(board,the_lines,best,token):
    traps = list()
    for line in the_lines:
        remaining, letter = remaining_to_win(board,line,token)
        if remaining == 1 and letter != token:
            traps.append(line)
    return traps


def select_for_victory(board,outcome_assign,proposals,token):
    for _, _, column in proposals:
        if outcome_assign.get(column) == token:
            return column
    return column

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
        remaining, letter = remaining_to_win(board,line,token)
        if remaining == 5:
            continue

        if best > remaining:
            outcome = defaultdict(int)
            outcome_assign = defaultdict()
            best = remaining

        if best == remaining:
            the_moves = list(set(line) & set(available_play))
            for move in the_moves:
                outcome[move[0]] += 1
                if letter == token:
                    outcome_assign[move[0]] = letter

                
    #tuple number of line_4, row, cols
    proposals = list((j,board[i].index('.'),i) for i,j in outcome.items())

    if best == 1:
        return select_for_victory(board,outcome_assign,proposals,token)        
    
    traps = get_traps(board,game.LINES_OF_4,best,token)
    proposals_minus_traps = [prop for prop in proposals if not any((prop[2],prop[1]+1) in trap for trap in traps)]
    outputs = [e[2] for e in proposals_minus_traps if cut_fn(e) == max(cut_fn(x) for x in proposals_minus_traps)]

    outputs = outputs or [avail[0] for avail in available_play if not any((avail[0],avail[1]+1) in trap for trap in traps)]
    if len(outputs) == 0:
        deadly_traps = get_his_deadly_traps(board,game.LINES_OF_4,best,token)
        outputs = [avail[0] for avail in available_play if not any((avail[0],avail[1]+1) in trap for trap in deadly_traps)] 
    outputs = outputs or available_moves
    try:
        output = random.choice(outputs)
    except:
        output = random.choice(available_moves)
    return output
