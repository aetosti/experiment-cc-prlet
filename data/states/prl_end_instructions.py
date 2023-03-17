# Pygame Packages
import pygame

# Import BaseState
from .base import BaseState

# Import Elements
from data.elements.cards import TextCard

# Import Settings
import settings


class PrlEndInstructions(BaseState):
    def __init__(self):
        super(PrlEndInstructions, self).__init__()

        self.text = "This are the Instructions to Follow After completing the experiment. Change the text by editing prl_end_instructions.py"

        self.end_text = self.font.render(
            "Premi QUALSIASI tasto per terminare l'esperimento.",
            True,
            pygame.Color(settings.WHITE),
        )

        self.end_text_rect = self.end_text.get_rect(
            center=(
                self.screen_rect.centerx,
                self.screen_rect.bottom - self.end_text.get_height(),
            )
        )
        self.count_click = 0

    def get_event(self, event):
        if event.type == pygame.KEYUP:
            self.quit += 1
            if self.count_click > 1:
                self.quit = True

    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.text_box = TextCard(
            surface.get_width(),
            surface.get_height(),
            self.text,
        )

        surface.blit(self.text_box.image, self.text_box.rect)
        surface.blit(self.end_text, self.end_text_rect)
