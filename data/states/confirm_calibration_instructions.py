# Pygame Packages
import pygame

# Import BaseState
from .base import BaseState

# Import Elements
from data.elements.cards import TextCard

# Import Settings
import settings


class ConfirmCalibrationInstructions(BaseState):
    def __init__(self):
        super(ConfirmCalibrationInstructions, self).__init__()

        self.next_state = "CONFIRM_CALIBRATION_TASK"

        self.text = "This are the Instructions to tollow to Confirm the Calibration Task. The text should go automatically in a new line when needed"

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

    # GET SUBJECT'S INPUT
    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.done = True

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.text_box = TextCard(
            surface.get_width(),
            surface.get_height(),
            self.text,
        )

        surface.blit(self.text_box.image, self.text_box.rect)
        surface.blit(self.go_next_text, self.go_next_text_rect)
