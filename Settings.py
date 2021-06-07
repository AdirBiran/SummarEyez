import os

# Project path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Directories
PARTICIPANTS_PATH = os.path.join(PROJECT_PATH, 'Participants')
TEXTS_PATH = os.path.join(PROJECT_PATH, 'Texts')
RESULTS_MAIN_PATH = os.path.join(PROJECT_PATH, "Results")
RESULTS_WORDS_PATH = os.path.join(RESULTS_MAIN_PATH, "Words")
RESULTS_SENTENCES_PATH = os.path.join(RESULTS_MAIN_PATH, "Sentences")

# Files
PARTICIPANTS_FILE = os.path.join(PARTICIPANTS_PATH, 'ParticipantsDetails.csv')
RESULTS_EXPERIMENT_FILE = os.path.join(RESULTS_MAIN_PATH, "Experiment.csv")
CONFIG_FILE = os.path.join(PROJECT_PATH, "Config.json")

# Highlighted Text Color
HIGHLIGHTED_COLOR = "#fbf224"
RANKING_COLOR = "#8efb84"

# App Name
APP_NAME = "SummarEyes"

# Min text reading time in seconds before Next button appear
MIN_TEXT_READING_TIME = 5