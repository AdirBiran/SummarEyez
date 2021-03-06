import os

# Project path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Directories
PARTICIPANTS_PATH = os.path.join(PROJECT_PATH, 'Participants')
TEXTS_PATH = os.path.join(PROJECT_PATH, 'Texts')
RESOURCES_PATH = os.path.join(PROJECT_PATH, 'Resources')
RESULTS_MAIN_PATH = os.path.join(PROJECT_PATH, "Results")
RESULTS_WORDS_PATH = os.path.join(RESULTS_MAIN_PATH, "Words")
RESULTS_SENTENCES_PATH = os.path.join(RESULTS_MAIN_PATH, "Sentences")

# Files
TEXTS_FILE = os.path.join(TEXTS_PATH, 'Texts.csv')
PARTICIPANTS_FILE = os.path.join(PARTICIPANTS_PATH, 'ParticipantsDetails.csv')
RESULTS_EXPERIMENT_FILE = os.path.join(RESULTS_MAIN_PATH, "Experiment.csv")

# Highlighted Text Color
HIGHLIGHTED_COLOR = "#fbf224"

# App Name
APP_NAME = "SummarEyez"

