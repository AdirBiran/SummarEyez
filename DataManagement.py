import csv
from Settings import *


class DataManagement:
    def __init__(self):

        # Create Participants Directory
        if not os.path.exists(PARTICIPANTS_PATH):
            os.mkdir(PARTICIPANTS_PATH)

        # Create Texts Directory
        if not os.path.exists(TEXTS_PATH):
            os.mkdir(TEXTS_PATH)

        # Create Resources Directory
        if not os.path.exists(RESOURCES_PATH):
            os.mkdir(RESOURCES_PATH)

        # Create Results Directory
        if not os.path.exists(RESULTS_MAIN_PATH):
            os.mkdir(RESULTS_MAIN_PATH)

        # Create Words Results Directory
        if not os.path.exists(RESULTS_WORDS_PATH):
            os.mkdir(RESULTS_WORDS_PATH)

        # Create Sentences Results Directory
        if not os.path.exists(RESULTS_SENTENCES_PATH):
            os.mkdir(RESULTS_SENTENCES_PATH)

        # Texts file headers
        texts_file_headers = ['TextID', 'Title', 'Text']

        # Create texts file if not exist
        if not os.path.exists(TEXTS_FILE):
            with open(TEXTS_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(texts_file_headers))

        # Participant file headers
        participant_file_headers = ['ParticipantID', 'FirstName', 'LastName', 'Gender', 'Age']

        # Create participants file if not exist
        if not os.path.exists(PARTICIPANTS_FILE):
            with open(PARTICIPANTS_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(participant_file_headers))

        # Experiment file headers
        experiment_results_headers = ['ParticipantID', 'TextID', 'HighlightedSentences', 'SentencesScores', 'TextSummarization', 'Q1', 'Q2', 'Q3', 'TimeTextReading', 'TimeTextSummarization', 'TimeHighlighting', 'TimeRanking', 'TimeQ1', 'TimeQ2', 'TimeQ3']

        # Create Experiment file if not exist
        if not os.path.exists(RESULTS_EXPERIMENT_FILE):
            with open(RESULTS_EXPERIMENT_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(experiment_results_headers))

    # Adds new participant
    def add_new_participant(self, *args):
        if not os.path.exists(os.path.join(RESULTS_MAIN_PATH, args[0])):
            os.mkdir(os.path.join(RESULTS_MAIN_PATH, args[0]))

        if not os.path.exists(os.path.join(RESULTS_MAIN_PATH, args[0], "Words")):
            os.mkdir(os.path.join(RESULTS_MAIN_PATH, args[0], "Words"))

        if not os.path.exists(os.path.join(RESULTS_MAIN_PATH, args[0], "Sentences")):
            os.mkdir(os.path.join(RESULTS_MAIN_PATH, args[0], "Sentences"))

        with open(PARTICIPANTS_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(list(args))

    # Adds participant's record
    def add_participant_records(self, participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times):

        # Arranging parameters
        records = [participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary]
        for q in questions_answers:
            records.append(q)
        for time in times:
            records.append(time)

        with open(RESULTS_EXPERIMENT_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(records)

    # Adds new text
    def add_text(self, title, text):
        with open(TEXTS_FILE, 'r', newline='') as fd:
            reader = csv.reader(fd);
            row_count = sum([1 for row in reader])

        with open(TEXTS_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow([row_count, title, text])

