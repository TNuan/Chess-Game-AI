import pygame, sys
from element import Button, OptionBox, SliderBar

pygame.init()

SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Chess game AI")

BG = pygame.image.load("assets/images/background.png")

def get_font(size): 
    return pygame.font.Font("assets/font/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    
    mode_options = ["PvP", "PvAI", "AIvAI"]
    mode_box = OptionBox(160, 220, 300, 50, (193, 167, 132), (100, 100, 100), get_font(30), mode_options)

    AI_options = ["Greedy", "Minimax", "Negamax", "Negascout"]
    ai_box = OptionBox(800, 220, 300, 50, (193, 167, 132), (100, 100, 100), get_font(30), AI_options)

    slider = SliderBar(520, 490, 400, 30, 4, (193, 167, 132), (100, 100, 100), (117, 98, 73))

    clock = pygame.time.Clock()
    FPS = 60
    while True:
        clock.tick(FPS)
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(pygame.image.load("assets/images/options_bg.png"), (0, 0))
        SCREEN.blit(pygame.image.load("assets/images/options_blur.png"), (0, 0))

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

        events = pygame.event.get()
        # Draw the mode OptionBox and update its state
        mode_box.draw(SCREEN)
        ai_box.draw(SCREEN)
        slider.draw(SCREEN)

        selected_mode = mode_box.update(events)
        selected_ai = ai_box.update(events)
        slider.update(OPTIONS_MOUSE_POS)
        

        OPTIONS_BACK = Button(image=pygame.image.load("assets/images/quit_rect.png"), pos=(640, 660), 
                            text_input="BACK", font=get_font(50), base_color="#FFEDD4", hovering_color="#C1A784")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        # If a mode has been selected, print it to the console
        if selected_mode >= 0:
            print("Selected mode:", mode_options[selected_mode])

        pygame.display.flip()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/play_rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/options_rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/quit_rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#FFEDD4", hovering_color="#C1A784")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()