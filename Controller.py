from DataManagement import *
import random
import json


class Controller:
    def __init__(self):
        self.data_access = DataManagement()
        self.texts_counter = 1

    # Add new participant to database
    def add_new_participant(self, participant_id, first_name, last_name, gender, department, age):
        print("New Participant", participant_id, first_name, last_name, gender, department, age)
        self.data_access.add_new_participant(participant_id, first_name, last_name, gender, department, age)

    # Save text's results
    def save_text_results(self, current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times):
        print("Saved Results", current_text_id, participant_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)
        self.data_access.add_participant_records(participant_id, current_text_id, highlighted_sentences, highlighted_sentences_scores, text_summary, questions_answers, times)



    # Get 4 texts
    # questions = 3 questions
    # answers = 12 answers
    # [ [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]], [text_id, text, [questions], [answers]] ]
    def get_texts(self):

        user_counter = self.get_current_users_counter()
        user_texts_indexes = [user_counter, user_counter + 20, user_counter + 40, user_counter + 60]

        texts = []
        for text_idx in user_texts_indexes:
            text_path = os.path.join(TEXTS_PATH, str(text_idx), str(text_idx) + ".json")
            with open(text_path) as f:
                data = json.load(f)
                data["ID"] = text_idx
                texts.append(data)

        self.update_current_users_counter(user_counter + 1)

        return texts

    def get_current_users_counter(self):
        with open(CONFIG_FILE) as f:
            data = json.load(f)
            return data["Current_User"]

    def update_current_users_counter(self, new_texts_counter):

        config_dict = {"Current_User": new_texts_counter}

        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_dict, f)

    # Getting 1 demo text
    def get_demo_texts(self):

        filename = "demo.json"

        text_path = os.path.join(TEXTS_PATH, filename)
        with open(text_path) as f:
            data = json.load(f)
            return [data]




    # Getting 4 demo texts
    def get_demo_texts_archive(self):


        """ files for 15 inch screen"""
        file1 = 'Text1/Text1'
        file2 = 'Text2/Text2'
        file3 = 'Text3/Text3'
        file4 = 'Text4/Text4'
        file5 = 'Text5/Text5'
        file6 = 'Text6/Text6'
        file7 = 'Text7/Text7'
        file8 = 'Text8/Text8'
        file9 = 'Text9/Text9'
        file10 = 'Text10/Text10'
        # file11 = 'Text10/Text10'

        # file_14 = 'file14'  # 815 words
        # file_15 = 'file15'  # 760 words
        # file_16 = 'file16'  # 688 words
        # file_17 = 'file17'  # 582 words
        # file_18 = 'file18'  # 523 words

        file_name = file6

        texts = []

        for i in range(1, 5):

            text_id = random.randint(0, 100)
            text = (open('Texts/' + file_name + '.txt'.format(file_name), 'r')).read()

            split = text.split(" ")
            fixed_text = []
            for sp in split:
                if len(sp) == 0:
                    pass
                elif "\n" in sp or "<P>" in sp or "</P>" in sp:
                    fixed_text.append(sp.replace("\n", " ").replace("<P>", "").replace("</P>", ""))
                else:
                    fixed_text.append(sp)

            text = ' '.join(fixed_text)

            with open('Texts/{}_fixed.txt'.format(file_name), 'w') as f:
                f.write(text)

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