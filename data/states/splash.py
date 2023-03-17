import pygame
from .base import BaseState

import settings


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.title = self.font.render(
            "SPLASH STATE", True, pygame.Color(settings.WHITE)
        )
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "BIOGRAPHICAL_DATA"
        # self.next_state = "CONFIRM_CALIBRATION_TASK"
        self.time_active = 0

    def update(self, dt, face_mesh, cap):
        self.time_active += dt
        if self.time_active >= 3000:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))
        surface.blit(self.title, self.title_rect)
