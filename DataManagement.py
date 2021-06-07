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

        # Create Results Directory
        if not os.path.exists(RESULTS_MAIN_PATH):
            os.mkdir(RESULTS_MAIN_PATH)

        # Participant file headers
        participant_file_headers = ['ParticipantID', 'FirstName', 'LastName', 'Gender', 'Department', 'Age']

        # Create participants file if not exist
        if not os.path.exists(PARTICIPANTS_FILE):
            with open(PARTICIPANTS_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(participant_file_headers))


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

        if not os.path.exists(os.path.join(RESULTS_MAIN_PATH, args[0], "Results.csv")):
            experiment_results_headers = ['ParticipantID', 'TextID', 'HighlightedSentences', 'SentencesScores', 'TextSummarization', 'Q1', 'Q2', 'Q3', 'TimeTextReading', 'TimeTextSummarization', 'TimeHighlighting', 'TimeRanking', 'TimeQ1', 'TimeQ2', 'TimeQ3']

            with open(os.path.join(RESULTS_MAIN_PATH, args[0], "Results.csv"), "a", newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(experiment_results_headers))

    # Adds participant's record
    def add_participant_records(self, participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times):

        # Arranging parameters
        records = [participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary]
        for q in questions_answers:
            records.append(q)
        for time in times:
            records.append(time)

        with open(os.path.join(RESULTS_MAIN_PATH, str(participant_id), "Results.csv"), 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(records)