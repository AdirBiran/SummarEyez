import os

# Project path
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Directories
DATA_PATH = os.path.join(PROJECT_PATH, 'Data')
PARTICIPANTS_PATH = os.path.join(DATA_PATH, 'Participants')
TEXTS_PATH = os.path.join(DATA_PATH, 'Texts')
RESOURCES_PATH = os.path.join(PROJECT_PATH, 'Resources')

# Files
TEXTS_FILE = os.path.join(TEXTS_PATH, 'Texts.csv')
PARTICIPANTS_FILE = os.path.join(DATA_PATH, 'ParticipantsDetails.csv')

# Timers
SUMMARIZATION_TIMER = 300
HIGHLIGHTING_TIMER = 300
RANKING_TIMER = 300
QUESTIONS_TIMER = 300

# Highlighted Text Color
HIGHLIGHTED_COLOR = "#fbf224"

# App Name
APP_NAME = "SummarEyes"

