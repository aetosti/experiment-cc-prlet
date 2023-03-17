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


class RecalibrationTask(BaseState):
    def __init__(self):
        super(RecalibrationTask, self).__init__()

        self.next_state = "CONFIRM_CALIBRATION_TASK"

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
        self.left_coordinate_recalibration_array = np.array(0, dtype=np.int32)
        self.right_coordinate_recalibration_array = np.array(0, dtype=np.int32)
        self.left_ratio_recalibration_array = np.array(0.00, dtype=np.float32)
        self.right_ratio_recalibration_array = np.array(0.00, dtype=np.float32)

    def startup(self, persistent):
        self.time_active = 0

        pygame.mouse.set_visible(False)

        self.persist = persistent

        self.id_number = self.persist["subject_id_number"]
        self.id_string = self.persist["subject_id_string"]

        self.to_recalibrate = self.persist["recalibrate"]

        self.left_side_left_eye_coordinate = self.persist[
            "left_side_left_eye_coordinate"
        ]
        self.left_side_right_eye_coordinate = self.persist[
            "left_side_right_eye_coordinate"
        ]
        self.right_side_left_eye_coordinate = self.persist[
            "right_side_left_eye_coordinate"
        ]
        self.right_side_right_eye_coordinate = self.persist[
            "right_side_right_eye_coordinate"
        ]
        self.left_side_left_eye_ratio = self.persist["left_side_left_eye_ratio"]
        self.left_side_right_eye_ratio = self.persist["left_side_right_eye_ratio"]
        self.right_side_left_eye_ratio = self.persist["right_side_left_eye_ratio"]
        self.right_side_right_eye_ratio = self.persist["right_side_right_eye_ratio"]

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
            if self.to_recalibrate == "right":
                self.left_coordinate_recalibration_array = np.append(
                    self.left_coordinate_recalibration_array, int(self.left_center_x)
                )
                self.right_coordinate_recalibration_array = np.append(
                    self.right_coordinate_recalibration_array,
                    int(self.right_center_x),
                )
                self.left_ratio_recalibration_array = np.append(
                    self.left_ratio_recalibration_array, round(self.left_ratio, 2)
                )

                self.right_ratio_recalibration_array = np.append(
                    self.right_ratio_recalibration_array, round(self.right_ratio, 2)
                )
            else:
                self.left_coordinate_recalibration_array = np.append(
                    self.left_coordinate_recalibration_array, int(self.left_center_x)
                )
                self.right_coordinate_recalibration_array = np.append(
                    self.right_coordinate_recalibration_array,
                    int(self.right_center_x),
                )
                self.left_ratio_recalibration_array = np.append(
                    self.left_ratio_recalibration_array, round(self.left_ratio, 2)
                )
                self.right_ratio_recalibration_array = np.append(
                    self.right_ratio_recalibration_array, round(self.right_ratio, 2)
                )
        elif self.time_active >= 8000:
            if self.to_recalibrate == "left":
                self.left_calibration = self.calc_recalibration_values()
                self.persist["recalibrate"] = "left"
            else:
                self.right_calibration = self.calc_recalibration_values()
                self.persist["recalibrate"] = "right"

            self.save_recalibrate_task()
            self.done = True

    # GET USER INPUT
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))

        self.screen_width = surface.get_width()
        self.screen_height = surface.get_height()

        if self.to_recalibrate == "left":
            img = self.left_calibration_image
            rect = self.left_calibration_rect
        else:
            img = self.right_calibration_image
            rect = self.right_calibration_rect

        if self.displayed:
            surface.blit(img, rect)
        else:
            surface.fill(pygame.Color(settings.BLACK))

    # CALIBRATION FUNCTIONS
    def calc_recalibration_values(self):
        self.left_coordinate_value = np.argmax(
            np.bincount(self.left_coordinate_recalibration_array)
        )
        self.right_coordinate_value = np.argmax(
            np.bincount(self.right_coordinate_recalibration_array)
        )
        self.left_ratio_value = st.mode(self.left_ratio_recalibration_array)
        self.right_ratio_value = st.mode(self.right_ratio_recalibration_array)

        return (
            self.left_coordinate_value,
            self.right_coordinate_value,
            self.left_ratio_value,
            self.right_ratio_value,
        )

    # SAVE DATA FUNCTIONS
    def save_recalibrate_task(self):
        self.save_calibration_path = os.path.join(
            "results", f"{self.id_string}", "calibration_data"
        )

        self.persist["left_side_left_eye_coordinate"] = (
            self.left_calibration[0]
            if self.to_recalibrate == "left"
            else self.left_side_left_eye_coordinate
        )

        self.persist["left_side_right_eye_coordinate"] = (
            self.left_calibration[1]
            if self.to_recalibrate == "left"
            else self.left_side_right_eye_coordinate
        )

        self.persist["right_side_left_eye_coordinate"] = (
            self.right_calibration[0]
            if self.to_recalibrate == "right"
            else self.right_side_left_eye_coordinate
        )

        self.persist["right_side_right_eye_coordinate"] = (
            self.right_calibration[1]
            if self.to_recalibrate == "right"
            else self.right_side_right_eye_coordinate
        )

        self.persist["left_side_left_eye_ratio"] = (
            self.left_calibration[2]
            if self.to_recalibrate == "left"
            else self.left_side_left_eye_ratio
        )

        self.persist["left_side_right_eye_ratio"] = (
            self.left_calibration[3]
            if self.to_recalibrate == "left"
            else self.left_side_right_eye_ratio
        )

        self.persist["right_side_left_eye_ratio"] = (
            self.right_calibration[2]
            if self.to_recalibrate == "right"
            else self.right_side_left_eye_ratio
        )

        self.persist["right_side_right_eye_ratio"] = (
            self.right_calibration[3]
            if self.to_recalibrate == "right"
            else self.right_side_right_eye_ratio
        )
        calibration_excel = {
            "webcam_width": [self.webcam_width],
            "webcam_height": [self.webcam_height],
            "screen_width": [self.screen_width],
            "screen_height": [self.screen_height],
            "left_side_left_eye_coordinate": [
                self.persist["left_side_left_eye_coordinate"]
            ],
            "left_side_right_eye_coordinate": [
                self.persist["left_side_right_eye_coordinate"]
            ],
            "right_side_left_eye_coordinate": [
                self.persist["right_side_left_eye_coordinate"]
            ],
            "right_side_right_eye_coordinate": [
                self.persist["right_side_right_eye_coordinate"]
            ],
            "left_side_left_eye_ratio": [self.persist["left_side_left_eye_ratio"]],
            "left_side_right_eye_ratio": [self.persist["left_side_right_eye_ratio"]],
            "right_side_left_eye_ratio": [self.persist["right_side_left_eye_ratio"]],
            "right_side_right_eye_ratio": [self.persist["right_side_right_eye_ratio"]],
        }

        df = pd.DataFrame(calibration_excel)

        df.to_csv(
            os.path.join(
                f"{self.save_calibration_path}",
                f"{self.id_number}_data_calibration.csv",
            ),
            index=False,
            sep=";",
        )
