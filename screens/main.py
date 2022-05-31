import pygame

from screens.about import About

from .menu import Menu
from .board import Board


class MainUI:
    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption("Chess Game")
        self.window = pygame.display.set_mode((512, 512))

        self.game = game
        self.active_screen = Menu()
        
        self.running = True

        self.transitions = {
            'new_game': self.to_new_game,
            'about': self.to_about,
            'menu': self.to_menu,
            'exit': self.exit,
        }

    def run(self):
        while self.running:
            self.active_screen.update(self.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                transition = self.active_screen.handle_event(event)
                transition_function = self.transitions.get(transition)

                if transition_function is not None:
                    transition_function()

            pygame.display.update()

        pygame.quit()

    def to_new_game(self):
        self.game.new_game()
        self.active_screen = Board(self.game)

    def to_about(self):
        self.active_screen = About()
    
    def to_menu(self):
        self.active_screen = Menu()
    
    def exit(self):
        self.running = False