from DataManagement import *
import random

class Controller:
    def __init__(self):
        self.data_access = DataManagement()

    # Add new participant to database
    def add_new_participant(self, participant_id, first_name, last_name, gender, age):
        print("New Participant", participant_id, first_name, last_name, gender, age)


    def save_text_results(self, current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times):
        print("Saved Results", current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)

    # Get 4 texts
    # questions = 3 questions
    # answers = 12 answers
    # [ [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]] ]
    def get_texts(self):
        pass

    def get_demo_texts(self):

        texts = []

        for i in range(1, 5):

            text_id = random.randint(0, 100)

            text = " There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc."

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