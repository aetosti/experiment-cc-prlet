# Pygame Packages
import pygame

# Import BaseState
from .base import BaseState

# Import Elements
from data.elements.cards import TextCard

# Import Settings
import settings


class PrlStartInstructions(BaseState):
    def __init__(self):
        super(PrlStartInstructions, self).__init__()

        self.next_state = "PRL_TASK"

        self.text = "This are the Instructions to Follow for the PRL Task. Change the text in the prl_start_instructions.py file"

        self.go_next_text = self.font.render(
            "Premi SPAZIO per continuare",
            True,
            pygame.Color(settings.WHITE),
        )

        self.go_next_text_rect = self.go_next_text.get_rect(
            center=(
                self.screen_rect.centerx,
                self.screen_rect.bottom - self.go_next_text.get_height(),
            )
        )

    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.text_box = TextCard(
            surface.get_width(),
            surface.get_height(),
            self.text,
        )

        surface.blit(self.text_box.image, self.text_box.rect)
        surface.blit(self.go_next_text, self.go_next_text_rect)
