import tkinter as tk
import time
import pandas as pd
import pyautogui
from Settings import *

class Create_text(tk.Tk):
    def __init__(self, participant_id, text, text_id, eye_tracker=False, see_rectangle=True
                 , points=True, verbose=True):
        super().__init__()
        self.start_time = time.time()
        self.config(cursor='circle red')
        self.participant_id = participant_id
        self.text_id = text_id
        self.text = text
        self.see_rectangle = see_rectangle
        self.points = points
        self.verbose = verbose
        self.title("SummerEyes")
        self.width = self.winfo_screenwidth()  # get display width
        self.height = self.winfo_screenheight()  # get display height
        self.attributes('-fullscreen', True)
        self.font = ("helvetica", 20)  # font
        self.canvas_background = "white"  # background color
        self.canvas = tk.Canvas(self, bg=self.canvas_background, width=self.width, height=self.height)
        self.canvas.pack()  # necessarily
        self.eye_tracker = eye_tracker  # if x,y coordinates from 0 to 1 set eye_tracker=True to convert them to px
        self.start_position_x = 40  # start text position (x)
        self.start_position_y = 40  # start text position (y)
        self.fixation_number = 0
        self.previous_fixation = None
        self.bbox_info = None
        self.exit = False
        self.word_bbox_info = {}
        self.word_previous_fixation = None
        self.word_fixation_number = 0
        self.print_text()

    def print_text(self):
        self.button_save = tk.Button(self, text="Next", command=self.quit, font=self.font, anchor="w")
        self.button_save.place(relx=0.03, rely=0.9)
        index_word = 1

        """indexing each sentence in asecnding order"""
        bbox_info = {}
        for index, sentenсe in enumerate(self.text.split(".")):
            if len(sentenсe) == 0:
                continue
            sentenсe = sentenсe.lstrip()
            positions = []
            for number, word in enumerate(sentenсe.split(" ")):
                if len(word) == 0:
                    continue
                if number == len(sentenсe.split(" ")) - 1:
                    suffix = '. '  # including suffix '.' as the word area
                else:
                    suffix = ' '  # including suffix space as the word area
                sent_id = self.canvas.create_text(self.start_position_x, self.start_position_y,  # id for specify word
                                                  text=word + suffix, font=self.font,
                                                  justify="left", fill="black", anchor="nw")
                bbox = self.canvas.bbox(sent_id)  # X1,Y1,X2,Y2 coordinates for a rectangle which encloses word item
                if self.see_rectangle == True:
                    self.canvas.create_rectangle(bbox, outline="black")  # draw word rectangles
                width = self.start_position_x + bbox[2] - bbox[0] + 5  # calculate word width
                x_left = self.start_position_x
                x_right = self.start_position_x + bbox[2] - bbox[0]
                y_up = self.start_position_y
                y_down = self.start_position_y + bbox[3] - bbox[1]
                if width + 120 < self.width:
                    self.start_position_x += bbox[2] - bbox[0]
                else:
                    self.start_position_x = 40
                    self.start_position_y += 40
                position = [x_left, x_right, y_up, y_down]
                positions.append(position)
                self.word_bbox_info[tuple(position)] = [word, 0, [], {}, index_word]
                index_word += 1
            bbox_info[index + 1] = [sentenсe, positions, 0, [], {}]
            """ define for each word in specific sentence her borders coordinates, for example:
                x1, x2, y1, y2 ['Pulvinar elementum integer enim neque volutpat', 
                [[1183, 1263, 40, 63], [1263, 1370, 40, 63], [1370, 1439, 40, 63], [1439, 1490, 40, 63],
                [1490, 1554, 40, 63], [1554, 1638, 40, 63]], 0, []]"""
            self.bbox_info = bbox_info
            self.update()

    def draw_point(self, x, y):
        try:
            self.canvas.delete(self.point)
        except:
            pass
        x0 = x - 5
        y0 = y - 5
        x1 = x + 5
        y1 = y + 5
        # self.point=self.canvas.create_oval(x-10, y-10, x, y, outline="#2541f4",width=5)
        self.point = self.canvas.create_oval(x0, y0, x1, y1, outline="#2541f4", width=5)
        self.update()

    def quit(self):
        self.finish_time = time.time()
        self.read_time = round(self.finish_time - self.start_time, 1)
        self.get_output(save=True)  # for sentences
        self.words_get_output(save=True)  # for words
        #messagebox.showinfo('File was saved', 'File was saved/n You read {} sec'.format(self.read_time))
        self.destroy()

    def get_bbox(self, x, y):
        if self.eye_tracker == True:
            # pass
            x = (x * self.width)
            y = (y * self.height)
            print(x)
            print(y)
        if self.points == True:
            self.draw_point(x, y)
        for key, value in self.bbox_info.items():
            positions = value[1]
            for i, position in enumerate(positions):
                x_left = position[0]
                x_right = position[1]
                y_up = position[2]
                y_down = position[3]
                if x_left <= x <= x_right and y_up <= y <= y_down:
                    self.update_info_on_word(x_left, x_right, y_up, y_down)
                    index = key
                    sentenсe = value[0]
                    positions = value[1]
                    fixations = value[2] + 1
                    # count_fixation_sentence = value[4]
                    if self.previous_fixation != index:
                        self.fixation_number += 1
                    self.previous_fixation = index
                    if self.fixation_number in value[4].keys():
                        value[4][self.fixation_number] += 1
                    else:
                        value[4][self.fixation_number] = 1
                    order = value[3]
                    order.append(self.fixation_number)
                    self.bbox_info[index] = [sentenсe, positions, fixations, order, value[4]]
                    if self.verbose == True:
                        print('Number sentence:{}, Sentence:{}, Order sentence:{}'.format(index, sentenсe,
                                                                                          self.fixation_number))
                    self.update()
                    break

    def update_info_on_word(self, x_left, x_right, y_up, y_down):
        tuple_coordinates = tuple([x_left, x_right, y_up, y_down])
        word_info = self.word_bbox_info[tuple_coordinates]
        index = word_info[4]
        if self.word_previous_fixation != index:
            self.word_fixation_number += 1
        self.word_previous_fixation = index
        fixations = word_info[1] + 1
        if self.word_fixation_number in word_info[3].keys():
            word_info[3][self.word_fixation_number] += 1
        else:
            word_info[3][self.word_fixation_number] = 1
        order = word_info[2]
        order.append(self.word_fixation_number)
        word_info[1] = fixations
        word_info[2] = order
        self.word_bbox_info[tuple_coordinates] = word_info

    def words_get_output(self, save):  # create dataframe from bbox_info
        self.output = pd.DataFrame([(b[4], b[0], b[2], b[3], b[1])
                                    for a, b in self.word_bbox_info.items()],
                                   columns=['index', 'word', 'fixation_order',
                                            'duration_fixation', 'total_duration_fixation'])
        self.output['count_letters'] = self.output['word'].apply(lambda x: len(x))
        self.output['count_fixation_normalized'] = self.output['total_duration_fixation'] / self.output['count_letters']
        self.output['fixation_order'] = self.output['fixation_order'].apply(lambda x: list(set(x)))

        if save == True:
            path = os.path.join(RESULTS_WORDS_PATH, "{}_{}.csv")
            self.output.to_csv(path.format(self.participant_id, self.text_id), index=False)

    def get_output(self, save):  # create dataframe from bbox_info
        self.output = pd.DataFrame([(a, b[0], b[3], b[4], b[2]) for a, b in self.bbox_info.items()],
                                   columns=['index', 'sentenсe', 'fixation_order', 'duration_fixation',
                                            'total_duration_fixation'])
        self.output['count_words'] = self.output['sentenсe'].apply(lambda x: len(x.split(' ')))
        self.output['count_fixation_normalized'] = self.output['total_duration_fixation'] / self.output['count_words']
        self.output['fixation_order'] = self.output['fixation_order'].apply(lambda x: list(set(x)))

        if save == True:
            path = os.path.join(RESULTS_SENTENCES_PATH, "{}_{}.csv")
            self.output.to_csv(path.format(self.participant_id, self.text_id), index=False)
            # display(self.output)

def start_eye_tracking(text, participant_id, current_text_id):

    experiment_screen = Create_text(participant_id, text, current_text_id,
                                    points=True, eye_tracker=False, verbose=True, see_rectangle=True)
    for i in range(150):  # need to change to specific time or exit button
        x = pyautogui.position().x
        y = pyautogui.position().y
        print(i)
        # x=random.random()
        # y=random.random()
        # print("x is: " + str(x))
        # print("y is: " + str(y))
        try:
            experiment_screen.get_bbox(x, y)
            time.sleep(0.25)
        except:
            print('TclError')
            break

    return experiment_screen.read_time

    # except AttributeError:
    #
    #     print('AttributeError')
    #     pass

    # In[ ]:
