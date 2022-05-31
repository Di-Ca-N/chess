import pygame
import pygame_gui


class Menu:
    def __init__(self):
        window = pygame.display.get_surface()

        self.manager = pygame_gui.UIManager(window.get_size(), "assets/theme.json")

        self.title = pygame_gui.elements.UITextBox(
            "<font size=7>Chess</font>",
            relative_rect=pygame.Rect((50, 50), (400, 100)),
            manager=self.manager,
        )
        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 150), (200, 50)),
            text="New Game",
            manager=self.manager,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        self.about_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 210), (200, 50)),
            text="About",
            manager=self.manager,
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 270), (200, 50)),
            text="Exit",
            manager=self.manager,
        )

    def update(self, screen):
        self.manager.update(pygame.time.get_ticks() / 1000)
        screen.fill((255, 255, 255))
        self.manager.draw_ui(screen)

    def handle_event(self, event):
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element is self.new_game_button:
                return "new_game"
            elif event.ui_element is self.about_button:
                return "about"
            elif event.ui_element is self.exit_button:
                return "exit"
