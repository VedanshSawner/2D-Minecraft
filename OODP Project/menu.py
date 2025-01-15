import pygame
import sys

class Menu:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Menu")
        self.BG = pygame.image.load("assets/gui/menu_background.jpg")
        pygame.mixer.music.load('assets/gui/game_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def get_font(self, size):
        return pygame.font.Font("assets/gui/menu_font.ttf", size)

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            menu_bg2 = pygame.image.load("assets/gui/menu_background.jpg")
            self.SCREEN.blit(menu_bg2, (0, 0))

            OPTIONS_TEXT_1 = self.get_font(30).render("D: Moving right", True, "White")
            OPTIONS_RECT_1 = OPTIONS_TEXT_1.get_rect(center=(400, 150))
            self.SCREEN.blit(OPTIONS_TEXT_1, OPTIONS_RECT_1)

            OPTIONS_TEXT_2 = self.get_font(30).render("A: Moving left", True, "White")
            OPTIONS_RECT_2 = OPTIONS_TEXT_2.get_rect(center=(400, 200))
            self.SCREEN.blit(OPTIONS_TEXT_2, OPTIONS_RECT_2)

            OPTIONS_TEXT_3 = self.get_font(30).render("Spacebar: Jump", True, "White")
            OPTIONS_RECT_3 = OPTIONS_TEXT_3.get_rect(center=(400, 250))
            self.SCREEN.blit(OPTIONS_TEXT_3, OPTIONS_RECT_3)

            OPTIONS_TEXT_4 = self.get_font(30).render("Number keys: Change item", True, "White")
            OPTIONS_RECT_4 = OPTIONS_TEXT_4.get_rect(center=(400, 300))
            self.SCREEN.blit(OPTIONS_TEXT_4, OPTIONS_RECT_4)

            OPTIONS_TEXT_5 = self.get_font(30).render("L Shift: Spirint", True, "White")
            OPTIONS_RECT_5 = OPTIONS_TEXT_5.get_rect(center=(400, 350))
            self.SCREEN.blit(OPTIONS_TEXT_4, OPTIONS_RECT_4)

            OPTIONS_BACK = Button(image=None, pos=(400, 450),
                                  text_input="BACK", font=self.get_font(75), base_color="White", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        return

            pygame.display.update()

    def volume_menu(self):
        running = True
        slider_rect = pygame.Rect(300, 300, 200, 10)
        knob_x = slider_rect.x + int(pygame.mixer.music.get_volume() * slider_rect.width)

        while running:
            menu_bg = pygame.image.load("assets/gui/menu_background.jpg")
            self.SCREEN.blit(menu_bg, (0, 0))
            VOLUME_MOUSE_POS = pygame.mouse.get_pos()
            VOLUME_TEXT = self.get_font(40).render("Volume", True, "White")
            VOLUME_RECT = VOLUME_TEXT.get_rect(center=(400, 200))
            self.SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

            pygame.draw.rect(self.SCREEN, (200, 200, 200), slider_rect)
            pygame.draw.circle(self.SCREEN, (0, 0, 0), (knob_x, slider_rect.y + slider_rect.height // 2), 10)

            BACK_BUTTON = Button(image=None, pos=(400, 500),
                                 text_input="BACK", font=self.get_font(30), base_color="#d7fcd4", hovering_color="Black")
            BACK_BUTTON.changeColor(VOLUME_MOUSE_POS)
            BACK_BUTTON.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(VOLUME_MOUSE_POS):
                        running = False
                    elif slider_rect.collidepoint(event.pos):
                        knob_x = event.pos[0]
                if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                    if slider_rect.collidepoint(event.pos):
                        knob_x = max(slider_rect.x, min(event.pos[0], slider_rect.x + slider_rect.width))
                        volume = (knob_x - slider_rect.x) / slider_rect.width
                        pygame.mixer.music.set_volume(volume)

            pygame.display.update()

    def main_menu(self):
        Vol_icon = pygame.image.load("assets/gui/volume_icon.jpg").convert_alpha()
        for x in range(Vol_icon.get_width()):
            for y in range(Vol_icon.get_height()):
                color = Vol_icon.get_at((x, y))
                if color.r > 240 and color.g > 240 and color.b > 240:
                    Vol_icon.set_at((x, y), (255, 255, 255, 0))

        Vol_icon = pygame.transform.scale(Vol_icon, (90, 90))
        Vol_icon_rect = Vol_icon.get_rect(topleft=(720, 0.5))

        game_run = True
        while game_run:
            self.SCREEN.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(60).render("Block Survival", True, "Black")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 70))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/gui/gray_box.png"), pos=(400, 200),
                                 text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="Black")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/gui/gray_box.png"), pos=(400, 330),
                                    text_input="CONTROLS", font=self.get_font(30), base_color="#d7fcd4", hovering_color="Black")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/gui/gray_box.png"), pos=(400, 460),
                                 text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="Black")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            self.SCREEN.blit(Vol_icon, Vol_icon_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        return True
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                        game_run = True
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        game_run = False
                    if Vol_icon_rect.collidepoint(event.pos):
                        self.volume_menu()
                        game_run = True
            if game_run:
                pygame.display.update()
        return game_run

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)