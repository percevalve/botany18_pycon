# This bot looks one move ahead, and if possible it will make a move to
# block its opponent winning.  Otherwise, it picks a move at random.

import copy
import random
from botany_connectfour import game
from collections import defaultdict

def cut_fn(x):
    return (-x[2],x[3],x[4],x[5])

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

def get_letter_of_pos(position,board):
    col, row = position
    return board[col][row]


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

def get_his_deadly_traps(board,the_lines,best,the_toten):
    traps = list()
    for line in the_lines:
        remaining, letter = remaining_to_win(board,line,the_toten)

        if remaining == 1 and letter != the_toten:
            traps.append(line)
    return traps


def select_for_victory(board,outcome_assign,proposals,token):
    for column,_,_,_,_,_ in proposals:
        if outcome_assign.get(column) == token:
            print("finally nailing it=======>",token,column)
            print(game.render_text(board))
            return column
    print("not nailing it=======>",token,column)
    print(game.render_text(board))
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
            outcome = defaultdict(list)
            outcome_assign = defaultdict()
            best = remaining

        if best == remaining:
            the_moves = list(set(line) & set(available_play))
            for move in the_moves:
                outcome[move[0]].append(list)
                if letter == token:
                    outcome_assign[move[0]] = letter

                
    #tuple number of line_4, row, cols
    proposals = [(i,board[i].index('.'),9,0,0,len(j)) for i,j in outcome.items()]

    if best == 1:
        return select_for_victory(board,outcome_assign,proposals,token)        
    
    traps = get_traps(board,game.LINES_OF_4,best,token)
       #Do not fall in a trap.
    proposals_minus_traps = [prop for prop in proposals if not any((prop[0],prop[1]+1) in trap for trap in traps)]
    friendly_traps = get_his_deadly_traps(board,game.LINES_OF_4,best,other_token)
    available_traps = set(pos for trap in friendly_traps for pos in trap if get_letter_of_pos(pos,board) == ".")
    enemy_traps = get_his_deadly_traps(board,game.LINES_OF_4,best,token)
    available_enemy_traps = set(pos for trap in enemy_traps for pos in trap if get_letter_of_pos(pos,board) == ".")
    
    print("outcome",outcome,outcome_assign,best)
    print("athanase => proposals ==>",proposals)
    print("athanase => traps ======>",traps)
    print("athanase => proposals_minus_traps =>",proposals_minus_traps)
    


    for move in available_moves:
        sequence_play = set([a[1] - board[a[0]].index('.') for a in available_traps if a[0] == move])
        separation = len(set(a%2 for a in sequence_play))
        no_enemy = True
        if len(set([a[1] - board[a[0]].index('.') for a in available_enemy_traps if a[0] == move])):
            first_enemy = min(set([a[1] - board[a[0]].index('.') for a in available_enemy_traps if a[0] == move]))
            print("+++++++++=+=>",min(sequence_play),first_enemy)
            print(enemy_traps)
            print("==============>",sequence_play)
            print(game.render_text(board))
            if min(sequence_play) == first_enemy:
                no_enemy = False
        if len(sequence_play) > 1 and separation == 2 and no_enemy:
            print("nailing it=======>",available_traps)
            print(enemy_traps)
            print("nailing it=======>",token,move)
            print("==============>",sequence_play)
            print(game.render_text(board))

            return move

    
    #We have a choice, let's see if we can set a trap
    if len(traps) > 1:
        board1 = copy.deepcopy(board)
        improved_proposals = list()
        only_him = set((row,col) for row,col in available_play if not any((row,col+1) in trap for trap in traps)) - set((row,col) for row,col,_,_,_,_ in proposals)

        if len(enemy_traps)>0 and len(friendly_traps) == 0:
            for col,row in only_him:
                board1[col][row] = other_token
                new_enemy_traps = get_his_deadly_traps(board1,(enemy_traps+possible),best,token)
                all_new_traps = set(pos for trap in new_enemy_traps for pos in trap if get_letter_of_pos(pos,board1) == ".")
                new_traps = all_new_traps - available_enemy_traps
                if len(new_traps) > 0:
                    potential_traps = (all_new_traps.union(available_enemy_traps))
                    
                    sequence_play = [a[1] - board[a[0]].index('.') for a in potential_traps]
                    if len(potential_traps)>0:
                        next_one = min(sequence_play)
                    else:
                        next_one = 9
                    order = len(set(a%2 for a in sequence_play))
                    improved_proposals.append((col,row,next_one,order,len(new_traps),0))
                board1[col][row] = '.'

        for col,row,_,_,_,remaining in proposals_minus_traps:
            board1[col][row] = token
            new_friendly_traps = get_his_deadly_traps(board1,(traps+possible),best,other_token)
            all_new_traps = set(pos for trap in new_friendly_traps for pos in trap if get_letter_of_pos(pos,board1) == ".")
            new_traps = all_new_traps - available_traps
            potential_traps = (all_new_traps.union(available_traps))
            
            sequence_play = [a[1] - board[a[0]].index('.') for a in potential_traps]
            if len(potential_traps)>0:
                next_one = min(sequence_play)
            else:
                next_one = 9
            order = len(set(a%2 for a in sequence_play))
            improved_proposals.append((col,row,next_one,order,len(new_traps),remaining))
            board1[col][row] = '.'
        if len(improved_proposals):
            proposals_minus_traps = improved_proposals

    outputs = list()
    if len(proposals_minus_traps):
        outputs = [e[0] for e in proposals_minus_traps if e == max(proposals_minus_traps,key=cut_fn)]
    if len(outputs) == 0:
        outputs = available_moves
    
    outputs = [move for move in outputs if not any((move,board[move].index('.')+1) in trap for trap in enemy_traps)]
    print("athanase => outputs =>",outputs)
    try:
        output = random.choice(outputs)
    except:
        output = random.choice(available_moves)
    return output
