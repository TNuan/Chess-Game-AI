from AI.Score import *

count = 0

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global count 
    global next_move
    if depth == 0:
        return quiescenceSearch(game_state, alpha, beta, turn_multiplier)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        count += 1
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves,
                                          depth - 1, -beta, -alpha, -turn_multiplier)
        game_state.undoMove()
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        alpha = max(alpha, max_score)
        # if max_score > alpha:
        #     alpha = max_score
        if alpha >= beta:
            break
    return max_score


def quiescenceSearch(game_state, alpha, beta, turn_multiplier):
    global count
    score = turn_multiplier * scoreBoard(game_state)
    if score >= beta:
        return beta
    alpha = max(alpha, score)
    captures = game_state.getAllPossibleAttacks()
    for move in captures:
        count += 1
        game_state.makeMove(move)
        score = -quiescenceSearch(game_state, -beta, -alpha, -turn_multiplier)
        game_state.undoMove()
        if score >= beta:
            return beta
        alpha = max(alpha, score)
    return alpha

def getCount():
    global count
    return count