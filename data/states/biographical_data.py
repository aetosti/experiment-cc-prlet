# Pygame  Packages
import pygame

# Pygame Gui Packages
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIButton
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UILabel
from pygame_gui.windows import UIMessageWindow

# General Packages
import datetime
import os
import random
import string

# Data Packages
import pandas as pd

# Import BaseState
from .base import BaseState

# Import Settings
import settings


class BiographicalData(BaseState):
    def __init__(self):
        super(BiographicalData, self).__init__()

        self.next_state = "EYE_TRACKING_INSTRUCTIONS"

    def startup(self, persistent):
        pygame.mouse.set_visible(True)

        self.persist = persistent

        self.ui_manager = UIManager(
            (self.screen_rect.width, self.screen_rect.height),
            PackageResource(package="data.themes", resource="theme.json"),
        )

        self.widgets_coordinate()

        # Initialize instance variables
        self.first_name = ""
        self.last_name = ""
        self.gender = ""
        self.day_bd = ""
        self.month_bd = ""
        self.year_bd = ""
        self.birthplace = ""
        self.email = ""
        self.phone = ""
        self.school_id = ""

        self.create_ui()

    # GET SUBJECT'S INPUT
    def get_event(self, event):
        self.ui_manager.process_events(event)

        # Get Subject's First Name
        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
            and event.ui_object_id == "#first_name_entry"
        ):
            self.first_name = event.text

        # Get Subject's Last Name
        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
            and event.ui_object_id == "#last_name_entry"
        ):
            self.last_name = event.text

        # Get Subject's Gender
        if (
            event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element == self.gender_drop_down
        ):
            self.gender = event.text

        # Get Subject's Birthdate
        if (
            event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element == self.day_drop_down
        ):
            self.day_bd = event.text

        if (
            event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element == self.month_drop_down
        ):
            self.month_bd = event.text

        if (
            event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element == self.year_drop_down
        ):
            self.year_bd = event.text

        # Get Subject's Birthplace

        if (
            event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
            and event.ui_element == self.birthplace_drop_down
        ):
            self.birthplace = event.text

        # Get Subject's Email
        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
            and event.ui_object_id == "#email_entry"
        ):
            self.email = event.text

        # Get Subject's Phone Number
        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
            and event.ui_object_id == "#phone_entry"
        ):
            self.phone = event.text

        # Get Subject's School Id
        if (
            event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED
            and event.ui_object_id == "#school_id_entry"
        ):
            self.school_id = event.text

        # Get Start Button Event
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.start_task()

    # UPDATE FUNCTION
    def update(self, dt, face_mesh, cap):
        time_delta = dt / 1000.0
        self.ui_manager.update(time_delta)

    # DRAW ON THE SCREEN FUNCTION
    def draw(self, surface):
        surface.fill(pygame.Color(settings.BLACK))
        self.ui_manager.draw_ui(surface)

    # CREATE UI FUNCTION
    def create_ui(self):
        self.ui_manager.clear_and_reset()

        # First Name Input
        self.first_name_label = UILabel(
            pygame.Rect(self.label_x_pos + 14, self.pos_y[0], 100, 35),
            "Nome:",
            self.ui_manager,
            object_id="#first_name_label",
        )

        self.first_name_entry = UITextEntryLine(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[0],
                ),
                (360, 35),
            ),
            self.ui_manager,
            object_id="#first_name_entry",
        )

        # Last Name Input
        self.last_name_label = UILabel(
            pygame.Rect(self.label_x_pos, self.pos_y[1], 100, 35),
            "Cognome:",
            self.ui_manager,
            object_id="#last_name_label",
        )

        self.last_name_entry = UITextEntryLine(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[1],
                ),
                (360, 35),
            ),
            self.ui_manager,
            object_id="#last_name_entry",
        )

        # Gender
        self.gender_label = UILabel(
            pygame.Rect(self.label_x_pos + 5, self.pos_y[2], 100, 35),
            "Genere:",
            self.ui_manager,
            object_id="#gender_label",
        )

        self.gender_drop_down = UIDropDownMenu(
            ["-------", "Donna", "Uomo"],
            "-------",
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[2],
                ),
                (360, 35),
            ),
            self.ui_manager,
        )

        # Birthdate
        self.birthdate_label = UILabel(
            pygame.Rect(self.label_x_pos - 25, self.pos_y[3], 100, 35),
            "Compleanno:",
            self.ui_manager,
            object_id="#birthdate_label",
        )

        days = list(f"{num:02}" for num in range(1, 32))
        days.insert(0, "--")

        self.day_drop_down = UIDropDownMenu(
            days,
            "--",
            pygame.Rect(((self.input_x_pos, self.pos_y[3]), (120, 35))),
            self.ui_manager,
        )

        self.months = {
            "00": "-------",
            "01": "Gennaio",
            "02": "Febbraio",
            "03": "Marzo",
            "04": "Aprile",
            "05": "Maggio",
            "06": "Giugno",
            "07": "Luglio",
            "08": "Agosto",
            "09": "Settembre",
            "10": "Ottobre",
            "11": "Novembre",
            "12": "Dicembre",
        }

        self.month_drop_down = UIDropDownMenu(
            list(self.months.values()),
            "-------",
            pygame.Rect(((self.input_x_pos + 120, self.pos_y[3]), (120, 35))),
            self.ui_manager,
        )

        years = list(f"{num}" for num in range(1930, 2024))
        years.insert(0, "----")

        self.year_drop_down = UIDropDownMenu(
            years,
            "----",
            pygame.Rect(((self.input_x_pos + 240, self.pos_y[3]), (120, 35))),
            self.ui_manager,
        )

        # Birthplace
        self.birthplace_label = UILabel(
            pygame.Rect(self.label_x_pos - 20, self.pos_y[4], 100, 35),
            "Provenienza:",
            self.ui_manager,
            object_id="#birthplace_label",
        )

        self.birthplace_drop_down = UIDropDownMenu(
            ["-----", "Nord", "Centro", "Sud"],
            "-----",
            pygame.Rect(((self.input_x_pos, self.pos_y[4]), (360, 35))),
            self.ui_manager,
        )

        # Email
        self.email_label = UILabel(
            pygame.Rect(self.label_x_pos, self.pos_y[5], 100, 35),
            "Email:",
            self.ui_manager,
            object_id="#email_label",
        )

        self.email_entry = UITextEntryLine(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[5],
                ),
                (360, 35),
            ),
            self.ui_manager,
            object_id="#email_entry",
        )

        # Phone
        self.phone_label = UILabel(
            pygame.Rect(self.label_x_pos, self.pos_y[6], 100, 35),
            "Telefono:",
            self.ui_manager,
            object_id="#phone_label",
        )

        self.phone_entry = UITextEntryLine(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[6],
                ),
                (360, 35),
            ),
            self.ui_manager,
            object_id="#phone_entry",
        )

        # School Id
        self.school_id_label = UILabel(
            pygame.Rect(self.label_x_pos, self.pos_y[7], 100, 35),
            "Matricola:",
            self.ui_manager,
            object_id="#scoool_id_label",
        )

        self.school_id_entry = UITextEntryLine(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[7],
                ),
                (360, 35),
            ),
            self.ui_manager,
            object_id="#school_id_entry",
        )

        self.start_button = UIButton(
            pygame.Rect(
                (
                    self.input_x_pos,
                    self.pos_y[8],
                ),
                (360, 35),
            ),
            "Start",
            self.ui_manager,
            object_id="#start_button",
        )

    def create_warning_message(self):
        self.message_window = UIMessageWindow(
            rect=pygame.Rect((self.message_x_pos, self.message_y_pos), (300, 200)),
            window_title="Attenzione",
            html_message="Inserisci tutte le informazioni richieste per poter continuare",
            manager=self.ui_manager,
        )

    def start_task(self):
        if (
            self.first_name == ""
            or self.last_name == ""
            or self.gender == ""
            or self.day_bd == ""
            or self.month_bd == ""
            or self.year_bd == ""
            or self.birthplace == ""
            or self.email == ""
            or self.phone == ""
            or self.school_id == ""
        ):
            self.create_warning_message()
        else:
            self.generate_subject_ids_code()
            self.save_biographical_data()

            self.done = True

    def widgets_coordinate(self):
        FRAME_HEIGHT = self.screen_rect.height
        FRAME_CENTER_WIDTH = self.screen_rect.centerx
        FRAME_CENTER_HEIGHT = self.screen_rect.centery
        NUM_LABELS = 9
        LABEL_HEIGHT = 50
        TOP_PADDING = FRAME_HEIGHT // 5
        BOTTOM_PADDING = FRAME_HEIGHT // 5

        # Calculate the remaining vertical space above and below the labels
        available_space = (
            FRAME_HEIGHT - NUM_LABELS * LABEL_HEIGHT - TOP_PADDING - BOTTOM_PADDING
        )
        space_per_label = available_space / (NUM_LABELS - 1)

        # Calculate the y-position of each label
        self.pos_y = [
            TOP_PADDING + space_per_label * i + LABEL_HEIGHT * i
            for i in range(NUM_LABELS)
        ]

        # Label x position
        self.label_x_pos = FRAME_CENTER_WIDTH - 200

        # Input x position
        self.input_x_pos = FRAME_CENTER_WIDTH - 100

        # Button x position
        self.button_x_pos = FRAME_CENTER_WIDTH - 150

        # Message Coordinate
        self.message_x_pos = FRAME_CENTER_WIDTH - 150
        self.message_y_pos = FRAME_CENTER_HEIGHT - 100

    # GENERATE ID NUMBER AND ID STRING FUNCTION
    def generate_subject_ids_code(self):
        self.month_number = [
            month_name
            for month_name, month_number in self.months.items()
            if month_number == self.month_bd
        ]

        # Create the Subject ID Number
        self.subject_id_number = "".join(
            random.choices(string.ascii_letters + string.digits, k=11)
        ).upper()

        self.persist["subject_id_number"] = self.subject_id_number

        # Create the Subject ID String
        self.subject_id_string = (
            f"{self.first_name[:2].lower()}_"
            f"{self.last_name[:2].lower()}_"
            f"{self.year_bd}_"
            f"{self.month_number[0]}_"
            f"{self.day_bd}_"
            f"{self.phone[7:10]}_"
            f"{self.gender[:1].lower()}"
        )
        self.persist["subject_id_string"] = self.subject_id_string

    # DIRECTORY FUNCTIONS
    def make_subject_directory(self):
        self.subject_path = os.path.join("results", f"{self.subject_id_string}")
        os.makedirs(self.subject_path)

    def make_biographic_data_directory(self):
        self.save_biographical_data_path = os.path.join(
            f"{self.subject_path}", "biographical_data"
        )
        os.makedirs(self.save_biographical_data_path)

    def save_biographical_data(self):
        self.make_subject_directory()
        self.make_biographic_data_directory()

        # Create a pandas DataFrame with the Subject Personal Information
        birth_date = datetime.date(
            int(self.year_bd), int(self.month_number[0]), int(self.day_bd)
        )

        data = {
            "subject_id_string": [self.subject_id_string],
            "subject_id_number": [self.subject_id_number],
            "first_name": [self.first_name],
            "last_name": [self.last_name],
            "gender": [self.gender],
            "birthdate": [birth_date],
            "birthplace": [self.birthplace],
            "email": [self.email],
            "mobile_phone": [self.phone],
            "school_id": [self.school_id],
        }
        df = pd.DataFrame(data)

        # Save the DataFrame to a CSV file
        df.to_csv(
            os.path.join(
                self.save_biographical_data_path,
                f"{self.subject_id_number}_data_biographic.csv",
            ),
            index=False,
            sep=";",
        )
