"""
Handling the AI moves.
"""
import random

from AI.Greedy import findMoveGreedy
from AI.MiniMax import findMoveMinimax
from AI.Negamax import findMoveNegaMaxAlphaBeta
from AI.Negascout import findMoveNegascout

from AI.Score import  *
    
def findBestMove(game_state, valid_moves, return_queue, algorithm_option):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    if(algorithm_option == 'Greedy'):
        findMoveGreedy(game_state, valid_moves, 1 if game_state.white_to_move else -1)
    elif (algorithm_option == 'Minimax'):
        findMoveMinimax(game_state, valid_moves, DEPTH, game_state.white_to_move, -CHECKMATE, CHECKMATE,)  
    elif (algorithm_option == 'Negamax'):
        findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)     
    elif (algorithm_option == 'Negascout'):
        findMoveNegascout(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1) 
    return_queue.put(next_move)


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)
