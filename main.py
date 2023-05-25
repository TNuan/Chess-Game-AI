import pygame as p, sys
from element import Button, OptionBox, SliderBar
import chess.ChessAI as ChessAI
import chess.ChessEngine as ChessEngine 
from multiprocessing import Process, Queue

p.init()

BOARD_WIDTH = BOARD_HEIGHT = 800
MOVE_LOG_PANEL_WIDTH = 480
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
IMAGES = {} 


#----------------------------------
SCREEN = p.display.set_mode((1280, 800))
p.display.set_caption("Chess game AI")

BG = p.image.load("assets/images/background.png")

def get_font(size): 
    return p.font.Font("assets/font/font.ttf", size)
#-----------------------------------

def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./chess/images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


def play():
    clock = p.time.Clock()
    SCREEN.fill("white")
    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    loadImages()  # do this only once before while loop
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = False  # if a hyman is playing white, then this will be True, else False

    while True:
        clock.tick(60)
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        PLAY_MOUSE_POS = p.mouse.get_pos()
        PLAY_BACK = Button(image=p.image.load("assets/images/quit_rect.png"), pos=(1040, 700), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")
        

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
                        location = PLAY_MOUSE_POS  # (x, y) location of the mouse
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
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
                move_finder_process = Process(target=ChessAI.findBestMove, args=(game_state, valid_moves, return_queue))
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
                animateMove(game_state.move_log[-1], SCREEN, game_state.board, clock)
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

     
        p.display.flip()



def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQUARE_SIZE, last_move.end_row * SQUARE_SIZE))
    if square_selected != ():
        row, col = square_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # square_selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQUARE_SIZE, move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQUARE_SIZE, enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)
    
def options():
    
    mode_options = ["PvP", "PvAI", "AIvAI"]
    mode_box = OptionBox(160, 220, 300, 50, (193, 167, 132), (100, 100, 100), get_font(30), mode_options)

    AI_options = ["Greedy", "Minimax", "Negamax", "Negascout"]
    ai_box = OptionBox(800, 220, 300, 50, (193, 167, 132), (100, 100, 100), get_font(30), AI_options)

    slider = SliderBar(520, 490, 400, 30, 4, (193, 167, 132), (100, 100, 100), (117, 98, 73))

    clock = p.time.Clock()
    FPS = 60
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

        events = p.event.get()
        # Draw the mode OptionBox and update its state
        mode_box.draw(SCREEN)
        ai_box.draw(SCREEN)
        slider.draw(SCREEN)

        selected_mode = mode_box.update(events)
        selected_ai = ai_box.update(events)
        slider.update(OPTIONS_MOUSE_POS)
        

        OPTIONS_BACK = Button(image=p.image.load("assets/images/quit_rect.png"), pos=(640, 660), 
                            text_input="BACK", font=get_font(50), base_color="#FFEDD4", hovering_color="#C1A784")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in events:
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main()

        # If a mode has been selected, print it to the console
        if selected_mode >= 0:
            print("Selected mode:", mode_options[selected_mode])

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
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    p.quit()
                    sys.exit()

        p.display.update()

if __name__ == "__main__":
    main()
