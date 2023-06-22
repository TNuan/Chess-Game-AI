from AI.Score import *

count = 0

def findMoveGreedy(game_state, valid_moves, turn_multiplier):
    max_score = -CHECKMATE
    best_move = None
    global count
    for player_move in valid_moves:
        count += 1
        game_state.makeMove(player_move)
        score = turn_multiplier * scoreBoard(game_state)
        game_state.undoMove()
        if score > max_score:
            max_score = score
            best_move = player_move
    return best_move

def getCount():
    global count
    return count