# Pygame Packages
import pygame

# General Packages
import sys

# Import States
from data.states.splash import Splash
from data.states.biographical_data import BiographicalData
from data.states.eye_tracking_instructions import EyeTrackingInstructions
from data.states.calibration_instructions import CalibrationInstructions
from data.states.calibration_task import CalibrationTask
from data.states.confirm_calibration_instructions import ConfirmCalibrationInstructions
from data.states.confirm_calibration_task import ConfirmCalibrationTask
from data.states.recalibration_task import RecalibrationTask
from data.states.prl_start_instructions import PrlStartInstructions
from data.states.prl_task import PrlTask
from data.states.prl_end_instructions import PrlEndInstructions

# Import Main App
from app import App

pygame.init()


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


states = {
    "SPLASH": Splash(),
    # consenso ?
    "BIOGRAPHICAL_DATA": BiographicalData(),
    "EYE_TRACKING_INSTRUCTIONS": EyeTrackingInstructions(),
    "CALIBRATION_INSTRUCTIONS": CalibrationInstructions(),
    "CALIBRATION_TASK": CalibrationTask(),
    "CONFIRM_CALIBRATION_INSTRUCTIONS": ConfirmCalibrationInstructions(),
    "CONFIRM_CALIBRATION_TASK": ConfirmCalibrationTask(),
    "RECALIBRATION_TASK": RecalibrationTask(),
    "PRL_START_INSTRUCTIONS": PrlStartInstructions(),
    "PRL_TASK": PrlTask(),
    "PRL_END_INSTRUCTIONS": PrlEndInstructions(),
}

app = App(screen, states, "SPLASH")
app.run()

pygame.quit()
sys.exit()
