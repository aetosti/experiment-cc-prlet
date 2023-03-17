# Pygame Packages
import pygame

# General Packages
import os

# Import BaseState
from .base import BaseState

# Import Elements
from data.elements.cards import ImageTextCard

# Import Settings
import settings


class EyeTrackingInstructions(BaseState):
    def __init__(self):
        super(EyeTrackingInstructions, self).__init__()

        self.next_state = "CALIBRATION_INSTRUCTIONS"

        self.go_next_text = self.font.render(
            "Premi SPAZIO per continuare",
            True,
            pygame.Color(settings.WHITE),
        )

        self.text_one = "This are the Instructions for the first ET Card. Change the text by editing -data -states -eye_tracking_instructions.py"
        self.text_two = "This are the Instructions for the second ET Card. Change the text by editing -data -states -eye_tracking_instructions.py"
        self.text_three = "This are the Instructions for the third ET Card. Change the text by editing -data -states -eye_tracking_instructions.py"

        self.instruction_one_image = os.path.join(
            "data", "assets", "images", "instructions", "one.png"
        )

        self.instruction_two_image = os.path.join(
            "data", "assets", "images", "instructions", "two.png"
        )

        self.instruction_three_image = os.path.join(
            "data", "assets", "images", "instructions", "three.png"
        )

    def startup(self, persistent):
        pygame.mouse.set_visible(False)

        self.time_active = 0

        self.persist = persistent

        self.id_number = self.persist["subject_id_number"]
        self.id_string = self.persist["subject_id_string"]

        self.instruction_two = False
        self.instruction_three = False
        self.go_next = False

    # GET SUBJECT'S INPUT
    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.done = True

    # UPDATE FUNCTION
    def update(self, dt, face_mesh, cap):
        self.time_active += dt
        if self.time_active >= 3000:
            self.instruction_two = True
        if self.time_active >= 6000:
            self.instruction_three = True
        if self.time_active >= 7000:
            self.go_next = True

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.instruction_one = ImageTextCard(
            surface.get_width(),
            surface.get_height(),
            self.instruction_one_image,
            self.text_one,
            "left",
        )

        surface.blit(self.instruction_one.image, self.instruction_one.rect)

        if self.instruction_two:
            self.instruction_two = ImageTextCard(
                surface.get_width(),
                surface.get_height(),
                self.instruction_two_image,
                self.text_two,
                "center",
            )
            surface.blit(self.instruction_two.image, self.instruction_two.rect)
        if self.instruction_three:
            self.instruction_three = ImageTextCard(
                surface.get_width(),
                surface.get_height(),
                self.instruction_three_image,
                self.text_three,
                "right",
            )
            surface.blit(self.instruction_three.image, self.instruction_three.rect)

        if self.go_next:
            go_next_text_rect = self.go_next_text.get_rect(
                center=(
                    self.screen_rect.centerx,
                    self.screen_rect.bottom - self.go_next_text.get_height(),
                )
            )
            surface.blit(self.go_next_text, go_next_text_rect)
