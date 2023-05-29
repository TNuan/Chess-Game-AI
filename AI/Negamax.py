from AI.Score import *


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return quiescenceSearch(game_state, alpha, beta, turn_multiplier)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves,
                                          depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def quiescenceSearch(game_state, alpha, beta, turn_multiplier):
    score = turn_multiplier * scoreBoard(game_state)
    if score >= beta:
        return beta
    alpha = max(alpha, score)
    captures = game_state.getAllPossibleAttacks()
    for move in captures:
        game_state.makeMove(move)
        score = -quiescenceSearch(game_state, -beta, -alpha, -turn_multiplier)
        game_state.undoMove()
        if score >= beta:
            return beta
        alpha = max(alpha, score)
    return alpha
