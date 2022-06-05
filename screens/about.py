import pygame
import pygame_gui

from screens.base import ScreenTransition, Screen


class About(Screen):
    def __init__(self):
        super().__init__()

        window = pygame.display.get_surface()

        self.manager = pygame_gui.UIManager(window.get_size(), "assets/theme.json")

        self.text = pygame_gui.elements.UITextBox(
            "<font size=7>About</font><br>"
            "<p>This project was developed as an exercise of Design Patterns and SOLID principles.</p>"
            "<p>It is a simple game of chess. To undo a movement, just press 'u'."
            "To start a new game, press 'n'. To go back to menu, press 'ESC'.</p>",
            relative_rect=pygame.Rect((50, 50), (400, 300)),
            manager=self.manager,
            wrap_to_height=True,
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 300), (200, 50)),
            text="Back",
            manager=self.manager,
        )

    def draw(self, screen):
        self.manager.update(pygame.time.get_ticks() / 1000)
        screen.fill((255, 255, 255))
        self.manager.draw_ui(screen)

    def handle_event(self, event):
        self.manager.process_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.transition = ScreenTransition("about", "menu")
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element is self.back_button:
                self.transition = ScreenTransition("about", "menu")
