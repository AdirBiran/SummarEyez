from DataManagement import *
import random


class Controller:
    def __init__(self):
        self.data_access = DataManagement()

    # Add new participant to database
    def add_new_participant(self, participant_id, first_name, last_name, gender, age):
        print("New Participant", participant_id, first_name, last_name, gender, age)
        self.data_access.add_new_participant(participant_id, first_name, last_name, gender, age)

    # Save text's results
    def save_text_results(self, current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times):
        print("Saved Results", current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)
        self.data_access.add_participant_records(participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)

    # Get 4 texts
    # questions = 3 questions
    # answers = 12 answers
    # [ [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]] ]
    def get_texts(self):
        pass

    # Getting 4 demo texts
    def get_demo_texts(self):

        """ files for 15 inch screen"""
        file_14 = 'file14'  # 815 words
        file_15 = 'file15'  # 760 words
        file_16 = 'file16'  # 688 words
        file_17 = 'file17'  # 582 words
        file_18 = 'file18'  # 523 words


        texts = []

        for i in range(1, 5):

            text_id = random.randint(0, 100)
            text = (open('Texts/{}.txt'.format(file_17), 'r')).read()

            q1 = "What is...............................?"
            q2 = "Where is...............................?"
            q3 = "How is...............................?"
            questions = [q1, q2, q3]

            a1 = "answer 1" + " text " + str(i)
            a2 = "answer 2" + " text " + str(i)
            a3 = "answer 3" + " text " + str(i)
            a4 = "answer 4" + " text " + str(i)
            answers = [a1, a2, a3, a4] * 3

            texts.append([text_id, text, questions, answers])

        return texts