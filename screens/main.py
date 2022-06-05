import pygame

from .about import About
from .game_over import GameOver
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
            "new_game": self.to_new_game,
            "about": self.to_about,
            "menu": self.to_menu,
            "game_over": self.game_over,
            "exit": self.exit,
        }

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.active_screen.handle_event(event)

            self.active_screen.draw(self.window)
            pygame.display.update()

            transition = self.active_screen.get_transition()
            if transition is not None and transition.to_state in self.transitions:
                self.transitions[transition.to_state](transition)
        pygame.quit()

    def to_new_game(self, transition=None):
        self.game.new_game()
        self.active_screen = Board(self.game)

    def to_about(self, transition=None):
        self.active_screen = About()

    def to_menu(self, transition=None):
        self.active_screen = Menu()

    def game_over(self, transition=None):
        self.active_screen = GameOver(transition)

    def exit(self, transition=None):
        self.running = False
