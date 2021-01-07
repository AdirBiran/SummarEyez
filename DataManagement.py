import csv
from Settings import *


class DataManagement:
    def __init__(self):

        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)

        if not os.path.exists(PARTICIPANTS_PATH):
            os.mkdir(PARTICIPANTS_PATH)

        if not os.path.exists(TEXTS_PATH):
            os.mkdir(TEXTS_PATH)

        if not os.path.exists(RESOURCES_PATH):
            os.mkdir(RESOURCES_PATH)

        texts_file_headers = ['TextID', 'Title', 'Text']

        if not os.path.exists(TEXTS_FILE):
            with open(TEXTS_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(texts_file_headers))

        participant_file_headers = ['ParticipantID', 'FirstName', 'LastName', 'Age', 'Gender']

        if not os.path.exists(PARTICIPANTS_FILE):
            with open(PARTICIPANTS_FILE, 'a', newline='') as fd:
                writer = csv.writer(fd)
                writer.writerow(list(participant_file_headers))



    def add_new_participant(self, *args):
        with open(PARTICIPANTS_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(list(args))


    def create_participant_files(self, id):
        id_path = os.path.join(PARTICIPANTS_PATH, str(id))
        csv_file_text_1 = os.path.join(id_path, "Text_1_Info.csv")
        csv_file_text_2 = os.path.join(id_path, "Text_2_Info.csv")
        csv_file_text_3 = os.path.join(id_path, "Text_3_Info.csv")

        files = [csv_file_text_1, csv_file_text_2, csv_file_text_3]
        if not os.path.exists(id_path):
            os.mkdir(id_path)

        headers = ['header_1', 'header_2', 'header_3', 'header_4', 'header_5', 'header_6', 'header_7']

        for file_path in files:
            if not os.path.exists(file_path):
                with open(file_path, 'a', newline='') as fd:
                    writer = csv.writer(fd)
                    writer.writerow(list(headers))


    def add_participant_records(self, id, records):
        pass


    def add_text(self, title, text):
        with open(TEXTS_FILE, 'r', newline='') as fd:
            reader = csv.reader(fd);
            row_count = sum([1 for row in reader])

        with open(TEXTS_FILE, 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow([row_count, title, text])

