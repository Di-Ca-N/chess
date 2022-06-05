import pygame
import pygame_gui

from screens.base import ScreenTransition, Screen


class GameOver(Screen):
    def __init__(self, transition: ScreenTransition = None):
        super().__init__()

        display_surface = pygame.display.get_surface()
        display_size = display_surface.get_size()

        self.overlay = pygame.Surface(display_size)
        self.overlay.set_alpha(64)
        self.overlay.fill((0, 0, 0))
        display_surface.blit(self.overlay, (0, 0))

        self.manager = pygame_gui.UIManager(display_size, "assets/theme.json")

        winner = transition.data["winner"]
        winner_str = winner.name.capitalize()

        self.title = pygame_gui.elements.UITextBox(
            f"<font size=7>Game Over!</font><br><font size=5>{winner_str} won!</font>",
            relative_rect=pygame.Rect((50, 50), (412, 100)),
            manager=self.manager,
            wrap_to_height=True,
            object_id=pygame_gui.core.ObjectID(class_id="@overlay_textbox"),
        )

        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 50), (212, 50)),
            text="New Game",
            manager=self.manager,
            anchors={
                "left": "right",
                "right": "right",
                "top": "top",
                "bottom": "top",
                "top_target": self.title,
                "right_target": self.title,
            },
        )

        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 10), (212, 50)),
            text="Main Menu",
            manager=self.manager,
            anchors={
                "left": "right",
                "right": "right",
                "top": "top",
                "bottom": "top",
                "top_target": self.new_game_button,
                "right_target": self.new_game_button,
            },
        )

    def draw(self, screen):
        self.manager.update(pygame.time.get_ticks() / 1000)
        self.manager.draw_ui(screen)

    def handle_event(self, event):
        self.manager.process_events(event)

        match event.type:
            case pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is self.new_game_button:
                    self.transition = ScreenTransition("game_over", "new_game")
                elif event.ui_element is self.main_menu_button:
                    self.transition = ScreenTransition("game_over", "menu")
