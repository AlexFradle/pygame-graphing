import pygame
from constants import PANE_BACKGROUND_COLOUR, PANE_SELECTED_COLOUR, MAIN_BODY_FONT, MAIN_FONT_COLOUR


class Pane(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height), pygame.SRCALPHA)
        self.__width = width
        self.__height = height
        self.__title_bar_height = 20
        self.__selected = True

    def draw(self):
        self.fill(PANE_BACKGROUND_COLOUR)
        pygame.draw.rect(self, (60, 60, 60), (0, 0, self.__width, self.__title_bar_height))
        if self.__selected:
            pygame.draw.rect(self, PANE_SELECTED_COLOUR, self.get_rect(), 1)

        text = MAIN_BODY_FONT.render("testststsetse", True, MAIN_FONT_COLOUR)
        self.blit(text, (5, 50))


