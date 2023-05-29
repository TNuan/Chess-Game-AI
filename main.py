import pygame as p
import sys
from UI.Element import Button, OptionBox, SliderBar
from UI.Board import *
import Engine.ChessEngine as ChessEngine
import AI.ChessAI as ChessAI
from multiprocessing import Process, Queue

SCREEN = p.display.set_mode((1280, 800))
BG = p.image.load("assets/images/background.png")
FPS = 60

p.init()
p.display.set_caption("Chess game AI")

choosing_options = ['PvP', 'Greedy', 2]  # this is default options


def get_font(size):
    return p.font.Font("assets/font/font.ttf", size)


def play(choosing_options):
    clock = p.time.Clock()
    SCREEN.blit(p.image.load("assets/images/play_bg.png"), (0, 0))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    square_selected = ()
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = get_font(16)
    mode = choosing_options[0]
    algorithm_option = choosing_options[1]
    depth = choosing_options[2]

    if mode == 'PvP':
        player_one = True  # if a human is playing white, then this will be True, else False
        player_two = True  # if a hyman is playing white, then this will be True, else False
    elif mode == 'PvAI':
        player_one = True  # if a human is playing white, then this will be True, else False
        player_two = False  # if a hyman is playing white, then this will be True, else False
    elif mode == 'AIvAI':
        player_one = False  # if a human is playing white, then this will be True, else False
        player_two = False  # if a hyman is playing white, then this will be True, else False

    while True:
        clock.tick(FPS)
        human_turn = (game_state.white_to_move and player_one) or (
            not game_state.white_to_move and player_two)
        PLAY_MOUSE_POS = p.mouse.get_pos()
        PLAY_BACK = Button(image=p.image.load("assets/images/quit_rect.png"), pos=(1040, 700),
                           text_input="BACK", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        events = p.event.get()
        for e in events:
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            # mouse handler
            if e.type == p.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main()
                else:
                    if not game_over:
                        # (x, y) location of the mouse
                        location = PLAY_MOUSE_POS
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        # user clicked the same square twice
                        if square_selected == (row, col) or col >= 8:
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            # append for both 1st and 2nd click
                            player_clicks.append(square_selected)
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(
                                player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    animate = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=ChessAI.findBestMove, args=(
                    game_state, valid_moves, return_queue, algorithm_option, depth))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = ChessAI.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1],
                            SCREEN, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(SCREEN, game_state, valid_moves, square_selected)

        if not game_over:
            drawMoveLog(SCREEN, game_state, move_log_font)

        PLAY_BACK.update(SCREEN)
        if game_state.checkmate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(SCREEN, "Black wins by checkmate")
            else:
                drawEndGameText(SCREEN, "White wins by checkmate")

        elif game_state.stalemate:
            game_over = True
            drawEndGameText(SCREEN, "Stalemate")
        elif game_state.checkdraw:
            game_over = True
            drawEndGameText(SCREEN, "Draw")

        p.display.flip()


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def options(choosing_options):
    mode_options = ["PvP", "PvAI", "AIvAI"]
    ai_options = ["Greedy", "Minimax", "Negamax", "Negascout"]

    mode_box = OptionBox(160, 220, 300, 50, (193, 167, 132),
                         (100, 100, 100), get_font(30), mode_options)
    ai_box = OptionBox(800, 220, 300, 50, (193, 167, 132),
                       (100, 100, 100), get_font(30), ai_options)
    slider = SliderBar(520, 490, 400, 30, 4, (193, 167, 132),
                       (100, 100, 100), (117, 98, 73))

    clock = p.time.Clock()

    while True:
        clock.tick(FPS)
        OPTIONS_MOUSE_POS = p.mouse.get_pos()
        SCREEN.blit(p.image.load("assets/images/options_bg.png"), (0, 0))
        SCREEN.blit(p.image.load("assets/images/options_blur.png"), (0, 0))

        OPTIONS_TEXT = get_font(75).render("SETTING", True, "#55301E")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))

        LEVEL_TEXT = get_font(45).render("Mức độ ", True, "#FFEDD4")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(420, 500))

        MODE_TEXT = get_font(45).render("Chế độ ", True, "#FFEDD4")
        MODE_RECT = MODE_TEXT.get_rect(center=(320, 180))

        AI_TEXT = get_font(45).render("AI ", True, "#FFEDD4")
        AI_RECT = AI_TEXT.get_rect(center=(960, 180))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        SCREEN.blit(MODE_TEXT, MODE_RECT)
        SCREEN.blit(AI_TEXT, AI_RECT)

        # Draw the mode OptionBox and update its state
        mode_box.draw(SCREEN)
        ai_box.draw(SCREEN)
        slider.draw(SCREEN)

        events = p.event.get()
        mode_box.update(events)
        ai_box.update(events)
        slider.update(OPTIONS_MOUSE_POS)

        OPTIONS_BACK = Button(image=p.image.load("assets/images/quit_rect.png"), pos=(640, 660),
                              text_input="BACK", font=get_font(50), base_color="#FFEDD4", hovering_color="#C1A784")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        choosing_options[0] = mode_options[mode_box.get_value()]
        choosing_options[1] = ai_options[ai_box.get_value()]
        choosing_options[2] = slider.get_value()

        for event in events:
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main()

        p.display.flip()


def main():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = p.mouse.get_pos()

        PLAY_BUTTON = Button(image=p.image.load("assets/images/play_rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")
        OPTIONS_BUTTON = Button(image=p.image.load("assets/images/options_rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")
        QUIT_BUTTON = Button(image=p.image.load("assets/images/quit_rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(choosing_options)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(choosing_options)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()


if __name__ == "__main__":
    main()
