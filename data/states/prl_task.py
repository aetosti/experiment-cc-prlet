# Pygame Packages
import pygame

# Data Packages
import pandas as pd
import numpy as np

# Import BaseState
from .base import BaseState

# General Packages
import datetime
import os
import random

# Import Settings
import settings


class PrlTask(BaseState):
    def __init__(self):
        super(PrlTask, self).__init__()

        self.next_state = "PRL_END_INSTRUCTIONS"

        # Load Stimuli Images
        stimuli_image_path = os.path.join("data", "assets", "images", "stimuli")

        self.stimuli_dict = {}

        ## Blue
        blue_stimuli_path = os.path.join(stimuli_image_path, "blue")
        blue_stimuli_path_list = os.listdir(blue_stimuli_path)

        self.stimuli_dict[0] = [
            (
                pygame.image.load(os.path.join(blue_stimuli_path, path)),
                os.path.basename(os.path.join(blue_stimuli_path, path)),
            )
            for path in blue_stimuli_path_list
        ]

        ## Orange
        orange_stimuli_path = os.path.join(stimuli_image_path, "orange")
        orange_stimuli_path_list = os.listdir(orange_stimuli_path)

        self.stimuli_dict[1] = [
            (
                pygame.image.load(os.path.join(orange_stimuli_path, path)),
                os.path.basename(os.path.join(orange_stimuli_path, path)),
            )
            for path in orange_stimuli_path_list
        ]

        # Load Feedback Images
        self.feedback_zero_img = pygame.image.load(
            os.path.join("data", "assets", "images", "feedback", "img_feedback_0.png")
        )
        self.feedback_one_img = pygame.image.load(
            os.path.join("data", "assets", "images", "feedback", "img_feedback_1.png")
        )

        # Load Fixation Image
        self.fixation_img = pygame.image.load(
            os.path.join("data", "assets", "images", "fixation", "fixation.png")
        )

        # Load Feedback Sounds Effects
        self.feedback_zero_sound = pygame.mixer.Sound(
            os.path.join("data", "assets", "sounds", "sound_feedback_0.mp3")
        )
        self.feedback_one_sound = pygame.mixer.Sound(
            os.path.join("data", "assets", "sounds", "sound_feedback_1.mp3")
        )

        # DATA SETTINGS
        ## PRL Task
        self.prl_data = {}
        self.prl_data["trial"] = []
        self.prl_data["stimulus_choice"] = []
        self.prl_data["location_choice"] = []
        self.prl_data["left_img_name"] = []
        self.prl_data["right_img_name"] = []
        self.prl_data["keyboard_input"] = []
        self.prl_data["outcome"] = []
        self.prl_data["start_reaction_time"] = []
        self.prl_data["end_reaction_time"] = []
        self.prl_data["start_absolute_time"] = []
        self.prl_data["end_absolute_time"] = []

        ## Eye Tracking
        self.eye_tracking_data = np.array([[]], dtype="object")

    def update(self, dt, face_mesh, cap):
        self.get_points(face_mesh, cap)
        self.eye_tracking_data = np.append(
            self.eye_tracking_data,
            [
                [
                    f"{self.left_ratio:.2f}",
                    int(self.left_center_x),
                    int(self.right_center_x),
                    pygame.time.get_ticks(),
                    datetime.datetime.now().strftime("%H:%M:%S.%f"),
                ]
            ],
        )

    def startup(self, persistent):
        # Variables
        self.trial = 0
        self.block = 0
        self.count_block = 0
        self.start_count = 0

        self.persist = persistent

        self.id_number = self.persist["subject_id_number"]
        self.id_string = self.persist["subject_id_string"]

        self.show_feedback = False

        self.generate_prl_task()

        self.prl_data["start_reaction_time"].append(pygame.time.get_ticks())
        self.prl_data["start_absolute_time"].append(
            datetime.datetime.now().strftime("%H:%M:%S.%f")
        )
        self.end_count = self.blocks[0]
        self.draw_stimuli()

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
            if event.key == pygame.K_a:
                self.keyboard_input = "a"
                self.direction_choice = "left"
                self.choice(self.more_rewarded_color, self.less_rewarded_color, 1, 0)

            if event.key == pygame.K_l:
                self.keyboard_input = "l"
                self.direction_choice = "right"
                self.choice(self.less_rewarded_color, self.more_rewarded_color, 0, 1)

    def draw(self, surface):
        # Show the Feedback
        if self.show_feedback:
            ## Display the Feedback Image for 1000ms
            center_rect = self.feedback_image.get_rect(
                center=(
                    surface.get_width() / 2,
                    surface.get_height() / 2,
                )
            )

            surface.blit(self.feedback_image, center_rect)

            feedback_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - feedback_time < 1000:
                surface.blit(self.feedback_image, center_rect)
                pygame.display.update()

            ## Display the Fixation Point for a random time between 250ms and 1750ms
            wait_time = random.randint(250, 1750)

            empty_frame_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - empty_frame_time < wait_time:
                # Disable Keyboard Input
                pygame.event.clear(eventtype=[pygame.KEYDOWN, pygame.KEYUP])

                # Show Empty Screen
                surface.fill(settings.BLACK)
                pygame.display.update()
            fixation_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - fixation_time < 200:
                # Disable Keyboard Input
                pygame.event.clear(eventtype=[pygame.KEYDOWN, pygame.KEYUP])

                surface.blit(self.fixation_img, center_rect)
                pygame.display.update()
            fixation_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - fixation_time < 200:
                # Disable Keyboard Input
                pygame.event.clear(eventtype=[pygame.KEYDOWN, pygame.KEYUP])

                surface.fill(settings.BLACK)
                pygame.display.update()
            fixation_time = pygame.time.get_ticks()

            while pygame.time.get_ticks() - fixation_time < 200:
                # Disable Keyboard Input
                pygame.event.clear(eventtype=[pygame.KEYDOWN, pygame.KEYUP])

                surface.blit(self.fixation_img, center_rect)
                pygame.display.update()

            self.prl_data["start_reaction_time"].append(pygame.time.get_ticks())
            self.prl_data["start_absolute_time"].append(
                datetime.datetime.now().strftime("%H:%M:%S.%f")
            )

            self.show_feedback = False

        # Show Stimuli
        surface.fill(pygame.Color(settings.BLACK))

        self.padx = self.get_image_padx(surface.get_width())

        left_rect = self.left_image.get_rect(
            midleft=(self.padx, surface.get_height() / 2)
        )

        right_rect = self.right_image.get_rect(
            midright=(surface.get_width() - self.padx, surface.get_height() / 2)
        )

        surface.blit(self.left_image, left_rect)
        surface.blit(self.right_image, right_rect)

    def generate_prl_task(self):
        # Create PRL Task Directory
        self.make_task_directory()
        self.make_eye_tracking_directory()

        # Set the Block's volatility as Low or High
        self.volatility = random.choices(
            settings.VOLATILITY_VERSION, weights=[0.5, 0.5], k=1
        )[0]

        self.blocks = settings.BLOCK_SEQUENCES[self.volatility]

        # Count the total number of trials
        self.num_of_trials = sum(self.blocks)

        # Set the more rewarded and the less rewarded stimulus and color
        ## 0 == Blue / 1 == Orange
        self.more_rewarded_stimulus = random.randint(0, 1)
        self.less_rewarded_stimulus = 0 if self.more_rewarded_stimulus == 1 else 1

        self.more_rewarded_color = (
            "orange" if self.more_rewarded_stimulus == 1 else "blue"
        )
        self.less_rewarded_color = (
            "blue" if self.more_rewarded_color == "orange" else "orange"
        )

        self.prl_data["more_rewarded_color"] = [
            color
            for i, num in enumerate(self.blocks)
            for color in [
                self.more_rewarded_color if i % 2 == 0 else self.less_rewarded_color
            ]
            * num
        ]

        # Create the Feedback Sequence
        self.feedback_list = [
            [
                1
                if random.random()
                < (
                    settings.PROBABILITY
                    if i % 2 == 0
                    else round(1 - settings.PROBABILITY, 2)
                )
                else 0
                for j in range(block_len)
            ]
            for i, block_len in enumerate(self.blocks)
        ]

        self.feedback_list = [
            feedback for sublist in self.feedback_list for feedback in sublist
        ]

        # Set the location of the stimuli
        self.locs_list = [
            1 if random.random() < 0.5 else 2 for _ in range(self.num_of_trials)
        ]

    def choice(self, color_one, color_two, reward_one, reward_two):
        self.save_eye_tracking()

        self.prl_data["end_reaction_time"].append(pygame.time.get_ticks())
        self.prl_data["end_absolute_time"].append(
            datetime.datetime.now().strftime("%H:%M:%S.%f")
        )

        # Save Trial Number
        self.prl_data["trial"].append(self.trial)

        # # Save More Rewarded Color
        # color = "orange" if self.block == 0 or self.block % 2 == 0 else "blue"
        # self.prl_data["more_rewarded_color"].append(self.more_rewarded_color)

        # Save Chosen Stimulus
        stimulus_choice = (
            color_one if self.locs_list[self.trial - 1] == 1 else color_two
        )

        self.prl_data["stimulus_choice"].append(stimulus_choice)

        # Save Chosen Location
        self.prl_data["location_choice"].append(self.direction_choice)

        # Save Keyboard Input
        self.prl_data["keyboard_input"].append(self.keyboard_input)

        # Save Outcome
        reward = reward_one if self.locs_list[self.trial - 1] == 1 else reward_two
        self.outcome = (
            "euro" if self.feedback_list[self.trial - 1] == reward else "noeuro"
        )
        self.prl_data["outcome"].append(self.outcome)

        self.draw_feedback()
        self.show_feedback = True
        self._save_task_if_needed()
        self.draw_stimuli()

    def draw_stimuli(self):
        if self.trial != self.num_of_trials:
            left_index = (
                self.more_rewarded_stimulus
                if self.locs_list[self.trial] == 1
                else self.less_rewarded_stimulus
            )
            right_index = (
                self.less_rewarded_stimulus
                if self.locs_list[self.trial] == 1
                else self.more_rewarded_stimulus
            )

            # Access a random image from the stimuli dictionary for the left Image
            left_stimuli_list = self.stimuli_dict[left_index]
            random_left_img = random.choice(left_stimuli_list)

            self.left_image = random_left_img[0]
            self.left_image_name = random_left_img[1][:-4]

            self.prl_data["left_img_name"].append(random_left_img[1][:-4])

            # Access a random image from the stimuli dictionary for the Right Image
            right_stimuli_list = self.stimuli_dict[right_index]
            random_right_img = random.choice(right_stimuli_list)

            self.right_image = random_right_img[0]
            self.right_image_name = random_right_img[1][:-4]

            self.prl_data["right_img_name"].append(random_right_img[1][:-4])

        else:
            self.save_prl_task()
            self.done = True

        self.count_block += 1
        self.trial += 1

    def draw_feedback(self):
        # Set the Feedback
        self.feedback_image = (
            self.feedback_one_img if self.outcome == "euro" else self.feedback_zero_img
        )

        # Play the Feedback Sound Effect
        if self.outcome == "euro":
            self.feedback_one_sound.play(loops=0)
        else:
            self.feedback_zero_sound.play(loops=0)

    def make_task_directory(self):
        self.save_prl_task_path = os.path.join(
            "results", f"{self.id_string}", "prl_task_data"
        )
        os.makedirs(self.save_prl_task_path)

    def make_eye_tracking_directory(self):
        self.save_eye_tracking_path = os.path.join(
            "results", f"{self.id_string}", "eye_tracking_data"
        )
        os.makedirs(self.save_eye_tracking_path)

    def _save_task_if_needed(self):
        if self.end_count != self.num_of_trials:
            if int(self.count_block) == int(self.blocks[self.block]):
                self.save_prl_task()
                self.start_count += int(self.blocks[self.block])
                self.block += 1
                self.count_block = 0
                self.end_count += int(self.blocks[self.block])

    def save_prl_task(self):
        # Save Trial Number
        df = pd.DataFrame({"trial": self.prl_data["trial"]})
        self.prl_data["trial"] = []

        # Save More Rewarded Color
        df = df.assign(
            more_rewarded_color=self.prl_data["more_rewarded_color"][
                self.start_count : self.end_count
            ]
        )

        # Save Stimulus Choice
        df = df.assign(stimulus_choice=self.prl_data["stimulus_choice"])
        self.prl_data["stimulus_choice"] = []

        # Save Stimuli Location
        df = df.assign(blue_position=self.locs_list[self.start_count : self.end_count])
        df["orange_position"] = df["blue_position"].apply(lambda x: 2 if x == 1 else 1)

        # Save Image Name
        df = df.assign(left_img_name=self.prl_data["left_img_name"])
        self.prl_data["left_img_name"] = []

        df = df.assign(right_img_name=self.prl_data["right_img_name"])
        self.prl_data["right_img_name"] = []

        # Save Location Choice
        df = df.assign(location_choice=self.prl_data["location_choice"])
        self.prl_data["location_choice"] = []

        # Save Keyboard Input
        df = df.assign(keyboard_input=self.prl_data["keyboard_input"])
        self.prl_data["keyboard_input"] = []

        # Save Feedback
        # df = df.assign(
        #     blue_reward=self.feedback_list[self.start_count : self.end_count]
        # )
        df = df.assign(
            **{
                f"{self.more_rewarded_color}_reward": self.feedback_list[
                    self.start_count : self.end_count
                ]
            }
        )

        df[f"{self.less_rewarded_color}_reward"] = df[
            f"{self.more_rewarded_color}_reward"
        ].apply(lambda x: 1 if x == 0 else 0)

        # Save Outcome
        df = df.assign(outcome=self.prl_data["outcome"])
        self.prl_data["outcome"] = []

        # Save Reaction Time
        df = df.assign(start_reaction_time=self.prl_data["start_reaction_time"])
        self.prl_data["start_reaction_time"] = []

        df = df.assign(end_reaction_time=self.prl_data["end_reaction_time"])
        self.prl_data["end_reaction_time"] = []

        # Save Absolute Time
        df = df.assign(start_absolute_time=self.prl_data["start_absolute_time"])
        self.prl_data["start_absolute_time"] = []

        df = df.assign(end_absolute_time=self.prl_data["end_absolute_time"])
        self.prl_data["end_absolute_time"] = []

        # Save Data to a CSV file
        df.to_csv(
            os.path.join(
                self.save_prl_task_path,
                f"{self.id_number}_b{self.block+1}_data_prl_task.csv",
            ),
            index=False,
            sep=";",
        )

    def save_eye_tracking(self):
        ratio = []
        left_eye_coordinate = []
        right_eye_coordinate = []
        time = []
        absolute_time = []

        for i in range(0, len(self.eye_tracking_data), 5):
            ratio.append(float(self.eye_tracking_data[i]))
            left_eye_coordinate.append(int(self.eye_tracking_data[i + 1]))
            right_eye_coordinate.append(int(self.eye_tracking_data[i + 2]))
            time.append(int(self.eye_tracking_data[i + 3]))
            absolute_time.append(self.eye_tracking_data[i + 4])

        df = pd.DataFrame(
            {
                "ratio": ratio,
                "left_eye_coordinate": left_eye_coordinate,
                "right_eye_coordinate": right_eye_coordinate,
                "time": time,
                "absolute_time": absolute_time,
            }
        )

        # Save Data to a CSV file
        df.to_csv(
            os.path.join(
                self.save_eye_tracking_path,
                f"{self.id_number}_b{self.block+1}_t{self.trial}_{self.left_image_name}_{self.right_image_name}_data_eye_tracking.csv",
            ),
            index=False,
            sep=";",
        )

        self.eye_tracking_data = []

    def get_image_padx(self, width):
        padx = width // 45

        return padx
