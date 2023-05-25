from AI.Score import  *


def findMoveGreedy(game_state, valid_moves, turn_multiplier):
    max_score = -CHECKMATE
    best_move = None
    for player_move in valid_moves:
            game_state.makeMove(player_move)
            score = turn_multiplier * scoreBoard(game_state)
            game_state.undoMove()
            if score > max_score:
                max_score = score
                best_move = player_move
    return best_move