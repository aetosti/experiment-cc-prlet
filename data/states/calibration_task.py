# Pygame Packages
import pygame

# Data Packages
import numpy as np
import pandas as pd
import statistics as st

# General Packages
import os

# Import BaseState
from .base import BaseState

# Import Elements
from data.elements.images import CalibrationLoader

# Import Settings
import settings


class CalibrationTask(BaseState):
    def __init__(self):
        super(CalibrationTask, self).__init__()

        self.next_state = "CONFIRM_CALIBRATION_INSTRUCTIONS"

        image_loader = CalibrationLoader()

        # LOAD LEFT CALIBRATION IMAGE
        (
            self.left_calibration_image,
            self.left_calibration_rect,
        ) = image_loader.load_image(
            os.path.join(
                "data", "assets", "images", "calibration", "right_side_calibration.png"
            ),
            self.screen_rect.width,
            self.screen_rect.height,
            "left",
        )

        # LOAD RIGHT CALIBRATION IMAGE
        (
            self.right_calibration_image,
            self.right_calibration_rect,
        ) = image_loader.load_image(
            os.path.join(
                "data", "assets", "images", "calibration", "left_side_calibration.png"
            ),
            self.screen_rect.width,
            self.screen_rect.height,
            "right",
        )

        # LOAD SOUND EFFECT
        self.preparation_bip_sound = pygame.mixer.Sound(
            os.path.join("data", "assets", "sounds", "sound_preparation_bip.mp3")
        )
        self.final_bip_sound = pygame.mixer.Sound(
            os.path.join("data", "assets", "sounds", "sound_final_bip.mp3")
        )

        # CALIBRATION SETTNGS
        self.first_calibration = False
        self.sound_played = False

        # DATA SETTINGS
        self.left_coordinate_calibration_array = np.array(0, dtype=np.int32)
        self.right_coordinate_calibration_array = np.array(0, dtype=np.int32)
        self.left_ratio_calibration_array = np.array(0.00, dtype=np.float32)
        self.right_ratio_calibration_array = np.array(0.00, dtype=np.float32)

    # STARTUP FUNCTION
    def startup(self, persistent):
        pygame.mouse.set_visible(False)

        self.time_active = 0

        self.persist = persistent

        self.id_number = self.persist["subject_id_number"]
        self.id_string = self.persist["subject_id_string"]

        self.persist["recalibrate"] = ""

    # UPDATE FUNCTION
    def update(self, dt, face_mesh, cap):
        self.time_active += dt
        self.get_points(face_mesh, cap)

        if self.time_active <= 1000:
            if not self.sound_played:
                self.preparation_bip_sound.play(loops=0)
                self.sound_played = True
            self.displayed = True
        elif self.time_active <= 2000:
            self.displayed = False
            self.sound_played = False
        elif self.time_active <= 3000:
            if not self.sound_played:
                self.preparation_bip_sound.play(loops=0)
                self.sound_played = True
            self.displayed = True
        elif self.time_active <= 4000:
            self.displayed = False
            self.sound_played = False
        elif 5000 <= self.time_active <= 8000:
            if not self.sound_played:
                self.final_bip_sound.play(loops=0)
                self.sound_played = True
            self.displayed = True
            if not self.first_calibration:
                self.left_coordinate_calibration_array = np.append(
                    self.left_coordinate_calibration_array, int(self.left_center_x)
                )
                self.right_coordinate_calibration_array = np.append(
                    self.right_coordinate_calibration_array,
                    int(self.right_center_x),
                )
                self.left_ratio_calibration_array = np.append(
                    self.left_ratio_calibration_array, round(self.left_ratio, 2)
                )

                self.right_ratio_calibration_array = np.append(
                    self.right_ratio_calibration_array, round(self.right_ratio, 2)
                )
            else:
                self.left_coordinate_calibration_array = np.append(
                    self.left_coordinate_calibration_array, int(self.left_center_x)
                )
                self.right_coordinate_calibration_array = np.append(
                    self.right_coordinate_calibration_array,
                    int(self.right_center_x),
                )
                self.left_ratio_calibration_array = np.append(
                    self.left_ratio_calibration_array, round(self.left_ratio, 2)
                )
                self.right_ratio_calibration_array = np.append(
                    self.right_ratio_calibration_array, round(self.right_ratio, 2)
                )
        if self.time_active >= 8000:
            if self.first_calibration == True:
                self.right_calibration = self.calc_calibration_values()
                self.save_calibration_task()
                self.done = True
            else:
                self.left_calibration = self.calc_calibration_values()
                self.displayed = False
                self.sound_played = False
                self.first_calibration = True

                self.left_coordinate_calibration_array = np.array(0, dtype=np.int32)
                self.right_coordinate_calibration_array = np.array(0, dtype=np.int32)
                self.left_ratio_calibration_array = np.array(0.00, dtype=np.float32)
                self.right_ratio_calibration_array = np.array(0.00, dtype=np.float32)
                self.time_active = 0

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        if self.first_calibration:
            img = self.right_calibration_image
            rect = self.right_calibration_rect
        else:
            img = self.left_calibration_image
            rect = self.left_calibration_rect

        if self.displayed:
            surface.blit(img, rect)
        else:
            surface.fill(pygame.Color(settings.BLACK))

    # DIRECTORY FUNCTIONS
    def make_calibration_directory(self):
        self.save_calibration_path = os.path.join(
            "results", f"{self.id_string}", "calibration_data"
        )
        os.makedirs(self.save_calibration_path)

    # CALIBRATION FUNCTIONS
    def calc_calibration_values(self):
        self.left_coordinate_value = np.argmax(
            np.bincount(self.left_coordinate_calibration_array)
        )
        self.right_coordinate_value = np.argmax(
            np.bincount(self.right_coordinate_calibration_array)
        )
        self.left_ratio_value = st.mode(self.left_ratio_calibration_array)
        self.right_ratio_value = st.mode(self.right_ratio_calibration_array)

        return (
            self.left_coordinate_value,
            self.right_coordinate_value,
            self.left_ratio_value,
            self.right_ratio_value,
        )

    # SAVE DATA FUNCTIONS
    def save_calibration_task(self):
        self.make_calibration_directory()

        calibration_excel = {
            "webcam_width": [self.webcam_width],
            "webcam_height": [self.webcam_height],
            "screen_width": [self.screen_width],
            "screen_height": [self.screen_height],
            "left_side_left_eye_coordinate": [self.left_calibration[0]],
            "left_side_right_eye_coordinate": [self.left_calibration[1]],
            "right_side_left_eye_coordinate": [self.right_calibration[0]],
            "right_side_right_eye_coordinate": [self.right_calibration[1]],
            "left_side_left_eye_ratio": [self.left_calibration[2]],
            "left_side_right_eye_ratio": [self.left_calibration[3]],
            "right_side_left_eye_ratio": [self.right_calibration[2]],
            "right_side_right_eye_ratio": [self.right_calibration[3]],
        }

        self.persist["left_side_left_eye_coordinate"] = self.left_calibration[0]
        self.persist["left_side_right_eye_coordinate"] = self.left_calibration[1]
        self.persist["right_side_left_eye_coordinate"] = self.right_calibration[0]
        self.persist["right_side_right_eye_coordinate"] = self.right_calibration[1]
        self.persist["left_side_left_eye_ratio"] = self.left_calibration[2]
        self.persist["left_side_right_eye_ratio"] = self.left_calibration[3]
        self.persist["right_side_left_eye_ratio"] = self.right_calibration[2]
        self.persist["right_side_right_eye_ratio"] = self.right_calibration[3]

        df = pd.DataFrame(calibration_excel)

        df.to_csv(
            os.path.join(
                f"{self.save_calibration_path}",
                f"{self.id_number}_data_calibration.csv",
            ),
            index=False,
            sep=";",
        )
