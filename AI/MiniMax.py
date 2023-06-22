from AI.Score import *

count = 0

def findMoveMinimax(game_state, valid_moves, depth, white_to_move, alpha, beta):
    global count
    global next_move
    if depth == 0:
        return quiescenceSearch(game_state, alpha, beta, white_to_move)
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            count += 1
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinimax(
                game_state, next_moves, depth - 1, False, alpha, beta)
            game_state.undoMove()
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            alpha = max(alpha, max_score)
            if alpha >= beta:
                break
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            count += 1
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = findMoveMinimax(
                game_state, next_moves, depth - 1, True, alpha, beta)
            game_state.undoMove()
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            beta = min(beta, min_score)
            if alpha >= beta:
                break
        return min_score


def quiescenceSearch(game_state, alpha, beta, white_to_move):
    global count
    best_score = scoreBoard(game_state)
    if white_to_move:
        captures = game_state.getAllPossibleAttacks()
        for move in captures:
            count += 1
            game_state.makeMove(move)
            score = quiescenceSearch(game_state, alpha, beta, False)
            game_state.undoMove()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
    else:
        captures = game_state.getAllPossibleAttacks()
        for move in captures:
            count += 1
            game_state.makeMove(move)
            score = quiescenceSearch(game_state, alpha, beta, True)
            game_state.undoMove()
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if alpha >= beta:
                break
    return best_score

def getCount():
    global count
    return count