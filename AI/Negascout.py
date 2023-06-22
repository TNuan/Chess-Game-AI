from AI.Score import *
count = 0

def findMoveNegascout(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global count
    global next_move
    best_move = None
    if depth == 0:
        return quiescenceSearch(game_state, alpha, beta, turn_multiplier)
    for i, move in enumerate(valid_moves):
        count += 1
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        if i == 0:
            score = -findMoveNegascout(game_state, next_moves,
                                       depth - 1, -beta, -alpha, -turn_multiplier)
        else:
            score = -findMoveNegascout(game_state, next_moves, depth - 1, -
                                       alpha - 1, -alpha, -turn_multiplier)  # search with a null window
            if alpha < score < beta:
                # if it failed high, do a full re-search
                score = -findMoveNegascout(game_state, next_moves,
                                           depth - 1, -beta, -score, -turn_multiplier)
        game_state.undoMove()
        if alpha < score:
            best_move = move
            alpha = score
        if alpha >= beta:
            break  # cut-off
    if depth == DEPTH:
        next_move = best_move
    return alpha


def quiescenceSearch(game_state, alpha, beta, turn_multiplier):
    global count
    score = turn_multiplier * scoreBoard(game_state)
    if score >= beta:
        return beta
    if score > alpha:
        alpha = score
    capture_moves = game_state.getAllPossibleAttacks()
    for move in capture_moves:
        count += 1
        if beta <= alpha:
            break
        game_state.makeMove(move)
        score = -quiescenceSearch(game_state, -beta, -alpha, -turn_multiplier)
        game_state.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def getCount():
    global count
    return count
