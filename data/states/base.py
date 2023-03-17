# Pygame Packages
import pygame

# Eye Tracking Packages
import cv2

# General Packages
import os

# Data Packages
import math
import numpy as np

# Import Settings
import settings


class BaseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

        self.mesh_points = []

        self.warning_sound = pygame.mixer.Sound(
            os.path.join("data", "assets", "sounds", "sound_warning.mp3")
        )

    def get_points(self, face_mesh, cap):
        ret, frame = cap.read()

        self.webcam_height, self.webcam_width = frame.shape[:2]

        frame.flags.writeable = False

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        frame.flags.writeable = True

        if results.multi_face_landmarks:
            self.mesh_points = np.array(
                [
                    np.multiply(
                        [p.x, p.y], [self.webcam_width, self.webcam_height]
                    ).astype(int)
                    for p in results.multi_face_landmarks[0].landmark
                ]
            )

            (
                self.left_center_x,
                left_center_y,
            ), left_radious = cv2.minEnclosingCircle(
                self.mesh_points[settings.LEFT_IRIS]
            )
            (
                self.right_center_x,
                right_center_y,
            ), right_radious = cv2.minEnclosingCircle(
                self.mesh_points[settings.RIGHT_IRIS]
            )

            self.center_left = np.array(
                [self.left_center_x, left_center_y], dtype=np.int32
            )
            self.center_right = np.array(
                [self.right_center_x, right_center_y], dtype=np.int32
            )

            self.right_ratio = self.iris_ratio(
                self.center_right,
                self.mesh_points[settings.RIGHT_H_LEFT],
                self.mesh_points[settings.RIGHT_H_RIGHT][0],
            )
            self.left_ratio_list = self.left_ratio = self.iris_ratio(
                self.center_left,
                self.mesh_points[settings.LEFT_H_RIGHT],
                self.mesh_points[settings.LEFT_H_LEFT][0],
            )
        else:
            self.warning_sound.play(loops=0)
            print("No Face Detected")

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt, face_mesh, cap):
        pass

    def draw(self, surface):
        pass

    # EYE TRACKING FUNCTIONS
    def distance_between_points(self, point1, point2):  # distance between
        x1, y1 = point1.ravel()
        x2, y2 = point2.ravel()

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return distance

    def iris_ratio(self, iris_center, right_point, left_point):
        center_to_right_dist = self.distance_between_points(iris_center, right_point)

        total_distance = self.distance_between_points(right_point, left_point)

        ratio = center_to_right_dist / total_distance

        return ratio
