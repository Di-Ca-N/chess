import pygame

from screens.menu import Menu

from .board import BoardUI


class MainUI:
    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption("Chess Game")
        self.window = pygame.display.set_mode((512, 512))

        self.game = game
        self.menu = Menu()
        self.game_ui = BoardUI(game)

        self.active_screen = self.menu
    
    def run(self):
        try:
            while True:
                self.active_screen.update(self.window)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    transition = self.active_screen.handle_event(event)
                    if transition is not None:
                        if transition == 'new_game':
                            self.to_new_game()
                        elif transition == 'about':
                            self.to_about()
                        elif transition == 'menu':
                            self.to_menu()

                pygame.display.update()
        except pygame.error as e:
            print(e)

    def to_new_game(self):
        self.game.new_game()
        self.active_screen = self.game_ui

    def to_about(self):
        print("About...")
    
    def to_menu(self):
        self.active_screen = self.menu