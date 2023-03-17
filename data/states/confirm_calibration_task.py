# Pygame Packages
import pygame

# Import BaseState
from .base import BaseState

# Import Settings
import settings


class ConfirmCalibrationTask(BaseState):
    def __init__(self):
        super(ConfirmCalibrationTask, self).__init__()

        self.next_state = "PRL_START_INSTRUCTIONS"

        self.left_text = self.font.render(
            "Premi SPAZIO per continuare o A per ricalibrare",
            True,
            pygame.Color(settings.WHITE),
        )

        self.right_text = self.font.render(
            "Premi SPAZIO per continuare o L per ricalibrare",
            True,
            pygame.Color(settings.WHITE),
        )
        self.text_rect = self.left_text.get_rect(
            center=(
                self.screen_rect.centerx,
                self.screen_rect.bottom - self.left_text.get_height(),
            )
        )

        self.rect = pygame.Rect(0, 0, 222, 323)

    # STARTUP FUNCTION
    def startup(self, persistent):
        self.color = settings.RED

        self.first_confirm = False
        self.next = False

        self.persist = persistent

        self.id_number = self.persist["subject_id_number"]
        self.id_string = self.persist["subject_id_string"]
        self.left_calibration_value = self.persist["left_side_left_eye_ratio"]
        self.right_calibration_value = self.persist["right_side_left_eye_ratio"]

        print("start", self.persist["recalibrate"])
        # self.recalibrate = self.persist["recalibrate"]

    # GET SUBJECT'S INPUT
    def get_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.first_confirm = True
                if self.next:
                    self.next_state = "PRL_START_INSTRUCTIONS"
                    self.done = True
            elif event.key == pygame.K_ESCAPE:
                self.quit = True
            elif event.key == pygame.K_a:
                self.next_state = "RECALIBRATION_TASK"
                self.persist["recalibrate"] = "left"
                self.done = True
            elif event.key == pygame.K_l:
                self.next_state = "RECALIBRATION_TASK"
                self.persist["recalibrate"] = "right"
                self.done = True

    # UPDATE FUNCTION
    def update(self, dt, face_mesh, cap):
        self.get_points(face_mesh, cap)

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))
        print(self.persist["recalibrate"])

        if self.first_confirm == False or self.persist["recalibrate"] == "left":
            self.rect.x = 50
            self.rect.y = int(surface.get_height() // 2 - self.rect.height // 2)

            if round(self.left_ratio, 2) < self.left_calibration_value:
                self.color = settings.GREEN
            else:
                self.color = settings.RED

            surface.blit(self.left_text, self.text_rect)
            # self.persist["recalibrate"] = ""

        # elif self.first_confirm == True or self.persist["recalibrate"] == "right":
        else:
            self.next = True
            # self.color = settings.GREEN

            self.rect.x = int(surface.get_width() - 50 - self.rect.width)
            self.rect.y = int(surface.get_height() // 2 - self.rect.height // 2)

            if round(self.left_ratio, 2) > self.right_calibration_value:
                self.color = settings.GREEN
            else:
                self.color = settings.RED

            surface.blit(self.right_text, self.text_rect)
        pygame.draw.rect(surface, self.color, self.rect)
