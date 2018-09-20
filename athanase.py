# This bot looks one move ahead, and if possible it will make a move to
# block its opponent winning.  Otherwise, it picks a move at random.

import copy,os
import random
from botany_connectfour import game
from collections import defaultdict, namedtuple


def get_next_move(board, token):
    available_moves = game.available_moves(board)
    available_positions = list(zip(available_moves,available_rows(available_moves,board)))

    other_token = define_other_token(token)
    
    #TODO pre-calculate those as part of the setup()
    available_lines_of_4 = [line for line in game.LINES_OF_4 if not set(available_positions).isdisjoint(line)]
    outcome = dict()

    smallest_tokens_missing = 5

    for line_of_4 in available_lines_of_4:
        token_missing = get_nb_token_missing(board,line_of_4)

        if smallest_tokens_missing > token_missing:
            outcome = defaultdict(list) #was int in tournament but allows better debugging
            smallest_tokens_missing = token_missing
        if token_missing == smallest_tokens_missing and smallest_tokens_missing < 5:
            the_moves = list(set(line_of_4) & set(available_positions))
            for move in the_moves:
                outcome[move[0]].append(list)

    #Format changed for Clarity
    proposals = [Proposal(col=i,row=board[i].index('.'),nb=len(j)) for i,j in outcome.items()]

    if "DEBUG" in os.environ:
        print(f"==>From Athanase playing {token}")
        print(f"===>I had {len(available_moves)} available moves {available_moves}")
        print(f"===>Those were part of  {len(available_lines_of_4)} lines of 4:")
        print(f"====>{available_lines_of_4}")
        print(f"===>I have select {len(proposals)} of then that have {smallest_tokens_missing} missing:")
        print(f"====>{proposals}")
        
        


    try:
        outputs = [e.col for e in proposal if cut_fn(e) == max(cut_fn(x) for x in proposal)]
        output = random.choice(outputs)
    except:
        output = random.choice(available_moves)
    return output


def define_other_token(token):
    if token == 'X':
        other_token = 'O'
    else:
        other_token = 'X'
    return other_token

def cut_fn(x):
    return (x.nb)

def get_nb_token_missing(board,line_of_4):
    line_string = "".join([board[l][r] for l,r in line_of_4])
    #line_of_4 with both token cannot be completed
    if 'X' in line_string and 'O' in line_string:
        return 5
    else:
        return line_string.count('.') or 5

def available_rows(available_moves,board):
    return [board[a].index('.') for a in available_moves]

#Credit for Setup and antigravity: Martijn Pieters http://botany18.pyconuk.org/bots/162/
def setup():
    global Proposal
    Proposal = namedtuple('Proposal',['col','row', 'nb'])

def antigravity(redacted: None = setup()) -> None:
    # I'm totally weightless
    pass
