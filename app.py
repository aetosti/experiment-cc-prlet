import pygame

# Eye Tracking Packages
import cv2
import mediapipe as mp

import os


class App(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.dt = 0.0
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.font_size = self.set_font_size()
        self.font = pygame.font.Font(
            os.path.join("data", "fonts", "Poppins-Regular.ttf"), self.font_size
        )

        # WEBCAM AND EYE TRACKING
        # Stays open the entire time and only FaceMesh is used. Moved here instead and we will close() manually
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        # self.cap = cv2.VideoCapture(0)
        for i in range(10):
            self.cap = cv2.VideoCapture(i)
            if self.cap.isOpened():
                print(f"Camera at index {i} is in use.")
                break

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(
            self.dt, self.face_mesh, self.cap
        )  # passing face_meseh and cap here

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(
                self.fps

            self.event_loop()
            self.update()
            self.draw()

            pygame.display.update()
        self.face_mesh.close() 

    def set_font_size(self):
        font_size = self.screen.get_width() // 45
        return font_size
